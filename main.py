from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from threading import Thread
  
# given url to dappradar, finds number of dapps for that crypto
def get_num_dapps(crypto_code, dict):
  # given list of elements with text, returns the greatest int in the texts
  def get_max_digit(elements):
    digits = []
    for el in elements:
      if el.text.isdigit():
        digits += [int(el.text)]
    return max(digits)

  # create driver
  chrome_options = Options()
  # chrome_options.add_argument("--headless")
  chrome_service = ChromeService(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
  driver.maximize_window()

  # get url to last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}")
  nav_els = WebDriverWait(driver, 12).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "sc-breuTD.malUw")))
  last_page = get_max_digit(nav_els)

  # get num dapps from last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}/{last_page}")
  dapp_num_els = WebDriverWait(driver, 12).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "sc-olbas.iVmbMh")))

  num = get_max_digit(dapp_num_els)

  # remove driver and return
  driver.close()
  driver.quit()
  dict[crypto_code] = num
  return

def get_used_dapps(crypto_code, dict):
  # given list of elements with text, returns the greatest int in the texts
  def get_max_digit(elements):
    digits = []
    for el in elements:
      if el.text.isdigit():
        digits += [int(el.text)]
    return max(digits)

  # create driver
  chrome_options = Options()
  # chrome_options.add_argument("--headless")
  chrome_options.add_argument("--enable-javascript") # needed to load correct end page for >1 user
  chrome_service = ChromeService(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
  driver.maximize_window()

  # get url to last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}/1?greaterUser=1")
  filter_btn = WebDriverWait(driver, 12).until(EC.visibility_of_element_located((By.CLASS_NAME, "sc-hKMtZM.gJGSuK.sc-gKXOVf.sc-bBXxYQ.elfFbJ.cyfpQG")))
  filter_btn.click()
  apply_btn = WebDriverWait(driver, 12).until(EC.visibility_of_element_located((By.CLASS_NAME, "sc-hKMtZM.gJGSuK.sc-gKXOVf.bxXfRK")))
  apply_btn.click()
  time.sleep(2.0) # wait for filter to be applied

  nav_els = WebDriverWait(driver, 12).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "sc-breuTD.malUw")))
  last_page = get_max_digit(nav_els)

  # get num dapps from last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}/{last_page}")
  user_num_els = WebDriverWait(driver, 12).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "sc-gCoyRa.TwgEd")))
  
  # count num dapps with more than 1 user
  count = 0
  for el in user_num_els:
    if el.text.isdigit() and int(el.text) >= 1:
      count += 1
  num = 25 * (last_page - 1) + count

  # remove driver and return
  driver.close()
  driver.quit()
  dict[crypto_code] = num
  return

# run threads recursively in groups of 7
def run_threads(threads):
  if len(threads) < 7:
    # base case, run all
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
    return
  else:
    # run 8, then recurse on remaining
    for i in range(7):
      threads[i].start()
    for i in range(7):
      threads[i].join()
    run_threads(threads[7:])

# input and output to threads
crypto_codes = [
  "ethereum",
  "solana",
  "avalanche",
  "binance-smart-chain",
  "tron",
  "algorand",
  "near",
  "flow",
  "polygon",
  "tezos",
  "eos",
  "harmony",
  "fantom"
]
crypto_codes = ["ethereum", "solana"]
dict_all = {}
dict_used = {}

# create threads and run with helper function
threads = []
for code in crypto_codes:
  threads += [Thread(target=get_num_dapps, args=(code, dict_all))]
  threads += [Thread(target=get_used_dapps, args=(code, dict_used))]
run_threads(threads)

# for code in crypto_codes:
#   get_num_dapps(code, dict_all)
#   get_used_dapps(code, dict_used)

# print output
print(dict_all)
print(dict_used)

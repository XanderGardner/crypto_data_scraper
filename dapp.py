from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from threading import Thread
from collections import OrderedDict
  
# TODO CHANGE DYNAMICALLY
nav_els_class = "sc-eDWCr.hFKXSa"

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

  # TODO: change dynamically
  
  row_num_class = "sc-efhLOa"

  # get url to last page
  try:
    driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}")
    nav_els = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, nav_els_class)))
    last_page = get_max_digit(nav_els)
  except:
    print(f"not many dapps for {crypto_code}...")
    last_page = 1

  # get num dapps from last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}/{last_page}")
  WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, row_num_class)))
  time.sleep(2.0) # allow javascript to finish loading
  dapp_num_els = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, row_num_class)))

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
  
  # TODO: change dynamically
  filter_btn_class = "sc-hLBbgP.fZhtXy.sc-gKPRtg.sc-cOxWqc"
  btn_div_class = "sc-eAnmvA"
  btn_apply_class = "sc-hLBbgP"

  filter_btn = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, filter_btn_class)))
  filter_btn.click()
  btn_div = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CLASS_NAME, btn_div_class)))
  apply_btn = btn_div.find_element(By.CLASS_NAME, btn_apply_class)
  apply_btn.click()
  time.sleep(2.0) # wait for filter to be applied

  # TODO: change dynamically
  row_class = "sc-oZIhv.hFbnZp"

  try:
    nav_els = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, nav_els_class)))
    last_page = get_max_digit(nav_els)
  except:
    print(f"2:not many dapps with users for {crypto_code}...")
    last_page = 1

  # get num dapps from last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}/{last_page}")
  rows = WebDriverWait(driver, 15).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, row_class)))
  
  row_data = []
  for row in rows:
    tds = row.find_elements(By.TAG_NAME, "td")
    if len(tds) >= 6:
      users = tds[5].find_elements(By.TAG_NAME, "div")
      numbers = tds[0]
      if len(users) >= 2:
        row_data += [(users[1], numbers)]
  # users: sc-gCoyRa TwgEd
  # number: sc-inRwDn LrPBw

  # count num dapps with more than 1 user
  count = 0
  for dapp in row_data:
    if dapp[1].text != "Ad" and dapp[0] and dapp[0].text != "0":
      count += 1
  num = 25 * (last_page - 1) + count

  # remove driver and return
  driver.close()
  driver.quit()
  dict[crypto_code] = num
  return

# run threads recursively in groups of 6
def run_threads(threads):
  if len(threads) < 6:
    # base case, run all
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
    return
  else:
    # run 6, then recurse on remaining
    for i in range(6):
      threads[i].start()
    for i in range(6):
      threads[i].join()
    run_threads(threads[6:])

def main():
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
  dict_all = OrderedDict()
  dict_used = OrderedDict()

  # create threads and run with helper function
  threads = []
  for code in crypto_codes:
    dict_all[code] = []
    dict_used[code] = []
    threads += [Thread(target=get_num_dapps, args=(code, dict_all))]
    threads += [Thread(target=get_used_dapps, args=(code, dict_used))]
  run_threads(threads)

  # print output
  print(f"All dapps: {dict_all}")
  print(f"All dapps: {dict_used}")

if __name__ == "__main__":
  main()

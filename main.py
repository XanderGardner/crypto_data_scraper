from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from threading import Thread

# given list of elements with text, returns the greatest int in the texts
def get_max_digit(elements):
  digits = []
  for el in elements:
    if el.text.isdigit():
      digits += [int(el.text)]
  return max(digits)
  
# given url to dappradar, finds number of dapps for that crypto
def get_num_dapps(crypto_code):
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
  return num

def get_used_dapps(crypto_code):
  # create driver
  chrome_options = Options()
  # chrome_options.add_argument("--headless")
  chrome_service = ChromeService(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
  driver.maximize_window()

  # get url to last page
  driver.get(f"https://dappradar.com/rankings/protocol/{crypto_code}/1?greaterUser=1")
  filter_btn = WebDriverWait(driver, 12).until(EC.visibility_of_element_located((By.CLASS_NAME, "sc-hKMtZM.gJGSuK.sc-gKXOVf.sc-bBXxYQ.elfFbJ.cyfpQG")))
  filter_btn.click()
  apply_btn = WebDriverWait(driver, 12).until(EC.visibility_of_element_located((By.CLASS_NAME, "sc-hKMtZM.gJGSuK.sc-gKXOVf.bxXfRK")))
  apply_btn.click()
  time.sleep(1.0) # wait for filter to be applied
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
  return num

solana = get_used_dapps('solana')
print(solana)






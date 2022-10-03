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
def get_staking(crypto_code, dict_yield, dict_staked):
  # create driver
  chrome_options = Options()
  # chrome_options.add_argument("--headless")
  chrome_service = ChromeService(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
  driver.maximize_window()

  # get yield percent
  driver.get(f"https://www.stakingrewards.com/earn/{crypto_code}")
  nav_els = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "assetEarn_asset-information-value__xCpNU")))
  time.sleep(2.0) # allow javascript to finish loading
  yield_percent = nav_els[0].text

  # get amount staked from same webpage
  staking_ratio_el = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "assetCharts_participating-stat-container__W_XUH")))
  staked = staking_ratio_el[0].find_element(By.TAG_NAME, "h3").text

  # remove driver and return
  driver.close()
  driver.quit()
  dict_yield[crypto_code] = yield_percent
  dict_staked[crypto_code] = staked
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

# input and output to threads
crypto_codes = [
  "ethereum-2-0",
  "cardano",
  "solana",
  "avalanche",
  "binance-smart-chain",
  "tron",
  "algorand",
  "near-protocol",
  "flow",
  "matic-network",
  "polkadot",
  "cosmos",
  "tezos",
  "dfinity",
  "elrond",
  "thorchain",
  "eos",
  "harmony",
  "fantom"
]
dict_yield = {}
dict_staked = {}

# create threads and run with helper function
threads = []
for code in crypto_codes:
  threads += [Thread(target=get_staking, args=(code, dict_yield, dict_staked))]
run_threads(threads)

# print output
print("Staking yield: ")
print(dict_yield)
print("Percent of currency staked: ")
print(dict_staked)

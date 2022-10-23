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
def get_members(crypto, d):
  # variables
  crypto_name = crypto[0]
  crypto_code = crypto[1]

  # create driver
  chrome_options = Options()
  chrome_options.add_argument("--headless")
  chrome_service = ChromeService(ChromeDriverManager().install())
  driver = webdriver.Chrome(service=chrome_service, options=chrome_options)
  driver.maximize_window()

  # get yield percent
  driver.get(f"https://discord.com/invite/{crypto_code}")
  els = WebDriverWait(driver, 20).until(EC.visibility_of_all_elements_located((By.CLASS_NAME, "defaultColor-24IHKz.text-sm-normal-3Zj3Iv.pillMessage-3pHz6R")))
  # time.sleep(2.0) # allow javascript to finish loading
  members = els[1].text
  
  driver.close()
  driver.quit()
  d[crypto_name] = members
  return

# run threads recursively in groups of groups
groups = 1
def run_threads(threads):
  if len(threads) < groups:
    # base case, run all
    for thread in threads:
      thread.start()
    for thread in threads:
      thread.join()
    return
  else:
    # run 6, then recurse on remaining
    for i in range(groups):
      threads[i].start()
    for i in range(groups):
      threads[i].join()
    run_threads(threads[groups:])

# input and output to threads
crypto_codes = [
  ("Ethereum", "CetY6Y4"),
  ("Cardano", "TUr9RDU"),
  ("Solana", "pquxPsq"),
  ("Avalanche", "RwXY7P6"),
  ("Binance Chain", "bnbchain"),
  ("Tron", "tron"),
  ("Algorand", "84AActu3at"),
  ("Near", "UY9Xf2k"),
  ("Flow", "flow"),
  ("Polygon", "XvpHAxZ"),
  ("Polkadot", "CarTrFyppf"),
  ("Cosmos", "cosmosnetwork"),
  ("Tezos", "yXaPy6s5Nr"),
  ("Internet Computer", "rB96MMn"),
  ("Elrond", "VsmrGNWjND"),
  ("Thor Chain", "tW64BraTnX"),
  ("EOS", "eos-network"),
  ("Harmony", "rdCmBpe"),
  ("Fantom", "zS4Ek4WByA"),
  ("Bitcoin", "okcash")
]
d = {}

# create threads and run with helper function
threads = []
for code in crypto_codes:
  threads += [Thread(target=get_members, args=(code, d))]
run_threads(threads)

# print output
print("Number of discord members: ")
print(d)

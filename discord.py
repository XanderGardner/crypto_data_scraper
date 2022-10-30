#!/usr/bin/python3

import os
import pathlib
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
from threading import Thread
from collections import OrderedDict
import re
  
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
  active = els[0].text
  members = els[1].text
  
  driver.close()
  driver.quit()
  d[crypto_name] += [active, members] # d[crypto_name] must already exist
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

# returns resource path for users environment given the relative path
def resource_path(relative_path):
  try:
    base_path = sys._MEIPASS
  except Exception:
    base_path = os.path.dirname(__file__)
  return os.path.join(base_path, relative_path)

def main():
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

  # create threads and run with helper function
  d = OrderedDict()
  threads = []
  for code in crypto_codes:
    d[code[0]] = []
    threads += [Thread(target=get_members, args=(code, d))]
  run_threads(threads)
  print(f"found all values: {d}")

  # get current time
  dt = datetime.now()
  time_string = dt.strftime("%m-%d-%y %I%p %z")[:-1]

  # check output csv file
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    print('running in a PyInstaller bundle')
    rel_path = os.path.dirname(sys.executable)
    path = os.path.join(rel_path, 'discord_data.csv')
  else:
    print('running in a normal Python process')
    path = pathlib.Path(__file__).parent / 'discord_data.csv'
  
  exists = os.path.isfile(path)
  file = open(path, 'a')
  if not exists:
    # create top header row
    file.write("Type,Time,")
    for code in crypto_codes:
      file.write(f"{code[0]},")
    file.write("\n")

  # print to output csv
  file.write(f"Online,{time_string},")
  for key in d.keys():
    # format active number
    active = d[key][0][:-7]
    active =  re.sub(",","",active)
    file.write(f"{active},")
  file.write("\n")

  file.write(f"Members,{time_string},")
  for key in d.keys():
    # format members number
    members = d[key][1][:-8]
    members =  re.sub(",","",members)
    file.write(f"{members},")
  file.write("\n")

  #file.write(time_string + "\n")
  file.close()

if __name__ == "__main__":
  main()
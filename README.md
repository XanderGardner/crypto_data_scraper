Python scripts for scrapping data online for various cryptos

## Set up

Requirements
- Python 3
- Chrome

Python Installs
```
pip install selenium
pip install webdriver-manager
```

## Scripts

Scrape data from dappradar. Gets number of dapps and number of dapps with >= 1 user for each crypto:
```
python3 dapp.py
```

Scrape data from stakingrewards. Gets ratio staked and staking yield for each crypto:
```
python3 stake.py
```
## Discord Continuous Scraping

Set up a job to scrape every 12 hrs:
source: https://towardsdatascience.com/how-to-easily-automate-your-python-scripts-on-mac-and-windows-459388c9cc94

Create executable
```
pip install pyinstaller
pyinstaller --onefile discord.py
```
Then use crontab for mac or task scheduler for windows


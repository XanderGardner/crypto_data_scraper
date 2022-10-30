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

Set up a job to scrape every 6 hrs:

Useful sources: 
- https://betterprogramming.pub/how-to-execute-a-cron-job-on-mac-with-crontab-b2decf2968eb
- https://towardsdatascience.com/how-to-easily-automate-your-python-scripts-on-mac-and-windows-459388c9cc94
- https://crontab.guru/

How I got it to work on my mac:

Make discord.py executable for all
```
chmod 777 discord.py
ls -l
```

Added to crontab the following text:
```
0 */6 * * * cd ~/Desktop/Artemis/discord_scraping && /Library/Frameworks/Python.framework/Versions/3.9/bin/python3 discord.py >> ~/Desktop/Artemis/discord_scraping/cron.txt 2>&1
```
which in general is 
```
0 */6 * * * cd path_to_directory_with_py_file && path_to_python3 discord.py >> path_to_output_for_cron_errors 2>&1
```
Add using VIM in terminal
```
crontab -e
crontab -l
```

Give cron ability to run python3 by going to 
1. System Preference -> Security and Privacy -> Full Disk Access -> 
2. Click the Lock to Allow Changes 
3. Click the + Sign 
4. hit Command + Shift + G and in type '/usr/sbin/' 
5. scroll to find "cron" in the list of binaries 
6. Click "Open"

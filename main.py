from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
driver.get("https://www.google.com/robots.txt")

dom_text = None
try:
    WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.TAG_NAME, "body")
    ))
    time.sleep(1.0) # if need extra time to wait for javascript
    
    main_element = driver.find_element(by=By.TAG_NAME, value="body")
    dom_text = main_element.text
finally:
    driver.close()
    driver.quit()
print(dom_text)
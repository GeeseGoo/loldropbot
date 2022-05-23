from time import sleep
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Enter your riot account username and password for the bot to auto log in
username = 'RIOT USERNAME'
password = 'PASSWORD'

# If you wish to use chrome you must get the webdriver for chromium
service = Service(".\geckodriver.exe")
service.start()
driver = webdriver.Firefox()

driver.get("https://lolesports.com/live")
sleep(5)
driver.find_element(By.CSS_SELECTOR, "._2I66LI-wCuX47s2um7O7kh").click()
sleep(5)
action = webdriver.ActionChains(driver)
action.send_keys(username, Keys.TAB, password, Keys.ENTER).perform()
sleep(5)

while True:
    sleep(300)
    if driver.current_url != "https://lolesports.com/live":
        continue
    driver.refresh()


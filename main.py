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

driver.get("https://lolesports.com")
driver.maximize_window()
sleep(3)
driver.find_element(By.CSS_SELECTOR, "._2I66LI-wCuX47s2um7O7kh").click()
sleep(3)
action = webdriver.ActionChains(driver)
action.send_keys(username, Keys.TAB, password, Keys.ENTER).perform()
sleep(6)
a = driver.find_elements(by=By.CLASS_NAME, value="live")
for i in a:
    print(i.get_attribute('href'))

while True:
    driver.switch_to.window(driver.window_handles[0])
    sleep(2)
    streams = driver.find_elements(by=By.CLASS_NAME, value="live")
    tabs = []
    for handle in driver.window_handles:
        driver.switch_to.window(handle)
        tabs.append(driver.current_url)
        sleep(1)
    for i in streams:
        if i.get_attribute('href') not in tabs:
            driver.execute_script(f"window.open('{i.get_attribute('href')}','_blank');")
            driver.switch_to.window(driver.window_handles[-1])
            sleep(5)

    sleep(300)

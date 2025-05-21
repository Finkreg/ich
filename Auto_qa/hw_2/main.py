from selenium import webdriver
import time
from selenium.webdriver.firefox.service import Service
service = Service("/snap/bin/firefox.geckodriver")
driver = webdriver.Firefox( service=service)


driver.get("https://itcareerhub.de")
time.sleep(3)

driver.get("https://itcareerhub.de/#rec725797078")
time.sleep(3)

driver.save_screenshot("payment.png")
driver.quit()
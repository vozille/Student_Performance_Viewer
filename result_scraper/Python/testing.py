import threading
import time
from datetime import date
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


def find_by_xpath(driver, locator, timeout=2):
    element = WebDriverWait(driver, timeout).until(
        ec.presence_of_element_located((By.XPATH, locator))
    )
    return element
driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
driver.get('http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')

i = 2
while True:
    try:
        find_by_xpath(driver, '//*[@id="ddlSession"]').click()
        find_by_xpath(driver, '//*[@id="ddlSession"]/option['+ str(i) +']').click()
        find_by_xpath(driver, '//*[@id="ddlSession"]').click()
        i += 1
    except Exception:
        break


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
driver = webdriver.Chrome()
driver.get('http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
find_by_xpath(driver, '//*[@id="ddlSession"]').click()
find_by_xpath(driver, '//*[@id="ddlSession"]/option[2]').click()
find_by_xpath(driver, '//*[@id="ddlSession"]').click()

import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import string
import os

i = 0
driver = webdriver.Chrome()
# the url of the post/comment
driver.get('https://m.facebook.com/birthdays')

while i < 2: # the number of comments you want to post
    def find_by_xpath(locator):
        element = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, locator))
        )
        return element

    class FormPage(object):
        def fill_form(self):
            cnt = 1
            while True:
                try:
                    res = find_by_xpath('//*[@id="events_card_list"]/article[2]/div/div/ul/li[' + str(cnt) + ']').text
                    print res
                    cnt += 1
                except selenium.common.exceptions.TimeoutException:
                    break
            time.sleep(1)
    if i == 0:
        # open your account, login with username and password
        # find_by_xpath('//*[@id="root"]/div[1]/div/a[2]').click()
        find_by_xpath('//*[@id="u_0_1"]/div[1]/div/input').send_keys('anwesh063@rediffmail.com')
        find_by_xpath('//*[@id="u_0_2"]').send_keys('temporary12345')
        find_by_xpath('//*[@id="u_0_6"]').click()
    else:
        FormPage().fill_form()
        #driver.get('https://m.facebook.com/messages/thread/100005719363135/')
    i += 1

driver.close()

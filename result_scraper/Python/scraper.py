import sys
import threading
import time
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class Webscraper(threading.Thread):
    def __init__(self, start, end, birthday, url):
        threading.Thread.__init__(self)
        self.start_roll = start
        self.end_roll = end
        self.birthday = birthday
        self.url = url

    @staticmethod
    def __find_by_xpath(driver, locator, timeout=4):
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, locator))
        )
        return element

    def run(self):
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        driver.get(self.url)
        mybirthday = self.birthday.strftime("%d/%m/%Y")
        self.__find_by_xpath(driver, '//*[@id="dpStudentdob_dateInput"]').send_keys(mybirthday)
        for roll_num in range(self.start_roll, self.end_roll):
            year_iterator = 2
            while True:
                try:
                    self.__find_by_xpath(driver, '//*[@id="ddlSession"]').click()
                    self.__find_by_xpath(driver, '//*[@id="ddlSession"]/option[' + str(year_iterator) + ']').click()
                    self.__find_by_xpath(driver, '//*[@id="ddlSession"]').click()
                    year_iterator += 1
                    try:
                        self.__find_by_xpath(driver, '//*[@id="txtRegNo"]').clear()
                        self.__find_by_xpath(driver, '//*[@id="txtRegNo"]').send_keys(str(roll_num))
                        self.__find_by_xpath(driver, '//*[@id="btnView"]').click()
                        # print self.__find_by_xpath(driver, '', 1)
                        try:
                            try:
                                # gets last link
                                list_links = driver.find_elements_by_xpath("//*[contains(text(), 'View Result')]")
                                del list_links[0]
                                result_links = []
                                # add more fine control if required
                                while len(list_links) > 0:
                                    result_link = list_links[-1].get_attribute('href')[25:60]
                                    result_link = result_link.replace("$", "_")
                                    result_links.append(result_link)
                                    list_links.pop(-1)
                            except:
                                continue
                            # print result_links
                            for result_link in result_links:
                                """
                                The webpage has been loaded, do anything you want
                                """
                                self.__find_by_xpath(driver, '//*[@id="' + result_link + '"]').click()
                                name = self.__find_by_xpath(driver, '//*[@id="lblName"]').text
                                branch = self.__find_by_xpath(driver, '//*[@id="lblResultName"]').text
                                subjects = self.__find_by_xpath(driver,
                                                                '//*[@id="tblBasicDetail"]/table/tbody/tr[8]/td').text
                                # remove commas
                                name = name.replace(",", "")
                                branch.replace(",", "")
                                branch = branch.split(',')

                                """
                                What I am doing here is printing data so that i can save it later in a csv file
                                And upload it later to a database
                                """
                                output_files = {
                                    '1st': 'o1.csv',
                                    'First': 'o1.csv',
                                    '2nd': 'o2.csv',
                                    'Second': 'o2.csv',
                                    '3rd': 'o3.csv',
                                    'Third': 'o3.csv',
                                    '4th': 'o4.csv',
                                    'Fourth': 'o4.csv',
                                    '5th': 'o5.csv',
                                    'Fifth': 'o5.csv',
                                    '6th': 'o6.csv',
                                    'Sixth': 'o6.csv',
                                    '7th': 'o7.csv',
                                    'Seventh': 'o7.csv',
                                    '8th': 'o8.csv',
                                    'Eigth': 'o8.csv'}
                                for i in output_files:
                                    if i in branch[1]:
                                        sys.stdout = open('../inputs/' + output_files[i], 'a')
                                # filter sem wise
                                # if '7th' not in branch[1]:
                                #     continue
                                print name + ' ,' + branch[0] + ' ,' + str(roll_num).strip(' ') + ',',
                                subjects = subjects.split('\n')
                                del subjects[0]
                                for k in subjects:
                                    res = k.replace(",", "")
                                    res = res.replace(' *', "")
                                    print res + ',',
                                print
                                sys.stdout = sys.__stdout__
                                time.sleep(0.2)
                                # uncomment to do semester wise scraping
                                # break
                        except:
                            pass
                    except:
                        pass
                except:
                    print 'Done ' + str(roll_num).strip(' ')
                    break
        driver.close()


def clean():
    output_files = {'First': 'o1.csv', '2nd': 'o2.csv', '3rd': 'o3.csv', '4th': 'o4.csv', '5th': 'o5.csv',
                    '6th': 'o6.csv', '7th': 'o7.csv', '8th': 'o8.csv'}
    for i in output_files:
        sys.stdout = open('../inputs/' + output_files[i], 'w')
        sys.stdout = sys.__stdout__


def main():
    clean()
    # dont know why this date works for everyone
    bday = date(1995, 1, 1)
    # start roll
    start, end = 1401106001, 1401106610
    if abs(start - end) > 1000:
        raise Exception("Too many values to extract, use proper limits")
    i = start
    threads = []
    while i < end:
        increment = 180
        t = Webscraper(i, i + increment, bday,
                       'http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx')
        threads.append(t)
        i += increment

    for i in threads:
        i.start()
        # well, opening web browsers takes time
        time.sleep(6)
    for i in threads:
        i.join()
    print
    print
    print "Done "


if __name__ == '__main__':
    main()
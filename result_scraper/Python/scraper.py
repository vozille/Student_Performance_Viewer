import sys
import threading
import time
from datetime import date
import pymysql
import result_scraper.Python.Constants as Constants

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait


class Webscraper(threading.Thread):
    def __init__(self, start, end, custom_rolls=None):
        threading.Thread.__init__(self)
        self._start_roll = start
        self._end_roll = end
        self._birthday = date(1995, 1, 1)
        self._url = 'http://www.bputexam.in/StudentSection/ResultPublished/StudentResult.aspx'
        self._custom_rolls = custom_rolls
        self._ERROR_URL = "http://www.bputexam.in/ErrorMessege.htm?aspxerrorpath=/" \
                          "StudentSection/ResultPublished/StudentResult.aspx"

        self._connection = None

        if self._custom_rolls is None:
            self._custom_rolls = []
            for roll in range(self._start_roll, self._end_roll):
                self._custom_rolls.append(roll)

    def _connect_to_database(self):
        self._connection = pymysql.connect(host=Constants.db_host, user=Constants.db_user, passwd=Constants.db_password,
                                           db=Constants.db_name)

    def _get_missing_rolls(self, semester_id, limit):
        if self._connection is None:
            self._connect_to_database()

        cursor = self._connection.cursor()
        query = 'SELECT student_id FROM exam WHERE semester_id = "' + semester_id + '";'
        cursor.execute(query)
        present = set()
        self._custom_rolls = []
        for row in cursor:
            present.add(int(row[0]))
        semester_id = semester_id[:-2] + str(int(semester_id[-1]) - 1)
        query = 'SELECT student_id FROM exam WHERE semester_id = "' + semester_id + '";'
        cursor.execute(query)
        for row in cursor:
            if int(row[0]) not in present and int(row[0]) < limit:
                self._custom_rolls.append(row[0])


    @staticmethod
    def __find_by_xpath(driver, locator, timeout=4):
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, locator))
        )
        return element

    def run(self):
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        driver.get(self._url)
        mybirthday = self._birthday.strftime("%d/%m/%Y")
        self.__find_by_xpath(driver, '//*[@id="dpStudentdob_dateInput"]').send_keys(mybirthday)

        for roll_num in self._custom_rolls:
            year_iterator = 2
            while True:
                try:
                    if driver.current_url == self._ERROR_URL:
                        driver.execute_script("window.history.go(-1)")
                        continue
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
                                output_files = Constants.output_files_dict
                                for i in output_files:
                                    if i in branch[1]:
                                        sys.stdout = open(Constants.input_path + output_files[i], 'a')
                                # filter sem wise
                                # if '7th' not in branch[1]:
                                #     continue
                                print(name + ' ,' + branch[0] + ' ,' + str(roll_num).strip(' ') + ',', end=' ')
                                subjects = subjects.split('\n')
                                del subjects[0]
                                for k in subjects:
                                    res = k.replace(",", "")
                                    res = res.replace(' *', "")
                                    print(res + ',', end=' ')
                                print()
                                sys.stdout = sys.__stdout__
                                # time.sleep(0)
                                # uncomment to do semester wise scraping
                                # break
                        except:
                            pass
                    except:
                        pass
                except:
                    print('Done ' + str(roll_num).strip(' '))
                    break
        driver.close()


class LegacyWebScraper(threading.Thread):
    def __init__(self, start, end, url_code, output_file, custom_rolls=None):
        threading.Thread.__init__(self)

        self.output_file = output_file
        self._start_roll = start
        self._end_roll = end + 1
        self._url_code = str(url_code)
        self._url = "http://results.bput.ac.in/" + self._url_code + "_RES/"
        self._custom_rolls = custom_rolls
        self._connection = None

        if self._custom_rolls is None:
            self._custom_rolls = []
            for roll in range(self._start_roll, self._end_roll):
                self._custom_rolls.append(roll)

    def _connect_to_database(self):
        self._connection = pymysql.connect(host=Constants.db_host, user=Constants.db_user, passwd=Constants.db_password,
                                           db=Constants.db_name)

    def _get_missing_rolls(self, semester_id, limit):
        if self._connection is None:
            self._connect_to_database()
        cursor = self._connection.cursor()
        query = 'SELECT student_id FROM exam WHERE semester_id = "' + semester_id + '";'
        cursor.execute(query)
        present = set()
        self._custom_rolls = []
        for row in cursor:
            present.add(int(row[0]))
        semester_id = semester_id[:-2] + str(int(semester_id[-1]) - 1)
        query = 'SELECT student_id FROM exam WHERE semester_id = "' + semester_id + '";'
        cursor.execute(query)
        for row in cursor:
            if int(row[0]) not in present and int(row[0]) < limit:
                self._custom_rolls.append(row[0])


    @staticmethod
    def __find_by_xpath(driver, locator, timeout=1):
        element = WebDriverWait(driver, timeout).until(
            ec.presence_of_element_located((By.XPATH, locator))
        )
        return element

    def run(self):
        driver = webdriver.Chrome('/usr/lib/chromium-browser/chromedriver')
        for roll in self._custom_rolls:
            driver.get(self._url + str(roll) + ".html")
            try:
                name = self.__find_by_xpath(driver, "/html/body/table/tbody/tr[3]/td/table/tbody/tr[2]/td[2]/b").text
                roll = self.__find_by_xpath(driver, "/html/body/table/tbody/tr[3]/td/table/tbody/tr[1]/td[2]").text
                branch = self.__find_by_xpath(driver, "/html/body/table/tbody/tr[3]/td/table/tbody/tr[4]/td[2]/b").text
                raw_table = self.__find_by_xpath(
                    driver, "/html/body/table/tbody/tr[5]/td/table").text
                table = (raw_table.split("\n"))
                sys.stdout = open(self.output_file, 'a')
                print(name, sep=',', end=',')
                print(branch, sep=',', end=',')
                print(roll, sep=',', end=', ')
                for i in range(1, len(table) - 1):
                    print(table[i][:-9],sep=',', end=', ')
                print("Total Credits: 26 SGPA: 8.11")
                sys.stdout = sys.__stdout__
            except:
                pass
        driver.close()


def clean():
    output_files = Constants.output_files_dict
    for i in output_files:
        sys.stdout = open(Constants.input_path + output_files[i], 'w')
        sys.stdout = sys.__stdout__


def main():
    clean()
    # # dont know why this date works for everyone
    # start roll
    start, end = 1422106001, 1422106012
    if abs(start - end) > 1000:
        raise Exception("Too many values to extract, use proper limits")
    i = start
    threads = []
    while i < end:
        increment = 20
        t = Webscraper(i, i + increment)
        threads.append(t)
        i += increment

    for i in threads:
        i.start()
        # well, opening web browsers takes time
        time.sleep(6)
    for i in threads:
        i.join()

    """
    zone II
    """

    # ids = [475, 534]
    # for i in range(len(ids)):
    #     scraper = LegacyWebScraper(1422106001, 1422106040,
    #                                ids[i], Constants.input_path + Constants.output_files_names[i])
    #     scraper.start()
    #     time.sleep(1)

    # t = Webscraper(-1,-1, bday, custom_rolls)
    # t.start()


if __name__ == '__main__':
    main()

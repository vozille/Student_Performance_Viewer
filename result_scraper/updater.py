import csv
import sys
from operator import itemgetter
from collections import OrderedDict
import pymysql

sys.stdout = open('update.txt', 'w')
sys.stdout = open('insert.txt', 'w')
sys.stdout = open('output.txt', 'w')

# TODO : be really careful about ID's
# FIXME : code is horrible, rewrite it again
# TODO : add documentation

exam_id = 1012


class PreprocessData:
    def __init__(self, exam_id, batch_year, student_type, input_file):
        self.exam_id = exam_id
        self.input_file = input_file
        self.data = []
        self.year = batch_year
        self.type = student_type
        self.__get_data()

    def __get_data(self):
        data = []
        with open(self.input_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            flag = False
            for i in reader:
                if not flag:
                    flag = True
                else:
                    data.append(i)
        data.sort(key=itemgetter(2))
        self.data = data


class UpdateGradeCG(PreprocessData):
    def print_grades(self):
        new_data = self.filter_data()
        # you could directly connect with db if it's locally available
        print 'INSERT IGNORE INTO `score` (student_id, subject_id, grade, semester_id) VALUES',
        while len(new_data) > 0:
            data = new_data[0]
            while len(data[2]) > 0:
                print '("' + data[0] + '","' + str(data[2][0][0]) + '","' + str(data[2][0][1]) + '",' + str(
                    data[2][0][-1]) + '),'
                data[2].pop(0)
            new_data.pop(0)

    def print_cg(self):
        new_data = self.filter_data()
        # you could directly connect with db if it's locally available
        print 'INSERT IGNORE INTO exam (student_id,semester_id,sgpa,credits) VALUES ',
        while len(new_data) > 0:
            data = new_data[0]
            print '("' + data[0] + '",' + str(data[1]) + ',' + str(data[3]) + ',' + str(data[-1]) + '),'
            new_data.pop(0)

    def filter_data(self):
        # more formatting of data wrt to our needs
        """
        :param data: unformatted data
        :rtype: list
        """
        roll = self.data[2]
        subjects = []
        i = 3
        self.exam_id = 0
        while True:
            try:
                element = map(str, self.data[i].split(' '))
                element.pop(0)
                int(element[0])
                i += 1
                subjects.append(tuple([element[1], element[-1], exam_id]))
            except ValueError:
                break
        element = map(str, self.data[i].split(' '))
        element.pop(0)
        credit = int(element[2])
        sgpa = float(element[-1])
        return roll, self.exam_id, subjects, sgpa, credit


class NewStudents(PreprocessData):
    def print_student(self):
        # you could directly connect with db if it's locally available
        print 'INSERT IGNORE IGNORE INTO `student` (regno, name, branch_id, batch, cgpa, course) VALUES',
        new_data = list(self.data)
        while len(new_data) > 0:
            print '("' + new_data[0][2] + '","' + new_data[0][0][1:-1] + '","' + self.__branch_helper(new_data[0][1]) + \
                  '","' \
                  + self.year + '",' + "null" + ',"' + self.type + '"' + '),'
            new_data.pop(0)

    def print_subjects(self):
        d = {}
        for i in self.data:
            res = self.__get_subject_credit_combo(i)
            for j in res:
                if j[0] not in d:
                    d[j[0]] = tuple([j[1], j[2]])
        print 'INSERT IGNORE INTO `subject` (code, name, credits) VALUES',
        for i in d:
            print '("' + i + '","' + d[i][1] + '",' + d[i][0] + '),'

    @staticmethod
    def __get_subject_credit_combo(data):
        res = []
        for i in range(3, len(data) - 2):
            k = map(str, data[i].split())
            try:
                res.append([k[1], k[-2]])
                subname = ''
                k.pop(0)
                k.pop(0)
                while True:
                    try:
                        int(k[0])
                        break
                    except ValueError:
                        subname += k[0] + ' '
                        k.pop(0)
                res[-1].append(subname[:-1])
            except IndexError:
                return res
        return res

    @staticmethod
    def __branch_helper(branch_name):
        if "MECHANICAL" in branch_name:
            return "ME"
        if "BIO" in branch_name:
            return "BT"
        if "COMPUTER" in branch_name:
            return "CSE"
        if "ELECTRICAL" in branch_name:
            return "EE"
        if "FASHION" in branch_name:
            return "FT"
        if "ELECTRONICS" in branch_name:
            return "IEE"
        if "INFORMATION" in branch_name:
            return "IT"
        if "TEXTILE" in branch_name:
            return "TE"
        if "CIVIL" in branch_name:
            return "CE"
        return "chutiya"


def get_data(input_file):
    """
    :type input_file: object
    """
    data = []
    with open(input_file, 'r') as csvFile:
        reader = csv.reader(csvFile)
        flag = False
        for i in reader:
            if not flag:
                flag = True
            else:
                data.append(i)
    return data


def filter_data(data):
    # more formatting of data wrt to our needs
    """
    :param data: unformatted data
    :rtype: list
    """
    global exam_id
    roll = data[2]
    subjects = []
    i = 3
    while True:
        try:
            element = map(str, data[i].split(' '))
            element.pop(0)
            int(element[0])
            i += 1
            subjects.append(tuple([element[1], element[-1], exam_id]))
        except ValueError:
            break
    element = map(str, data[i].split(' '))
    element.pop(0)
    credit, sgpa = '', ''
    try:
        credit = int(element[2])
        sgpa = float(element[-1])
    except:
        pass
    return roll, exam_id, subjects, sgpa, credit


def insert_sgpa(data2):
    sys.stdout = open('output.txt', 'a')
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
    cursor = conn.cursor()

    # you could directly connect with db if it's locally available
    while len(data2) > 0:
        data = data2[0]
        q = 'SELECT * FROM exam WHERE student_id ="' + data[0] + '" and semester_id =' + str(data[1])
        cursor.execute(q)
        if cursor.rowcount == 0:
            print 'INSERT IGNORE INTO exam (student_id,semester_id,sgpa,credits) VALUES ',
            print '("' + data[0] + '",' + str(data[1]) + ',' + str(data[3]) + ',' + str(data[-1]) + ');'
        data2.pop(0)


def insert_grades(data2):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
    # you could directly connect with db if it's locally available
    sys.stdout = sys.__stdout__

    while len(data2) > 0:
        data = data2[0]
        while len(data[2]) > 0:
            cursor = conn.cursor()
            query = 'SELECT * FROM score where student_id = "' + data[0] + '" and subject_id ="' + data[2][0][0] + '"'
            cursor.execute(query)
            if cursor.rowcount != 0:
                sys.stdout = sys.__stdout__
                sys.stdout = open('update.txt', 'a')
                print 'UPDATE `score` SET `grade` = "' + data[2][0][1] + '" where student_id = "' + data[
                    0] + '" and subject_id ="' + data[2][0][0] + '";'
                pass
            else:
                sys.stdout = sys.__stdout__
                sys.stdout = open('insert.txt', 'a')
                print 'INSERT IGNORE INTO `score` (student_id, subject_id, grade, semester_id) VALUES',
                print '("' + data[0] + '","' + str(data[2][0][0]) + '","' + str(data[2][0][1]) + '",' + str(
                    data[2][0][-1]) + ');'
            data[2].pop(0)
            cursor.close()
        data2.pop(0)


def insert_student(data,batch, student_type='reg'):
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
    cursor = conn.cursor()
    q = 'SELECT * FROM student WHERE regno ="' + data[2] + '";'
    cursor.execute(q)
    if cursor.rowcount != 0:
        return
    # you could directly connect with db if it's locally available
    # change reg = regular, le = lateral entry
    # change year as well as per requirement
    print 'INSERT IGNORE INTO `student` (regno, name, branch_id, batch, cgpa, course) VALUES',
    print '("' + data[2] + '","' + data[0][:-1] + '","' + branch_helper(data[1]) + '",' + batch + "," + "null" + \
          ',"' + student_type + '");'


def branch_helper(branch_name):
    """
    picks out the branch code on the basis of branch name
    :param branch_name: branch name
    :return:
    """
    if "MECHANICAL" in branch_name:
        return "ME"
    if "BIO" in branch_name:
        return "BT"
    if "COMPUTER" in branch_name:
        return "CSE"
    if "ELECTRICAL" in branch_name:
        return "EE"
    if "FASHION" in branch_name:
        return "FT"
    if "ELECTRONICS" in branch_name:
        return "IEE"
    if "INFORMATION" in branch_name:
        return "IT"
    if "TEXTILE" in branch_name:
        return "TE"
    if "CIVIL" in branch_name:
        return "CE"
    return "chutiya"


def get_subject_credit_combo(data):
    # TODO : add database connection to better this
    res = []
    for i in range(3, len(data) - 2):
        k = map(str, data[i].split())
        try:
            res.append([k[1], k[-2]])
            subname = ''
            k.pop(0)
            k.pop(0)
            while True:
                try:
                    int(k[0])
                    break
                except ValueError:
                    subname += k[0] + ' '
                    k.pop(0)
            res[-1].append(subname[:-1])
        except IndexError:
            return res
    return res


def update_sgpa(start, end):
    """
    modifies the sgpa after rechecking/back paper results
    :param start: start roll number
    :param end: end roll number
    """
    if abs(start - end) > 1500:
        raise Exception("Difference too large")
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
    cursor = conn.cursor()
    grade_dict = {'O': 10, 'E': 9, 'A': 8, 'B': 7, 'C': 6, 'D': 5, 'F': 2, 'M': 0, 'S': 0}
    for roll in range(start, end):
        query = 'select DISTINCT semester_id FROM score where student_id="' + str(roll) + '";'
        cursor.execute(query)
        if cursor.rowcount == 0:
            continue
        sem_ids = []
        for row in cursor:
            sem_ids.append(row[0])
        for sem in sem_ids:
            query = 'SELECT subject_id,grade FROM score where student_id ="' + str(roll) + '" and semester_id=' + str(
                sem)
            cursor.execute(query)
            if cursor.rowcount == 0:
                continue
            total_credits = 0
            earned_credits = 0
            for row in cursor:
                sub_code, sub_grade = row[0], row[1]
                query = 'SELECT credits FROM subject WHERE code ="' + sub_code + '"'
                cursor2 = conn.cursor()
                cursor2.execute(query)
                credit = 0
                for credit_iter in cursor2:
                    credit = credit_iter[0]
                earned_credits += grade_dict[sub_grade] * credit / 10.0
                total_credits += credit
            new_sgpa = round(earned_credits * 10.0 / total_credits, 2)
            sys.stdout = open('update.txt', 'a')
            print 'UPDATE `exam` SET `sgpa` =' + str(new_sgpa) + ' WHERE `semester_id`= ' + str(
                sem) + ' AND `student_id`="' + str(roll) + '";'


def porting():
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
    cursor = conn.cursor()
    query = 'SELECT student_id, subject_id, grade from back_score'
    cursor.execute(query)
    sys.stdout = open('update.txt', 'a')
    for row in cursor:
        print 'UPDATE `score` SET `grade` = "' + row[2] + '" where student_id = "' + row[0] + '" and subject_id ="' + \
              row[1] + '";'


def update_cgpa(start, end):
    if abs(start - end) > 1000:
        raise Exception("Difference too large")
    conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
    cursor = conn.cursor()
    for roll in range(start, end):
        query = ' SELECT sgpa, credits FROM exam WHERE student_id ="' + str(roll) + '";'
        cursor.execute(query)
        total_credits = 0.0
        credits_secured = 0.0
        if cursor.rowcount == 0:
            continue
        for row in cursor:
            total_credits += float(row[1])
            credits_secured += float(row[0]) * float(row[1])
        cgpa = round(credits_secured/total_credits, 2)
        sys.stdout = open('update.txt', 'a')
        print 'UPDATE `student` SET `cgpa` = ' + str(cgpa) + ' WHERE regno = "' + str(roll) + '";'


def main():
    global exam_id
    exam_id = 1002
    output_files = OrderedDict()
    output_files['First'] = 'o1.csv'
    output_files['2nd'] = 'o2.csv'
    output_files['3rd'] = 'o3.csv'
    output_files['4th'] = 'o4.csv'
    output_files['5th'] = 'o5.csv'
    output_files['6th'] = 'o6.csv'
    output_files['7th'] = 'o7.csv'
    output_files['8th'] = 'o8.csv'
    """
    Fill the exam ids carefully
    """
    exam_ids = [345, 398, 473, 525, 1003, 1011]
    # separate
    update_cgpa(1301106000, 1301106650)
    # separate
    # for f in output_files:
    #     if len(exam_ids) == 0:
    #         break
    #     exam_id = exam_ids[0]
    #     exam_ids.pop(0)
    #     data = get_data(output_files[f])
    #     data.sort(key=itemgetter(2))
    #     # separate
    #
    #     newdata = []
    #     for i in range(len(data)):
    #         newdata.append(filter_data(data[i]))
    #     insert_grades(newdata)
    #     insert_sgpa(newdata)

        # separate

        # for i in data:
        #     insert_student(i, '2018', 'le')

    # separate
    # d = {}
    # for i in data:
    #     res = get_subject_credit_combo(i)
    #     for j in res:
    #         if j[0] not in d:
    #             d[j[0]] = tuple([j[1], j[2]])
    # print 'INSERT INTO `subject` (code, name, credits) VALUES',
    # for i in d:
    #     print '("' + i + '","' + d[i][1] + '",' + d[i][0] + '),'


if __name__ == '__main__':
    main()

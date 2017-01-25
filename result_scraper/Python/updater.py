import csv
import sys
from operator import itemgetter
import pymysql


class StudentType:
    def __init__(self):
        self.regular = "reg"
        self.lateral_entry = "le"


class PreprocessData:
    def __init__(self, batch_year, student_type):

        self.__total_semesters = 8
        self.__input_path = '../inputs/'
        self._input_files = []
        self._input_files.append(self.__input_path + 'o1.csv')
        self._input_files.append(self.__input_path + 'o2.csv')
        self._input_files.append(self.__input_path + 'o3.csv')
        self._input_files.append(self.__input_path + 'o4.csv')
        self._input_files.append(self.__input_path + 'o5.csv')
        self._input_files.append(self.__input_path + 'o6.csv')
        self._input_files.append(self.__input_path + 'o7.csv')
        self._input_files.append(self.__input_path + 'o8.csv')
        self._data = None
        self.__exam_id = None
        self.__current_exam_id = None

        self._batch_year = batch_year
        self._student_type = student_type
        self._connection = None
        self._sgpa_cgpa_data = []

        self._INSERT_SGPA_PATH = '../sql_queries/insert_sgpa.txt'
        self._INSERT_GRADES_PATH = '../sql_queries/update.txt'
        self._INSERT_NEW_STUDENT_PATH = '../sql_queries/insert_new_students.txt'
        self._UPDATE_PATH = '../sql_queries/update.txt'

        self.__clean_files()
        self.__generate_exam_ids()

    def __generate_exam_ids(self):
        self.__exam_id = []
        for i in range(self.__total_semesters):
            self.__exam_id.append(str(self._batch_year) + "-" + str(i + 1))

    def _connect_to_database(self):
        try:
            self._connection = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='results_db')
        except:
            pass

    def _get_data(self, input_file):
        data = []
        with open(input_file, 'r') as csvFile:
            reader = csv.reader(csvFile)
            flag = False
            for i in reader:
                if not flag:
                    flag = True
                else:
                    data.append(i)
        data.sort(key=itemgetter(2))
        self._data = data
        self.__current_exam_id = self.__exam_id[self._input_files.index(input_file)]

    def _filter_data_sgpa_grade(self):

        for row in self._data:
            roll = row[2]
            subjects = []
            i = 3
            while True:
                try:
                    element = map(str, row[i].split(' '))
                    element.pop(0)
                    int(element[0])
                    i += 1
                    subjects.append(tuple([element[1], element[-1], self.__current_exam_id]))
                except ValueError:
                    break
            element = map(str, row[i].split(' '))
            element.pop(0)
            credit, sgpa = '', ''
            try:
                credit = int(element[2])
                sgpa = float(element[-1])
            except:
                pass
            self._sgpa_cgpa_data.append([roll, self.__current_exam_id, subjects, sgpa, credit])

    def _add_subject_to_db(self):

        self.__clean_files()
        sys.stdout = open(self._UPDATE_PATH, 'w')

        if self._connection is None:
            self._connect_to_database()

        for ifile in self._input_files:
            self._get_data(ifile)
            for data in self._data:
                subject_list = []
                for i in range(3, len(data) - 2):
                    k = map(str, data[i].split())
                    try:
                        subject_list.append([k[1], k[-2]])
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
                        subject_list[-1].append(subname[:-1])
                    except IndexError:
                        break
                for subject in subject_list:
                    print 'INSERT IGNORE INTO `subject`(`code`, `name`, `credits`)' \
                          ' VALUES ("' + subject[0] + '", "'  + subject[2] + '", ' + subject[1] + ');'

        print "Run CommitToDB to commit the changes to database and rerun this program again to continue"
        exit(0)

    @staticmethod
    def _branch_helper(branch_name):

        branch_name = branch_name.upper()
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

    def __clean_files(self):
        sys.stdout = open(self._INSERT_SGPA_PATH, 'w')
        sys.stdout = open(self._INSERT_GRADES_PATH, 'w')
        sys.stdout = open(self._INSERT_NEW_STUDENT_PATH, 'w')
        sys.stdout = open(self._UPDATE_PATH, 'w')
        sys.stdout = sys.__stdout__


class GenerateSGCG(PreprocessData):

    def insert_sgpa(self):

        sys.stdout = open(self._INSERT_SGPA_PATH, "a")

        if self._connection is None:
            self._connect_to_database()

        for ifile in self._input_files:
            self._get_data(ifile)
            self._filter_data_sgpa_grade()

            cursor = self._connection.cursor()

            for data in self._sgpa_cgpa_data:
                q = 'SELECT * FROM exam WHERE student_id ="' + data[0] + '" and semester_id = "' + str(data[1]) + '"'
                cursor.execute(q)
                if cursor.rowcount == 0:
                    print 'INSERT IGNORE INTO exam (student_id,semester_id,sgpa,credits) VALUES ',
                    print '("' + data[0] + '","' + str(data[1]) + '",' + str(data[3]) + ',' + str(data[-1]) + ');'
        sys.stdout = sys.__stdout__

    def insert_grades(self):

        sys.stdout = open(self._UPDATE_PATH, 'a')

        if self._connection is None:
            self._connect_to_database()

        for ifile in self._input_files:
            self._get_data(ifile)
            self._filter_data_sgpa_grade()

            cursor = self._connection.cursor()

            for row in self._sgpa_cgpa_data:
                data = row
                while len(data[2]) > 0:
                    query = 'SELECT * FROM score where student_id = "' + data[0] + '" and subject_id ="' + data[2][0][
                        0] + '"'
                    cursor.execute(query)
                    if cursor.rowcount != 0:
                        print 'UPDATE `score` SET `grade` = "' + data[2][0][1][0] + '" where student_id = "' + data[
                            0] + '" and subject_id ="' + data[2][0][0] + '";'
                        pass
                    else:
                        cursor2 = self._connection.cursor()
                        query2 = 'SELECT * FROM subject WHERE code = "' + data[2][0][0] + '";'
                        cursor2.execute(query2)

                        # subject not present in db, add it

                        if cursor2.rowcount != 0:
                            sys.stdout = sys.__stdout__
                            print 'Subject missing, generating files to commit'
                            self._add_subject_to_db()
                        else:
                            sys.stdout = open(self._INSERT_GRADES_PATH, 'a')
                            print 'INSERT IGNORE INTO `score` (student_id, subject_id, grade, semester_id) VALUES',
                            print '("' + data[0] + '","' + str(data[2][0][0]) + '","' + str(data[2][0][1])[0] + '","' + str(
                                data[2][0][-1]) + '");'
                    data[2].pop(0)
        sys.stdout = sys.__stdout__

    def update_sgpa(self, start_roll, end_roll):
        """
        modifies the sgpa after rechecking/back paper results
        :param start_roll: start roll number
        :param end_roll: end roll number
        """
        if abs(start_roll - end_roll) > 1500:
            raise Exception("Difference too large")

        if self._connection is None:
            self._connect_to_database()

        cursor = self._connection.cursor()
        grade_dict = {'O': 10, 'E': 9, 'A': 8, 'B': 7, 'C': 6, 'D': 5, 'F': 2, 'M': 0, 'S': 0}

        for roll in range(start_roll, end_roll):
            query = 'select DISTINCT semester_id FROM score where student_id="' + str(roll) + '";'
            cursor.execute(query)
            if cursor.rowcount == 0:
                continue
            sem_ids = []
            for row in cursor:
                sem_ids.append(row[0])
            for sem in sem_ids:
                query = 'SELECT subject_id,grade FROM score where student_id ="' + str(
                    roll) + '" and semester_id= "' + str(sem) + '"'
                cursor.execute(query)
                if cursor.rowcount == 0:
                    continue
                total_credits = 0
                earned_credits = 0
                for row in cursor:
                    sub_code, sub_grade = row[0], row[1]
                    query = 'SELECT credits FROM subject WHERE code ="' + sub_code + '"'
                    cursor2 = self._connection.cursor()
                    cursor2.execute(query)
                    credit = 0
                    for credit_iter in cursor2:
                        credit = credit_iter[0]
                    earned_credits += grade_dict[sub_grade] * credit / 10.0
                    total_credits += credit
                new_sgpa = round(earned_credits * 10.0 / total_credits, 2)
                sys.stdout = open(self._UPDATE_PATH, 'a')
                print 'UPDATE `exam` SET `sgpa` =' + str(new_sgpa) + ' WHERE `semester_id`= "' + str(
                    sem) + '" AND `student_id`="' + str(roll) + '";'

    def update_cgpa(self, start, end):

        if self._connection is None:
            self._connect_to_database()

        if abs(start - end) > 1000:
            raise Exception("Difference too large")
        cursor = self._connection.cursor()

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
            cgpa = round(credits_secured / total_credits, 2)
            sys.stdout = open(self._UPDATE_PATH, 'a')
            print 'UPDATE `student` SET `cgpa` = ' + str(cgpa) + ' WHERE regno = "' + str(roll) + '";'


class NewStudents(PreprocessData):

    def insert_student(self):

        sys.stdout = open(self._INSERT_NEW_STUDENT_PATH, 'a')

        if self._connection is None:
            self._connect_to_database()

        cursor = self._connection.cursor()

        for ifile in self._input_files:
            self._get_data(ifile)
            for data in self._data:
                q = 'SELECT * FROM student WHERE regno ="' + data[2] + '";'
                cursor.execute(q)
                if cursor.rowcount == 0:
                    continue
                print 'INSERT IGNORE INTO `student` (regno, name, branch_id, batch, cgpa, course) VALUES',
                print '("' + data[2] + '","' + data[0][:-1] + '","' + self._branch_helper(data[1]) + '",' + \
                      str(self._batch_year) + "," + "null" + \
                      ',"' + self._student_type + '");'


def main():
    student_type = StudentType()
    s = GenerateSGCG(2017, student_type.regular)
    s.insert_grades()


if __name__ == '__main__':
    main()

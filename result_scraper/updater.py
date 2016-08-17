from operator import itemgetter
import sys
import csv

sys.stdout = open('output.txt', 'w')


# TODO : be really careful about ID's
# FIXME : code is horrible, rewrite it again
# TODO : add documentation

exam_id = 1002


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
        print 'INSERT INTO `score` (student_id, subject_id, grade, semester_id) VALUES',
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
        print 'INSERT INTO exam (student_id,semester_id,sgpa,credits) VALUES ',
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
        print 'INSERT INTO `student` (regno, name, branch_id, batch, cgpa, course) VALUES',
        new_data = list(self.data)
        while len(new_data) > 0:
            print '("' + new_data[0][2] + '","' + new_data[0][0][1:-1] + '","' + self.__branch_helper(new_data[0][1]) +\
                  '","'\
                  + self.year + '",' + "null" + ',"' + self.type + '"' + '),'
            new_data.pop(0)

    def print_subjects(self):
        d = {}
        for i in self.data:
            res = self.__get_subject_credit_combo(i)
            for j in res:
                if j[0] not in d:
                    d[j[0]] = tuple([j[1], j[2]])
        print 'INSERT INTO `subject` (code, name, credits) VALUES',
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
    exam_id = 0
    while True:
        try:
            element = map(str, data[i].split(' '))
            element.pop(0)
            int(element[0])
            exam_id = 1002  # started this new website at 1001
            i += 1
            subjects.append(tuple([element[1], element[-1], exam_id]))
        except ValueError:
            break
    element = map(str, data[i].split(' '))
    element.pop(0)
    credit = int(element[2])
    sgpa = float(element[-1])
    return roll, exam_id, subjects, sgpa, credit


def insert_sgpa(data2):
    # you could directly connect with db if it's locally available
    print 'INSERT INTO exam (student_id,semester_id,sgpa,credits) VALUES ',
    while len(data2) > 0:
        data = data2[0]
        print '("' + data[0] + '",' + str(data[1]) + ',' + str(data[3]) + ',' + str(data[-1]) + '),'
        data2.pop(0)


def insert_grades(data2):
    # you could directly connect with db if it's locally available
    print 'INSERT INTO `score` (student_id, subject_id, grade, semester_id) VALUES',
    while len(data2) > 0:
        data = data2[0]
        while len(data[2]) > 0:
            print '("' + data[0] + '","' + str(data[2][0][0]) + '","' + str(data[2][0][1]) + '",' + str(
                data[2][0][-1]) + '),'
            data[2].pop(0)
        data2.pop(0)


def insert_student(data):
    # you could directly connect with db if it's locally available
    # change reg = regular, le = lateral entry
    # change year as well as per requirement
    print '("' + data[2] + '","' + data[0][1:-1] + '","' + branch_helper(data[1]) + '",' + "2018" + "," + "null" + \
                                                                                              ',"' "le" + '"' + '),'


def branch_helper(s):

    if "MECHANICAL" in s:
        return "ME"
    if "BIO" in s:
        return "BT"
    if "COMPUTER" in s:
        return "CSE"
    if "ELECTRICAL" in s:
        return "EE"
    if "FASHION" in s:
        return "FT"
    if "ELECTRONICS" in s:
        return "IEE"
    if "INFORMATION" in s:
        return "IT"
    if "TEXTILE" in s:
        return "TE"
    if "CIVIL" in s:
        return "CE"
    return "chutiya"


def get_subject_credit_combo(data):
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


def main():
    data = get_data("databaseactive.csv")
    data.sort(key=itemgetter(2))
    # separate

    # newdata = []
    # for i in range(len(data)):
    #     newdata.append(filter_data(data[i]))
    # insert_sgpa(newdata)
    # insert_grades(newdata)

    # separate

    print 'INSERT INTO `student` (regno, name, branch_id, batch, cgpa, course) VALUES',
    for i in data:
        insert_student(i)

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

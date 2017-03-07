class SgpaCgpaModel:
    def __init__(self, roll, semester_id, subjects, sgpa, credits):
        self.student_id = roll
        self.semester_id = semester_id
        self.subjects = []
        for data in subjects:
            self.subjects.append(SubjectModel(data))
        self.sgpa = sgpa
        self.credits = credits


class SubjectModel:
    def __init__(self, raw_data):
        self.subject_id = raw_data[0]
        self.subject_grade = raw_data[1][0]
        self.semester_id = raw_data[2]


class StudentModel:
    def __init__(self, raw_data):
        self.student_id = raw_data[2]
        self.name = raw_data[0][:-1]
        self.branch = raw_data[1]
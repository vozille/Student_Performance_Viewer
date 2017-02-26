import os
import peewee


class ISubject:
    def __init__(self, raw_data):
        self.subject_id = raw_data[0]
        self.subject_grade = raw_data[1]
        self.semester_id = raw_data[2]


class IScore:
    def __init__(self):
        self.student_id = None
        self.subject_id = None
        self.grade = None
        self.semester_id = None


class IExam:
    def __init__(self):
        self.student_id = None
        self.semester_id = None
        self.sgpa = None
        self.credits = None

class IStudent:
    def __init__(self):
        self.student_id = None
        self.name = None
        self.branch_id = None
        self.batch = None
        self.cgpa = None
        self.course = None
        self.is_visible = None

DB_HOST = os.environ.get('OPENSHIFT_MYSQL_DB_HOST', 'localhost')
DB_PORT = os.environ.get('OPENSHIFT_MYSQL_DB_POORT', 3306)
DB_USER = os.environ.get('OPENSHIFT_MYSQL_DB_USERNAME', 'root')
DB_PASS = os.environ.get('OPENSHIFT_MYSQL_DB_PASSWORD', 'trymiracle')

DB_DEBUG_HOST = "localhost"
DB_DEBUG_PORT = 3306
DB_DEBUG_USER = 'root'
DB_DEBUG_PASS = 'root'
DB_DEBUG_DATABASE = 'results_db'

db = peewee.MySQLDatabase(
    DB_DEBUG_DATABASE, host=DB_DEBUG_HOST, port=DB_DEBUG_PORT, user=DB_DEBUG_USER, passwd=DB_DEBUG_PASS)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Branch(BaseModel):
    code = peewee.FixedCharField(unique=True)
    name = peewee.CharField()


class Student(BaseModel):
    student_id = peewee.CharField()
    name = peewee.CharField()
    branch_id = peewee.CharField()
    batch = peewee.IntegerField()
    cgpa = peewee.FloatField()
    course = peewee.CharField(choices = (('reg', 'regular'), ('le', 'lateral-entry')))
    is_visible = peewee.BooleanField(default=True)

    class Meta:
        primary_key = peewee.CompositeKey('student_id', 'batch')
        order_by = ('student_id',)


class Exam(BaseModel):
    student_id = peewee.CharField()
    semester_id = peewee.CharField()
    sgpa = peewee.FloatField()
    credits = peewee.IntegerField()

    class Meta:
        primary_key = peewee.CompositeKey('student_id', 'semester_id')


class Score(BaseModel):
    student_id = peewee.CharField()
    subject_id = peewee.CharField()
    grade = peewee.FixedCharField()
    semester_id = peewee.CharField()

    class Meta:
        primary_key = peewee.CompositeKey('student_id', 'subject_id')


class Semester(BaseModel):
    code = peewee.PrimaryKeyField()
    batch = peewee.IntegerField()
    num = peewee.IntegerField() # from 1 to 8


class Subject(BaseModel):
    code = peewee.CharField()
    name = peewee.CharField()
    credits = peewee.IntegerField()

    class Meta:
        primary_key = peewee.CompositeKey('code')
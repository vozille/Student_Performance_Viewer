import pymysql

conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
cursor = conn.cursor()

cursor.execute('SELECT * FROM exam WHERE student_id in ( SELECT regno FROM student where branch_id = "ME" and batch = 2017)')

student = {}

for row in cursor:
    if row[1] not in student:
        student[row[1]] = float(row[3])
    else:
        student[row[1]] += float(row[3])

ranks = []
for i in student:
    if int(i) < 1401106000:
        ranks.append([student[i]/6.0, i])
    else:
        ranks.append([student[i] / 4.0, i])
ranks.sort(reverse=True)
for i, j in enumerate(ranks):
    print i + 1, j
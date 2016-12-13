import pymysql
import sys
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
cursor = conn.cursor()

# with open('update.txt', 'r') as f:
#     i = 0
#     for q in f:
#         i += 1
#         cursor.execute(q)
#         conn.commit()
#         print 'committed : ' + str(i)
#
# with open('insert.txt', 'r') as f:
#     i = 0
#     for q in f:
#         i += 1
#         cursor.execute(q)
#         conn.commit()
#         print 'committed : ' + str(i)
#
# with open('output.txt', 'r') as f:
#     i = 0
#     for q in f:
#         i += 1
#         cursor.execute(q)
#         conn.commit()
#         print 'committed : ' + str(i)

batches = [2014, 2015, 2016]
q = 'SELECT code FROM branch'
cursor.execute(q)
branch_id = []
for row in cursor:
    branch_id.append(row[0])

d = {}
for i in batches:
    d[i] = {}
    for j in branch_id:
        d[i][j] = {}


for year in batches:
    for branch in branch_id:
        q = 'SELECT regno FROM student WHERE batch =' + str(year) + ' and branch_id = "' + branch + '";'
        cursor.execute(q)
        rolls = []
        for row in cursor:
            rolls.append(row[0])
        for roll in rolls:
            d[year][branch][roll] = []
            q = 'SELECT sgpa FROM exam WHERE student_id = "' + str(roll) + '";'
            cursor.execute(q)
            for grades in cursor:
                d[year][branch][roll].append(grades[0])
for i in batches:
    for j in branch_id:
        name = './results/' + str(i) + '_' + j + '.csv'
        sys.stdout = open(name, 'w')
        ctr = 0
        while True:
            if ctr > 7:+
                break
            print 'semester - ' + str(ctr + 1)
            print 'roll, sgpa'
            for roll in d[i][j]:
                if len(d[i][j][roll]) == 0:
                    continue
                print roll + ',' + str(d[i][j][roll][0])
                d[i][j][roll].pop(0)
            ctr += 1
            print

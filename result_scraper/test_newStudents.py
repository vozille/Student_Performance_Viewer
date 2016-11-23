import pymysql
import sys
conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='fakechintu', db='results_db')
cursor = conn.cursor()
sys.stdin = open('update.txt', 'r')


n = 602
for i in range(n):
    q = raw_input()
    if i == n - 1:
        print q
    cursor.execute(q)
    conn.commit()
    print 'committed : ' + str(i + 1)
# print cursor.rowcount
# student = {}
#
# for row in cursor:
#     if row[1] not in student:
#         student[row[1]] = float(row[3])
#     else:
#         student[row[1]] += float(row[3])
#
# ranks = []
# for i in student:
#     if int(i) < 1401106000:
#         ranks.append([student[i]/6.0, i])
#     else:
#         ranks.append([student[i] / 4.0, i])
# ranks.sort(reverse=True)
# for i, j in enumerate(ranks):
#     print i + 1, j
import pymysql
import sys
conn = pymysql.connect(host='localhost', user='root', passwd='root', db='results_db')
cursor = conn.cursor()

with open('../sql_queries/update.txt', 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print 'committed : ' + str(i)

with open('../sql_queries/insert_grades.txt', 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print 'committed : ' + str(i)

with open('../sql_queries/insert_sgpa.txt', 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print 'committed : ' + str(i)



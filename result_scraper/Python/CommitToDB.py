import pymysql
import result_scraper.Python.Constants as Constants

conn = pymysql.connect(host=Constants.db_host,
                       port=Constants.port,
                       user=Constants.db_user,
                       passwd=Constants.db_password,
                       db=Constants.db_name)

cursor = conn.cursor()

with open(Constants.UPDATE_PATH, 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print('committed : ' + str(i))

with open(Constants.INSERT_SGPA_PATH, 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print('committed : ' + str(i))

with open(Constants.INSERT_GRADES_PATH, 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print('committed : ' + str(i))


with open(Constants.INSERT_NEW_STUDENT_PATH, 'r') as f:
    i = 0
    for q in f:
        i += 1
        cursor.execute(q)
        conn.commit()
        print('committed : ' + str(i))

conn.close()

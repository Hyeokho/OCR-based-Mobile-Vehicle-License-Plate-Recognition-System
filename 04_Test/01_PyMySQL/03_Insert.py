# 데이터 베이스 값 삽입

import pymysql.cursors

conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor :
        sql = 'INSERT INTO test_mysql (email, password) VALUES (%s, %s)'
        cursor.execute(sql, ('test@test.com', 'my-passwd'))
    conn.commit()
    print(cursor.lastrowid)
    # 1 (last insert id)
finally:
    conn.close()
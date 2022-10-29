# 데이터 삭제

import pymysql.cursors

conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = 'DELETE FROM test_mysql WHERE email = %s'

        # 일치하는 내용 삭제
        cursor.execute(sql, ('my@test.com1123',))
    conn.commit()
    print(cursor.rowcount) # 1 (affected rows)
finally:
    conn.close()
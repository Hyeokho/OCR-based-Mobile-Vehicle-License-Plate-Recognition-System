# 데이터 베이스 생성 예제

import pymysql

conn = pymysql.connect(host='devcvc.iptime.org',
                       port=6050,
                       user='user1',
                       password='0000',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = 'CREATE DATABASE db'
        cursor.execute(sql)
    conn.commit()
finally:
    conn.close()
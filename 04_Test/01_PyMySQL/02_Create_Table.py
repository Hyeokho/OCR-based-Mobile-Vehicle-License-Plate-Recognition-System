# 데이터베이스 테이블 생성


import pymysql.cursors

conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')
try:
    with conn.cursor() as cursor:
        sql = '''
            CREATE TABLE test_mysql (
                id int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                email varchar(255) NOT NULL,
                password varchar(255) NOT NULL
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8
'''
        cursor.execute(sql)
    conn.commit()
finally:
    conn.close()
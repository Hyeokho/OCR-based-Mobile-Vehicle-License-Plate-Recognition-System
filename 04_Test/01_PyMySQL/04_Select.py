# 데이터 조회

import pymysql.cursors



id_temp = input('아이디를 입력하세요: ')
password_temp = input('패스워드를 입력하세요: ')

id = str(id_temp)
password = str(password_temp)

print(id+password)


conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')

#sql = 'SELECT * FROM test_python WHERE id ='+ id +'AND paswword ='+ password


# try 문법은 예외처리 할때 사용함
# finally : finally절은 try문 수행 도중 예외 발생 여부에 상관없이 항상 수행

try:
    with conn.cursor() as cursor:
        sql = "SELECT * FROM test_python WHERE id = %s AND password = %s"
        #sql = 'SELECT * FROM test_python WHERE id ='+ id +' AND password ='+ password
        #sql = 'SELECT * FROM test_python'
        cursor.execute(sql, (id, password))
        result = cursor.fetchall()
        #result = cursor.fetchone()
        print(result)

        # (1, 'test@test.com', 'my-passwd')
finally:
    conn.close()

'''
try:
    with conn.cursor() as cursor:
        sql = 'INSERT INTO users (email, password) VALUES (%s, %s)'
        cursor.execute(sql, ('your@test.com', 'your-passwd'))
    conn.commit()

    with conn.cursor() as cursor:
        sql = 'SELECT * FROM users'
        cursor.execute(sql)
        result = cursor.fetchall()
        print(result)
        # ((1, 'test@test.com', 'my-passwd'), (2, 'your@test.com', 'your-passwd'))
finally:
    conn.close()
'''
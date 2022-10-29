# 주차장 관리 : 입차

import pymysql.cursors
import time


# def regist_car_num(car_number:str, name:str, contact:str, DP:bool ):

car_number = '34다9988'
in_time = "1999-12-23 21:11:00" # 이것도 가능은 함
in_time = time.strftime("%Y-%m-%d %H:%M:00")


name = '홍길동'
contact = '019-1199-9090'
DP = '1'

conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = "INSERT INTO parking ( name, contact, car_number, DP, in_time) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(sql, (name, contact, car_number, DP, in_time))
        conn.commit()
        print(cursor.lastrowid)
        # 1 (last insert id)
finally:
    conn.close()
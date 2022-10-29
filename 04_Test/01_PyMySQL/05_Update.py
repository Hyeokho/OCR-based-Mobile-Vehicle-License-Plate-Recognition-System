# 데이터 수정

import pymysql.cursors

car_number = '40보4243' # 원래 차량 번호
change_car_number = '40보 4243' # 바꾸고자 할 차량 번호
name = '김'
contact = '010-1111-2222'
DP = 1

conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        # UPDATE freeboard SET title="how to update in mysql", date="07, Jul, 2016", writer="James" WHERE no="2000" LIMIT 1;
        sql = 'UPDATE test_python SET car_number = %s, name = %s, contact = %s, DP = %s  WHERE car_number = %s LIMIT 1'


        cursor.execute( sql, (change_car_number, name, contact, DP, car_number) )
    conn.commit()

    # print(cursor.rowcount) # 몇개 수정했는지 나옴 (affected rows)
finally:
    conn.close()
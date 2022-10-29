# 데이터 삭제

import pymysql.cursors
import dev_mysql
import dev_time

car_number = '34다9988'

conn = pymysql.connect(host='devcvc.iptime.org',
                       port = 6050,
                       user='user1',
                       password='0000',
                       db='dbc',
                       charset='utf8mb4')

try:
    with conn.cursor() as cursor:
        sql = 'DELETE FROM parking WHERE car_number = %s'

        in_time = dev_mysql.search_car_num_from_parking(car_number)['in_time']

        useHours = dev_time.getDiffTimetoTimeString(in_time)

        # 일치하는 내용 삭제
        cursor.execute(sql, car_number)
        conn.commit()
        # print(cursor.rowcount) # 몇개 삭제했는지 표시
finally:
    conn.close()
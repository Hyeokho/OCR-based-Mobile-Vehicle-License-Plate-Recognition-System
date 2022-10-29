import pymysql.cursors
import dev_time
import time
import datetime

zoneA = 100
zoneB = 200
zoneC = 50
zoneD = 30





# 7/23일 패치노트
#
# 07_func_test.py에서
# 1번에 registUser 함수 추가
# 11번에 creat_table_Sessio 함수 추가 (테이블 추가하는 함수라 준호는 필요없음)
# 7번에 입차 함수 수정 -> 입차하면 파킹테이블, 세션테이블 모두 추가함
# 8번에 출차 함수 수정 -> 출차하면 파킹테이블에서 삭제, 세션테이블에서 출차시간 추가


# 7/24일 패치노트
# A, B, C, D 구역 최대 주차구역 설정
# def in_out_re_able_Parking() 함수 추가


# 7/27일 패치노트
# 테이블, 필드, 데이터베이스 변경


# 8/26일 패치노트
# 1. 선불 주차장을 위한 자동 출차 시스템 추가
# 기존 후불 주차장과 다르게 입차 부분이 아래 함수를 사용
# prepay_in_car_parking(userCar:str, userName:str, userPhone:str, userDP:bool, userZone:str) 사용
# - 입차 후 3시간이 지나면 자동으로 출차 함
# - 입차 시 세션테이블에 자동으로 입차시간, 출차시간 추가함
#
#
# 2. 아파트 주차장을 위한 주차장 리셋 기능 추가
# 아파트 주차장의 경우 '리셋' 버튼을 누르면 주차장을 초기화 하고 아파트 주차장에 있는 차량을 다시 입차시킴
# APTreset_car_parking(userZone:str) 함수 사용
# - 아파트 이름을 입력 받아서 parking 테이블에서 해당 주차장의 데이터 다 삭제



# 9/8일 패치노트
# 1.  입차함수에 userZone:str 파라미터 추가






# 차량 등록 기능, 회원가입
def registUser(userID:str, userCar:str, userName:str, userPhone:str, userDP:bool):


    userPassword  = '000000'


    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            #
            sql = "INSERT INTO member (userID, userPassword, userName, userPhone, userCar, userDP) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (userID, userPassword, userName, userPhone, userCar, userDP))
        conn.commit()
        print(cursor.lastrowid)
        # 1 (last insert id)
    finally:
        conn.close()






# 차 번호판으로 회원 정보를 찾음
# 입력 파라미터는 문자열 타입의 car_number
def search_car_num_from_member(userCar:str):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')


    try:
        # 딕셔너리로 접근함
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM member WHERE userCar = %s"
            cursor.execute(sql, userCar)
            result = cursor.fetchone()
    finally:
        conn.close()

    return result



# 차 번호판으로 회원 정보를 찾음
# 입력 파라미터는 문자열 타입의 car_number
# 세션테이블에서 검색하여 정보를 찾음
def search_car_num_from_session(userCar:str):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')


    try:
        # 딕셔너리로 접근함
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM session WHERE userCar = %s ORDER BY inTime DESC"
            cursor.execute(sql, userCar)
            result = cursor.fetchone()

    finally:
        conn.close()

    return result





# 현재 입차된 차 중에서 차 번호판으로 회원 정보를 찾음
# 입력 파라미터는 문자열 타입의 car_number
def search_car_num_from_parking(userCar:str) :

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')


    try:
        # 딕셔너리로 접근함
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql = "SELECT * FROM parking WHERE userCar = %s"
            cursor.execute(sql, userCar)
            result = cursor.fetchone()
    finally:
        conn.close()

    return result





# 파킹테이블을 만듬
def creat_table_parking():

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = '''
                CREATE TABLE parking (
                    seq int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY, 
                    userName varchar(20) NOT NULL,
                    userPhone varchar(20) NOT NULL,
                    userCar varchar(20) NOT NULL,
                    userDP bool NOT NULL,
                    inTime varchar(20) NOT NULL,
                    outTime varchar(20) NOT NULL,
                    userZone varchar(20) NOT NULL
                ) ENGINE = InnoDB DEFAULT CHARSET=utf8

    '''
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()





# 출차 기능
# 차 번호판을 입력 받아서 parking 테이블에서 차량의 데이터 삭제
def out_car_parking(userCar:str):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    outTime = time.strftime("%Y-%m-%d %H:%M:00")

    try:
        with conn.cursor() as cursor:
            sql = 'UPDATE session SET outTime = %s WHERE userCar = %s AND outTime = %s LIMIT 1'

            cursor.execute(sql, (outTime, userCar, '0000-00-00 00:00:00'))


            sql = 'DELETE FROM parking WHERE userCar = %s LIMIT 1'

            # 일치하는 내용 삭제
            cursor.execute(sql, userCar)
            conn.commit()
            # print(cursor.rowcount) # 몇개 삭제했는지 표시
    finally:
        conn.close()


# 아파트 주차장
# 리셋 기능
# 아파트 이름을 입력받아서 특정 아파트의 주차장을 리셋시킴
def APTreset_car_parking(userZone:str):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:

            sql = 'DELETE FROM parking WHERE userZone = %s'

            # 일치하는 내용 삭제
            cursor.execute(sql, userZone)
            conn.commit()
            # print(cursor.rowcount) # 몇개 삭제했는지 표시
    finally:
        conn.close()






# 입차 기능
# 차 번호, 이름, 연락처, 장애인 차량 여부를 입력 받아서 parking 테이블에 차량의 데이터 입력
def in_car_parking(userCar:str, userName:str, userPhone:str, userDP:bool, userZone:str):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    inTime = time.strftime("%Y-%m-%d %H:%M:00")

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO parking ( userName, userPhone, userCar, userDP, inTime, userZone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (userName, userPhone, userCar, userDP, inTime, userZone))

            sql = "INSERT INTO session ( userName, userPhone, userCar, userDP, inTime, outTime, userZone) VALUES (%s, %s, %s, %s, %s, %s,  %s)"
            cursor.execute(sql, (userName, userPhone, userCar, userDP, inTime, '0000-00-00 00:00:00', userZone))

            conn.commit()
            #print(cursor.lastrowid) # 시퀀스 표시해줌
            # 1 (last insert id)
    finally:
        conn.close()




# 선불 주차장
# 입차 기능
# 차 번호, 이름, 연락처, 장애인 차량 여부를 입력 받아서 parking 테이블에 차량의 데이터 입력
# 선불 주차장은 따로 출차가 없으니까 출차 시간을 (입차시간+3시간)으로 해서 세션테이블에 넣음
def prepay_in_car_parking(userCar:str, userName:str, userPhone:str, userDP:bool, userZone:str):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    inTime = time.strftime("%Y-%m-%d %H:%M:00")
    outTime = dev_time.getCurrentStrMinTimLater(180)

    try:
        with conn.cursor() as cursor:
            sql = "INSERT INTO parking ( userName, userPhone, userCar, userDP, inTime, userZone) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (userName, userPhone, userCar, userDP, inTime, userZone))

            sql = "INSERT INTO session ( userName, userPhone, userCar, userDP, inTime, outTime, userZone) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(sql, (userName, userPhone, userCar, userDP, inTime, outTime, userZone))

            conn.commit()
            #print(cursor.lastrowid) # 시퀀스 표시해줌
            # 1 (last insert id)
    finally:
        conn.close()










# parking 테이블의 총 개수를 구함
#
def count_row_parking():

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = 'SELECT COUNT(*) FROM parking'

            # parking 테이블의 총 개수를 구함
            cursor.execute(sql)

            result = cursor.fetchone()

            conn.commit()

    finally:
        conn.close()

    return result[0]




# car_number = '13난3332' # 원래 차량 번호
# change_car_number = '11가3344' # 바꾸고자 할 차량 번호
def update_member(userCar:str, change_car_number:str, userName:str, userPhone:str, userDP:bool):

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            # UPDATE freeboard SET title="how to update in mysql", date="07, Jul, 2016", writer="James" WHERE no="2000" LIMIT 1;
            sql = 'UPDATE member SET userCar = %s, userName = %s, userPhone = %s, userDP = %s  WHERE userCar = %s LIMIT 1'

            cursor.execute(sql, (change_car_number, userName, userPhone, userDP, userCar))

        conn.commit()

        # print(cursor.rowcount) # 몇개 수정했는지 나옴 (affected rows)
    finally:
        conn.close()






# 세션테이블을 만듬
def creat_table_session():

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try:
        with conn.cursor() as cursor:
            sql = '''
                CREATE TABLE session (
                    seq int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
                    inTime varchar(20) NOT NULL,
                    outTime varchar(20) NOT NULL,
                    userName varchar(20) NOT NULL,
                    userPhone varchar(20) NOT NULL,
                    userCar varchar(20) NOT NULL,
                    userDP bool NOT NULL,
                    userZone varchar(20) NOT NULL
                ) ENGINE = InnoDB DEFAULT CHARSET=utf8

    '''
            cursor.execute(sql)
        conn.commit()
    finally:
        conn.close()




# 입차, 출차, 재차, 가능을 가져오는 함수
def in_out_re_able_Parking():

    conn = pymysql.connect(host='devcvc.iptime.org',
                           port=6050,
                           user='appuser',
                           password='0000',
                           db='testdb',
                           charset='utf8mb4')

    try :
        # 딕셔너리로 접근함
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            # 오늘 0시 이후에 입력된 레코드 들을 불러옴, 미래에 입차는 불가능하니까
            sql = "SELECT COUNT(*) as cnt_in_car from session where inTime  > CURRENT_DATE()"
            cursor.execute(sql)
            result = cursor.fetchone()
            cntInCar = result["cnt_in_car"]

            sql = "SELECT COUNT(*) as cnt_out_car from session where outTime  > CURRENT_DATE()"
            cursor.execute(sql)
            result = cursor.fetchone()
            cntOutCar = result["cnt_out_car"]

            sql = 'SELECT COUNT(*) as cnt_re_car FROM parking'
            cursor.execute(sql)
            result = cursor.fetchone()
            cntReCar = result["cnt_re_car"]

            cntAbleCar = zoneA - cntReCar

            in_out_re_able = [cntInCar, cntOutCar , cntReCar, cntAbleCar]

    finally :
        conn.close()

    return in_out_re_able
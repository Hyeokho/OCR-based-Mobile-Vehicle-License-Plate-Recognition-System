# 팁
# 여러줄 주석 : 컨트롤 + /
# 예외처리 문법 : try ~
# KPU라는 변수의 타입 보기 : type(KPU)
# 문자열로 만들기 : str(CVC)


# http://devcvc.iptime.org:6010/phpmyadmin/
# id : user1
# pw : 0000
# test_python = 멤버테이블 = 회원테이블 -> 회원, 주민의 정보가 있음
# parking = 파킹테이블 = 주차장 현황 테이블 -> 현재 주차장에 주차되어 있는 차량의 정보가 있음

import dev_mysql
import dev_time

id = 'honora'
name = '홍길동'
contact = '019-1199-9090'
DP = '1'





number = '12가3456'
number = '12가2222'
number = '02난2211'





# 1. 차량 등록기능 = 회원 가입기능
# 아이디, 차량번호, 이름, 연락처, 장애인 차량 여부를 입력받아서
#dev_mysql.registUser(id, number, name, contact, DP)



# 2. 차량번호를보냈을때 db에 차량번호와 일치하는 데이터가져오는거 "member" 테이블임!!
#    차량번호를 파라미터로하여 시퀀스, 아이디, 패스워드, 이름, 연락처, 차량번호를
#    확인할 수 있음 / 리턴은 딕셔너리 ( key : value )

# # ex) 2-1. dev_mysql.search_car_num_from_member(number)['name'] 하면 이름
# print(  dev_mysql.search_car_num_from_member(number)['name'] )


# # ex) 2-2. dev_mysql.search_car_num_from_member(number)['contact'] 하면 연락처
# print(  dev_mysql.search_car_num_from_member(number)['contact'] )


# ex) 2-3.
# try문 사용해서 예외처리 하는 방법
try:
    # 실행해서 에러가 나면
    print(  dev_mysql.search_car_num_from_member('40보 4243')['contact']  )
except TypeError : # 가져올 값이 없을 때 에러남
    print('가져온 값이 없음!')
finally:
    # finally 부분은 무조건 실행함
    print('여긴 무조건 실행')


# if문 사용해서 예외처리 할때는 이렇게
# DB에서 값을 가져왔는데 값이 없으면
# if dev_mysql.search_car_num(number) == None:
#     print('데이터가 없습니다.')
# else:
#     # DB에서 값을 가져왔는데 값이 있으면 아래에 코딩
#     print('')





# 3. 현재시간출력하는 함수

# ex) 3-1. 현재시간을 문자열로 표현해줌 형식은 2019-07-16 16:30:00 처럼 분까지 나옴 (초는 항상 0)
print(  dev_time.getCurrentStrMinTime()  )




# 4. 차 번호를 보냈을때 정보를 가져오는거 "parking" 테이블임!!! 2번하고 다름!!!
#print(  dev_mysql.search_car_num_from_parking('12가0099')['contact'] )




# 5. 현재시간과 입력한 시간의 차이를 비교
# (입력한 시간이 현재 시간보다 무조건 과거임!!)
# in_time : datetime 객체임!, 데이터베이스에서 가져오면 저 자료형(?)임!!
#in_time = dev_mysql.search_car_num_from_parking('12가0099')['in_time']
#print(  dev_time.getDiffTimetoTimeString(in_time)  )




# 6. 시퀀스, 이름, 연락처, 차량번호, 장애인 차량 여부, 입차시간 테이블 생성
# dev_mysql.creat_table_parking()






# 7. 입차기능, 차 번호, 이름, 연락처, 장애인 차량 여부를 입력 받아서 parking 테이블에 입력 하고
#    세션테이블에 입차시간, 이름, 연락처, 차번호, 장애인 차량 여부를 입력함
#dev_mysql.in_car_parking(number, name, contact, DP)





# 8. 출차 기능, 차 번호를 입력 받아서 parking 테이블에서 삭제하고
#    세션테이블에 출차시간을 입력함
#dev_mysql.out_car_parking(number)



# 9. 현재 주차되어 있는 차량의 수를 체크함, parking 테이블의 행의 갯수를 셈, 리턴타입=int
#print('현재 주차되어 있는 수는 %d 입니다.' %dev_mysql.count_row_parking())



# 10. 정보 수정기능, 차량 번호를 입력 받아서 새로운 차량번호, 이름, 연락처, 장애인차량 여부 수정 가능
# car_number : 원래 차량의 번호
# change_car_number : 수정하고자 하는 차량 번호
# name : 수정하고자 하는 이름
# contact : 수정하고자 하는 연락처
# DP : 수정하고자 하는 장애인 차량 여부
#dev_mysql.update_member(car_number='11가3344', change_car_number='66삿6666', name='홍길동', contact='010-9910-1234', DP='1')





# 11. 세션테이블 만들기
# 인식기에서는 의미 없음
# dev_mysql.creat_table_Session()


# 12. 입차, 출차, 재차, 가능을 가져오는 함수
#     입차 : 오늘 들어온 차
#     출차 : 오늘 나간 차
#     재차 : 현재 주차중인 차
#     가능 : 주차 가능한 대수
#     나중에 입력 파라미터로 A구역, B구역, C구역 등등 넣게 바꿔야함
#     출력 : 정수형 리스트
cntInCar = dev_mysql.in_out_re_able_Parking()[0]
cntOutCar = dev_mysql.in_out_re_able_Parking()[1]
cntReCar = dev_mysql.in_out_re_able_Parking()[2]
cntAbleCar = dev_mysql.in_out_re_able_Parking()[3]

print(cntInCar)

print(dev_mysql.in_out_re_able_Parking())



# 13. 차 번호를 입력하여 정보를 세션테이블에서 가져옴, 가장 최근의 정보를 가져옴
#     방문했던 차량인지 확인 가능함
#print( dev_mysql.search_car_num_from_Session(number) )



# 14. 선불 주차장에서 입차할 때
#dev_mysql.prepay_in_car_parking('12테1111', '테스트', '010-9999-9999', '1', 'prepay_A')

# 15. 아파트 주차장에서 주차장을 리셋할 때
dev_mysql.APTreset_car_parking('prepay_B')

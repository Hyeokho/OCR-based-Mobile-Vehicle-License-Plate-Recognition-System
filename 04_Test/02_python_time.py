import time
import datetime

# 2017-08-30 21:21:57.860000
def getCurrentTime():
   return datetime.datetime.now()

# 초를 문자열 시간으로
def getCurrentTimeBySec(s):
   m = s / 60
   timestr = "2016-05-19 {}:{}".format(m / 60, m%60)
   print (timestr)
   return datetime.datetime.strptime(timestr, "%Y-%m-%d %H:%M")

# dtTime 은 datetime 타입이 들어간다.
def getDiffTimeToTime(dtTime) :
   return getCurrentTime() - dtTime

# 1502108747.22 같은 누적초로 리턴
def getCurrentClock() :
   return time.time()

# time.struct_time(tm_year=2017, tm_mon=8, tm_mday=7, tm_hour=21, tm_min=36, tm_sec=9, tm_wday=0, tm_yday=219, tm_isdst=0)
def getlocalTime():
   return time.localtime()

# 2017-08-07 같이 날짜만 문자열로 리턴
def getCurrentStrDate() :
   return time.strftime("%Y-%m-%d")

# 2017-08-07 13:02:00 같이 날짜+시간을  문자열로 리턴
def getCurrentStrTime() :
   return time.strftime("%Y-%m-%d %H:%M:%S")

# 2017-08-07 13:07 처럼 분까지만 리턴
def getCurrentStrMinTime() :
   #return time.strftime("%Y-%m-%d %H:%M" + ":00")
   return time.strftime("%Y-%m-%d %H:%M")

# 2017-08-07 13:02 처럼 현재 시간에서 5분전 시간을 문자열로 리턴
# beforeMin 에는 이전 몇 분이 들어간다. 예) getCurrentStrMinTimeAgo(5)
def getCurrentStrMinTimeAgo(beforeMin) :
   return (datetime.datetime.now() - datetime.timedelta(minutes=beforeMin)).strftime("%Y-%m-%d %H:%M" + ":00")

# 2017-08-07 21:32:43.407 리턴
def getCurrentStrSecTime() :
   t = getCurrentClock()
   tmicsec = t - int(t)
   return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t)) + ".{:03d}".format(int(tmicsec * 1000))

# 2017-08-07 21 시간 까지 문자열로 리턴
def getCurrentPowerAllStrTime() :
   return time.strftime("%Y-%m-%d %H")

# tTime : 입력된 초
# time.localtime([secs]) 입력된 초를 변환하여, 지방표준시 기준의 struct_time 을 리턴
# time.gmtime([secs]) 입력된 초를 변환하여 , UTC 기준의 STRUCT_TIME 시퀀스 객체 리턴
def getStrTime(tTime) :
   return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(tTime))

# tTime 2개의 입력된 초의 차를 초로 리턴
def getDiffTime2(tTime1, tTime2) :
   return tTime2 - tTime1


# 현재 초와 tTime 초의 차를 초로 리턴
def getDiffTime(tTime) :
   return getCurrentClock() - tTime

# 입력받은 날짜(정수)와 현재 날짜의 날수 차이
def getDiffDay(year,month, day):
  input_day = datetime.date(year,month,day)
  today  = datetime.date.today()
  delta = today - input_day
  return delta.days


# 초를 입력으로 넣은 후에 해당 초에 해당하는 지방표준시의 시퀀스중에 nIdx 번째 값을 리턴한다. 순서는 아래와 같다.
# # time.struct_time(tm_year=2017, tm_mon=8, tm_mday=7, tm_hour=21, tm_min=36, tm_sec=9, tm_wday=0, tm_yday=219, tm_isdst=0)
def getDateTimeFromIndex(tTime, nIdx) :
   return time.localtime(tTime)[nIdx]

# 초를 입력으로 넣은 후에 해당 초에 해당하는 지방표준시의 시퀀스들을 리스트로 가져온다..
# # time.struct_time(tm_year=2017, tm_mon=8, tm_mday=7, tm_hour=21, tm_min=36, tm_sec=9, tm_wday=0, tm_yday=219, tm_isdst=0)
def getClockElement(tTime) :
    return [
        getDateTimeFromIndex(tTime, 0),
        getDateTimeFromIndex(tTime, 1),
        getDateTimeFromIndex(tTime, 2),
        getDateTimeFromIndex(tTime, 3),
        getDateTimeFromIndex(tTime, 4),
        getDateTimeFromIndex(tTime, 5)
    ]


# datetime 객체를 입력받아서 누적초로 리턴한다. 1502109843.0
def getTimeFromDateTime(dtTime) :
   return time.mktime(dtTime.timetuple()) # + dtTime.microsecond / 1E6

# 년, 월, 일 을 숫자로 입력 받아서 완성된 누적초로 리턴
def getTimeFromEachValue(nYear, nMonth, nDay) :
   return getTimeFromDateTime(datetime.date(nYear, nMonth, nDay))

# 누적초를 입력 받아서
#2017-08-07 21:49:35 같은 datetime.datetime 객체 리턴
def getDateTimeFromTime(tTime) :
   return datetime.datetime.fromtimestamp(time.mktime(time.localtime(tTime)))

# 시간 문자열을 입력 받아서
#2017-08-07 21:49:35 같은 datetime.datetime 객체 리턴
def getDateTimeFromString(szTime) :
   #return datetime.datetime.strptime(szTime, "%Y-%m-%d %H:%M:%S")
   return datetime.datetime.strptime(szTime, "%Y-%m-%d %H:%M:00")


#2017-08-07 21:49:35 같은 datetime.datetime 객체에 숫자로 일수를 더한 결과를 datetime 타입으로 리턴
def addDayToDateTime(dtTime, nDay) :
   return dtTime + datetime.timedelta(days=nDay)

# datetime 타입을 입력해서 누적초를 리턴
def convertDatetimeToSec(dtTime) :
   return dtTime.total_seconds()





#### 여기부터는 직접 만듬
# datetime 타입을 입력해서 누적초를 리턴
def getDiffTimetoTimeString(dtTime):

    # 입력받은 문자열형식의 시간을 데이터 타입으로 버꿔줌
    # dtTime = getDateTimeFromString(strTime)

    # 데이터 객체로 변환된 입력받은 시간과 현재 시간의 차이를 구함
    diffTime = getDiffTimeToTime(dtTime)

    # 앞에서 구한 차이의 일을 구함
    diffday = diffTime.days


    # 앞에서 구한 차이의 초를 60으로 나누면 분(diffmin)
    diffmin = diffTime.seconds / 60

    # diffmin의 값을 60으로 나누면 시(diffhour)
    diffhour = diffmin / 60

    # 시분초로 바꿔주는 것이므로, diffsec를 60으로 나눠 그 나머지가 남은 초
    diffsec = diffTime.seconds % 60

    # diffmin을 60으로 나눠 그 나머지가 남은 분
    diffmin = diffmin % 60

    # 날짜, 시간, 분 표시
    diffTimeString = "%d일 %0.2d:%0.2d" %(diffday, diffhour, diffmin)

    return diffTimeString
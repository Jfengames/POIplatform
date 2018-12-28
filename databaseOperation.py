import pymysql
from config import USER,PASSWD,HOST,DB,_TABLE_NAME_INDEX,TABLE_NAME_ANALYSIS_Commonparameters
import datetime
import os

def indexShow():
    database = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db='flaskr', use_unicode=True, charset="utf8")
    cursor = database.cursor()
    database1 = pymysql.connect(host=HOST, user=USER, passwd=PASSWD, db=DB, use_unicode=True, charset="utf8")
    cursor1 = database1.cursor()

    # provinces = ['安徽']
    provinces = ['安徽', '北京', '重庆', '福建', '广东', '甘肃', '广西', '贵州', '河南', '湖北', '河北', '海南', '黑龙江', '湖南', '吉林', '江苏',
                 '江西', '辽宁', '内蒙古', '宁夏', '青海', '四川', '山东', '上海', '陕西', '山西', '天津', '云南', '浙江','新疆','西藏']
    for province in provinces:

        crawlNum = """SELECT count(id) from {} where province like '{}%'
        """.format(_TABLE_NAME_INDEX,province)
        cursor.execute(crawlNum)
        cursor.scroll(0,mode='absolute')
        crawlNum = cursor.fetchone()[0]


        crawlRes = """SELECT count(id) from {} where typecode like '12%' and province like '{}%'
        """.format(_TABLE_NAME_INDEX,province)
        cursor.execute(crawlRes)
        cursor.scroll(0,mode='absolute')
        crawlRes = cursor.fetchone()[0]


        crawlHos = """SELECT count(id) from {} where typecode like '09%' and province like '{}%'
        """.format(_TABLE_NAME_INDEX,province)
        cursor.execute(crawlHos)
        cursor.scroll(0,mode='absolute')
        crawlHos = cursor.fetchone()[0]


        crawlNumWithShape = """SELECT count(id) from {} where province like '{}%' and wgs_shape is not null
        """.format(_TABLE_NAME_INDEX,province)
        cursor.execute(crawlNumWithShape)
        cursor.scroll(0,mode='absolute')
        crawlNumWithShape = cursor.fetchone()[0]

        crawlResWithShape = """SELECT count(id) from {} where province like '{}%' and typecode like '12%' and wgs_shape is not null
        """.format(_TABLE_NAME_INDEX,province)
        cursor.execute(crawlResWithShape)
        cursor.scroll(0,mode='absolute')
        crawlResWithShape = cursor.fetchone()[0]

        crawlHosWithShape = """SELECT count(id) from {} where province like '{}%' and typecode like '09%' and wgs_shape is not null
        """.format(_TABLE_NAME_INDEX,province)
        cursor.execute(crawlHosWithShape)
        cursor.scroll(0,mode='absolute')
        crawlHosWithShape = cursor.fetchone()[0]

        crawlToday = 0
        crawlTodayWithShape = 0
        # crawlToday = """SELECT count(id) from {} where province like '{}%' and  NOW() - create_time <= 1
        # """.format(_TABLE_NAME_INDEX,province)
        # cursor.execute(crawlToday)
        # cursor.scroll(0,mode='absolute')
        # crawlToday = cursor.fetchone()[0]
        #
        # crawlTodayWithShape = """SELECT count(id) from {} where province like '{}%' and  NOW() - create_time <= 1 and wgs_shape is not null
        # """.format(_TABLE_NAME_INDEX,province)
        # cursor.execute(crawlTodayWithShape)
        # cursor.scroll(0,mode='absolute')
        # crawlTodayWithShape = cursor.fetchone()[0]


        NumOfInsideRes  = """SELECT count(residential_flag) from {} where province = '{}' and residential_flag = 1
        """.format(TABLE_NAME_ANALYSIS_Commonparameters,province)
        cursor1.execute(NumOfInsideRes)
        cursor1.scroll(0,mode='absolute')
        NumOfInsideRes = cursor1.fetchone()[0]

        NumOfNearRes  = """SELECT count(residential_flag) from {} where province = '{}' and residential_flag = 2
        """.format(TABLE_NAME_ANALYSIS_Commonparameters,province)
        cursor1.execute(NumOfNearRes)
        cursor1.scroll(0,mode='absolute')
        NumOfNearRes = cursor1.fetchone()[0]

        NumOfMiddleRes  = """SELECT count(residential_flag) from {} where province = '{}' and residential_flag = 3
        """.format(TABLE_NAME_ANALYSIS_Commonparameters,province)
        cursor1.execute(NumOfMiddleRes)
        cursor1.scroll(0,mode='absolute')
        NumOfMiddleRes = cursor1.fetchone()[0]

        NumOfInsideHos = """SELECT count(hospital_flag) from {} where province = '{}' and hospital_flag = 1
              """.format(TABLE_NAME_ANALYSIS_Commonparameters, province)
        cursor1.execute(NumOfInsideHos)
        cursor1.scroll(0, mode='absolute')
        NumOfInsideHos = cursor1.fetchone()[0]

        NumOfNearHos = """SELECT count(hospital_flag) from {} where province = '{}' and hospital_flag = 2
        """.format(TABLE_NAME_ANALYSIS_Commonparameters,province)
        cursor1.execute(NumOfNearHos)
        cursor1.scroll(0,mode='absolute')
        NumOfNearHos = cursor1.fetchone()[0]

        NumOfMiddelHos = """SELECT count(hospital_flag) from {} where province = '{}' and hospital_flag = 3
        """.format(TABLE_NAME_ANALYSIS_Commonparameters,province)
        cursor1.execute(NumOfMiddelHos)
        cursor1.scroll(0,mode='absolute')
        NumOfMiddelHos = cursor1.fetchone()[0]
        print(province,crawlNum,crawlRes,crawlHos,crawlNumWithShape,crawlResWithShape,crawlHosWithShape,crawlToday,crawlTodayWithShape,NumOfInsideRes,NumOfNearRes,NumOfMiddleRes,NumOfInsideHos,NumOfNearHos,NumOfMiddelHos)



    #     sql = """INSERT INTO indexShow (province,crawlNum,crawlRes,crawlHos,crawlNumWithShape,crawlResWithShape,crawlHosWithShape,crawlToday,crawlTodayWithShape,NumOfInsideRes,NumOfNearRes,NumOfMiddleRes,NumOfInsideHos,NumOfNearHos,NumOfMiddelHos)
    # VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"""
    #     values1 = (province,crawlNum,crawlRes,crawlHos,crawlNumWithShape,crawlResWithShape,crawlHosWithShape,crawlToday,crawlTodayWithShape,NumOfInsideRes,NumOfNearRes,NumOfMiddleRes,NumOfInsideHos,NumOfNearHos,NumOfMiddelHos)
    #
    #     #
    #     # # 执行sql语句
    #     cursor1.execute(sql, values1)
        sql = """UPDATE indexShow SET crawlNum={},crawlRes={},crawlHos={},crawlNumWithShape={},crawlResWithShape={},crawlHosWithShape={},crawlToday={},crawlTodayWithShape={},NumOfInsideRes={},NumOfNearRes={},NumOfMiddleRes={},NumOfInsideHos={},NumOfNearHos={},NumOfMiddelHos={} WHERE province = '{}'
        """.format(crawlNum,crawlRes,crawlHos,crawlNumWithShape,crawlResWithShape,crawlHosWithShape,crawlToday,crawlTodayWithShape,NumOfInsideRes,NumOfNearRes,NumOfMiddleRes,NumOfInsideHos,NumOfNearHos,NumOfMiddelHos,province)
        print(sql)
        # cursor1.execute(sql)
    cursor1.close()

    # 提交
    # database1.commit()

    # 关闭数据库连接
    database1.close()

def timerFun(sched_Timer):
    flag = 0
    while True:
        now = datetime.datetime.now()
        if now == sched_Timer:
            indexShow()
            flag = 1

        else:
            if flag == 1:
                sched_Timer = sched_Timer + datetime.timedelta(days=1)
                flag = 0



if __name__ == '__main__':
    # sched_Timer = datetime.datetime(2018,12,25,0,0,0)
    # print('run the timer task at {0}'.format(sched_Timer))
    # timerFun(sched_Timer)
    indexShow()
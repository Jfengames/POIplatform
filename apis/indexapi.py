from flask import render_template, request, session, Blueprint
from database import User,Adcode,Scenecode,ScrapeMissions,db,IndexShow,Note
from decorators import login_required
from database import User,Adcode,Scenecode,ScrapeMissions,db,GaodeMapScene
from config import KEYS
from sqlalchemy import func
from toolbox import takeSecond
index = Blueprint('index',__name__)

@index.route('/',methods=['GET','POST'])
@login_required
def home():

    return render_template('base.html')

@index.route('/index/',methods=['GET', 'POST'])
@login_required
def indexs():
    if request.method == 'GET':
        # provinces = ['安徽', '北京', '重庆', '福建', '广东', '甘肃', '广西', '贵州', '河南', '湖北', '河北', '海南', '黑龙江', '湖南', '吉林', '江苏',
        #              '江西', '辽宁', '内蒙古', '宁夏', '青海', '四川', '山东', '上海', '陕西', '山西', '天津', '云南', '浙江','新疆','西藏']
        provinces = ['安徽','北京']
        crawlTotalNum =0
        crawlTotalRes = 0
        listOfcrawlTotalRes = []
        listOfcrawlTotalResSorted = []
        crawlTotalHos = 0
        listOfcrawlTotalHos = []
        listOfcrawlTotalHosSorted = []
        crawlTotalNumWithShape = 0
        crawlTotalResWithShape =0
        crawlTotalHosWithShape =0
        crawlTotalToday = 0
        crawlTotalTodayWithShape = 0
        NumOfTotalInsideRes = 0
        NumOfTotalNearRes = 0
        NumOfTotalMiddleRes = 0
        NumOfTotalInsideHos = 0
        NumOfTotalNearHos = 0
        NumOfTotalMiddelHos = 0
        for province in provinces:
            indexShow = IndexShow.query.filter(IndexShow.province == province).first()
            print(indexShow)
            crawlNum = indexShow.crawlNum
            crawlTotalNum += crawlNum
            crawlRes = indexShow.crawlRes
            crawlTotalRes += crawlRes
            listOfcrawlTotalRes.append(crawlRes)
            listOfcrawlTotalResSorted.append((province,crawlRes))
            print(listOfcrawlTotalResSorted)
            crawlHos = indexShow.crawlHos
            crawlTotalHos += crawlHos
            listOfcrawlTotalHos.append(crawlHos)
            listOfcrawlTotalHosSorted.append((province,crawlHos))
            crawlNumWithShape = indexShow.crawlNumWithShape
            crawlTotalNumWithShape +=crawlNumWithShape
            crawlResWithShape = indexShow.crawlResWithShape
            crawlTotalResWithShape += crawlResWithShape
            crawlHosWithShape = indexShow.crawlHosWithShape
            crawlTotalHosWithShape += crawlHosWithShape
            crawlToday = indexShow.crawlToday
            crawlTotalToday += crawlToday
            crawlTodayWithShape = indexShow.crawlTodayWithShape
            crawlTotalTodayWithShape += crawlTodayWithShape
            NumOfInsideRes = indexShow.NumOfInsideRes
            NumOfNearRes = indexShow.NumOfNearRes
            NumOfMiddleRes = indexShow.NumOfMiddleRes
            NumOfInsideHos = indexShow.NumOfInsideHos
            NumOfNearHos = indexShow.NumOfInsideHos
            NumOfMiddelHos = indexShow.NumOfMiddelHos
            NumOfTotalInsideRes += NumOfInsideRes
            NumOfTotalNearRes += NumOfNearRes
            NumOfTotalMiddleRes += NumOfMiddleRes
            NumOfTotalInsideHos += NumOfInsideHos
            NumOfTotalNearHos += NumOfNearHos
            NumOfTotalMiddelHos += NumOfMiddelHos
        crawlTotalRes = crawlTotalRes // 10000
        crawlTotalHos = crawlTotalHos // 10000
        crawlTotalResWithShape = crawlTotalResWithShape // 10000
        crawlTotalHosWithShape = crawlTotalHosWithShape // 10000
        ratioOfTotalInsideRes = 0#NumOfTotalInsideRes/(NumOfTotalInsideRes+NumOfTotalNearRes+NumOfTotalMiddleRes)
        ratioOfTotalNearRes = 0#NumOfTotalNearRes/(NumOfTotalInsideRes+NumOfTotalNearRes+NumOfTotalMiddleRes)
        ratioOfTotalMiddleRes = 0#NumOfTotalMiddleRes/(NumOfTotalInsideRes+NumOfTotalNearRes+NumOfTotalMiddleRes)
        ratioOfTotalInsideHos = 0#NumOfTotalInsideHos/(NumOfTotalInsideHos+NumOfTotalNearHos+NumOfTotalMiddelHos)
        ratioOfTotalNearHos = 0#NumOfTotalNearHos/(NumOfTotalInsideHos+NumOfTotalNearHos+NumOfTotalMiddelHos)
        ratioOfTotalMiddelHos = 0#NumOfTotalMiddelHos/(NumOfTotalInsideHos+NumOfTotalNearHos+NumOfTotalMiddelHos)
        listOfcrawlTotalResSorted.sort(key=takeSecond,reverse=True)
        listOfcrawlTotalHosSorted.sort(key=takeSecond,reverse=True)
        context = {
            'cards': Note.query.order_by('create_time').all()
        }
        return render_template('index.html',crawlTotalNum=crawlTotalNum,crawlTotalRes=crawlTotalRes,crawlTotalHos=crawlTotalHos,crawlTotalNumWithShape=crawlTotalNumWithShape,crawlTotalResWithShape=crawlTotalResWithShape,crawlTotalHosWithShape=crawlTotalHosWithShape,
                               ratioOfTotalInsideRes=ratioOfTotalInsideRes,ratioOfTotalNearRes=ratioOfTotalNearRes,ratioOfTotalMiddleRes=ratioOfTotalMiddleRes,ratioOfTotalInsideHos=ratioOfTotalInsideHos,ratioOfTotalNearHos=ratioOfTotalNearHos,ratioOfTotalMiddelHos=ratioOfTotalMiddelHos,
                               listOfcrawlTotalRes=listOfcrawlTotalRes,listOfcrawlTotalHos=listOfcrawlTotalHos,listOfcrawlTotalResSorted=listOfcrawlTotalResSorted,listOfcrawlTotalHosSorted=listOfcrawlTotalHosSorted,crawlTotalToday=crawlTotalToday,crawlTotalTodayWithShape=crawlTotalTodayWithShape,**context)











# @index.route('/show/',methods=['GET','POST'])
# @login_required
# def show():
#     city = request.args.get('city')
#     scene = request.args.get('scene')
#     adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
#     type_code = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
#
#     type_code = remove_zero(type_code)
#
#     conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
#     cur = conn.cursor()
#     sql_limit="""
#             select * from {} where city_adcode={} and typecode like '{}%'limit 20
#         """.format(TABLE_NAME, adcode,type_code)
#     cur.execute(sql_limit)
#     scrape_res = cur.fetchall()
#
#     return render_template('show.html', scrape_res=scrape_res, city=city, scene=scene)





#     city = request.args.get('city')
#     scene = request.args.get('scene')
#     adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
#     type_code = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
#     type_code = remove_zero(type_code)
#     conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
#     cur = conn.cursor()
#     sql="""
#             select * from {} where city_adcode={} and typecode like '{}%'
#             """.format(TABLE_NAME, adcode, type_code)
#     cur.execute(sql)
#     total_res = cur.fetchall()
#     fields = cur.description
#     workbook = xlwt.Workbook()
#     sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
#
#     # 写上字段信息
#     for field in range(0, len(fields)):
#         sheet.write(0, field, fields[field][0])
#
#     # 获取并写入数据段信息
#
#     for row in range(1, len(total_res) + 1):
#         for col in range(0, len(fields)):
#             sheet.write(row, col, u'%s' % total_res[row - 1][col])
#
#     workbook.save(r'./readout.xls')
#     conn.close()
#     directory = os.getcwd()
#
#     filename = "readout.xls"
#     return send_from_directory(directory, filename, as_attachment=True)
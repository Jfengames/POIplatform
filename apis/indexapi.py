from flask import render_template, request, session, Blueprint
from database import User,Adcode,Scenecode,ScrapeMissions,db
from decorators import login_required
from database import User,Adcode,Scenecode,ScrapeMissions,db,GaodeMapScene
from config import KEYS
from sqlalchemy import func
index = Blueprint('index',__name__)


@index.route('/',methods=['GET', 'POST'])
@login_required
def indexs():
    if request.method == 'GET':
        crawlTotalNum = db.session.query(func.count(GaodeMapScene.id)).scalar()
        _crawlTotalRes = db.session.query(func.count(GaodeMapScene.id)).filter(GaodeMapScene.typecode.like("12%")).scalar()
        _crawlTotalHos = db.session.query(func.count(GaodeMapScene.id)).filter(GaodeMapScene.typecode.like("09%")).scalar()
        crawlTotalRes = _crawlTotalRes//10000
        crawlTotalHos = _crawlTotalHos//10000
        crawlTotalNumWithShape = db.session.query(func.count(GaodeMapScene.id)).filter(GaodeMapScene.wgs_shape != None).scalar()
        _crawlTotalResWithShape = db.session.query(func.count(GaodeMapScene.id)).filter(GaodeMapScene.typecode.like("12%"),GaodeMapScene.wgs_shape != None).scalar()
        _crawlTotalHosWithShape = db.session.query(func.count(GaodeMapScene.id)).filter(GaodeMapScene.typecode.like("09%"),GaodeMapScene.wgs_shape != None).scalar()
        crawlTotalResWithShape = _crawlTotalResWithShape//10000
        crawlTotalHosWithShape = _crawlTotalHosWithShape//10000
        return render_template('index.html',crawlTotalNum=crawlTotalNum,crawlTotalRes=crawlTotalRes,crawlTotalHos=crawlTotalHos,crawlTotalNumWithShape=crawlTotalNumWithShape,crawlTotalResWithShape=crawlTotalResWithShape,crawlTotalHosWithShape=crawlTotalHosWithShape)











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
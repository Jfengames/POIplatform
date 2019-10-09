
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,TextAreaField
from wtforms.validators import DataRequired, EqualTo
import pymysql
import xlwt
from database import Adcode
import os
import xlrd
import numpy as np
import plotly.offline as py
import plotly.graph_objs as go
from config import HOST, USER, PASSWD, DB, TABLE_NAME_INDEX, ALLOWED_EXTENSIONS, DIRECTORY, \
    TABLE_NAME_ANALYSIS_GAODE, TABLE_NAME_ANALYSIS_Commonparameters,MAP_ACCESS_TOKEN,REGION
import matplotlib.path as mpath
from shapely.geometry import Polygon
import matplotlib.patches as mpatches
import shapefile
from database import Todos, db
import math
import csv

def bdToGaoDe(lon,lat):
    """
    百度坐标转高德坐标
    :param lon:
    :param lat:
    :return:
    """
    PI = 3.14159265358979324 * 3000.0 / 180.0
    x = lon - 0.0065
    y = lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * PI)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * PI)
    lon = z * math.cos(theta)
    lat = z * math.sin(theta)
    return lon,lat


def downloadcsvindex(city,scene):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = """
            select * from {} where city_adcode='{}' and typecode like '{}%'
            """.format(TABLE_NAME_INDEX,city,remove_zero(scene))
    cur.execute(sql)
    total_res = cur.fetchall()
    fields = cur.description
    with open(r'./downlaodcsvindex.csv','w') as f :
        write = csv.writer(f)
        head = []
        for field in fields:
            head.append(field[0])
        write.writerow(head)
        write.writerows(total_res)

    conn.close()
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
    #
    #
    # # 写上字段信息
    # for field in range(0, len(fields)):
    #     sheet.write(0, field, fields[field][0])
    #
    # # 获取并写入数据段信息
    #
    # for row in range(1, len(total_res) + 1):
    #     for col in range(0, len(fields)):
    #         sheet.write(row, col, u'%s' % total_res[row - 1][col])
    #
    # workbook.save(r'./downlaodcsvindex.csv')
    # conn.close()

def downloadcsvanalysis(city):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = """
            select * from {} where city='{}'
            """.format(TABLE_NAME_ANALYSIS_Commonparameters,city)
    cur.execute(sql)
    total_res = cur.fetchall()
    fields = cur.description
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
    # # 写上字段信息
    # for field in range(0, len(fields)):
    #     sheet.write(0, field, fields[field][0])
    #
    # # 获取并写入数据段信息
    #
    # for row in range(1, len(total_res) + 1):
    #     for col in range(0, len(fields)):
    #         sheet.write(row, col, u'%s' % total_res[row - 1][col])
    #
    # workbook.save(r'./downloadcsvanalysis.csv')
    with open(r'./downloadcsvanalysis.csv','w') as f :
        write = csv.writer(f)
        head = []
        for field in fields:
            head.append(field[0])
        write.writerow(head)
        write.writerows(total_res)
    conn.close()

def plotly(city,scene):
    traces = []
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    sql_center = """
                    select * from gaodemap_districtshape where adcode = '{}'
    """.format(city)
    cur = conn.cursor()
    cur.execute(sql_center)

    res = cur.fetchall()[0][6]
    res = res.split(',')


    sql = """
            select * from {} where city_adcode='{}' and typecode like '{}%' and wgs_shape is NOT NULL limit 1000
            """.format(TABLE_NAME_INDEX,city,remove_zero(scene))
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        cursor.execute(sql)

        for i in cursor:
            shape = np.array([float(p) for p in i['wgs_shape'].replace('|', ',').replace(';', ',').split(',')]).reshape(-1,
                                                                                                                        2)
            trace = dict(
                type='scattermapbox',
                opacity=0.7,
                lon=shape[:, 0],
                lat=shape[:, 1],
                name=i['name'],
                text=i['address'],
                mode='lines',
                line=dict(
                    width=1,
                    color='blue'),
            )

            traces.append(trace)
    #
    # layout = dict(
    #     title=i['province']+'示意图',
    #     showlegend=False,
    #     geo=dict(
    #         scope='asia',
    #         projection=dict(type='equirectangular',
    #                         scale=30,),
    #         showland=True,
    #         showcountries=True,
    #         landcolor='rgb(243, 243, 243)',
    #         countrycolor='rgb(204, 204, 204)',
    #
    #
    #         center=dict(
    #                         lat=float(res[1]),
    #                         lon=float(res[0])
    #                     ),
    #     ),
    # )
    layout = dict(
        title=i['province'] + '示意图',
        showlegend=False,
        autosize=True,
        hovermode='closest',
        mapbox=dict(
            accesstoken=MAP_ACCESS_TOKEN,
            bearing=0,
            center=dict(
                lat=float(res[1]),
                lon=float(res[0])
            ),
            pitch=0,
            zoom=10
        ),
    )
    fig = dict(data=traces, layout=layout)
    div = py.plot(fig,output_type='div', include_plotlyjs=False,auto_open=False, show_link=False)
    return div



def downloadcsvanalysis_gaode(city):
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cur = conn.cursor()
    sql = """
                select * from {} where city='{}'
                """.format(TABLE_NAME_ANALYSIS_GAODE, city)
    cur.execute(sql)
    total_res = cur.fetchall()
    fields = cur.description
    # workbook = xlwt.Workbook()
    # sheet = workbook.add_sheet('table_message', cell_overwrite_ok=True)
    # # 写上字段信息
    # for field in range(0, len(fields)):
    #     sheet.write(0, field, fields[field][0])
    # # 获取并写入数据段信息
    # for row in range(1, len(total_res) + 1):
    #     for col in range(0, len(fields)):
    #         sheet.write(row, col, u'%s' % total_res[row - 1][col])
    # workbook.save(r'./downloadcsvanalysis_gaode.csv')
    with open(r'./downloadcsvanalysis_gaode.csv','w') as f :
        write = csv.writer(f)
        head = []
        for field in fields:
            head.append(field[0])
        write.writerow(head)
        write.writerows(total_res)
    conn.close()




def remove_zero(input):
    b = str(input)[::-1]
    b = str(int(b))
    output = b[::-1]

    return output


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def upload_file(filename):
    print(str(os.path.join(DIRECTORY, filename)))
    book = xlrd.open_workbook(str(os.path.join(DIRECTORY, filename)))
    sheet = book.sheets()[0]
    conn = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = conn.cursor()

    query_insert_into = """INSERT INTO {} (dt,province,city,region,cgi,tac,chinesename,covertype,scenario,vendor,earfcn,nettype,pci,iscore,gpslat,gpslng,bdlat,bdlng,angle,height,totaltilt,iscounty,isauto,flag,residential_flag,hospital_flag,beauty_spot_flag,college_flag,food_centre_flag,subway_flag,high_speed_flag,high_speed_rail_flag,viaduct_flag,high_rise_flag)
       VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""".format(TABLE_NAME_ANALYSIS_Commonparameters)

    w = shapefile.Writer('D:/Polygon/point')

    w.autoBalance = 1
    # w = shapefile.Writer(shapefile.POINT)
    w.field('ANGLE', 'N')

    for r in range(1, sheet.nrows):
        dt = sheet.cell(r, 0).value
        province = sheet.cell(r, 1).value
        city = sheet.cell(r, 2).value
        region = sheet.cell(r,3).value
        cgi = sheet.cell(r, 4).value
        tac = int(sheet.cell(r, 5).value)
        chinesename = sheet.cell(r, 6).value
        covertype = sheet.cell(r, 7).value
        scenario = sheet.cell(r, 8).value
        vendor = sheet.cell(r, 9).value
        earfcn = int(sheet.cell(r, 10).value)
        nettype = sheet.cell(r, 11).value
        pci = int(sheet.cell(r, 12).value)
        iscore = sheet.cell(r, 13).value
        gpslat = float(sheet.cell(r, 14).value)
        gpslng = float(sheet.cell(r, 15).value)
        bdlat = float(sheet.cell(r, 16).value)
        bdlng = float(sheet.cell(r, 17).value)
        angle = int(sheet.cell(r, 18).value)
        w.point(bdToGaoDe(bdlng,bdlat))
        w.record(angle)


        height = sheet.cell(r, 19).value
        totaltilt = float(sheet.cell(r, 20).value)
        iscounty = bool(sheet.cell(r, 21).value)
        isauto = bool(sheet.cell(r, 22).value)
        flag = bool(sheet.cell(r, 23).value)
        residential_flag = 0
        hospital_flag = 0
        beauty_spot_flag = 0
        college_flag = 0
        food_centre_flag = 0
        subway_flag = 0
        high_speed_flag = 0
        high_speed_rail_flag = 0
        viaduct_flag = 0
        high_rise_flag = 0

        values = (dt,province,city,region,cgi,tac,chinesename,covertype,scenario,vendor,earfcn,nettype,pci,iscore,gpslat,gpslng,bdlat,bdlng,angle,height,totaltilt,iscounty,isauto,flag,residential_flag,hospital_flag,beauty_spot_flag,college_flag,food_centre_flag,subway_flag,high_speed_flag,high_speed_rail_flag,viaduct_flag,high_rise_flag)


        cursor.execute(query_insert_into, values)

    conn.commit()
    conn.close()
    w.close()
    print(province+'完成')

#小区与场景关联
def commonparameters(city):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """select * from {} where city= %s and residential_flag='0'""".format(TABLE_NAME_ANALYSIS_Commonparameters)
    values = (city)
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def gaodemapscene(district,city,typecode):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT * FROM {} WHERE district like %s and city LIKE %s and typecode LIKE %s and wgs_shape is not null""".format(TABLE_NAME_INDEX)
    values = (district+'%',city+'%',notzero(typecode)+'%')
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def analysis_new_mission_commonparameters_tagged_contains(city):
    lines = commonparameters(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    for l in range(0, len(lines)):
        cgi = lines[l][4]
        district = lines[l][3]
        shapes = gaodemapscene(district, city, 120000)
        Path = mpath.Path
        for s in range(0, len(shapes)):
            shape = shapes[s][-1]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            point = (float(lines[l][15]), float(lines[l][14]))
            p = Path(shape_array)
            if p.contains_points([point]):
                query_commonparameters_tagged = """UPDATE {} set residential_flag='1' where cgi='{}'""".format(TABLE_NAME_ANALYSIS_Commonparameters,cgi)
                cursor.execute(query_commonparameters_tagged)
                break
        print('%.2f%%' % (l / len(lines) * 100))
    cursor.close()
    db.commit()
    db.close()


def analysis_new_mission_commonparameters_tagged_100(city):
    lines = commonparameters(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    for l in range(0, len(lines)):
        cgi = lines[l][4]
        district = lines[l][3]
        shapes = gaodemapscene(district, city, 120000)
        Path = mpath.Path
        for s in range(0, len(shapes)):
            shape = shapes[s][-1]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            angle = float(lines[l][18])
            point = (float(lines[l][15]), float(lines[l][14]))
            Path(shape_array)
            try:
                a = mpatches.Wedge(point, 0.0009, angle - 65, angle + 65)._path.vertices
                a = Polygon(a).buffer(0)
                b = Polygon(shape_array)
                c = a.intersection(b)
                Polygon(c)
                overlap = 1
            except NotImplementedError as e:
                overlap = 0
            if overlap > 0:
                query_commonparameters_tagged = """UPDATE {} set residential_flag='2' where cgi='{}'""".format(TABLE_NAME_ANALYSIS_Commonparameters, cgi)
                cursor.execute(query_commonparameters_tagged)
                break
        print('%.2f%%' % (l / len(lines) * 100))
    cursor.close()
    db.commit()
    db.close()


def analysis_new_mission_commonparameters_tagged_100_200(city):
    lines = commonparameters(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    for l in range(0, len(lines)):
        cgi = lines[l][4]
        district = lines[l][3]
        shapes = gaodemapscene(district, city, 120000)
        Path = mpath.Path
        for s in range(0, len(shapes)):
            shape = shapes[s][-1]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,2)
            angle = float(lines[l][18])
            point = (float(lines[l][15]), float(lines[l][14]))
            Path(shape_array)
            try:
                a = mpatches.Wedge(point, 0.0018, angle - 65, angle + 65, width=0.0009)._path.vertices
                a = Polygon(a).buffer(0)
                b = Polygon(shape_array)
                c = a.intersection(b)
                polygon = Polygon(c)
                f = polygon.area / b.area
            except NotImplementedError as e:
                f = 0
            if f > 0.5:
                query_commonparameters_tagged = """UPDATE {} set residential_flag='3' where cgi='{}'""".format(TABLE_NAME_ANALYSIS_Commonparameters, cgi)
                cursor.execute(query_commonparameters_tagged)
                break
        print('%.2f%%' % (l / len(lines) * 100))
    cursor.close()
    db.commit()
    db.close()


#场景与小区关联
def analysis_new_mission_gaodemapscene_tagged(city):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    _region = findRegion(city, 120000)
    print(city)
    print('**********')
    print(_region)
    for region in _region:

        region = region[0]
        print(region)
        shapes = gaodemapscene1(city, region, 120000)
        print(len(shapes))
        region = REGION[region]
        print(region)
        lines = commonparameters1(city, region)
        print(len(lines))
        for s in range(0, len(shapes)):
            gaodemapscene_id = shapes[s][0]
            shape = shapes[s][16]
            shape_array = np.array([float(i) for i in shape.replace('|', ',').replace(';', ',').split(',')]).reshape(-1,                                                                                                                     2)
            Path = mpath.Path
            p = Path(shape_array)
            i = 0
            for l in range(0, len(lines)):

                angle = float(lines[l][18])

                point = (float(lines[l][15]), float(lines[l][14]))


                cgi = lines[l][4]

                chinesename = lines[l][6]
                pci = lines[l][12]

                if p.contains_points([point]):
                    i += 1
                    if i == 58:
                        print('超出范围')
                        break

                    cursor.execute(query_gaodemapscene(cgi, chinesename, pci, gaodemapscene_id, i))

                else:
                    try:
                        a = mpatches.Wedge(point, 0.0009, angle - 65, angle + 65)._path.vertices
                        a = Polygon(a).buffer(0)
                        b = Polygon(shape_array)
                        if not b.is_valid:
                            break
                        c = a.intersection(b)
                        Polygon(c)
                        overlap = 1
                    except AssertionError as e:
                        print(cgi,shape,gaodemapscene_id)
                        break
                    except ValueError as e:
                        print(shape)
                        break
                    except NotImplementedError as e:
                        overlap = 0
                    finally:
                        cursor.close()

                        db.close()
                    if overlap > 0:
                        i += 1
                        if i == 58:
                            print('超出范围')
                            break
                        cursor.execute(query_gaodemapscene(cgi, chinesename, pci, gaodemapscene_id, i))

                    else:
                        try:
                            a = mpatches.Wedge(point, 0.0018, angle - 65, angle + 65, width=0.0009)._path.vertices
                            a = Polygon(a).buffer(0)
                            b = Polygon(shape_array)

                            c = a.intersection(b)
                            polygon = Polygon(c)
                            f = polygon.area / b.area
                        except AssertionError as e:
                            print(cgi, shape, gaodemapscene_id)
                            break
                        except ValueError as e:
                            print(shape)
                            break
                        except NotImplementedError as e:
                            f = 0
                        finally:
                            cursor.close()

                            db.close()
                        if f > 0.5:
                            i += 1
                            if i == 58:
                                print('超出范围')
                                break

                            cursor.execute(query_gaodemapscene(cgi, chinesename, pci, gaodemapscene_id, i))

            print('%.2f%%' % (s / len(shapes) * 100))
    cursor.close()
    db.commit()
    db.close()

def findRegion(city,typecode):
    print(city)
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """SELECT district from {} where city like %s and typecode like %s GROUP BY district
    """.format(TABLE_NAME_INDEX)
    values = (city+'%',notzero(typecode)+'%')
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now

def commonparameters1(city,region):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    # sql = """
    # select * from {} where city like %s  and (region = %s )""".format(TABLE_NAME_ANALYSIS_Commonparameters)
    sql = """
    select * from {} where  (region = '{}' )""".format(TABLE_NAME_ANALYSIS_Commonparameters,region)

    cursor.execute(sql)
    re_now = cursor.fetchall()
    return re_now


def gaodemapscene1(city,region,typecode):
    db = pymysql.connect(host=HOST, user=USER, password=PASSWD, db=DB, charset='utf8')
    cursor = db.cursor()
    sql = """
    select * from {} where city like %s and district = %s and typecode like %s and wgs_shape is not null""".format(TABLE_NAME_INDEX)

    values = (city+'%',region,notzero(typecode)+'%')
    cursor.execute(sql,values)
    re_now = cursor.fetchall()
    return re_now


def query_gaodemapscene(cgi,chinesename,pci,gaodemapscene_id,i):
    cgi_i ='cgi_'+str(i)
    chinesename_j ='chinesename_'+str(i)
    pci_k ='pci_'+str(i)
    a_list = [cgi_i,chinesename_j,pci_k,cgi,chinesename,pci,gaodemapscene_id,TABLE_NAME_ANALYSIS_GAODE]
    sql = """update {0[7]} set {0[0]}= '{0[3]}',{0[1]}= '{0[4]}',{0[2]}= {0[5]} where id= '{0[6]}'""".format(a_list)
    print(sql)
    return sql


def notzero(input):
    b=str(input)[::-1]
    b=str(int(b))
    output=int(b[::-1])
    return str(output)

def takeSecond(elem):
    return elem[1]

class RegisterForm(FlaskForm):
    username = StringField(u'用户名', validators=[DataRequired()])

    password = PasswordField(u'密码', validators=[DataRequired()])

    password2 = PasswordField(u'确认密码', validators=[DataRequired(), EqualTo('password', '两次密码不一致')])

    email = StringField(u'工作邮箱', validators=[DataRequired()], )

    submit = SubmitField(u'立即注册')


class LoginForm(FlaskForm):
    username = StringField(validators=[DataRequired()])

    password = PasswordField(validators=[DataRequired()])

    submit = SubmitField(u'登录')


class CardForm(FlaskForm):
    title = StringField(validators=[DataRequired()])

    content = TextAreaField(validators=[DataRequired()])

    submit = SubmitField(u'立即发布')


class CommentForm(FlaskForm):
    content = StringField(validators=[DataRequired()])
    submit = SubmitField(u'发表评论')


# def celery_task(city,_city,todo_id):
#     todo = Todos.query.filter(Todos.id == todo_id).first()
#     main.data_operation.delay(city,_city)
#     # # todo.status = True
#     # db.session.add(todo)
#     # db.session.commit()

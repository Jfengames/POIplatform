from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash,g,Blueprint
from config import HOST,DB,PASSWD,PORT,USER,ADSL_SERVER_AUTH,ADSL_SERVER_URL,KEYS,TABLE_NAME_INDEX,DIRECTORY,SCENES,CITYS
from database import User,Adcode,Scenecode,ScrapeMissions,db,GaodeMapScene
from decorators import login_required
import json
import pymysql
from sqlalchemy import and_
import xlwt
import os

from toolbox import remove_zero,downloadcsvindex,plotly


crawl = Blueprint('crawl',__name__)


@crawl.route('/crawl/',methods=['GET','POST'])
@login_required
def crawls():
    page = int(request.args.get('page', 1))
    print(page)
    per_page = int(request.args.get('per_page', 10))
    if not request.args.get('city'):
        paginate = GaodeMapScene.query.filter(GaodeMapScene.adcode == 110000,GaodeMapScene.typecode.like("12%")).order_by('id').paginate(page,per_page,error_out=True)
        gaodemapscene = paginate.items
        return render_template('crawl.html', gaodemapscene=gaodemapscene,paginate=paginate,scenes=SCENES, citys=CITYS, provinceSelect='北京市', citySelect='北京市', sceneSelect='居民区')
    else:
        city = request.args.get('city')
        print(city)
        scene = request.args.get('scene')
        province = request.args.get('province')
        flag = request.args.get('flag')
        adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
        _typecode = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
        typecode = remove_zero(_typecode)
        paginate = GaodeMapScene.query.filter(GaodeMapScene.adcode == adcode,
                                              GaodeMapScene.typecode.like(typecode + "%")).order_by('id').paginate(
            page, per_page, error_out=True)
        gaodemapscene = paginate.items
        if gaodemapscene == []:
            flash('请联系管理员获取你想要的数据！')
            return redirect(url_for('crawl.crawls'))
        else:

            return render_template('crawl.html', gaodemapscene=gaodemapscene, scenes=SCENES, citys=CITYS,
                                   provinceSelect=province, citySelect=city, sceneSelect=scene, paginate=paginate,flag=flag)


    # else:
    #     page = int(request.args.get('page', 1))
    #     per_page = int(request.args.get('per_page', 10))
    #     province = request.form.get('province')
    #
    #     if request.form.get('city'):
    #         city = request.form.get('city')
    #         scene = request.form.get('scene')
    #         adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
    #         _typecode = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
    #         typecode = remove_zero(_typecode)
    #         paginate = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == adcode,
    #                                               GaodeMapScene.typecode.like(typecode + "%")).order_by('id').paginate(
    #             page, per_page, error_out=True)
    #         gaodemapscene = paginate.items
    #         if gaodemapscene == []:
    #             flash('请联系管理员获取你想要的数据！')
    #             return redirect(url_for('crawl.crawls'))
    #         else:
    #             downloadcsvindex(adcode, typecode)
    #             return render_template('crawl.html', gaodemapscene=gaodemapscene, scenes=SCENES, citys=CITYS,
    #                                    provinceSelect=province, citySelect=city, sceneSelect=scene, paginate=paginate)
    #
    #
    #     elif json.loads(request.form.get('data')):
    #         data = json.loads(request.form.get('data'))
    #         city = data['city']
    #         scene = data['scene']
    #         adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
    #         _typecode = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
    #         typecode = remove_zero(_typecode)
    #         g.adcode = adcode
    #         g.typecode = typecode
    #         print("******")
    #         # gaodemapscene = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == adcode,GaodeMapScene.typecode.like(typecode+"%")).order_by('-id').all()
    #
    #         # div = plotly(adcode,typecode)
    #
    #         paginate = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == adcode,GaodeMapScene.typecode.like(typecode+"%")).order_by('id').paginate(page,per_page,error_out=True)
    #         gaodemapscene = paginate.items
    #         if gaodemapscene==[]:
    #             flash('请联系管理员获取你想要的数据！')
    #             return redirect(url_for('crawl.crawls'))
    #         else:
    #             downloadcsvindex(adcode,typecode)
    #             print(gaodemapscene)
    #             return render_template('crawl.html', gaodemapscene=gaodemapscene, scenes=SCENES, citys=CITYS, provinceSelect=province, citySelect=city, sceneSelect=scene,paginate=paginate)
    #
    #

@crawl.route('/crawl/download/<city>/<scene>', methods=['GET'])
@login_required
def download1(city,scene):
    print(city)
    adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
    _typecode = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
    typecode = remove_zero(_typecode)
    downloadcsvindex(adcode, typecode)
    filename = "downlaodcsvindex.csv"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)




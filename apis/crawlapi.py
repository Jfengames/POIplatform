from flask import Flask,render_template,request,redirect,url_for,session,send_from_directory,flash,g,Blueprint
from config import HOST,DB,PASSWD,PORT,USER,ADSL_SERVER_AUTH,ADSL_SERVER_URL,KEYS,TABLE_NAME_INDEX,DIRECTORY
from database import User,Adcode,Scenecode,ScrapeMissions,db,GaodeMapScene
from decorators import login_required
import pymysql
from sqlalchemy import and_
import xlwt
import os

from toolbox import remove_zero,downloadcsvindex,plotly


crawl = Blueprint('crawl',__name__)


@crawl.route('/crawl',methods=['GET','POST'])
@login_required
def crawls():

    if request.method == 'GET':
        gaodemapscene = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == 110000).order_by('-id')
        # gaodemapscene = paginate.items
        return render_template('crawl.html', gaodemapscene=gaodemapscene)
    else:
        city = request.form.get('city')
        scene = request.form.get('scene')
        adcode = int(Adcode.query.filter(Adcode.city == city).first().adcode)
        _typecode = Scenecode.query.filter(Scenecode.scene == scene).one().scenecode
        typecode = remove_zero(_typecode)

        gaodemapscene = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == adcode,GaodeMapScene.typecode.like(typecode+"%")).order_by('-id').all()

        # div = plotly(adcode,typecode)

        # paginate = GaodeMapScene.query.filter(GaodeMapScene.city_adcode == adcode,GaodeMapScene.typecode.like(typecode+"%")).order_by('-id').paginate(page,per_page,error_out=True)
        # gaodemapscene = paginate.items
        if gaodemapscene==[]:
            flash('请联系管理员获取你想要的数据！')
            return redirect(url_for('crawl.crawls'))
        else:
            downloadcsvindex(adcode,typecode)

            return render_template('index.html', gaodemapscene=gaodemapscene)


@crawl.route('/crawl/download/', methods=['GET'])
@login_required
def download1():
    filename = "downlaodcsvindex.xls"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)




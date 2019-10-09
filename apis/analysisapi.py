
import shutil
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory, flash, g, Blueprint,abort
from database import User,Adcode,Scenecode,ScrapeMissions,db,CommonParameters_tagged_new,DBSession, Gaodemapscene_tagged, Todos
from decorators import login_required
from toolbox import downloadcsvanalysis,allowed_file,upload_file, downloadcsvanalysis_gaode
from config import UPLOAD_FOLDER,DIRECTORY,SCENES,CITYS,CITYTOCITY
from werkzeug.utils import secure_filename
import zipfile
import os
import main
# celery worker -l info -A main.celery



analysis = Blueprint('analysis', __name__)


@analysis.route('/analysis/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'GET':
        return render_template('analysis.html')

@analysis.route('/analysis/new_mission_todos/', methods=['GET', 'POST'])
def new_mission_todos():


    if request.method == 'GET':
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 4))
        paginate = Todos.query.order_by('-id').paginate(page, per_page, error_out=False)
        todos = paginate.items
        return render_template('analysis_new_mission.html', todos=todos,paginate=paginate)

    else:
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 4))
        paginate = Todos.query.order_by('-id').paginate(page, per_page, error_out=False)
        _city = request.form.get('city')
        print(_city)
        city = CITYTOCITY[_city]
        print(city)
        todo_list = Todos.query.filter().all()
        if todo_list == []:
            todo = Todos(todo_city=_city)
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            todo.author = user
            db.session.add(todo)
            db.session.commit()
            todos = paginate.items
            todo_id = Todos.query.order_by('-id').first().id
            main.data_operation.delay(city, _city)
            # celery_task(city, _city, todo_id)
            return render_template('analysis_new_mission.html', todos=todos, paginate=paginate)

        else:
            for todo_city in todo_list:
                if todo_city.todo_city == _city and todo_city.status == True:
                    return redirect(url_for('analysis.new_mission_todos'))
                elif todo_city.todo_city == _city and todo_city.status == False:
                    todos = paginate.items
                    return render_template('analysis_new_mission.html',todos=todos, paginate=paginate)

            todo = Todos(todo_city=_city)
            user_id = session['user_id']
            user = User.query.filter(User.id == user_id).first()
            todo.author = user
            db.session.add(todo)
            db.session.commit()
            todos = paginate.items
            todo_id = Todos.query.order_by('-id').first().id
            main.data_operation.delay(city, _city)
            return render_template('analysis_new_mission.html', todos=todos,paginate=paginate)

@analysis.route('/analysis/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')

            return redirect(url_for('analysis.new_mission'))
        file = request.files['file']

        if file.filename == '':
            flash('No selected file')

            return redirect(url_for('analysis.new_mission_todos'))


        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(DIRECTORY, filename))
            upload_file(filename)



            return redirect(url_for('analysis.new_mission_todos',filename=filename))


    return render_template('analysis_new_mission.html')



@analysis.route('/analysis/data_search', methods=['GET','POST'])
def data_search():
    if request.method == 'GET':
        return render_template('analysis_data_search.html', scenes=SCENES, citys=CITYS, provinceSelect='北京市', citySelect='北京市', sceneSelect='居民区')
    else:
        _city = request.form.get('city')
        city = _city[0:-1]
        province = request.form.get('province')

        scene = request.form.get('scene')

        commonparameters_tagged = CommonParameters_tagged_new.query.filter(CommonParameters_tagged_new.city == city).limit(1000).all()
        downloadcsvanalysis(city)

        gaodemapscene_tagged = Gaodemapscene_tagged.query.filter(Gaodemapscene_tagged.city == _city).limit(100).all()
        downloadcsvanalysis_gaode(_city)

        return render_template('analysis_data_search.html', commonparameters_tagged=commonparameters_tagged,gaodemapscene_tagged=gaodemapscene_tagged,scenes=SCENES, citys=CITYS, provinceSelect=province, citySelect=_city, sceneSelect=scene)



@analysis.route('/analysis/data_search/download/', methods=['GET'])
def download2():
    filename = "downloadcsvanalysis.csv"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)

@analysis.route('/analysis/data_search/download_gaode/', methods=['GET'])
def download2_gaode():
    filename = "downloadcsvanalysis_gaode.csv"
    return send_from_directory(DIRECTORY, filename, as_attachment=True)


@analysis.route('/analysis/new_mission_todos/download/', methods=['GET'])
def download():
    z = zipfile.ZipFile('download_new_mission.zip', 'w', zipfile.ZIP_STORED)
    filename_commonparameters = "downloadcsvanalysis.csv"
    filename_gaode = "downloadcsvanalysis_gaode.csv"
    z.write(filename_commonparameters)
    z.write(filename_gaode)
    z.close()

    filename = 'download_new_mission.zip'

    return send_from_directory(DIRECTORY, filename, as_attachment=True)


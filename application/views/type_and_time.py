from datetime import datetime

from flask import request, redirect, render_template, flash
from flask_login import login_required, current_user

from application import app, appDB
from application.db_model.activity_type import activity_type, activitytype_info
from application.db_model.timeline import timeline, timeline_info


@app.route('/type_and_time', methods=['GET'])
@login_required
def type_and_time():
    if current_user.role == 0 or current_user.role == 1:
        error = False

        type_list = activity_type.query.all()
        type_dict = []
        edit_type = {}
        if not type_list:
            type_dict = None
        else:
            for type_item in type_list:
                type_dict.append(activitytype_info(type_item))

        timeline_list = timeline.query.all()
        timeline_dict = []
        edit_time = {}
        if not timeline_list:
            timeline_dict = None
        else:
            for timeline_item in timeline_list:
                timeline_dict.append(timeline_info(timeline_item))

        return render_template('type_and_time.html',
                               page='type_and_time',
                               error=error,

                               activity_type=type_dict,
                               edit_type=edit_type,

                               timeline=timeline_dict,
                               edit_time=edit_time)
    else:
        return redirect('/')


@app.route('/type_and_time', methods=['POST'])
@login_required
def type_and_time_post():
    if current_user.role == 0 or current_user.role == 1:
        error = False

        type_list = activity_type.query.all()
        type_dict = []
        edit_type = {}
        if not type_list:
            type_dict = None
        else:
            for type_item in type_list:
                type_dict.append(activitytype_info(type_item))

        timeline_list = timeline.query.all()
        timeline_dict = []
        edit_time = {}
        if not timeline_list:
            timeline_dict = None
        else:
            for timeline_item in timeline_list:
                timeline_dict.append(timeline_info(timeline_item))

        if request.form['submit_type_and_type'] == 'add_type':
            title = request.form.get('type_title')
            type = activity_type(**{'title': title})
            appDB.session.add(type)
            appDB.session.commit()
            flash('Тип успешно добавлен!')
            error = False

            type_list = activity_type.query.all()
            type_dict = []
            if not type_list:
                type_dict = None
            else:
                for type_item in type_list:
                    type_dict.append(activitytype_info(type_item))
        elif request.form['submit_type_and_type'] == 'edit_type':
            id = request.form.get('typeID')
            title = request.form.get('type_title')

            edit_type = {
                'title': title
            }

            typeEdit = activity_type.query.filter(activity_type.typeID == id).first()
            for key, value in edit_type.items():
                setattr(typeEdit, key, value)
            appDB.session.commit()
            flash('Тип успешно изменён!')
            error = False

            type_list = activity_type.query.all()
            type_dict = []
            if not type_list:
                type_dict = None
            else:
                for type_item in type_list:
                    type_dict.append(activitytype_info(type_item))
        elif request.form['submit_type_and_type'] == 'add_timeline':
            title = request.form.get('timeline_title')
            start = datetime.strptime(request.form.get('timeline_start'), '%H:%M').time()
            end = datetime.strptime(request.form.get('timeline_end'), '%H:%M').time()

            if start < end:
                edit_time = {
                    'title': title,
                    'start': start,
                    'end': end
                }

                timelineAdd = timeline(**edit_time)
                appDB.session.add(timelineAdd)
                appDB.session.commit()

                flash('Промежуток успешно добавлен!')
                error = False

                timeline_list = timeline.query.all()
                timeline_dict = []
                if not timeline_list:
                    timeline_dict = None
                else:
                    for timeline_item in timeline_list:
                        timeline_dict.append(timeline_info(timeline_item))
            else:
                error = True
                flash('Окончание должно быть позже начала!')
        elif request.form['submit_type_and_type'] == 'edit_timeline':
            id = request.form.get('timelineID')
            title = request.form.get('timeline_title')
            start = request.form.get('timeline_start')
            end = request.form.get('timeline_end')

            edit_time = {
                'timelineID': id,
                'title': title,
                'start': start,
                'end': end
            }

            if start < end:
                edit_timeline = timeline.query.filter(timeline.timelineID == id).first()

                for key, value in edit_time.items():
                    setattr(edit_timeline, key, value)
                appDB.session.commit()
                flash('Промежуток успешно изменён')
                error = False

                timeline_list = timeline.query.all()
                timeline_dict = []
                if not timeline_list:
                    timeline_dict = None
                else:
                    for timeline_item in timeline_list:
                        timeline_dict.append(timeline_info(timeline_item))
            else:
                error = True
                flash('Окончание должно быть позже начала!')

        return render_template('type_and_time.html',
                               page='type_and_time',
                               error=error,

                               activity_type=type_dict,
                               edit_type=edit_type,

                               timeline=timeline_dict,
                               edit_time=edit_time)
    else:
        return redirect('/')
    pass

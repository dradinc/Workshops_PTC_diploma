from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash

from application import app, login_manager, appDB
from application.db_model.workshops import workshops
from application.db_model.users import get_users
from application.db_model.activity import activity, get_activity
from application.db_model.activity_type import activity_type, activitytype_info
from application.db_model.timeline import timeline, timeline_info


@app.route('/workshops/<number>', methods=['GET'])
def workshop_activity(number):
    error = False
    workshop_page = workshops.query.filter(workshops.number == number).first()
    workshop_page_dict = {
        'number': workshop_page.number,
        'title': workshop_page.title
    }



    week_number = request.args.get('week')
    year_number = request.args.get('year')
    week_days = _week_days(year_number, week_number)
    # Расписание актинвностей мастерской на неделю
    for day in week_days:
        day['activity'] = get_activity(day.get('day_for_query'), number)

    # Список типов
    activity_type_list = activity_type.query.all()
    activity_type_dict = []
    if activity_type_list:
        for types in activity_type_list:
            activity_type_dict.append(activitytype_info(types))

    # Список промежутков
    time_list = timeline.query.all()
    time_dict = []
    if time_list:
        for time_item in time_list:
            time_dict.append(timeline_info(time_item))

    # Списко мастерских
    workshop_list = workshops.query.all()
    workshop_dict = []
    if workshop_list:
        for workshop_item in workshop_list:
            workshop_dict.append(workshop_item)

    # Список заведующих
    owner_dict = get_users()

    return render_template(
        'workshop_activity.html',
        week_days=week_days,
        now_day=datetime.now().strftime('%Y-%m-%d'),
        activity_type=activity_type_dict,
        timeline=time_dict,
        workshops=workshop_dict,
        owner=owner_dict,

        workshop_page_dict=workshop_page_dict,
        number=number,
        new_activity={},
        error=error
    )


@app.route('/workshops/<number>', methods=['POST'])
def workshop_activity_post(number):
    error = False
    new_activity = {}
    workshop_page = workshops.query.filter(workshops.number == number).first()
    workshop_page_dict = {
        'number': workshop_page.number,
        'title': workshop_page.title
    }

    if request.form['workshop_activity_submit'] == 'last_week':
        last_week = str(int(request.args.get('week')) - 1)
        if int(last_week) < 0:
            last_week = '0'
        return redirect(
            '/workshops/' + str(number) + '?year=' + str(request.args.get('year')) + '&week=' + str(last_week))
    elif request.form['workshop_activity_submit'] == 'next_week':
        next_week = str(int(request.args.get('week')) + 1)
        if int(next_week) > 52:
            next_week = '52'
        return redirect(
            '/workshops/' + str(number) + '?year=' + str(request.args.get('year')) + '&week=' + str(next_week))
    elif request.form['workshop_activity_submit'] == 'add_activity':
        if (request.form.get('input_title')
                and request.form.get('select_type')
                and request.form.get('select_time')
                and request.form.get('select_workshop')
                and request.form.get('input_date')
                and request.form.get('input_count_seats')):
            try:
                new_activity = {
                    'activityID': '',
                    'title': request.form.get('input_title'),
                    'type': request.form.get('select_type'),
                    'timeline': request.form.get('select_time'),
                    'workshop': request.form.get('select_workshop'),
                    'owner': request.form.get('select_owner'),
                    'date': request.form.get('input_date'),
                    'count_seats': int(request.form.get('input_count_seats'))
                }
                new_activity_obj = activity(**new_activity)
                appDB.session.add(new_activity_obj)
                appDB.session.commit()
                flash('Активность успешно добавлена!')
                error = False
                new_activity['activityID'] = new_activity_obj.activityID
                new_activity = new_activity
            except ValueError:
                flash('В поле "Нужно мест" нужно вводить число!')
                error = True
                new_activity = {
                    'activityID': '',
                    'title': request.form.get('input_title'),
                    'type': request.form.get('select_type'),
                    'timeline': request.form.get('select_time'),
                    'workshop': request.form.get('select_workshop'),
                    'owner': request.form.get('select_owner'),
                    'date': request.form.get('input_date'),
                    'count_seats': ""
                }
        else:
            flash('Не все поля заполнены!')
            new_activity = {
                'activityID': '',
                'title': request.form.get('input_title'),
                'type': request.form.get('select_type'),
                'timeline': request.form.get('select_time'),
                'workshop': request.form.get('select_workshop'),
                'owner': request.form.get('select_owner'),
                'date': request.form.get('input_date'),
                'count_seats': request.form.get('input_count_seats')
            }
            error = True
    elif request.form['workshop_activity_submit'] == 'edit_activity':
        if (request.form.get('input_title')
                and request.form.get('select_type')
                and request.form.get('select_time')
                and request.form.get('select_workshop')
                and request.form.get('input_date')
                and request.form.get('input_count_seats')):
            try:
                edit_activity = {
                    'activityID': request.form.get('input_activity_id'),
                    'title': request.form.get('input_title'),
                    'type': request.form.get('select_type'),
                    'timeline': request.form.get('select_time'),
                    'workshop': request.form.get('select_workshop'),
                    'owner': request.form.get('select_owner'),
                    'date': request.form.get('input_date'),
                    'count_seats': int(request.form.get('input_count_seats'))
                }
                edit_activity_obj = activity.query.filter(
                    activity.activityID == int(edit_activity['activityID'])).first()
                for key, value in edit_activity.items():
                    setattr(edit_activity_obj, key, value)
                appDB.session.commit()
                flash('Активность успешно изменена!')
                new_activity = edit_activity
            except ValueError:
                flash('В поле "Нужно мест" нужно вводить число!')
                error = True
                new_activity = {
                    'activityID': request.form.get('input_activity_id'),
                    'title': request.form.get('input_title'),
                    'type': request.form.get('select_type'),
                    'timeline': request.form.get('select_time'),
                    'workshop': request.form.get('select_workshop'),
                    'owner': request.form.get('select_owner'),
                    'date': request.form.get('input_date'),
                    'count_seats': ""
                }
        else:
            flash('Не все поля заполнены!')
            new_activity = {
                'activityID': '',
                'title': request.form.get('input_title'),
                'type': request.form.get('select_type'),
                'timeline': request.form.get('select_time'),
                'workshop': request.form.get('select_workshop'),
                'owner': request.form.get('select_owner'),
                'date': request.form.get('input_date'),
                'count_seats': request.form.get('input_count_seats')
            }
            error = True
    elif request.form['workshop_activity_submit'] == 'del_activity':
        del_activity_obj = activity.query.filter(activity.activityID == request.form.get('input_activity_id')).first()
        appDB.session.delete(del_activity_obj)
        appDB.session.commit()
        flash('Активность успешно удалена!')
        error = False

    week_number = request.args.get('week')
    year_number = request.args.get('year')
    week_days = _week_days(year_number, week_number)
    # Расписание актинвностей мастерской на неделю
    for day in week_days:
        day['activity'] = get_activity(day.get('day_for_query'), number)

    # Список типов
    activity_type_list = activity_type.query.all()
    activity_type_dict = []
    if activity_type_list:
        for types in activity_type_list:
            activity_type_dict.append(activitytype_info(types))

    # Список промежутков
    time_list = timeline.query.all()
    time_dict = []
    if time_list:
        for time_item in time_list:
            time_dict.append(timeline_info(time_item))

    # Списко мастерских
    workshop_list = workshops.query.all()
    workshop_dict = []
    if workshop_list:
        for workshop_item in workshop_list:
            workshop_dict.append(workshop_item)

    # Список заведующих
    owner_dict = get_users()

    return render_template(
        'workshop_activity.html',
        week_days=week_days,
        now_day=datetime.now().strftime('%Y-%m-%d'),
        activity_type=activity_type_dict,
        timeline=time_dict,
        workshops=workshop_dict,
        owner=owner_dict,

        workshop_page_dict=workshop_page_dict,
        number=number,
        new_activity=new_activity,
        error=error
    )


def _week_days(year_number, week_number):
    startdate = time.asctime(time.strptime('%s %s 0' %(year_number, str(int(week_number)-1)), '%Y %W %w'))
    startdate = datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = []
    for i in range(1, 8):
        day = startdate + timedelta(days=i)
        dates.append({'day': day.strftime('%d.%m.%Y'), 'day_for_query': day.strftime('%Y-%m-%d'), 'activity': []})
    return dates

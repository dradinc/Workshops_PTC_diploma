from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from application import app, login_manager, appDB
from application.db_model.workshops import workshops
from application.db_model.users import get_users
from application.db_model.activity import activity, get_activity
from application.db_model.activity_type import activity_type, activitytype_info
from application.db_model.timeline import timeline, timeline_info
from application.views.activity.get import edit_activity_get
from application.views.activity.get_new import get_new_activity
from application.views.activity.post_new import add_new_activity
from application.views.activity.post_edit import edit_activity
from application.views.activity.delete import delete_activity
from application.views.activity.duplicate import duplicate_activity
from application.views.new_booking import new_booking_get, new_booking_post, accept_bookinh, reject_bookinh


@app.route('/workshops/<number>', methods=['GET'])
def workshop_activity(number):  # Изменение алгоритма рендера страницы
    if not request.args.get('activity') and not request.args.get('booking'):
        workshop_page = workshops.query.filter(workshops.number == number).first()
        workshop_page_dict = {
            'number': workshop_page.number,
            'title': workshop_page.title
        }
        week_number = request.args.get('week')
        year_number = request.args.get('year')
        week_days = None

        if not week_number or not year_number:
            now = datetime.now()
            return redirect('?year=' + str(now.isocalendar()[0])
                            + '&week=' + str(now.isocalendar()[1]))
        else:
            week_days = _week_days(year_number, week_number)

        # Расписание актинвностей мастерской на неделю
        for day in week_days:
            day['activity'] = get_activity(day.get('day_for_query'), number)

        return render_template(
            'workshop_activity_v2.html',
            year_number=year_number,
            week_number=week_number,
            week_days=week_days,
            now_day=datetime.now().strftime('%Y-%m-%d'),

            workshop_page_dict=workshop_page_dict,
            number=number
        )
    else:
        if request.args.get('activity') == 'new':
            return get_new_activity(request, number)
        else:
            if not request.args.get('booking'):
                return edit_activity_get(request, number)
            else:
                if request.args.get('booking') == 'new_booking':
                    return new_booking_get(request, number)
                else:
                    if current_user.role == 0 or current_user.role == 1:
                        if request.args.get('status') == 'True':
                            return accept_bookinh(request, number)
                        else:
                            return reject_bookinh(request, number)
                        pass
                    pass


# На переделку
@app.route('/workshops/<number>', methods=['POST'])
def workshop_activity_post(number):
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

    if not current_user.is_anonymous:
        if current_user.role == 0 or current_user.role == 1:
            if request.form['workshop_activity_submit'] == 'add_activity':
                return add_new_activity(request, number)
            elif request.form['workshop_activity_submit'] == 'edit_activity':
                return edit_activity(request, number)
            elif request.form['workshop_activity_submit'] == 'del_activity':
                return delete_activity(request, number)
            elif request.form['workshop_activity_submit'] == 'duplicate_activity':
                return duplicate_activity(request, number)
    else:
        if request.form['workshop_activity_submit'] == 'add_booking':
            return new_booking_post(request, number)
    '''
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
    '''


def _week_days(year_number, week_number):
    startdate = time.asctime(time.strptime('%s %s 0' %(year_number, str(int(week_number)-1)), '%Y %W %w'))
    startdate = datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = []
    for i in range(1, 8):
        day = startdate + timedelta(days=i)
        dates.append({'day': day.strftime('%d.%m.%Y'), 'day_for_query': day.strftime('%Y-%m-%d'), 'activity': []})
    return dates


def _check_timeline(date):
    pass

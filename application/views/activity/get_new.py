from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for

from application import app, login_manager, appDB
from application.db_model.workshops import workshops
from application.db_model.users import get_users
from application.db_model.activity import activity, get_activity
from application.db_model.activity_type import activity_type, activitytype_info
from application.db_model.timeline import timeline, timeline_info


def get_new_activity(this_request, workshop_number, activity_data=None):
    print(activity_data)
    week_number = this_request.args.get('week')
    year_number = this_request.args.get('year')
    day_number = this_request.args.get('day')
    startdate = time.asctime(time.strptime('%s %s 0' % (year_number, str(int(week_number) - 1)), '%Y %W %w'))
    startdate = datetime.strptime(startdate, '%a %b %d %H:%M:%S %Y')
    dates = []
    for i in range(1, 8):
        day = startdate + timedelta(days=i)
        dates.append(day.strftime('%Y-%m-%d'))

    this_workshop = workshops.query.filter(workshops.number == workshop_number).first()

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

    # Список мастерских
    workshop_list = workshops.query.all()
    workshop_dict = []
    if workshop_list:
        for workshop_item in workshop_list:
            workshop_dict.append(workshop_item)

    # Список заведующих
    owner_dict = get_users()

    return render_template('add_activity.html',
                           status='add',
                           date=dates[int(day_number)],
                           number=workshop_number,
                           owner=this_workshop.owner,

                           activity_type=activity_type_dict,
                           timeline=time_dict,
                           workshops=workshop_dict,
                           owners=owner_dict,

                           activity=activity_data)

from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for

from application import app, login_manager, appDB
from application.db_model.workshops import workshops
from application.db_model.users import get_users
from application.db_model.activity import activity, get_activity
from application.db_model.activity_type import activity_type, activitytype_info
from application.db_model.timeline import timeline, timeline_info
from application.db_model.booking import get_booking_activity


def edit_activity_get(this_request, workshop_number, edit_activity=None):
    # Данные о выбранной активности
    this_activity = activity.query.filter(activity.activityID == this_request.args.get('activity')).first()
    this_activity_dict = {
        'title': this_activity.title,
        'status': this_activity.status,
        'booking': this_activity.booking,
        'count_seats': this_activity.count_seats,
        'type': this_activity.type,
        'timeline': this_activity.timeline,
        'workshop': this_activity.workshop,
        'owner': this_activity.owner,
        'date': this_activity.date
    }

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

    # Список заявок
    booking_dict = get_booking_activity(this_request.args.get('activity'))

    if edit_activity:
        this_activity_dict = edit_activity

    return render_template('edit_activity.html',
                           status='edit',
                           activity=this_activity_dict,

                           activity_type=activity_type_dict,
                           timeline=time_dict,
                           workshops=workshop_dict,
                           owners=owner_dict,
                           booking_list=booking_dict)

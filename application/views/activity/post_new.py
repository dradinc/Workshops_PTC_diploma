from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for
from sqlalchemy import and_

from application import app, login_manager, appDB
from application.db_model.activity import activity
from application.db_model.timeline import timeline
from application.db_model.workshops import workshops
from application.views.activity.get_new import get_new_activity


def add_new_activity(this_request, workshop_number):
    if this_request.form.get("check_status"):
        if this_request.form.get("check_status") == '0':
            status = False
        else:
            status = True
    else:
        status = None
    if this_request.form.get("booking_status"):
        booking = True
    else:
        booking = False
    new_params = {
        'title': this_request.form.get("input_title"),
        'workshop': this_request.form.get("select_workshop"),
        'owner': this_request.form.get("select_owner"),
        'date': this_request.form.get("input_date"),
        'timeline': this_request.form.get("select_time"),
        'type': this_request.form.get("select_type"),
        'count_seats': this_request.form.get("input_count_seats"),
        'status': status,
        'booking': booking
    }

    if (this_request.form.get("input_title")
            and this_request.form.get("select_workshop")
            and this_request.form.get("select_owner")
            and this_request.form.get("input_date")
            and this_request.form.get("select_time")
            and this_request.form.get("select_type")
            and this_request.form.get("input_count_seats")):
        if not _check_timeline(new_params['date'], new_params['timeline']):
            if not _check_count_seats(new_params['count_seats'], workshop_number):
                new_activity = activity(**new_params)
                appDB.session.add(new_activity)
                appDB.session.commit()
            else:
                flash('Необходимое количество мест превышает количество рабочих мест в мастерской!')
                return get_new_activity(this_request, workshop_number, new_params)
        else:
            flash('В выбранный временной промежуток проходят другие активности!')
            return get_new_activity(this_request, workshop_number, new_params)

        flash('Активность успешно добавлена!')
        week_number = this_request.args.get('week')
        year_number = this_request.args.get('year')
        return redirect('?year=' + year_number
                        + '&week=' + week_number)
    else:
        flash('Не все поля заполнены!')
        return get_new_activity(this_request, workshop_number, new_params)


# Проверка, чтобы не было пересекающихся активностей
def _check_timeline(this_date, this_timeline):
    timeline_this_day = []
    this_timeline_item = timeline.query.filter(timeline.timelineID == this_timeline).first()
    activity_this_day = activity.query.filter(and_(activity.date == this_date, activity.status)).all()
    for this_activity in activity_this_day:
        timeline_this_day.append(timeline.query.filter(timeline.timelineID == this_activity.timeline).first())
    for timeline_item in timeline_this_day:
        if (timeline_item.start <= this_timeline_item.start) and (timeline_item.end > this_timeline_item.start):
            return True
        elif (timeline_item.start < this_timeline_item.end) and (timeline_item.end >= this_timeline_item.end):
            return True
    return False


# Проверка, чтобы количество мест активности не превышало количество мест в мастерской
def _check_count_seats(count_seats, number_workshop):
    this_workshop = workshops.query.filter(workshops.number == number_workshop).first()
    if int(count_seats) <= int(this_workshop.count_seats):
        return False
    return True

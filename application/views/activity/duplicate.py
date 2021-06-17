from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for
from sqlalchemy import and_

from application import app, login_manager, appDB
from application.db_model.activity import activity
from application.db_model.timeline import timeline
from application.db_model.workshops import workshops
from application.views.activity.get_new import get_new_activity


def duplicate_activity(this_request, workshop_number):
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
    return get_new_activity(this_request, workshop_number, new_params)

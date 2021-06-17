from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for
from sqlalchemy import and_

from application import app, login_manager, appDB
from application.db_model.activity import activity
from application.db_model.timeline import timeline
from application.db_model.workshops import workshops
from application.views.activity.get_new import get_new_activity


def delete_activity(this_request, workshop_number):
    del_activity_obj = activity.query.filter(
        activity.activityID == this_request.args.get('activity')).first()
    appDB.session.delete(del_activity_obj)
    appDB.session.commit()
    flash('Активность успешно удалена!')

    week_number = this_request.args.get('week')
    year_number = this_request.args.get('year')
    return redirect('?year=' + year_number
                    + '&week=' + week_number)

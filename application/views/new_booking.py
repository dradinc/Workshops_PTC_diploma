from datetime import datetime, timedelta
import time

from flask import request, redirect, render_template, flash, url_for
from flask_mail import Message

from application import app, login_manager, appDB
from application.db_model.booking import booking
from application.db_model.activity import activity
from application.db_model.users import users
from application.db_model.workshops import workshops
from application.db_model.activity_type import activity_type
from application.db_model.timeline import timeline
from application import mail_manager


def new_booking_get(this_request, workshop_number, new_booking=None):
    return render_template('new_booking.html', booking_param=new_booking)


def new_booking_post(this_request, workshop_number):
    new_param = {
        'lastname': this_request.form.get('input_lastname'),
        'firtsname': this_request.form.get('input_firstname'),
        'middlename': this_request.form.get('input_middlename'),
        'group': this_request.form.get('input_group'),
        'email': this_request.form.get('input_email'),
        'activity': this_request.args.get('activity')
    }
    if this_request.form.get('input_lastname')\
            and this_request.form.get('input_firstname')\
            and this_request.form.get('input_group')\
            and this_request.form.get('input_email'):
        new_booking = booking(**new_param)
        appDB.session.add(new_booking)
        appDB.session.commit()

        flash('Заявка успешно отправлена!')
        week_number = this_request.args.get('week')
        year_number = this_request.args.get('year')
        return redirect('?year=' + year_number
                        + '&week=' + week_number)
    else:
        flash('Заполнены не все обязательные поля!')
        return new_booking_get(this_request, workshop_number, new_param)
    pass


def accept_bookinh(this_request, workshop_number):
    edit_booking = booking.query.filter(booking.bookingID == this_request.args.get('booking')).first()
    setattr(edit_booking, 'status', True)
    appDB.session.commit()
    send_mail(True, [edit_booking.email], edit_booking.activity, edit_booking)
    return redirect(f"?year={this_request.args.get('year')}&week={this_request.args.get('week')}&day={this_request.args.get('day')}&activity={this_request.args.get('activity')}")


def reject_bookinh(this_request, workshop_number):
    edit_booking = booking.query.filter(booking.bookingID == this_request.args.get('booking')).first()
    setattr(edit_booking, 'status', False)
    appDB.session.commit()
    send_mail(False, [edit_booking.email], edit_booking.activity, edit_booking)
    return redirect(f"?year={this_request.args.get('year')}&week={this_request.args.get('week')}&day={this_request.args.get('day')}&activity={this_request.args.get('activity')}")


def send_mail(result, recipients, activityID, edit_booking):
    activity_item = activity.query.filter(activity.activityID == activityID).first()
    type_a = activity_type.query.filter(activity_type.typeID == activity_item.type).first()
    time = timeline.query.filter(timeline.timelineID == activity_item.timeline).first()
    workshop = workshops.query.filter(workshops.number == activity_item.workshop).first()
    owner = users.query.filter(users.id == activity_item.owner).first()

    message = Message("Заявка на работу в мастерской", recipients=recipients)
    if result:
        message.html = f"""
        <head>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet"
                  integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
        </head>
        <body>
          
          <section class="container">
            <section class="row">
              <article>
                <h2>
                  Заявка на {activity_item.date} одобрена
                </h2>
              </article>
            </section>
            <section class="row">
              <article class="row">
                Здравствуйте, {edit_booking.firstname} {edit_booking.middlename}! Ваша заявка на рабочее место во время "{activity_item.title}" была одобрена! <br>
              </article>
            </section>
            <section class="row">
              <article class="row">
                <b>Мастерская:</b> {workshop.number} | {workshop.title} <br>
              </article>
              <article class="row">
                <b>Время:</b> {str(':'.join(str(time.start).split(':')[:2]).zfill(5))} - {str(':'.join(str(time.end).split(':')[:2]).zfill(5))} <br>
              </article>
              <article class="row">
                <b>Ведущий:</b> {owner.lastname} {owner.firstname} {owner.middlename} <br>
              </article> 
            </section>
            <section class="row mt-4">
              <article class="row">
                <br><br>-------------------------------- <br>
              </article>
              <article class="row">
                Сообщение было отправлено автоматически. <br>
              </article>
              <article class="row">
                Хорошего настроения и продуктивной работы! <br>
                C уважением, Ваше приложение "Мастерские ПТК"! <br>
              </article>
            </section>
          </section>
        </body>"""
    else:
        message.html = f"""
        <head>
          <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet"
                  integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
        </head>
        <body>
          
          <section class="container">
            <section class="row">
              <article>
                <h2>
                  Заявка на {activity_item.date} отклонена
                </h2>
              </article>
            </section>
            <section class="row">
              <article class="row">
                Здравствуйте, {edit_booking.firstname} {edit_booking.middlename}! Ваша заявка на рабочее место во время "{activity_item.title}" была отклонена! <br>
              </article>
            </section>
            <section class="row">
              <article class="row">
                <b>Мастерская:</b> {workshop.number} | {workshop.title} <br>
              </article>
              <article class="row">
                <b>Время:</b> {str(':'.join(str(time.start).split(':')[:2]).zfill(5))} - {str(':'.join(str(time.end).split(':')[:2]).zfill(5))} <br>
              </article>
              <article class="row">
                <b>Ведущий:</b> {owner.lastname} {owner.firstname} {owner.middlename} <br>
              </article> 
            </section>
            <section class="row mt-4">
              <article class="row">
                <br><br>-------------------------------- <br>
              </article>
              <article class="row">
                Сообщение было отправлено автоматически. <br>
              </article>
              <article class="row">
                Хорошего настроения и удачного дня! <br>
                C уважением, Ваше приложение "Мастерские ПТК"! <br>
              </article>
            </section>
          </section>
        </body>"""
    mail_manager.send(message)

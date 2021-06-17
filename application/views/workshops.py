from datetime import datetime

from flask import request, redirect, render_template, flash, url_for

from application import app, login_manager, appDB
from application.db_model.workshops import workshops, workshop_info
from application.db_model.users import users


@app.route('/workshops', methods=['GET'])
def get_workshops():
    workshop_all = []
    workshop_all_list = []
    list_for_owner = []
    new_workshop = {
        'number': "",
        'title': "",
        'description': "",
        'owner': "",
        'count_seats': ""
    }
    status = ''
    error = False
    workshop_all = workshops.query.all()
    list_for_owner = users.query.all()
    if not workshop_all:
        workshop_all_list = None
    else:
        for workshop in workshop_all:
            workshop_all_list.append(workshop_info(workshop))
    return render_template('workshops.html',
                           workshop_all_list=workshop_all_list,
                           new_workshop=new_workshop,
                           list_for_owner=list_for_owner,
                           status=status,
                           error=error,
                           page='workshops')


@app.route('/workshops', methods=['POST'])
def workshop_post():
    status = ''
    error = False
    try:
        if request.form['submit_workshop'] == 'add_workshop':
            status = 'add_workshop'
            number = request.form.get('add_number')
            title = request.form.get('add_title')
            owner = request.form.get('add_owner')
            count_seats = request.form.get('add_count_seats')
            new_workshop = {
                'number': number,
                'title': title,
                'owner': owner,
                'count_seats': count_seats,
            }

            if owner and title and number:
                workshopA = workshops(**new_workshop)
                appDB.session.add(workshopA)
                appDB.session.commit()
                flash('Мастерская успешно добавлен!')
                workshop_all = workshops.query.all()
                list_for_owner = users.query.all()
                workshop_all_list = []
                if not workshop_all:
                    workshop_all_list = None
                else:
                    for workshop in workshop_all:
                        workshop_all_list.append(workshop_info(workshop))
                error = False
            else:
                flash('Не все поля заполнены!')
                error = True
        elif request.form['submit_workshop'] == 'edit_workshop':
            status = 'edit_workshop'
            now_number = request.form.get('now_number')
            number = request.form.get('number')
            title = request.form.get('title')
            owner = request.form.get('owner')
            count_seats = request.form.get('count_seats')

            if owner == "0":
                owner = None

            edit_workshop = {
                'number': number,
                'title': title,
                'owner': owner,
                'count_seats': count_seats,
            }

            workshopE = workshops.query.filter(workshops.number == now_number).first()
            for key, value in edit_workshop.items():
                setattr(workshopE, key, value)
            appDB.session.commit()
            new_workshop = edit_workshop

            flash('Изменения успешно внесены')

            workshop_all = workshops.query.all()
            list_for_owner = users.query.all()
            workshop_all_list = []
            if not workshop_all:
                workshop_all_list = None
            else:
                for workshop in workshop_all:
                    workshop_all_list.append(workshop_info(workshop))
        elif request.form['submit_workshop'] == 'open_activity':
            number = request.form.get('now_number')
            now = datetime.now()
            return redirect('/workshops/'
                            + str(number)
                            + '?year=' + str(now.isocalendar()[0])
                            + '&week=' + str(now.isocalendar()[1]))
    except ValueError:
        flash('В поле "Количество мест" нужно вводить число!')
        error = True
        if status == 'add_workshop':
            number = request.form.get('add_number')
            title = request.form.get('add_title')
            owner = request.form.get('add_owner')
            new_workshop = {
                'number': number,
                'title': title,
                'owner': owner,
                'count_seats': '',
            }
        elif status == 'edit_workshop':
            now_number = request.form.get('now_number')
            title = request.form.get('title')
            owner = request.form.get('owner')

            if owner == "0":
                owner = None

            edit_workshop = {
                'number': now_number,
                'title': title,
                'owner': owner,
                'count_seats': '',
            }

    return render_template('workshops.html',
                           workshop_all_list=workshop_all_list,
                           new_workshop=new_workshop,
                           list_for_owner=list_for_owner,
                           status=status,
                           error=error,
                           page='workshops')
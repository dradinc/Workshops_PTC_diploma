from flask import request, redirect, render_template, flash, url_for
from flask_login import login_required, current_user

from application import app, login_manager, appDB
from application.db_model.users import get_users, users, check_login, generate_password_hash


@app.route('/users', methods=['GET'])
@login_required
def users_page():
    if current_user.role == 0:
        all_users = get_users()
        params_empty = {
            'login': "",
            'password': "",
            'role': "",
            'firstname': "",
            'lastname': "",
            'middlename': ""
        }
        return render_template('users.html',
                               all_users=all_users,
                               page='users',
                               new_user=params_empty)
    else:
        return redirect('/')


# Нарисовать блок-схему
@app.route('/users', methods=['POST'])
@login_required
def users_post():
    if current_user.role == 0:
        all_users = get_users()
        params_empty = {
            'login': "",
            'password': "",
            'role': "",
            'firstname': "",
            'lastname': "",
            'middlename': ""
        }
        if request.form['submit_user'] == 'add_user':
            login = request.form.get('login')
            password = request.form.get('password')
            role = request.form.get('role')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            middlename = request.form.get('middlename')

            params = {
                'login': str(login),
                'password': str(generate_password_hash(password)),
                'role': str(role),
                'firstname': str(firstname),
                'lastname': str(lastname),
                'middlename': str(middlename)
            }

            if login and password and role and firstname and lastname and middlename:
                if (check_login(login)):
                    user = users(**params)
                    appDB.session.add(user)
                    appDB.session.commit()
                    flash('Пользователь успешно добавлен!')
                    all_users = get_users()
                    return render_template('users.html', all_users=all_users, page='users', new_user=params_empty,
                                           error=False)
                else:
                    flash('Пользователь с таким логином уже существует!')
                    return render_template('users.html', all_users=all_users, page='users', new_user=params, error=True)
            else:
                flash('Не все поля были заполнены заполнены!')
            return render_template('users.html', all_users=all_users, page='users', new_user=params, error=True)
        elif request.form['submit_user'] == 'edit_user':
            userID = request.form.get('userID')
            login = request.form.get('edit_login')
            # password = request.form.get('edit_password')
            role = request.form.get('edit_role')
            firstname = request.form.get('edit_firstname')
            lastname = request.form.get('edit_lastname')
            middlename = request.form.get('edit_middlename')

            user = users.query.filter(users.id == userID).first()

            params = {
                'id': int(userID),
                'login': str(login),
                # 'password': str(password),
                'role': str(role),
                'firstname': str(firstname),
                'lastname': str(lastname),
                'middlename': str(middlename)
            }
            for key, value in params.items():
                if key == 'login':
                    if user.login == login:
                        break
                    else:
                        if check_login(value):
                            break
                        else:
                            flash('Пользователь с таким логином уже существует!')
                            return render_template('users.html', all_users=all_users, page='users',
                                                   new_user=params_empty,
                                                   error=True)
            for key, value in params.items():
                setattr(user, key, value)
            appDB.session.commit()
            flash('Данные пользователя успешно изменены!')
            all_users = get_users()
            return render_template('users.html', all_users=all_users, page='users', new_user=params_empty, error=False)
        elif request.form['submit_user'] == 'del_user':
            return 'DELETE'
    else:
        return redirect('/')

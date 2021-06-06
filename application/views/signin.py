from flask import render_template, redirect, request, flash
from flask_login import current_user

from application import app, login_manager
from application.db_model.users import users


@app.route('/signin', methods=['GET'])
def signin_page_get():
    if current_user.is_anonymous:
        return render_template('signin.html')
    else:
        return redirect('/workshops')


@app.route('/signin', methods=['POST'])
def signin_post():
    login = request.form.get('login')
    password = request.form.get('password')
    if login and password:
        result = users.auth_user(login, password)
        if result:
            return redirect('/workshops')
        else:
            flash('Логин или пароль не верны!')
    else:
        flash('Заполните поля ввода!')
    return render_template('signin.html')

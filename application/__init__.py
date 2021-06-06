# Импорт установленных модулей и библиотек
from flask import Flask, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Импорт собственных модулей и библиотек
from config import Config


# Объявление приложения и получение конфигурации
app = Flask(__name__)
app.config.from_object(Config)

# Объявление экземпляра для работы с СУБД MySQL
appDB = SQLAlchemy(app)

# Объявление экземпляра для работы с пользователями
login_manager = LoginManager(app)


# Импорт обработчика ссылок
from application.views import index, workshops, signin, users, logout, type_and_time, workshop_activity


@app.after_request
def redirect_to_signin(response):
    if response.status_code == 401:
        return redirect('/signin')
    return response

import hashlib

from flask_login import UserMixin, login_user

from application import appDB, login_manager


class users(appDB.Model, UserMixin):
    # Поля таблицы
    id = appDB.Column(appDB.Integer, primary_key=True)
    login = appDB.Column(appDB.String(32), nullable=False)
    password = appDB.Column(appDB.String(128), nullable=False)
    role = appDB.Column(appDB.Integer, nullable=False)
    firstname = appDB.Column(appDB.String(64), nullable=False)
    lastname = appDB.Column(appDB.String(64), nullable=False)
    middlename = appDB.Column(appDB.String(64), nullable=False)
    remotely = appDB.Column(appDB.Boolean, nullable=False,  default=False)

    def __init__(self, **kwargs):
        self.login = kwargs.get('login')
        self.password = kwargs.get('password')
        self.role = int(kwargs.get('role'))
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.middlename = kwargs.get('middlename')
        self.remotely = kwargs.get('remotely')

    @classmethod
    def auth_user(cls, login, password):
        user = cls.query.filter(cls.login == login).first()
        if not user:
            return False
        if check_password_hash(user.password, password):
            login_user(user)
            return True
        return False


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(user_id)


def generate_password_hash(password):
    return hashlib.sha3_512(bytes(hashlib.sha3_512(bytes(password, encoding='utf-8')).hexdigest(), encoding='utf-8')).hexdigest()


def check_password_hash(password_hash, password):
    if password_hash == generate_password_hash(password):
        return True
    else:
        return False


def get_users():
    users_dict = []
    all_users = users.query.all()
    for user in all_users:
        users_dict.append(
            {
                'id': user.id,
                'login': user.login,
                'role': user.role,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'middlename': user.middlename,
                'remotely': user.remotely
            }
        )
    return users_dict


def check_login(login):  # Проверка логина на повторение
    result = users.query.filter(users.login == login).first()
    if not result:
        return True
    else:
        return False

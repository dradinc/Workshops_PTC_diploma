from application import appDB
from application.db_model.users import users


class workshops(appDB.Model):
    # Поля таблицы
    number = appDB.Column(appDB.String(4), primary_key=True)
    title = appDB.Column(appDB.String(64), unique=True, nullable=False)
    description = appDB.Column(appDB.Text, nullable=True)
    owner = appDB.Column(appDB.Integer, appDB.ForeignKey('users.id'), nullable=True)
    count_seats = appDB.Column(appDB.Integer, nullable=True)
    # Обратная связь
    workshop_for_user = appDB.relationship('users', backref=appDB.backref('workshop_data__user', lazy='dynamic'))

    def __init__(self, **kwargs):
        self.number = str(kwargs.get('number'))
        self.title = str(kwargs.get('title'))
        self.description = str(kwargs.get('description'))
        self.owner = int(kwargs.get('owner'))
        self.count_seats = int(kwargs.get('count_seats'))


def get_workshop(number):
    workshop = workshops.query.filter_by(workshops.number == number).first_or_404()
    return workshop


def workshop_info(workshop):
    workshop_dict = {}
    if not workshop.owner:
        workshop_dict = {
            'number': workshop.number,
            'title': workshop.title,
            'description': workshop.description,
            'count_seats': workshop.count_seats,
            'owner': {None}
        }
    else:
        owner = users.query.filter(users.id == workshop.owner).first()
        workshop_dict = {
            'number': workshop.number,
            'title': workshop.title,
            'description': workshop.description,
            'count_seats': workshop.count_seats,
            'owner': {
                'id': owner.id,
                'firstname': owner.firstname,
                'lastname': owner.lastname,
                'middlename': owner.middlename
            }
        }
    return workshop_dict

def check_number(number):  # Проверка логина на повторение
    result = workshops.query.filter(workshops.login == number).first()
    if not result:
        return True
    else:
        return False

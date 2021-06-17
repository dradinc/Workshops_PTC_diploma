from sqlalchemy import and_

from application import appDB
from application.db_model.users import users
from application.db_model.workshops import workshops
from application.db_model.activity_type import activity_type
from application.db_model.timeline import timeline


class activity(appDB.Model):
    # Поля таблицы
    activityID = appDB.Column(appDB.Integer, primary_key=True)
    title = appDB.Column(appDB.String(128), unique=True, nullable=False)
    description = appDB.Column(appDB.Text, nullable=True)
    type = appDB.Column(appDB.Integer, appDB.ForeignKey('activity_type.typeID'), nullable=False)
    timeline = appDB.Column(appDB.Integer, appDB.ForeignKey('timeline.timelineID'), nullable=False)
    workshop = appDB.Column(appDB.String(4), appDB.ForeignKey('workshops.number'), nullable=False)
    owner = appDB.Column(appDB.Integer, appDB.ForeignKey('users.id'), nullable=True)
    date = appDB.Column(appDB.DateTime, nullable=False)
    week = appDB.Column(appDB.Boolean, nullable=True)
    status = appDB.Column(appDB.Boolean, nullable=True)
    booking = appDB.Column(appDB.Boolean, nullable=True)
    count_seats = appDB.Column(appDB.Integer, nullable=True)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.workshop = kwargs.get('workshop')
        self.owner = kwargs.get('owner')
        self.date = kwargs.get('date')
        self.timeline = int(kwargs.get('timeline'))
        self.type = int(kwargs.get('type'))
        self.count_seats = kwargs.get('count_seats')
        self.status = kwargs.get('status')
        self.booking = kwargs.get('booking')


def get_activity(day, number):
    list_day_activity = activity.query.filter(and_(activity.date == day, activity.workshop == number)).order_by(activity.timeline).all()

    dict_day_activity = []
    for item_activity in list_day_activity:
        type_a = activity_type.query.filter(activity_type.typeID == item_activity.type).first()
        time = timeline.query.filter(timeline.timelineID == item_activity.timeline).first()
        workshop = workshops.query.filter(workshops.number == item_activity.workshop).first()
        owner = users.query.filter(users.id == item_activity.owner).first()
        if not owner:
            dict_day_activity.append({
                'activityID': item_activity.activityID,
                'title': item_activity.title,
                'status': item_activity.status,
                'booking': item_activity.booking,
                'count_seats': item_activity.count_seats,
                'type': {
                    'typeID': type_a.typeID,
                    'title': type_a.title
                },
                'time': {
                    'timelineID': time.timelineID,
                    'title': time.title,
                    'start': time.start,
                    'end': time.end
                },
                'workshop': {
                    'number': workshop.number,
                    'title': workshop.title,
                    'count_seats': workshop.count_seats
                },
                'owner': {
                    'id': '',
                    'firstname': '',
                    'lastname': '',
                    'middlename': ''
                }
            })
        else:
            dict_day_activity.append({
                'activityID': item_activity.activityID,
                'title': item_activity.title,
                'status': item_activity.status,
                'booking': item_activity.booking,
                'count_seats': item_activity.count_seats,
                'type': {
                    'typeID': type_a.typeID,
                    'title': type_a.title
                },
                'time': {
                    'timelineID': time.timelineID,
                    'title': time.title,
                    'start': str(':'.join(str(time.start).split(':')[:2]).zfill(5)),
                    'end': str(':'.join(str(time.end).split(':')[:2]).zfill(5))
                },
                'workshop': {
                    'number': workshop.number,
                    'title': workshop.title,
                    'count_seats': workshop.count_seats
                },
                'owner': {
                    'id': owner.id,
                    'firstname': owner.firstname,
                    'lastname': owner.lastname,
                    'middlename': owner.middlename
                }
            })
    return dict_day_activity

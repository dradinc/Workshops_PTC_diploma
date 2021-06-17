from application import appDB


class booking(appDB.Model):
    # Поля таблицы
    bookingID = appDB.Column(appDB.Integer, primary_key=True)
    firstname = appDB.Column(appDB.String(64), nullable=False)
    lastname = appDB.Column(appDB.String(64), nullable=False)
    middlename = appDB.Column(appDB.String(64), nullable=True)
    group = appDB.Column(appDB.String(4), nullable=False)
    email = appDB.Column(appDB.String(64), nullable=False)
    activity = appDB.Column(appDB.Integer, appDB.ForeignKey('activity.activityID'), nullable=False)
    status = appDB.Column(appDB.Boolean, nullable=True)

    def __init__(self, **kwargs):
        self.lastname = kwargs.get('lastname')
        self.firstname = kwargs.get('firtsname')
        if kwargs.get('middlename'):
            self.middlename = kwargs.get('middlename')
        self.group = kwargs.get('group')
        self.email = kwargs.get('email')
        self.activity = kwargs.get('activity')


def get_booking_activity(activityID):
    booking_list = booking.query.filter(booking.activity == activityID).all()
    booking_dict = []
    for booking_items in booking_list:
        booking_dict.append({
            'bookingID': booking_items.bookingID,
            'lastname': booking_items.lastname,
            'firstname': booking_items.firstname,
            'middlename': booking_items.middlename,
            'group': booking_items.group,
            'email': booking_items.email,
            'status': booking_items.status
        })
    return booking_dict

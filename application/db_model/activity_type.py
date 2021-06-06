from application import appDB


class activity_type(appDB.Model):
    # Поля таблицы
    typeID = appDB.Column(appDB.Integer, primary_key=True)
    title = appDB.Column(appDB.String(64), nullable=False)
    description = appDB.Column(appDB.Text, nullable=True)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')


def activitytype_info(activitytype):
    activitytype_dict = {
        'typeID': activitytype.typeID,
        'title': activitytype.title,
        'description': activitytype.description
    }
    return activitytype_dict

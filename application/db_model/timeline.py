from application import appDB


class timeline(appDB.Model):
    # Поля таблицы
    timelineID = appDB.Column(appDB.Integer, primary_key=True)
    title = appDB.Column(appDB.String, nullable=False)
    start = appDB.Column(appDB.DateTime, nullable=False)
    end = appDB.Column(appDB.DateTime, nullable=False)

    def __init__(self, **kwargs):
        self.title = kwargs.get('title')
        self.start = kwargs.get('start')
        self.end = kwargs.get('end')


def timeline_info(time_line, activity_time=None):
    if not activity_time:
        timeline_dict = {
            'timelineID': time_line.timelineID,
            'title': time_line.title,
            'start': str(':'.join(str(time_line.start).split(':')[:2]).zfill(5)),
            'end': str(':'.join(str(time_line.end).split(':')[:2]).zfill(5))
        }
        return timeline_dict

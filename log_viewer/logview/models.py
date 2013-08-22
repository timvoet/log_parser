from django.db import models

# Create your models here.
class LogEvent(models.Model):
    date_time = models.CharField()
    level = models.CharField(String)
    class_name = models.CharField(String)
    message = models.CharField(String)
    session_id = models.CharField(String)
    meeting_id = models.CharField(String)
    
    def __init__(self, date_time, level, class_name, message, session_id=None, meeting_id=None):
        self.date_time = date_time
        self.level = level
        self.class_name = class_name
        self.message = message
        self.session_id = session_id
        self.meeting_id = meeting_id
    def __repr__(self):
        return "<LogEvent('%s','%s', '%s')>" % (self.date_time, self.class_name, self.message)

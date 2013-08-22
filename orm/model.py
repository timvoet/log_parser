from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
class LogEvent(Base):
    """
    Model object representing the LogEvent Object
    
    entries are stored in a log_events table.
    """
    __tablename__ = "log_events"
    
    id = Column(Integer, primary_key=True)
    date_time = Column(String)
    level = Column(String)
    class_name = Column(String)
    message = Column(String)
    session_id = Column(String)
    meeting_id = Column(String)
    
    def __init__(self, date_time, level, class_name, message, session_id=None, meeting_id=None):
        self.date_time = date_time
        self.level = level
        self.class_name = class_name
        self.message = message
        self.session_id = session_id
        self.meeting_id = meeting_id
    def __repr__(self):
        return "<LogEvent('%s','%s', '%s')>" % (self.date_time, self.class_name, self.message)


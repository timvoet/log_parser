#!/usr/bin/env python
from orm.model import LogEvent
import optparse
import time
import re
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

supported_DBS = ['sqlite3']

date_pattern = re.compile(r'(\d\d\d\d\-\d\d\-\d\d.*)(INFO|WARN|DEBUG|ERROR|FATAL)')
level_pattern = re.compile(r'.*(DEBUG|ERROR|INFO|WARN|FATAL).*')
class_name_pattern = re.compile(r'.*\[([a-zA-Z0-9]*\.[a-zA-Z0-9\.]*).*')
message_pattern = re.compile(r'.*\[.*\]\s-(.*)')
sessionId_pattern = re.compile(r'.*\[(sessionId:[A-Z0-9]*)\].*')
meetingId_pattern = re.compile(r'.*\[(meetingId:[A-Z0-9]*)\].*')


def createEngine(options):
    """
    Create the engine for use
    """
    LogEvent_table = LogEvent.__table__
    metadata = LogEvent.metadata 
    if ( options.dbType == "sqlite3"):
        engine = create_engine('sqlite:///%s' % options.dataStorePath, echo=options.verbose)
        Session = sessionmaker(bind=engine)
        session = Session()

    metadata.create_all(engine)
    return session

def processFile(f, options):
    """
    Process the file and insert into the DB
    """
    session = createEngine(options)
    multiLineMessage = False
    for line in f:
        line = line.strip()

        if ( not lineStartsWithDate( line ) ):
            pass
        else:
            logEntry = processLine( line )
            session.add(logEntry)
            if options.verbose:
                print logEntry
        
    
    "Commit at end of file"
    session.commit()

def lineStartsWithDate(line):
    """
    checks to see if the line starts with a date
    """
    match = re.search("\d\d\d\d\-\d\d\-\d\d", line )
    if (re.search("\d\d\d\d\-\d\d\-\d\d", line ) ):
        return True
    else:
        return False
def processLine(line):
    """
    Parse the line and create the entry to log
    """
    date_match = date_pattern.match(line)
    if date_match:
        date = date_match.group(1)
    else:
        date = "Invalid pattern"
    
    level_match = level_pattern.match(line)
    if level_match:
        level = level_match.group(1)
    else:
        level = "UNKNOWN"
        
    class_name_match = class_name_pattern.match(line)
    if class_name_match:
        class_name = class_name_match.group(1)
    else:
        class_name = "UNKNOWN"
    message_match = message_pattern.match(line)
    if message_match:
        message = message_match.group(1)
    else:
        message = "CAN'T PARSE"
        
    sessionId_match = sessionId_pattern.match(line)
    if sessionId_match:
        sessionId = sessionId_match.group(1)
        pos = sessionId.index(":")
        sessionId = sessionId[pos+1:]
    else:
        sessionId = None
        
    meetingId_match = meetingId_pattern.match(line)
    if meetingId_match:
        meetingId = meetingId_match.group(1)
        pos = meetingId.index(":")
        meetingId = meetingId[pos+1:]
    else:
        meetingId = None

    le = LogEvent(date_time=date.strip(),level=level.strip(),class_name=class_name.strip(), message=message.strip(), session_id=sessionId, meeting_id = meetingId)
    return le


def main():
    """
    Main entry point.
    """
    p = optparse.OptionParser(description="Parses the log files to generate a DB for analysis.", prog="log_analyzer",version="0.1", usage="%prog --filePath <path_to_file>")
    p.add_option("--filePath","-f",action="store",help="specifies the log file to analyze")
    p.add_option("--dataStorePath","-s", action="store", help="The path to store the db file", default="tomcat_stats.db")
    p.add_option("--dbType", "-d", action="store", default="sqlite3", help="Database format, currently supports " + ' '.join(supported_DBS ))
    p.add_option("--verbose", "-v", action="store_true", default=False, help="Enables verbose output")
    options,arguments = p.parse_args()
    if ( not options.filePath ):
        p.print_help()
        return

    if ( not options.dbType in supported_DBS ):
        p.print_help()
        return
        
    try:
        f = open(options.filePath)
    except IOError:
        print "No such file: %s" % options.filePath
        raw_input("Press Enter to close window")
        return


    processFile(f, options)        
if __name__ == "__main__":
    main()

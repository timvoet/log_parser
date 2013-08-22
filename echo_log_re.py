#!/usr/bin/env python
import optparse
import time
import re

def functionThatAnalisesTheLine( line, searchString ):
    """
    Checks the line for the specific SearchString.
    
    This method filter's out lines that don't match the requested search string
    if no search string is specified will just echo everything back.
    """
    clean_line = line.strip()
    if ( not sessionId == None ):
        if re.search(sessionId, clean_line ):
            print clean_line
    else:
        print clean_line
def main():
    """
    Main entry point
    """
    p = optparse.OptionParser(description="Tails a log looking for a specific pattern.", prog="echo_log_re",version="0.1", usage="%prog")
    p.add_option("--filePath","-f",action="store",help="specifies the log file to analyze")
    p.add_option("--searchString","-s",action="store",help="The pattern to search the file")
    options,arguments = p.parse_args()
    try:
          f = open(options.filePath)
    except IOError:
            print "No such file: %s" % options.filePath
            raw_input("Press Enter to close window")
    try:
            lines = f.readlines()
            while True:
                    line = f.readline()
                    try:
                            if not line:
                                    time.sleep(1)
                            else:
                                    functionThatAnalisesTheLine(line, options.searchString)
                    except Exception, e:
                            # handle the exception somehow (for example, log the trace) and raise the same exception again
                            raw_input("Press Enter to close window")
                            raise e
    finally:
            f.close()

if __name__ == "__main__":
    """
    Main entry point
    """
    main()

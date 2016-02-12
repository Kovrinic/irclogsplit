#!/usr/bin/python
import re
from datetime import datetime, timedelta
import os
import sys, getopt

def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, 'hi:V', ['help', 'version', 'ifile'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit()
        elif opt in ('-V', '--version'):
            version()
            sys.exit()
        elif opt in ('-i', '--ifile'):
            inputfile = arg

    split_logs(inputfile)

def usage():
    print """
    NAME
        irclogsplit

    SYNOPSIS
        irclogsplit [options] <file>

    DESCRIPTION
        irc_log_split is a utility to break up long irc log files into
        smaller more manageable files.

    OPTIONS
        -i, --ifile <file>      - Input file
        -h, --help              - Display this help message and exit
        -V, --version           - Dispaly program version and exit
    """

def version():
    print """
    irclogsplit | Version 1.0.0
    By: Matthew Rotfuss
    """

def get_dtime(line):
    return datetime.strptime(line[:19], '%Y-%m-%d %H:%M:%S')

def file_name(dtime):
    return '%02d-%02d.log' %(dtime.month, dtime.day)

def setup_path(irc_name, date_time):
    year_folder = str(date_time.year)
    irc_folder = os.path.join(year_folder, irc_name)
    log_file = os.path.join(irc_folder, file_name(date_time))

    if not os.path.exists(year_folder):
        print '* Creating \"%s\" folder' %year_folder
        os.makedirs(year_folder)
    if not os.path.exists(irc_folder):
        print '* Creating \"%s\" folder' %(irc_folder)
        os.makedirs(irc_folder)
    if not os.path.exists(log_file):
        print '* Writing data to \"%s\" file' %log_file
        open(log_file, 'a').close()

    return log_file

def get_irc_name(f):
    irc_name = f.name.split('.')[2]
    print '* irc name = %s' %irc_name
    return irc_name

def split_logs(filename):
    print '*' * 80
    if not filename:
        print '* \"%s\" is not a valid input file'
        print '*' * 80
        return

    f = open(filename, 'r+')
    irc_name = get_irc_name(f)

    irc_file = f.read()
    larray = irc_file.splitlines()

    start_time = get_dtime(larray[0])
    log_file = setup_path(irc_name, start_time)

    nf = open(log_file, 'r+')

    for line in larray:
        current_time = get_dtime(line)
        if current_time.day >= (start_time.day + 1):
            start_time = current_time
            # create new log file location and file
            new_log_file = setup_path(irc_name, start_time)

            # close previouse file
            nf.close()

            # open new log_file to wirte
            nf = open(new_log_file, 'r+')
            # write current line to new file
            nf.write(line.strip() + '\n')
        else:
            nf.write(line.strip() + '\n')

    # close opened file(s)
    nf.close()

    # close opend file(s)
    f.close()

    print '* Finished spliting \"%s\"' %filename
    print '*' * 80
    return

if __name__ == "__main__":
    main(sys.argv[1:])

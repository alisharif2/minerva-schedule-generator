#!/usr/bin/python3

# Written by Ali Murtaza Sharif
# Date: 10-Sept-2016
# Please don't steal

import requests, os, sys, argparse, getpass, pytz
from login import login
from sched_html_reader import extract_schedule
from ical_gen import *
from datetime import datetime

# Command line argument check
parser = argparse.ArgumentParser(description='Login to minerva and download personal schedule page in html')
parser.add_argument('userid', action='store')
parser.add_argument('-f', '--fall', action='store_true', default=False, dest='fall')
parser.add_argument('-w', '--winter', action='store_true', default=False, dest='winter')
parser.add_argument('year', action='store', type=int)
parser.add_argument('-p', '--password', action='store', dest='user_pass')

args = parser.parse_args()

# validate the semester argument
# -f and -w are much easier to write than 'fall' or 'winter'
# unfortunately that means I have to deal with them being optional
# TODO find a way to make the semester argument exclusive or
if args.fall and args.winter:
    print("Please enter either 'fall' or 'winter' not both")
if not args.fall and not args.winter:
    print("Please pass a semester")

# Collect user's password without echo
if args.user_pass is None:
    user_pass = getpass.getpass()
else:
    user_pass = args.user_pass

# calculate the 'term_in' variable for the target POST
term = 0
if args.fall:
    term = args.year * 100 + 9
    semester = 'fall'
elif args.winter:
    term = args.year * 100 + 1
    semester = 'winter'

raw_html = login(args.userid, user_pass, term, semester, args.year)
course_data = extract_schedule(raw_html)

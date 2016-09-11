#!/usr/bin/python3

import requests, os, sys, argparse, getpass
from lxml import html

# Command line argument check
parser = argparse.ArgumentParser(description='Login to minerva and download personal schedule page in html')
parser.add_argument('userid', action='store')
parser.add_argument('-f', '--fall', action='store_true', default=False, dest='fall')
parser.add_argument('-w', '--winter', action='store_true', default=False, dest='winter')
parser.add_argument('year', action='store', type=int)

args = parser.parse_args()

# validate the semester arg
if args.fall and args.winter:
    print("Please enter either 'fall' or 'winter' not both")
if not args.fall and not args.winter:
    print("Please pass a semester")

# Collect user's password without echo
user_pass = getpass.getpass()

# login details
payload = {
        "sid" : args.userid, 
        "PIN" : user_pass
        }

# calculate the 'term_in' variable for the target POST
term = 0
if args.fall:
    term = args.year * 100 + 9
    semester = 'fall'
elif args.winter:
    term = args.year * 100 + 1
    semester = 'winter'

# The important urls
base_url   = "https://horizon.mcgill.ca/pban1/"
start_url  = base_url + "twbkwbis.P_WWWLogin"
post_url   = base_url + "twbkwbis.P_ValLogin"
target_url = base_url + "bwskfshd.P_CrseSchdDetl"
logout_url = base_url + "twbkwbis.P_Logout"

# Create session entity that we will be using
minerva = requests.Session()

# Go to the login page with the form to get the initial session data
start_page = minerva.get(start_url)

# Place the session data in a dictionary and add the login page as the referer
post_headers = dict(start_page.headers)
post_headers['Referer'] = start_url

# Post the login data and header session data
post_result = minerva.post(post_url, data = payload, headers = post_headers)

# Goto the target page and pass the desired term
target_page = minerva.post(target_url, data = {"term_in": "{}".format(term)}, headers = post_result.headers)

with open("{}_{}.html".format(semester, args.year), 'w') as f:
    f.write(target_page.text)

# Logout and terminate our session
minerva.get(logout_url, cookies=target_page.cookies)

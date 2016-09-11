# Written by Ali Murtaza Sharif
# Date: 10-Sept-2016
# Please don't steal

from bs4 import BeautifulSoup as bsoup
from collections import defaultdict
import re

def extract_schedule(raw_html):
    clean_html = bsoup(raw_html, 'html.parser')
    info = []
    times = []
    for tag in clean_html.find_all("table", class_="datadisplaytable"):
        if "Scheduled Meeting Times" in tag.caption.get_text():
            times.append(tag)
        else:
            info.append(tag)

    tables = zip(info, times)
    course_data_raw = defaultdict(dict)
    for infobox, meeting_times in tables:
        class_title = infobox.caption.get_text()
        for title_box, value_box in zip(list(meeting_times.find_all('th')), list(meeting_times.find_all('td'))):
            course_data_raw[class_title][title_box.string] = value_box.string

    return clean_up(course_data_raw)

def clean_up(course_data_raw):
    course_data = dict(course_data_raw)
    # Rename the keys
    # When the keys are extracted from the page they're formatted like this:
    # [Course Name]. -[Course Code] - [Section]
    # Change the formatting to:
    # [Course Code] - [Section] - [Schedule Type]
    for raw_course_title, course_info in course_data_raw.items():
        course_title = re.fullmatch(r'.*\. \- (.*)', raw_course_title).group(1) + " - " + course_info['Schedule Type']
        course_data[course_title] = course_data.pop(raw_course_title)


    return course_data

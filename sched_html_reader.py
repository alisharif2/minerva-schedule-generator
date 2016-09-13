# Written by Ali Murtaza Sharif
# Date: 10-Sept-2016
# Please don't steal

from bs4 import BeautifulSoup as bsoup
from collections import defaultdict
import re

def extract_schedule(raw_html):
    clean_html = bsoup(raw_html, 'html.parser')
    info_table = []
    schedule_table = []
    for table in clean_html.find_all("table", class_="datadisplaytable"):
        if "Scheduled Meeting Times" in table.caption.get_text():
            schedule_table.append(table)
        else:
            info_table.append(table)

    tables = zip(info_table, schedule_table)
    course_data_raw = defaultdict(dict)
    for infobox, meeting_times in tables:
        class_title = infobox.caption.get_text()
        for title_box, value_box in zip(list(meeting_times.find_all('th')), list(meeting_times.find_all('td'))):
            course_data_raw[class_title][title_box.string] = value_box.string

    return format(course_data_raw)

def convert_days(day_string):
    return day_string.replace('M', 'MO,').replace('T', 'TU,').replace('W', 'WE,').replace('R', 'TR,').replace('F', 'FR,')[:-1]

def format(course_data_raw):
    course_data = dict(course_data_raw)
    # Rename the keys
    # When the keys are extracted from the page they're formatted like this:
    # [Course Name]. -[Course Code] - [Section]
    # Change the formatting to:
    # [Course Code] - [Section] - [Schedule Type]
    for raw_course_title, course_info in course_data_raw.items():
        course_title = re.fullmatch(r'.*\. \- (.*)', raw_course_title).group(1) + " - " + course_info['Schedule Type']
        course_data[course_title] = course_data.pop(raw_course_title)

        # Create 2 new entries for the start time and end time
        # This makes it easier to convert them to datetime objects
        time_range = course_info['Time'].replace(' ', '').split('-')
        start_end = course_info['Date Range'].split('-')
        course_data[course_title]['dtstart'] = start_end[0] + time_range[0]
        course_data[course_title]['dtend'] = start_end[0] + time_range[1]
        course_data[course_title]['last day'] = start_end[1]

    return course_data

#!/usr/bin/python3

# Written by Ali Murtaza Sharif
# Date: 10-Sept-2016
# Please don't steal

from bs4 import BeautifulSoup as bsoup
from collections import defaultdict

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

    return course_data_raw

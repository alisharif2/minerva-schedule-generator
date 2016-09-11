from icalendar import Calendar, Event
from datetime import *
from dateutil.relativedelta import *

class course_calendar(Calendar):
    pass

class course(Event):
    @classmethod
    def create(cls, summary, location, start_time, end_time, days, last_day):
        new_course = cls()
        # Create new VEVENT entry
        new_course.add('summary', summary)
        new_course.add('dtstart', start_time)
        new_course.add('dtend', end_time)
        new_course.add('location', location)
        new_course['RRULE'] = "FREQ=WEEKLY;UNTIL={};BYDAY={}".format(ical_dt_format(last_day), ''.join(days))

        return new_course

# Returns the last weekday before a certain day
# For example 2nd Dec, 2016 is the last friday before 5th Dec, 2016
def last_day_before(day, end_date):
    return end_date + relativedelta(weeks=-1, weekday=day)

def ical_dt_format(dt):
    return dt.strftime("%Y%m%dT%H%M%S")


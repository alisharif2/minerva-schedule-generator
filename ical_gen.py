from icalendar import Calendar, Event
from datetime import *
from dateutil.relativedelta import *

class Course_calendar(Calendar):
    @classmethod
    def create(cls, course_data):
        cal = cls()
        cal.add('prodid', '-//Ali Sharif//Minerva Schedule Generator//EN')
        cal.add('version', '2.0')

        # The dates are stored like this
        # Sep 02, 2016 9:35AM
        date_format = "%b %d, %Y %I:%M%p"

        for course_name, course_info in course_data.items():
            # Read and convert the course times into datetime objects
            dtstart = datetime.strptime(course_info['dtstart'], date_format)
            dtend = datetime.strptime(course_info['dtend'], date_format)
            # last_day also has the same date format but lacks the time part so we just use the first part of the string and insert a space at the beginning of the format string
            last_day = datetime.strptime(course_info['last day'], " %b %d, %Y")

            cal.add_component(Course.create(course_name, course_info['Where'], dtstart, dtend, course_info['Days'], last_day))

        return cal

# Use the iCalendar notation for weekdays
# TODO figure out a better way to do this
def ical_weekdays(days):
    ical_days = []
    if 'M' in days: ical_days.append(MO)
    if 'T' in days: ical_days.append(TU)
    if 'W' in days: ical_days.append(WE)
    if 'R' in days: ical_days.append(TH)
    if 'F' in days: ical_days.append(FR)

    return ical_days

class Course(Event):
    @classmethod
    def create(cls, summary, location, start_time, end_time, days, last_day):
        # Create new VEVENT entry
        new_course = cls()
        new_course.add('summary', summary)
        new_course.add('dtstart', start_time)
        new_course.add('dtend', end_time)
        new_course.add('location', location)
        # Since these are classes we can assume that they occur weekly
        # TODO fix last day - last day isn't calculated properly and instead uses the last day of the semester
        # NOTE the above fix might not be necessary
        new_course.add('rrule', { 'FREQ' : 'WEEKLY', 'UNTIL' : last_day, 'BYDAY' : ical_weekdays(days) })

        return new_course

# Returns the last weekday before a certain day
# For example 2nd Dec, 2016 is the last friday before 5th Dec, 2016
# Function currently isn't being used
def last_day_before(day, end_date):
    return end_date + relativedelta(weeks=-1, weekday=day)


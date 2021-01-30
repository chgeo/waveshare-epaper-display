from datetime import datetime, date
from time import time
from tzlocal import get_localzone
import locale
import os.path
import os
import sys
import codecs
import caldav
import vobject

locale.setlocale(locale.LC_TIME, os.getenv('LC_TIME',''))

# convert dates w/o time to datetimes in local timezone
def normalizeDatetime(d):
    # print (d, type(d).__name__)
    if (type(d).__name__ == 'date'):
        d = datetime.combine(d, datetime.min.time())
    if (d.tzinfo is None or d.tzinfo.utcoffset(d) is None):
        d = get_localzone().localize(d)
    # print (d, type(d).__name__)
    return d

user = os.getenv('APPLE_CAL_USER', '')
passwd = os.getenv('APPLE_CAL_PASSWORD', '')
if user == '' or passwd == '' :
    print('APPLE_CAL_USER or APPLE_CAL_PASSWORD is missing')
    sys.exit(1)

template = 'screen-output-weather.svg'
resultCal = None
stale = True

if (os.path.isfile(os.getcwd() + '/calendar.cal')):
    print('Found cached calendar response')
    with open('calendar.cal', 'r') as cal:
        resultCal = vobject.readOne(cal)
    stale=time() - os.path.getmtime(os.getcwd() + '/calendar.cal') > (1*60*60)

if stale:
    print('Calender data is stale, calling the Calendar API')
    client = caldav.DAVClient('https://caldav.icloud.com/', username=user, password=passwd)
    principal = client.principal()
    resultCal = vobject.iCalendar()
    for calendar in principal.calendars():
        events = calendar.date_search(
            start=datetime.utcnow(), #datetime(2015, 1, 1)
            end=datetime(2024, 1, 1), expand=False)
        for event in events:
            vevent = event.vobject_instance.vevent
            resultCal.add(vevent)
        with open('calendar.cal', 'w') as cal:
            print(resultCal.serialize(), file=cal)

if not resultCal:
    print('No upcoming events found.')

events = []
for event in resultCal.components():
    if (event.name == 'VEVENT'):
        # normalize dates, otherwise we can't compare them below
        event.dtstart.value = normalizeDatetime(event.dtstart.value)
        events.append(event)

events.sort(key=lambda k: k.dtstart.value)

output = codecs.open(template , 'r', encoding='utf-8').read()
i = 0
while (i < 3):
    day=desc=''
    if (i < len(events)):
        start = events[i].dtstart.value.astimezone(get_localzone())
        end = events[i].dtend.value
        if (type(end).__name__ == 'datetime'):
            day = start.strftime('%a %-d.%-m. %H:%M')
        else: # no end time (whole day event)
            day = start.strftime('%a %-d.%-m.')
        desc = events[i].summary.value
        print(day, desc, start)
    output = output.replace('CAL_'+str(i),day)
    output = output.replace('CAL_DESC_'+str(i),desc)
    i = i + 1

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)

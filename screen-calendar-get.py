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

# normalize dates, otherwise we can't compare them
def byStartDate(event):
    d = dn = event.dtstart.value
    if (type(dn).__name__ == 'date'):
        dn = datetime.combine(dn, datetime.min.time())
    if (dn.tzinfo is None or dn.tzinfo.utcoffset(dn) is None):
        dn = get_localzone().localize(dn)
    # print (d, '-->', dn)
    return dn

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
        events.append(event)

events.sort(key=byStartDate)

output = codecs.open(template , 'r', encoding='utf-8').read()
i = 0
while (i < 3): # we have 3 slots in the UI
    day=desc=''
    if (i < len(events)):
        desc = events[i].summary.value
        start = events[i].dtstart.value
        end = events[i].dtend.value
        if (type(start).__name__ == 'date' and type(end).__name__ == 'date'):  # date (whole day event)
            day = start.strftime('%a %-d.%-m.')
            if (abs(start - end).days > 1): # show end date for multi-day events
                day = day + end.strftime(' – %a %-d.%-m.')
        else: # event within a day
            start = start.astimezone(get_localzone())
            day = start.strftime('%a %-d.%-m. %H:%M')
        print(day, desc, start)
    output = output.replace('CAL_'+str(i),day)
    output = output.replace('CAL_DESC_'+str(i),desc)
    i = i + 1

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)

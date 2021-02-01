#!/usr/bin/python

import json
import requests
from xml.dom import minidom
from datetime import datetime, date
import locale
import codecs
import os.path
import time
import sys
import os
import html
import pytz
from astral import LocationInfo
from astral.sun import sun


climacell_apikey=os.getenv("CLIMACELL_APIKEY","")

if climacell_apikey=="":
    print("CLIMACELL_APIKEY is missing")
    sys.exit(1)

town_lat=49.341841200000005
town_long=8.6640058
locale.setlocale(locale.LC_TIME, os.getenv("LC_TIME",""))

template = 'screen-template.svg'


#Map Climacell icons to local icons
#Reference: https://openweathermap.org/weather-conditions#Icon-list


icon_dict={
    '01d': 'clear_sky_day',
    '02d': 'few_clouds',
    '03d':'mostly_cloudy',
    '04d': 'scattered_clouds_fog',
    '09d': 'rain_day',
    '10d': 'rain_day',
    '11d': 'thundershower_rain',
    '13d': 'snow',
    '50d': 'foggy',
    '01n': 'clearnight',
    '02n': 'partlycloudynight',
    '03n': 'partlycloudynight',
    '04n': 'partlycloudynight',
    '09n': 'rain_night',
    '10n': 'rain_night',
    '11n': 'thundershower_rain',
    '13n': 'snow',
    '50n': 'foggy'
}



weather_json=''
stale=True

if(os.path.isfile(os.getcwd() + "/apiresponse.json")):
    #Read the contents anyway
    with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
        weather_json = content_file.read()
    stale=time.time() - os.path.getmtime(os.getcwd() + "/apiresponse.json") > (1*60*60)

#If old file or file doesn't exist, time to download it
if(stale):
    try:
        print("Old file, attempting re-download")
        url = "https://api.openweathermap.org/data/2.5/onecall"
        resp = requests.get(url, params={"lat":town_lat,"lon":town_long,"units":"metric","appid":climacell_apikey})
        weather_json = resp.text
        with open(os.getcwd() + "/apiresponse.json", "w") as text_file:
            text_file.write(weather_json)
    except:
        print("Failed to get new API response, will use older response")
        with open(os.getcwd() + "/apiresponse.json", 'r') as content_file:
            weather_json = content_file.read()

weather_data = json.loads(weather_json)
current = weather_data['current']
daily1 = weather_data['daily'][0]
daily2 = weather_data['daily'][1]

temp1 = round(current['temp'])
icon1 = current['weather'][0]['icon']
high1 = round(daily1['temp']['max'])
low1 = round(daily1['temp']['min'])
day1 = datetime.fromtimestamp(current['dt']).strftime('%a %-d.%-m.')
print(day1, temp1, high1, low1)

temp2 = round(daily2['temp']['day'])
icon2 = daily2['weather'][0]['icon']
high2 = round(daily2['temp']['max'])
low2 = round(daily2['temp']['min'])
day2 = datetime.fromtimestamp(daily2['dt']).strftime('%a %-d.%-m.')
print(day2, temp2, high2, low2)

latest_alert=""
if 'alerts' in weather_data:
    msg = weather_data['alerts'][0]['event']
    latest_alert = html.escape(msg.capitalize())
    print(latest_alert)


# Process the SVG
output = codecs.open(template , 'r', encoding='utf-8').read()

output = output.replace('NOW',datetime.now().strftime("%H:%M"))
output = output.replace('ALERT_MESSAGE', latest_alert)

output = output.replace('TEMP_1',str(temp1)+"°")
output = output.replace('#ICON_1','#'+icon_dict[icon1])
output = output.replace('HIGH_LOW_1',str(high1)+"° / "+str(low1)+"°")
output = output.replace('DAY_1',day1)

output = output.replace('TEMP_2',str(temp2)+"°")
output = output.replace('#ICON_2','#'+icon_dict[icon2])
output = output.replace('HIGH_LOW_2',str(high2)+"° / "+str(low2)+"°")
output = output.replace('DAY_2',day2)

codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)

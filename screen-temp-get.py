import asyncio
import platform
from bleak import BleakClient
import os
import sys
from time import time
import configparser
import codecs

addr = (
    '10:08:2C:21:DC:9E'
    if platform.system() != 'Darwin'
    else
    'CB8A04B0-864F-443D-85DE-D5158E9F9DC4'
)

def float_value(nums):
    # check if temp is negative
    num = (nums[1]<<8)|nums[0]
    if nums[1] == 0xff:
        num = -( (num ^ 0xffff ) + 1)
    return float(num)

temp = 0
humidity = 0

async def fetch_data(addr: str):
    async with BleakClient(addr) as client:
        await client.is_connected()
        temp = await client.read_gatt_char('0000fff2-0000-1000-8000-00805f9b34fb')
        temp = int(float_value(temp[0:2]) / 100)
        humidity = await client.read_gatt_char('0000fff5-0000-1000-8000-00805f9b34fb')
        humidity = int(float_value(humidity[0:2]) / 10)
        with open('sensor.ini', 'w') as configfile:
            config = configparser.ConfigParser()
            config['Sensor'] = { 'temperature': temp, 'humidity' : humidity }
            config.write(configfile)

stale = True

if (os.path.isfile(os.getcwd() + '/sensor.ini')):
    print('Found cached sensor data')
    stale=time() - os.path.getmtime(os.getcwd() + '/sensor.ini') > (1*60*60)
    config = configparser.ConfigParser()
    config.read('sensor.ini')
    temp = config['Sensor']['temperature']
    humidity = config['Sensor']['humidity']

if stale:
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch_data(addr))
    except:
        print('Failed to get new sensor data, will use older data')
        config = configparser.ConfigParser()
        config.read('sensor.ini')
        temp = config['Sensor']['temperature']
        humidity = config['Sensor']['humidity']

print('{0} °'.format(temp))
print('Humidity: {0} %'.format(humidity))

template = 'screen-output-weather.svg'
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('TEMP_INS', str(temp)+"°")
output = output.replace('HUMIDITY', str(humidity)+"%")
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)

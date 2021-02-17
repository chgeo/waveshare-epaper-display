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
data_uuid = '0000{0:x}-0000-1000-8000-00805f9b34fb'.format(0xfff2)
sensor_filepath = os.getcwd() + '/sensor.ini'

def float_value(nums):
    # check if temp is negative
    num = (nums[1]<<8)|nums[0]
    if nums[1] == 0xff:
        num = -( (num ^ 0xffff ) + 1)
    return float(num) / 100

temp = 0
humidity = 0

async def fetch_data(addr: str):
    async with BleakClient(addr) as client:
        global temp, humidity
        await client.is_connected()
        data = await client.read_gatt_char(data_uuid)
        temp = round(float_value(data[0:2]))
        humidity = round(float_value(data[2:4]))
        with open(sensor_filepath, 'w') as configfile:
            config = configparser.ConfigParser()
            config['Sensor'] = { 'temperature': temp, 'humidity' : humidity }
            config.write(configfile)

stale = True

if (os.path.isfile(sensor_filepath)):
    print('Found cached sensor data')
    stale=time() - os.path.getmtime(sensor_filepath) > (15*60)
    config = configparser.ConfigParser()
    config.read(sensor_filepath)
    temp = config['Sensor']['temperature']
    humidity = config['Sensor']['humidity']

if stale:
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(fetch_data(addr))
    except:
        print('Failed to get new sensor data, will use older data')
        if (os.path.isfile(sensor_filepath)):
            config = configparser.ConfigParser()
            config.read(sensor_filepath)
            temp = config['Sensor']['temperature']
            humidity = config['Sensor']['humidity']

print('{0} °'.format(temp))
print('Humidity: {0} %'.format(humidity))

template = 'screen-output-weather.svg'
output = codecs.open(template , 'r', encoding='utf-8').read()
output = output.replace('TEMP_INS', str(temp)+"°")
output = output.replace('HUMIDITY', str(humidity)+"%")
codecs.open('screen-output-weather.svg', 'w', encoding='utf-8').write(output)

import asyncio
import platform
from bleak import BleakClient, BleakScanner
from bleak.uuids import uuid16_dict

uuid16_dict = {v: k for k, v in uuid16_dict.items()}

mac_addr = (
    '24:71:89:cc:09:05'
    if platform.system() != 'Darwin'
    else 
    '953FBFB2-8B50-4BDD-96DF-9BB7F995551A'
)
CURRENT_TIME = '0000{0:x}-0000-1000-8000-00805f9b34fb'.format(
    uuid16_dict.get('Current Time')
)
BATTERY_LEVEL_UUID = '0000{0:x}-0000-1000-8000-00805f9b34fb'.format(
    uuid16_dict.get('Battery Level')
)
MODEL_NBR_UUID = '0000{0:x}-0000-1000-8000-00805f9b34fb'.format(
    uuid16_dict.get('Model Number String')
)

async def print_services(mac_addr: str):
    device = await BleakScanner.find_device_by_address(mac_addr)
    async with BleakClient(device) as client:
        # svcs = await client.get_services()
        # for srv in svcs:
        #   for char in srv.characteristics:
        #     print(char)
        
        model_number = await client.read_gatt_char(MODEL_NBR_UUID)
        print('Model Number: {0}'.format(''.join(map(chr, model_number))))
        battery_level = await client.read_gatt_char(BATTERY_LEVEL_UUID)
        print('Battery Level: {0}%'.format(int(battery_level[0])))
        current_time = await client.read_gatt_char(CURRENT_TIME)
        print('Current Time: {0}'.format(int(current_time[0])))


loop = asyncio.get_event_loop()
loop.run_until_complete(print_services(mac_addr))

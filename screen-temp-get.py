import asyncio
from bleak import BleakScanner

async def run():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d, d.metadata)

loop = asyncio.get_event_loop()
loop.run_until_complete(run())
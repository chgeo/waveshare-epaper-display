"""
Service Explorer
----------------

An example showing how to access and print out the services, characteristics and
descriptors of a connected GATT server.

Created on 2019-03-25 by hbldh <henrik.blidh@nedomkull.com>

"""
import platform
import asyncio
import logging

from bleak import BleakClient, BleakScanner

async def discover():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)


async def run(address, debug=False):
    log = logging.getLogger(__name__)
    if debug:
        import sys

        log.setLevel(logging.DEBUG)
        h = logging.StreamHandler(sys.stdout)
        h.setLevel(logging.DEBUG)
        log.addHandler(h)

    async with BleakClient(address) as client:
        x = await client.is_connected()
        log.info("Connected: {0}".format(x))

        for service in client.services:
            log.info("[Service] {0}: {1}".format(service.uuid, service.description))
            for char in service.characteristics:
                if "read" in char.properties:
                    try:
                        value = bytes(await client.read_gatt_char(char.uuid))
                    except Exception as e:
                        value = str(e).encode()
                else:
                    value = None
                log.info(
                    "\t[Characteristic] {0}: (Handle: {1}) ({2}) | Name: {3}, Value: {4} ".format(
                        char.uuid,
                        char.handle,
                        ",".join(char.properties),
                        char.description,
                        value,
                    )
                )
                for descriptor in char.descriptors:
                    value = await client.read_gatt_descriptor(descriptor.handle)
                    log.info(
                        "\t\t[Descriptor] {0}: (Handle: {1}) | Value: {2} ".format(
                            descriptor.uuid, descriptor.handle, bytes(value)
                        )
                    )


if __name__ == "__main__":
    address = (
        "7C:73:EB:92:89:B9"
        if platform.system() != "Darwin"
        # else "832FA3ED-72A7-4DF3-A9FD-CF9FFAE4570A"
        else "CB8A04B0-864F-443D-85DE-D5158E9F9DC4"
    )
    loop = asyncio.get_event_loop()
    # loop.set_debug(True)
    loop.run_until_complete(discover())
    loop.run_until_complete(run(address, True))

# 953FBFB2-8B50-4BDD-96DF-9BB7F995551A: iPhone
# 1717D1A8-0A55-42FB-B118-49CE5D005C69: 846B21DE648130AFE9
# 832FA3ED-72A7-4DF3-A9FD-CF9FFAE4570A: 846B21CFB43830A8E9
# BF9393C9-8D24-4D07-AB6D-B53C5A507A19: Apple Watch von Christian
# F3040964-1EFD-4654-A3C8-D9F8F66C6563: Unknown
# 0EE45599-D4D2-40D0-B150-C53EE2B8D899: 846B21CED94230A8E9
# 9D72E78C-8AFA-4BFC-9310-4D6EB8F483E9: Apple, Inc. (b'\x10\x05\x00\x14LG\xc6')
# 53D26618-B5DB-4807-9C33-23DFF44E27E6: Apple, Inc. (b"\t\x06\x03\xd9\xc0\xa8\xb2'")

# [Service] 0000180a-0000-1000-8000-00805f9b34fb: Device Information
#         [Characteristic] 00002a23-0000-1000-8000-00805f9b34fb: (Handle: 17) (read) | Name: System ID, Value: b'\x9e\xdc!\x00\x00,\x08\x10' 
#         [Characteristic] 00002a24-0000-1000-8000-00805f9b34fb: (Handle: 19) (read) | Name: Model Number String, Value: b'Model Number' 
#         [Characteristic] 00002a25-0000-1000-8000-00805f9b34fb: (Handle: 21) (read) | Name: Serial Number String, Value: b'Serial Number' 
#         [Characteristic] 00002a26-0000-1000-8000-00805f9b34fb: (Handle: 23) (read) | Name: Firmware Revision String, Value: b'Firmware Revision' 
#         [Characteristic] 00002a27-0000-1000-8000-00805f9b34fb: (Handle: 25) (read) | Name: Hardware Revision String, Value: b'Hardware Revision' 
#         [Characteristic] 00002a28-0000-1000-8000-00805f9b34fb: (Handle: 27) (read) | Name: Software Revision String, Value: b'1-1' 
#         [Characteristic] 00002a29-0000-1000-8000-00805f9b34fb: (Handle: 29) (read) | Name: Manufacturer Name String, Value: b'INKBIRD' 
#         [Characteristic] 00002a2a-0000-1000-8000-00805f9b34fb: (Handle: 31) (read) | Name: IEEE 11073-20601 Regulatory Cert. Data List, Value: b'\xfe\x00experimental' 
#         [Characteristic] 00002a50-0000-1000-8000-00805f9b34fb: (Handle: 33) (read) | Name: PnP ID, Value: b'\x01\r\x00\x00\x00\x10\x01' 
# [Service] 0000fff0-0000-1000-8000-00805f9b34fb: Vendor specific
#         [Characteristic] 0000fff1-0000-1000-8000-00805f9b34fb: (Handle: 36) (read,write) | Name: Vendor specific, Value: b'\x00\x00\x00\x00\x00\x00\x00<\x00\x00\x001-7ZK\x00\x00\x00\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 38) | Value: b'cfg data' 
#         [Characteristic] 0000fff2-0000-1000-8000-00805f9b34fb: (Handle: 39) (read) | Name: Vendor specific, Value: b'\xd6\tW\r\x00\xdb\x0e' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 41) | Value: b'Real time data' 
#         [Characteristic] 0000fff3-0000-1000-8000-00805f9b34fb: (Handle: 42) (read,write) | Name: Vendor specific, Value: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 44) | Value: b'cfg data2' 
#         [Characteristic] 0000fff4-0000-1000-8000-00805f9b34fb: (Handle: 45) (read) | Name: Vendor specific, Value: b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 47) | Value: b'measure' 
#         [Characteristic] 0000fff5-0000-1000-8000-00805f9b34fb: (Handle: 48) (read) | Name: Vendor specific, Value: b'\x0c\x00\x00\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 50) | Value: b'recoder frame' 
#         [Characteristic] 0000fff6-0000-1000-8000-00805f9b34fb: (Handle: 51) (notify) | Name: Vendor specific, Value: None 
#                 [Descriptor] 00002902-0000-1000-8000-00805f9b34fb: (Handle: 53) | Value: b'\x00\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 54) | Value: b'history data' 
#         [Characteristic] 0000fff7-0000-1000-8000-00805f9b34fb: (Handle: 55) (read,write) | Name: Vendor specific, Value: b'\x01~\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 57) | Value: b'run/stop recoder' 
#         [Characteristic] 0000fff8-0000-1000-8000-00805f9b34fb: (Handle: 58) (read,write) | Name: Vendor specific, Value: b'\x00' 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 60) | Value: b'his data type' 
#         [Characteristic] 0000fff9-0000-1000-8000-00805f9b34fb: (Handle: 61) (write) | Name: Vendor specific, Value: None 
#                 [Descriptor] 00002901-0000-1000-8000-00805f9b34fb: (Handle: 63) | Value: b'reset'
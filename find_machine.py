# -*- coding: utf-8 -*-
"""
Created on Wed Apr 26 16:01:23 2023

@author: HM
"""
import nest_asyncio
nest_asyncio.apply()
import asyncio
from bleak import BleakScanner
from bleak import BleakClient
from bleak.exc import BleakError
import platform
import sys

async def search():
    devices = await BleakScanner.discover()
    for d in devices:
        print(d)



# address = "24:71:89:cc:09:05"
# MODEL_NBR_UUID = "00002a24-0000-1000-8000-00805f9b34fb"


async def main(ble_address: str):
    device = await BleakScanner.find_device_by_address(ble_address, timeout=20.0)
    if not device:
        raise BleakError(f"A device with address {ble_address} could not be found.")
    async with BleakClient(device) as client:
        svcs = await client.get_services()
        print("Services:")
        for service in svcs:
            print(service)


asyncio.run(search()) 
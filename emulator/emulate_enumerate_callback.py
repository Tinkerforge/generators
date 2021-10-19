#!/usr/bin/env python3

# Copyright (C) 2021 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

import sys

if sys.hexversion < 0x3070000:
    raise Exception('Python >= 3.7 required')

import asyncio
import logging

from brick_daemon import BrickDaemon, set_global_debug
from ambient_light_v3_bricklet_skeleton import AmbientLightV3BrickletSkeleton

DEBUG = False

class AmbientLightV3Bricklet(AmbientLightV3BrickletSkeleton):
    pass

async def main():
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        set_global_debug(True)

    async with BrickDaemon('0.0.0.0', 5555) as brickd:
        await asyncio.sleep(1)

        print('Adding AmbientLightV3Bricklet')
        device = AmbientLightV3Bricklet('EALV3')
        await brickd.add_device(device)
        print('Added AmbientLightV3Bricklet')

        await asyncio.sleep(1)

        print('Removing AmbientLightV3Bricklet')
        await brickd.remove_device(device)
        print('Removed AmbientLightV3Bricklet')

        await asyncio.sleep(1)

        print('Done')

if __name__ == '__main__':
    asyncio.run(main(), debug=DEBUG)

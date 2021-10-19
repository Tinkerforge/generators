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

from brick_daemon import BrickDaemon, autorun, set_global_debug
from ambient_light_v3_bricklet_skeleton import AmbientLightV3BrickletSkeleton

DEBUG = False

class AmbientLightV3Bricklet(AmbientLightV3BrickletSkeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._illuminance = 10
        self._illuminance_range = 3
        self._integration_time = 2

    @autorun
    async def emulate(self):
        while True:
            await asyncio.sleep(0.1)

            self._illuminance += 10

            if self._illuminance > 1000:
                self._illuminance = 10

    async def get_illuminance(self):
        return self._illuminance

    async def set_configuration(self, illuminance_range, integration_time):
        self._illuminance_range = illuminance_range
        self._integration_time = integration_time

    async def get_configuration(self):
        return self._illuminance_range, self._integration_time

async def main():
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        set_global_debug(True)

    async with BrickDaemon('0.0.0.0', 5555) as brickd:
        await brickd.add_device(AmbientLightV3Bricklet('EALV3'))
        await brickd.run_forever()

if __name__ == '__main__':
    asyncio.run(main(), debug=DEBUG)

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
from common_test_bricklet_skeleton import CommonTestBrickletSkeleton

DEBUG = False

class CommonTestBricklet(CommonTestBrickletSkeleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._int8_value = 0

    async def set_int8_value(self, value):
        print('Int8 Value:', value)

        self._int8_value = value

    async def get_int8_value(self):
        return self._int8_value

async def main():
    if DEBUG:
        logging.basicConfig(level=logging.DEBUG)
        set_global_debug(True)

    async with BrickDaemon('0.0.0.0', 5555) as brickd:
        await brickd.add_device(CommonTestBricklet('CTV1'))
        await brickd.run_forever()

if __name__ == '__main__':
    asyncio.run(main(), debug=DEBUG)

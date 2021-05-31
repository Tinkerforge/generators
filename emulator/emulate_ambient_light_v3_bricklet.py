#!/usr/bin/env python3

import asyncio
import logging

from brick_daemon import BrickDaemon, autorun, function, set_global_debug
from ambient_light_v3_bricklet_skeleton import AmbientLightV3BrickletSkeleton

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
    logging.basicConfig(level=logging.DEBUG)
    set_global_debug(True)

    async with BrickDaemon('0.0.0.0', 5555) as brickd:
        await brickd.add_device(AmbientLightV3Bricklet('EALV3'))
        await brickd.run_forever()

asyncio.run(main(), debug=True)

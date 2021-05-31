# -*- coding: utf-8 -*-
# Copyright (C) 2021 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

import sys

if sys.hexversion < 0x3070000:
    raise Exception('Python >= 3.7 required')

from brick_daemon import Device, NoSupport, EnumerateFeature, CoMCUBrickletFeature, function

class AmbientLightV3BrickletSkeleton(Device, EnumerateFeature, CoMCUBrickletFeature):
    def __init__(self, uid, connected_uid='0', position='?', hardware_version=(1, 0, 0), firmware_version=(2, 0, 0), debug=None, passthrough_host=None, passthrough_port=None):
        super().__init__(uid, debug=debug, passthrough_host=passthrough_host, passthrough_port=passthrough_port)

        self.configure_enumerate_feature(connected_uid, position, hardware_version, firmware_version, 2131)

    @function(1, [], ['I'])
    async def get_illuminance(self):
        raise NoSupport

    @function(5, ['B', 'B'], [])
    async def set_configuration(self, illuminance_range, integration_time):
        raise NoSupport

    @function(6, [], ['B', 'B'])
    async def get_configuration(self):
        raise NoSupport

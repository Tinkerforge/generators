# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# GPS Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 278,
    'name': 'Thermal Imaging',
    'display_name': 'Thermal Imaging',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '60x80 pixel thermal imaging camera',
        'de': '60x80 Pixel Wärmebildkamera'
    },
    'comcu': True,
    'released': False,
    'documented': False,
    'packets': [],
    'examples': []
}

com['packets'].append({
'type': 'function',
'name': 'Get High Contrast Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint8', 62, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current high contrast image. See TODO for the difference between 
High Contrast and Temperature Image. If you don't know what to use
the High Contrast Image is probably right for you.

The data is organized as a 8-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 8-bit value represents one grey-scale image bit that can directly be
shown to a user on a display.

Before you can use this function you have to enable it with
:func:`Set Image Transfer Config`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint16', 31, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current temperature image. See TODO for the difference between 
High Contrast and Temperature Image. If you don't know what to use
the High Contrast Image is probably right for you.

The data is organized as a 16-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 16-bit value represents one temperature measurement in either
Kelvin/10 or Kelvin/100 (depending on the resolution set with:func:`Set Resolution`).

Before you can use this function you have to enable it with
:func:`Set Image Transfer Config`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Statistics',
'elements': [('Spotmeter Statistics', 'uint16', 4, 'out'), # mean, max, min, pixel count
             ('Temperatures', 'uint16', 4, 'out'), # focal plain array, focal plain array at last ffc, housing, housing at last ffc
             ('Resolution', 'uint8', 1, 'out', ('Resolution', [('0 To 6553 Kelvin', 0),
                                                               ('0 To 655 Kelvin', 1)])),
             ('Status', 'uint16', 1, 'out') # Lots of status bits # FIXME: convert to bools or add constants
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the spotmeter statistics, various temperatures, current resolution and status bits.

The spotmeter statistics are:

* Index 0: Mean Temperature.
* Index 1: Maximum Temperature.
* Index 2: Minimum Temperature.
* Index 3: Pixel Count of spotmeter region of interest.

The temperatures are:

* Index 0: Focal Plain Array temperature.
* Index 1: Focal Plain Array temperature at last FFC (Flat Field Correction).
* Index 2: Housing temperature.
* Index 3: Housing temperature at last FFC.

The resolution is either `0 to 6553 Kelvin` or `0 to 655 Kelvin`. If the resolution is the former,
the temperatures are in Kelvin/10, if it is the latter the temperatures are in Kelvin/100.

The status bits are (TODO: Use bool array?):
* bit 0: FFC desired
* bit 1-2: FFC never commanded, FFC imminent, FFC in progress, FFC complete
* bit 3: AGC State
* bit 4: Shutter lockout
* bit 5: Overtemp shut down imminent
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Resolution',
'elements': [('Resolution', 'uint8', 1, 'in', ('Resolution', [('0 To 6553 Kelvin', 0),
                                                              ('0 To 655 Kelvin', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the resolution. The Thermal Imaging Bricklet can either measure 

* from 0 to 6553 Kelvin (-273.15° to 6279.85°C) with 0.1°C resolution or
* from 0 to 655 Kelvin (-273.15° to 381.85°C) with 0.01°C resolution.

The default value is 0 to 655 Kelvin.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resolution',
'elements': [('Resolution', 'uint8', 1, 'out', ('Resolution', [('0 To 6553 Kelvin', 0),
                                                               ('0 To 655 Kelvin', 1)]))],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the resolution as set by :func:`Set Resolution`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Spotmeter Config',
'elements': [('Region Of Interest', 'uint8', 4, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the spotmeter region of interest. The 4 values are

* Index 0: Column start (has to be smaller then Colummn end).
* Index 1: Row start (has to be smaller then Row end).
* Index 2: Colum end (has to be smaller then 80).
* Index 3: Row end (has to be smaller then 60).

The spotmeter statistics can be read out with :func:`Get Statistics`.

The default region of interest is (39, 29, 40, 30).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Spotmeter Config',
'elements': [('Region Of Interest', 'uint8', 4, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the spotmeter config as set by :func:`Set Spotmeter Config`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set High Contrast Config',
'elements': [('Region Of Interest', 'uint8', 4, 'in'),
             ('Dampening Factor', 'uint16', 1, 'in'),
             ('Clip Limit', 'uint16', 2, 'in'),
             ('Empty Counts', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""

Sets the high contrast region of interest, dampening factor, clip limit and empty counts.
This config is only used in high contrast mode (see :func:`Set Image Transfer Config`).

The high contrast region of interest consists of four values:

* Index 0: Column start (has to be smaller or equal then Colummn end).
* Index 1: Row start (has to be smaller then Row end).
* Index 2: Colum end (has to be smaller then 80).
* Index 3: Row end (has to be smaller then 60).

The algorithm to generate the high contrast image is applied to this region.

Dampening Factor: This parameter is the amount of temporal dampening applied to the HEQ 
(history equalization) transformation function. An IIR filter of the form 
(N/256) * previous + ((256-N)/256) * current is applied, and the HEQ dampening factor 
represents the value N in the equation, i.e., a value that applies to the amount of
influence the previous HEQ transformation function has on the current function. The 
lower the value of N the higher the influence of the current video frame whereas
the higher the value of N the more influence the previous damped transfer function has.

Clip Limit Index 0: This parameter defines an artificial population that is added to 
every non-empty histogram bin. In other words, if the Clip Limit Low is set to L, a bin 
with an actual population of X will have an effective population of L + X. y empty bin 
that is nearby a populated bin will be given an artificial population of L. The effect of
higher values is to provide a more linear transfer function; lower values provide a more
non-linear (equalized) transfer function.

Clip Limit Index 1: This parameter defines the maximum number of pixels allowed 
to accumulate in any given histogram bin. Any additional pixels in a given bin are clipped.
The effect of this parameter is to limit the influence of highly-populated bins on the 
resulting HEQ transformation function.

Empty Counts: This parameter specifies the maximum number of pixels in a bin that will be 
interpreted as an empty bin. Histogram bins with this number of pixels or less will be 
processed as an empty bin.

The default values are

* Region Of Interest = (0, 0, 79, 59),
* Dampening Factor = 64,
* Clip Limit = (4800, 512) and
* Empty Counts = 2.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get High Contrast Config',
'elements': [('Region Of Interest', 'uint8', 4, 'out'),
             ('Dampening Factor', 'uint16', 1, 'out'),
             ('Clip Limit', 'uint16', 2, 'out'),
             ('Empty Counts', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the high contrast config as set by :func:`Set High Contrast Config`.
""",
'de':
"""
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set Image Transfer Config',
'elements': [('Config', 'uint8', 1, 'in', ('Image Transfer', [('Manual High Contrast Image', 0),
                                                              ('Manual Temperature Image', 1),
                                                              ('Callback High Contrast Image', 2),
                                                              ('Callback Temperature Image', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The necessary bandwith of this Bricklet is too high to use getter/callback or
high contrast/temperature image at the same time. You have to configure the one
you want to use, the Bricklet will optimize the internal configuration accordingly.

Corresponding functions:

* Manual High Contrast Image: :func:`Get High Contrast Image`.
* Manual Temperature Image: :func:`Get Temperature Image`.
* Callback High Contrast Image: :cb:`High Contrast Image`.
* Callback Temperature Image: :cb:`Temperature Image`.

The default is Manual High Contrast Image (0).
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Image Transfer Config',
'elements': [('Config', 'uint8', 1, 'out', ('Image Transfer', [('Manual High Contrast Image', 0),
                                                               ('Manual Temperature Image', 1),
                                                               ('Callback High Contrast Image', 2),
                                                               ('Callback Temperature Image', 3)]))],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the image trasfer config, as set by :func:`Set Image Transfer Config`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'High Contrast Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint8', 62, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered with every new high contrast image if the transfer image
config is configered for high contrast callback (see :func:`Set Image Transfer Config`.

The data is organized as a 8-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 8-bit value represents one grey-scale image bit that can directly be
shown to a user on a display.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out'),
             ('Image Chunk Data', 'uint16', 31, 'out')],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered with every new temperature image if the transfer image
config is configered for temperature callback (see :func:`Set Image Transfer Config`.

The data is organized as a 16-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 16-bit value represents one temperature measurement in either
Kelvin/10 or Kelvin/100 (depending on the resolution set with :func:`Set Resolution`).
""",
'de':
"""
"""
}]
})

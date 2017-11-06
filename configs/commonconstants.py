# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

THRESHOLD_OPTION_CONSTANTS = ('Threshold Option', [('Off', 'x'),
                                                   ('Outside', 'o'),
                                                   ('Inside', 'i'),
                                                   ('Smaller', '<'),
                                                   ('Greater', '>')])

def add_callback_value_function(packets, name, data_name, data_type, doc, since_firmware = [1, 0, 0]):
    name_get = name
    name_set = name.replace('Get ', 'Set ')
    name = name.replace('Get ', '')

    getter = {
'type': 'function',
'name': name_get,
'elements': [(data_name, data_type, 1, 'out')],
'since_firmware': since_firmware,
'doc': ['bf', doc]
}

    getter['doc'][1]['en'] += """

If you want to get the value periodically, it is recommended to use the
:cb:`{0}` callback. You can set the callback configuration
with :func:`{1} Callback Configuration`.
""".format(name, name_set)

    callback_config_setter = {
'type': 'function',
'name': (name_set + ' Callback Configuration'),
'corresponding_getter': name_get,
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in'),
             ('Option', 'char', 1, 'in', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'in'),
             ('Max', 'uint16', 1, 'in')],
'since_firmware': since_firmware,
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`{0}` callback is triggered
periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change
within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

It is furthermore possible to constrain the callback with thresholds.

The option-`parameter` together with min/max sets a thresholds for the :cb:`{0}` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Threshold is turned off"
 "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
 "'i'",    "Threshold is triggered when the value is *inside* the min and max values"
 "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
 "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"


If the option is set to 'x' (threshold turned off) the callback is triggered with the period.

The default value is (0, false, 'x', 0, 0).
""".format(name),
'de':
"""
TODO
"""
}]
}

    callback_config_getter = {
'type': 'function',
'name': (name_get + ' Callback Configuration'),
'corresponding_getter': name_get,
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out'),
             ('Option', 'char', 1, 'out', THRESHOLD_OPTION_CONSTANTS),
             ('Min', 'uint16', 1, 'out'),
             ('Max', 'uint16', 1, 'out')],
'since_firmware': since_firmware,
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by :func:`{0} Callback Configuration`.
""".format(name_set),
'de':
"""
Gibt die Callback-Konfiguration zurück, wie von :func:`{0} Callback Configuration` gesetzt.
""".format(name_set)
}]
}

    callback = {
'type': 'callback',
'name': name,
'corresponding_getter': name_get,
'elements': [(data_name, data_type, 1, 'out')],
'since_firmware': since_firmware,
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`{0} Callback Configuration`. 

The `parameter` is the same as :func:`{1}`.
""".format(name_set, name_get),
'de':
"""
TODO
"""
}]
}

    packets.append(getter)
    packets.append(callback_config_setter)
    packets.append(callback_config_getter)
    packets.append(callback)

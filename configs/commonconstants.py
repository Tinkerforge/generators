# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

THRESHOLD_OPTION_CONSTANT_GROUP = {
'name': 'Threshold Option',
'type': 'char',
'constants': [('Off', 'x'),
              ('Outside', 'o'),
              ('Inside', 'i'),
              ('Smaller', '<'),
              ('Greater', '>')]
}

def add_callback_value_function(packets, name, data_name, data_type, doc,
                                channel_count=1, since_firmware=None,
                                getter_since_firmware=None,
                                callback_since_firmware=None,
                                callback_config_getter_since_firmware=None,
                                callback_config_setter_since_firmware=None,
                                scale=None,
                                unit=None,
                                range_=None):
    name_get = name
    name_set = name.replace('Get ', 'Set ')
    name = name.replace('Get ', '')

    if since_firmware == None:
        since_firmware = [1, 0, 0]

    if getter_since_firmware == None:
        getter_since_firmware = since_firmware[:]

    if callback_since_firmware == None:
        callback_since_firmware = since_firmware[:]

    if callback_config_getter_since_firmware == None:
        callback_config_getter_since_firmware = callback_since_firmware[:]

    if callback_config_setter_since_firmware == None:
        callback_config_setter_since_firmware = callback_since_firmware[:]

    getter_element_info = {
        'unit': unit,
        'range': range_
    }

    if scale != None:
        getter_element_info['scale'] = scale

    getter = {
        'type': 'function',
        'name': name_get,
        'elements': [(data_name, data_type, 1, 'out', getter_element_info)],
        'since_firmware': getter_since_firmware,
        'doc': ['bf', doc]
    }

    if channel_count > 1:
        getter['elements'].insert(0, ('Channel', 'uint8', 1, 'in', {'range': (0, channel_count - 1)}))

    getter['doc'][1]['en'] += """

If you want to get the value periodically, it is recommended to use the
:cb:`{0}` callback. You can set the callback configuration
with :func:`{1} Callback Configuration`.
""".format(name, name_set)

    getter['doc'][1]['de'] += """

Wenn der Wert periodisch benötigt wird, kann auch der :cb:`{0}` Callback
verwendet werden. Der Callback wird mit der Funktion
:func:`{1} Callback Configuration` konfiguriert.
""".format(name, name_set)

    callback_config_setter_min_max_element_info = {
        'unit': unit,
        'default': 0
    }

    if scale != None:
        callback_config_setter_min_max_element_info['scale'] = scale

    callback_config_setter = {
        'type': 'function',
        'name': (name_set + ' Callback Configuration'),
        'corresponding_getter': name_get,
        'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
                     ('Value Has To Change', 'bool', 1, 'in', {'default': False}),
                     ('Option', 'char', 1, 'in', {'constant_group': 'Threshold Option', 'default': 'x'}),
                     ('Min', data_type, 1, 'in', callback_config_setter_min_max_element_info),
                     ('Max', data_type, 1, 'in', callback_config_setter_min_max_element_info)],
        'since_firmware': callback_config_setter_since_firmware,
        'doc': ['ccf', {
        'en': """
The period is the period with which the :cb:`{0}` callback is triggered
periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change
within the period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

It is furthermore possible to constrain the callback with thresholds.

The `option`-parameter together with min/max sets a threshold for the :cb:`{0}` callback.

The following options are possible:

.. csv-table::
 :header: "Option", "Description"
 :widths: 10, 100

 "'x'",    "Threshold is turned off"
 "'o'",    "Threshold is triggered when the value is *outside* the min and max values"
 "'i'",    "Threshold is triggered when the value is *inside* or equal to the min and max values"
 "'<'",    "Threshold is triggered when the value is smaller than the min value (max is ignored)"
 "'>'",    "Threshold is triggered when the value is greater than the min value (max is ignored)"

If the option is set to 'x' (threshold turned off) the callback is triggered with the fixed period.
""".format(name),
        'de': """
Die Periode ist die Periode mit der der :cb:`{0}` Callback ausgelöst wird. Ein Wert von 0
schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der Callback nur ausgelöst,
wenn der Wert sich im Vergleich zum letzten mal geändert hat. Ändert der Wert sich nicht innerhalb
der Periode, so wird der Callback sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der festen Periode ausgelöst
unabhängig von den Änderungen des Werts.

Desweiteren ist es möglich den Callback mittels Thresholds einzuschränken.

Der `option`-Parameter zusammen mit min/max setzt einen Threshold für den :cb:`{0}` Callback.

Die folgenden Optionen sind möglich:

.. csv-table::
 :header: "Option", "Beschreibung"
 :widths: 10, 100

 "'x'",    "Threshold ist abgeschaltet"
 "'o'",    "Threshold wird ausgelöst, wenn der Wert *außerhalb* der Min und Max Werte sind"
 "'i'",    "Threshold wird ausgelöst, wenn der Wert *innerhalb* der Min und Max Werte sind"
 "'<'",    "Threshold wird ausgelöst, wenn der Wert kleiner ist wie der Min Wert (Max wird ignoriert)"
 "'>'",    "Threshold wird ausgelöst, wenn der Wert größer ist wie der Max Wert (Min wird ignoriert)"

Wird die Option auf 'x' gesetzt (Threshold abgeschaltet), so wird der Callback mit der festen Periode
ausgelöst.
""".format(name)
        }]
    }

    if channel_count > 1:
        callback_config_setter['elements'].insert(0, ('Channel', 'uint8', 1, 'in', {'range': (0, channel_count - 1)}))

    callback_config_getter_min_max_element_info = {
        'unit': unit,
        'default': 0
    }

    if scale != None:
        callback_config_getter_min_max_element_info['scale'] = scale

    callback_config_getter = {
        'type': 'function',
        'name': (name_get + ' Callback Configuration'),
        'corresponding_getter': name_get,
        'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
                     ('Value Has To Change', 'bool', 1, 'out', {'default': False}),
                     ('Option', 'char', 1, 'out', {'constant_group': 'Threshold Option', 'default': 'x'}),
                     ('Min', data_type, 1, 'out', callback_config_getter_min_max_element_info),
                     ('Max', data_type, 1, 'out', callback_config_getter_min_max_element_info)],
        'since_firmware': callback_config_getter_since_firmware,
        'doc': ['ccf', {
        'en': """
Returns the callback configuration as set by :func:`{0} Callback Configuration`.
""".format(name_set),
        'de': """
Gibt die Callback-Konfiguration zurück, wie mittels :func:`{0} Callback Configuration` gesetzt.
""".format(name_set)
        }]
    }

    if channel_count > 1:
        callback_config_getter['elements'].insert(0, ('Channel', 'uint8', 1, 'in', {'range': (0, channel_count - 1)}))

    callback = {
        'type': 'callback',
        'name': name,
        'corresponding_getter': name_get,
        'elements': [(data_name, data_type, 1, 'out', getter_element_info)],
        'since_firmware': callback_since_firmware,
        'doc': ['c', {
        'en': """
This callback is triggered periodically according to the configuration set by
:func:`{0} Callback Configuration`.

The :word:`parameter` is the same as :func:`{1}`.
""".format(name_set, name_get),
        'de': """
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`{0} Callback Configuration` gesetzten Konfiguration

Der :word:`parameter` ist der gleiche wie :func:`{1}`.
""".format(name_set, name_get)
        }]
    }

    if channel_count > 1:
        callback['elements'].insert(0, ('Channel', 'uint8', 1, 'out', {'range': (0, channel_count - 1)}))

    packets.append(getter)
    packets.append(callback_config_setter)
    packets.append(callback_config_getter)
    packets.append(callback)

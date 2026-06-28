# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Energy Monitor Bricklet communication config

from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2169,
    'name': 'WARP Energy Manager',
    'display_name': 'WARP Energy Manager',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Manages heat pumps, WARP Chargers and logs energy and charge data to an SD card',
        'de': 'Steuert Heizungen, WARP Charger und protokolliert Energie- und Ladedaten auf eine SD-Karte'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
    'esp32_firmware': 'energy_manager',
    'features': [
        'device',
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Energy Meter Type',
'type': 'uint8',
'constants': [('Not Available', 0),
              ('SDM72', 1),
              ('SDM630', 2),
              ('SDM72V2', 3),
              ('SDM72CTM', 4),
              ('SDM630MCTV2', 5),
              ('DSZ15DZMOD', 6),
              ('DEM4A', 7),
              ('DMED341MID7ER', 8),
              ('DSZ16DZE', 9),
              ('WM3M4C', 10),
              ('WM3M4', 11)]
})

com['constant_groups'].append({
'name': 'Data Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('SD Error', 1),
              ('LFS Error', 2),
              ('Queue Full', 3),
              ('Date Out Of Range', 4)]
})

com['constant_groups'].append({
'name': 'Format Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Password Error', 1),
              ('Format Error', 2)]
})

com['constant_groups'].append({
'name': 'LED Pattern',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Blinking', 2),
              ('Breathing', 3)]
})

com['constant_groups'].append({
'name': 'Data Storage Status',
'type': 'uint8',
'constants': [('OK', 0),
              ('Not Found', 1),
              ('Busy', 2)]
})

com['packets'].append({
'type': 'function',
'name': 'Set Contactor',
'elements': [('Contactor Value', 'bool', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the contactor. *true* closes the contactor, *false* opens it.
""",
'de':
"""
Setzt den Zustand des Schütz. *true* schließt das Schütz, *false* öffnet es.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Contactor',
'elements': [('Contactor Value', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the contactor as set by :func:`Set Contactor`.
""",
'de':
"""
Gibt den Zustand des Schütz zurück, wie von :func:`Set Contactor` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set RGB Value',
'elements': [('R', 'uint8', 1, 'in', {}),
             ('G', 'uint8', 1, 'in', {}),
             ('B', 'uint8', 1, 'in', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the *r*, *g* and *b* values for the LED.
""",
'de':
"""
Setzt die *r*, *g* und *b* Werte für die LED.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get RGB Value',
'elements': [('R', 'uint8', 1, 'out', {}),
             ('G', 'uint8', 1, 'out', {}),
             ('B', 'uint8', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the *r*, *g* and *b* values of the LED as set by :func:`Set RGB Value`.
""",
'de':
"""
Gibt die *r*, *g* und *b* Werte der LED zurück, wie von :func:`Set RGB Value` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter Values',
'elements': [('Power', 'float', 1, 'out'),
             ('Current', 'float', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the total power (in W) and the current per phase (L1, L2, L3 in A) of
the connected energy meter.
""",
'de':
"""
Gibt die Gesamtleistung (in W) und den Strom pro Phase (L1, L2, L3 in A) des
angeschlossenen Stromzählers zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter Detailed Values Low Level',
'elements': [('Values Length', 'uint16', 1, 'out', {}),
             ('Values Chunk Offset', 'uint16', 1, 'out', {}),
             ('Values Chunk Data', 'float', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Values'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all values measured by the connected energy meter. The meaning of the
values depends on the energy meter type, see :func:`Get Energy Meter State`.
""",
'de':
"""
Gibt alle vom angeschlossenen Stromzähler gemessenen Werte zurück. Die Bedeutung
der Werte hängt vom Typ des Stromzählers ab, siehe :func:`Get Energy Meter State`.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter State',
'elements': [('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'}),
             ('Error Count', 'uint32', 6, 'out')], # local timeout, global timeout, illigal function, illegal data address, illegal data value, slave device failure
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the type of the connected energy meter and the Modbus communication
error counters. The error counters are: local timeout, global timeout,
illegal function, illegal data address, illegal data value and slave device
failure.
""",
'de':
"""
Gibt den Typ des angeschlossenen Stromzählers und die
Modbus-Kommunikationsfehlerzähler zurück. Die Fehlerzähler sind: Local Timeout,
Global Timeout, Illegal Function, Illegal Data Address, Illegal Data Value und
Slave Device Failure.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input',
'elements': [('Input', 'bool', 2, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values of the two inputs.
""",
'de':
"""
Gibt die Werte der beiden Inputs zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Output',
'elements': [('Output', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the state of the (open drain) output.
""",
'de':
"""
Setzt den Zustand des (Open-Drain-)Outputs.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Output',
'elements': [('Output', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the output as set by :func:`Set Output`.
""",
'de':
"""
Gibt den Zustand des Outputs zurück, wie von :func:`Set Output` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Input Voltage',
'elements': [('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the supply voltage of the Energy Manager.
""",
'de':
"""
Gibt die Versorgungsspannung des Energy Managers zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('Contactor Check State', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the contactor check.
""",
'de':
"""
Gibt den Zustand der Schützprüfung (Contactor Check) zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Uptime',
'elements': [('Uptime', 'uint32', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the uptime of the Energy Manager in milliseconds.
""",
'de':
"""
Gibt die Uptime des Energy Managers in Millisekunden zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data 1',
'elements': [('Contactor Value', 'bool', 1, 'out', {}),
             ('R', 'uint8', 1, 'out', {}),
             ('G', 'uint8', 1, 'out', {}),
             ('B', 'uint8', 1, 'out', {}),
             ('Power', 'float', 1, 'out'),
             ('Current', 'float', 3, 'out'),
             ('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'}),
             ('Error Count', 'uint32', 6, 'out'),
             ('Input', 'bool', 2, 'out'),
             ('Output', 'bool', 1, 'out'),
             ('Voltage', 'uint16', 1, 'out', {'scale': (1, 1000), 'unit': 'Volt'}),
             ('Contactor Check State', 'uint8', 1, 'out'),
             ('Uptime', 'uint32', 1, 'out')
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values of :func:`Get Contactor`, :func:`Get RGB Value`,
:func:`Get Energy Meter Values`, :func:`Get Energy Meter State`,
:func:`Get Input`, :func:`Get Output`, :func:`Get Input Voltage`,
:func:`Get State` and :func:`Get Uptime` combined in one call.
""",
'de':
"""
Gibt die Werte von :func:`Get Contactor`, :func:`Get RGB Value`,
:func:`Get Energy Meter Values`, :func:`Get Energy Meter State`,
:func:`Get Input`, :func:`Get Output`, :func:`Get Input Voltage`,
:func:`Get State` und :func:`Get Uptime` in einem Aufruf kombiniert zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get SD Information',
'elements': [('SD Status', 'uint32', 1, 'out'),
             ('LFS Status', 'uint32', 1, 'out'),
             ('Sector Size', 'uint16', 1, 'out'),
             ('Sector Count', 'uint32', 1, 'out'),
             ('Card Type', 'uint32', 1, 'out'),
             ('Product Rev', 'uint8', 1, 'out'),
             ('Product Name', 'char', 5, 'out'),
             ('Manufacturer ID', 'uint8', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns information about the connected SD card. This includes the status of
the SD card and the LittleFS file system, the sector size and count as well as
the card type and product information.
""",
'de':
"""
Gibt Informationen über die angeschlossene SD-Karte zurück. Dazu gehören der
Status der SD-Karte und des LittleFS-Dateisystems, die Sektorgröße und -anzahl
sowie der Kartentyp und Produktinformationen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set SD Wallbox Data Point',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Flags', 'uint8', 1, 'in'), # IEC_STATE (bit 0-2) + future use
             ('Power', 'uint16', 1, 'in', {'unit': 'Watt'}), # W
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a 5-minute charge data point for the wallbox with the given ID and the
given date and time to the SD card. The minute has to be a multiple of 5. The
flags contain the IEC 61851 state in bits 0-2. The power is the charging power
in W. The returned status indicates whether the data point could be queued for
writing.
""",
'de':
"""
Schreibt einen 5-Minuten-Lade-Datenpunkt für die Wallbox mit der angegebenen ID
und dem angegebenen Datum und der angegebenen Uhrzeit auf die SD-Karte. Die
Minute muss ein Vielfaches von 5 sein. Die Flags enthalten den IEC-61851-Zustand
in den Bits 0-2. Die Power ist die Ladeleistung in W. Der zurückgegebene Status
zeigt an, ob der Datenpunkt zum Schreiben eingereiht werden konnte.
"""
}]
})

# Triggers SD Wallbox Data callback
# Only access one day at a time!
com['packets'].append({
'type': 'function',
'name': 'Get SD Wallbox Data Points',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Amount', 'uint16', 1, 'in'), # 288 for one day
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Requests up to *Amount* 5-minute charge data points for the wallbox with the
given ID starting at the given date and time. The data points are returned
through the :cb:`SD Wallbox Data Points Low Level` callback. Only one day
(288 data points) can be requested at a time.
""",
'de':
"""
Fordert bis zu *Amount* 5-Minuten-Lade-Datenpunkte für die Wallbox mit der
angegebenen ID ab dem angegebenen Datum und der angegebenen Uhrzeit an. Die
Datenpunkte werden über den Callback :cb:`SD Wallbox Data Points Low Level`
zurückgegeben. Es kann immer nur ein Tag (288 Datenpunkte) auf einmal angefordert
werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set SD Wallbox Daily Data Point',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Energy', 'uint32', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a daily charge data point (the charged energy of the given day) for the
wallbox with the given ID to the SD card. The returned status indicates whether
the data point could be queued for writing.
""",
'de':
"""
Schreibt einen täglichen Lade-Datenpunkt (die geladene Energie des angegebenen
Tages) für die Wallbox mit der angegebenen ID auf die SD-Karte. Der
zurückgegebene Status zeigt an, ob der Datenpunkt zum Schreiben eingereiht werden
konnte.
"""
}]
})

# Triggers SD Wallbox Daily Data callback
# Only access one month at a time!
com['packets'].append({
'type': 'function',
'name': 'Get SD Wallbox Daily Data Points',
'elements': [('Wallbox ID', 'uint32', 1, 'in'),
             ('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Amount', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Requests up to *Amount* daily charge data points for the wallbox with the
given ID starting at the given date. The data points are returned through the
:cb:`SD Wallbox Daily Data Points Low Level` callback. Only one month can be
requested at a time.
""",
'de':
"""
Fordert bis zu *Amount* tägliche Lade-Datenpunkte für die Wallbox mit der
angegebenen ID ab dem angegebenen Datum an. Die Datenpunkte werden über den
Callback :cb:`SD Wallbox Daily Data Points Low Level` zurückgegeben. Es kann
immer nur ein Monat auf einmal angefordert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set SD Energy Manager Data Point',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Flags', 'uint8', 1, 'in'), #
             ('Power Grid', 'int32', 1, 'in', {'unit': 'Watt'}), # W
             ('Power General', 'int32', 6, 'in', {'unit': 'Watt'}), # W
             ('Price', 'uint32', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a 5-minute energy manager data point for the given date and time to the
SD card. The minute has to be a multiple of 5. Power Grid is the grid power in
W (positive = import, negative = export) and Power General are six additional
power values in W. The returned status indicates whether the data point could
be queued for writing.
""",
'de':
"""
Schreibt einen 5-Minuten-Energy-Manager-Datenpunkt für das angegebene Datum und
die angegebene Uhrzeit auf die SD-Karte. Die Minute muss ein Vielfaches von 5
sein. Power Grid ist die Netzleistung in W (positiv = Bezug, negativ =
Einspeisung) und Power General sind sechs zusätzliche Leistungswerte in W. Der
zurückgegebene Status zeigt an, ob der Datenpunkt zum Schreiben eingereiht werden
konnte.
"""
}]
})

# Triggers SD Energy Manager Data callback
# Only access one day at a time!
com['packets'].append({
'type': 'function',
'name': 'Get SD Energy Manager Data Points',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Hour', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Minute', 'uint8', 1, 'in', {'range': (0, 55)}), # 5 minute interval (0, 5, .., 50, 55)
             ('Amount', 'uint16', 1, 'in'), # 288 for one day
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Requests up to *Amount* 5-minute energy manager data points starting at the
given date and time. The data points are returned through the
:cb:`SD Energy Manager Data Points Low Level` callback. Only one day
(288 data points) can be requested at a time.
""",
'de':
"""
Fordert bis zu *Amount* 5-Minuten-Energy-Manager-Datenpunkte ab dem angegebenen
Datum und der angegebenen Uhrzeit an. Die Datenpunkte werden über den Callback
:cb:`SD Energy Manager Data Points Low Level` zurückgegeben. Es kann immer nur
ein Tag (288 Datenpunkte) auf einmal angefordert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set SD Energy Manager Daily Data Point',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Energy Grid In', 'uint32', 1, 'in'),
             ('Energy Grid Out', 'uint32', 1, 'in'),
             ('Energy General In', 'uint32', 6, 'in'),
             ('Energy General Out', 'uint32', 6, 'in'),
             ('Price', 'uint32', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Writes a daily energy manager data point (the imported and exported energy of
the given day) to the SD card. The returned status indicates whether the data
point could be queued for writing.
""",
'de':
"""
Schreibt einen täglichen Energy-Manager-Datenpunkt (die bezogene und
eingespeiste Energie des angegebenen Tages) auf die SD-Karte. Der zurückgegebene
Status zeigt an, ob der Datenpunkt zum Schreiben eingereiht werden konnte.
"""
}]
})

# Triggers SD Energy Manager Daily Data callback
# Only access one month at a time!
com['packets'].append({
'type': 'function',
'name': 'Get SD Energy Manager Daily Data Points',
'elements': [('Year', 'uint8', 1, 'in'), # base 2000
             ('Month', 'uint8', 1, 'in', {'range': (1, 12)}),
             ('Day', 'uint8', 1, 'in', {'range': (1, 31)}),
             ('Amount', 'uint8', 1, 'in'),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Requests up to *Amount* daily energy manager data points starting at the given
date. The data points are returned through the
:cb:`SD Energy Manager Daily Data Points Low Level` callback. Only one month
can be requested at a time.
""",
'de':
"""
Fordert bis zu *Amount* tägliche Energy-Manager-Datenpunkte ab dem angegebenen
Datum an. Die Datenpunkte werden über den Callback
:cb:`SD Energy Manager Daily Data Points Low Level` zurückgegeben. Es kann immer
nur ein Monat auf einmal angefordert werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'SD Wallbox Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint8', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by :func:`Get SD Wallbox Data Points` and returns
the requested 5-minute charge data points.
""",
'de':
"""
Dieser Callback wird durch :func:`Get SD Wallbox Data Points` ausgelöst und gibt
die angeforderten 5-Minuten-Lade-Datenpunkte zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'SD Wallbox Daily Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint32', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by :func:`Get SD Wallbox Daily Data Points` and
returns the requested daily charge data points.
""",
'de':
"""
Dieser Callback wird durch :func:`Get SD Wallbox Daily Data Points` ausgelöst und
gibt die angeforderten täglichen Lade-Datenpunkte zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'SD Energy Manager Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint8', 33, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by :func:`Get SD Energy Manager Data Points` and
returns the requested 5-minute energy manager data points.
""",
'de':
"""
Dieser Callback wird durch :func:`Get SD Energy Manager Data Points` ausgelöst
und gibt die angeforderten 5-Minuten-Energy-Manager-Datenpunkte zurück.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'SD Energy Manager Daily Data Points Low Level',
'elements': [('Data Length', 'uint16', 1, 'out', {}),
             ('Data Chunk Offset', 'uint16', 1, 'out', {}),
             ('Data Chunk Data', 'uint32', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Data'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered by :func:`Get SD Energy Manager Daily Data Points`
and returns the requested daily energy manager data points.
""",
'de':
"""
Dieser Callback wird durch :func:`Get SD Energy Manager Daily Data Points`
ausgelöst und gibt die angeforderten täglichen Energy-Manager-Datenpunkte zurück.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Format SD',
'elements': [('Password', 'uint32', 1, 'in'), # Password: 0x4223ABCD
             ('Format Status', 'uint8', 1, 'out', {'constant_group': 'Format Status'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Formats the SD card (LittleFS file system). The password is 0x4223ABCD. All
data on the card is deleted.
""",
'de':
"""
Formatiert die SD-Karte (LittleFS-Dateisystem). Das Passwort ist 0x4223ABCD.
Alle Daten auf der Karte werden gelöscht.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Date Time',
'elements': [('Seconds', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Minutes', 'uint8', 1, 'in', {'range': (0, 59)}),
             ('Hours', 'uint8', 1, 'in', {'range': (0, 23)}),
             ('Days', 'uint8', 1, 'in', {'range': (0, 31)}),
             ('Days Of Week', 'uint8', 1, 'in', {'range': (0, 6)}), # 0 = Sunday, 1 = Monday, ...
             ('Month', 'uint8', 1, 'in', {'range': (0, 11)}),
             ('Year', 'uint16', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the date and time of the internal real-time clock. The day of the week is
0 for Sunday, 1 for Monday and so on.
""",
'de':
"""
Setzt das Datum und die Uhrzeit der internen Echtzeituhr. Der Wochentag ist
0 für Sonntag, 1 für Montag und so weiter.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Date Time',
'elements': [('Seconds', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Minutes', 'uint8', 1, 'out', {'range': (0, 59)}),
             ('Hours', 'uint8', 1, 'out', {'range': (0, 23)}),
             ('Days', 'uint8', 1, 'out', {'range': (0, 31)}),
             ('Days Of Week', 'uint8', 1, 'out', {'range': (0, 6)}), # 0 = Sunday, 1 = Monday, ...
             ('Month', 'uint8', 1, 'out', {'range': (0, 11)}),
             ('Year', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the date and time of the internal real-time clock as set by
:func:`Set Date Time`.
""",
'de':
"""
Gibt das Datum und die Uhrzeit der internen Echtzeituhr zurück, wie von
:func:`Set Date Time` gesetzt.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Set LED State',
'elements': [('Pattern', 'uint8', 1, 'in', {'constant_group': 'LED Pattern'}),
             ('Hue', 'uint16', 1, 'in', {'range': (0, 359)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the pattern (off, on, blinking or breathing) and the hue (0-359) of the
status LED. This overrides a color set with :func:`Set RGB Value`.
""",
'de':
"""
Setzt das Pattern (Off, On, Blinking oder Breathing) und den Hue (0-359) der
Status-LED. Dies überschreibt eine mit :func:`Set RGB Value` gesetzte Farbe.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get LED State',
'elements': [('Pattern', 'uint8', 1, 'out', {'constant_group': 'LED Pattern'}),
             ('Hue', 'uint16', 1, 'out', {'range': (0, 359)})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the LED state as set by :func:`Set LED State`.
""",
'de':
"""
Gibt den LED-Zustand zurück, wie von :func:`Set LED State` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Data Storage',
'elements': [('Page', 'uint8', 1, 'in', {'range': (0, 4)}),
             ('Status', 'uint8', 1, 'out', {'constant_group': 'Data Storage Status'}),
             ('Data', 'uint8', 63, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the content (63 bytes) of the given storage page, see
:func:`Set Data Storage`. The status is *Not Found* if the page has not been
written yet and *Busy* while the page is being read back from the SD card.
""",
'de':
"""
Gibt den Inhalt (63 Byte) der angegebenen Storage-Page zurück, siehe
:func:`Set Data Storage`. Der Status ist *Not Found*, wenn die Page noch nicht
geschrieben wurde, und *Busy*, während die Page von der SD-Karte zurückgelesen
wird.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Data Storage',
'elements': [('Page', 'uint8', 1, 'in', {'range': (0, 4)}),
             ('Data', 'uint8', 63, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Stores 63 bytes of data in the given storage page. The data is held in RAM and
written to the SD card about 10 minutes after the last change.
""",
'de':
"""
Speichert 63 Byte Daten in der angegebenen Storage-Page. Die Daten werden im RAM
gehalten und etwa 10 Minuten nach der letzten Änderung auf die SD-Karte
geschrieben.
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Reset Energy Meter Relative Energy',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the relative energy value of the energy meter to zero. This sets the
point in time from which on the relative energy meter values are counted.
""",
'de':
"""
Setzt den relativen Energiewert des Stromzählers auf null. Damit wird der
Zeitpunkt festgelegt, ab dem die relativen Energiewerte gezählt werden.
"""
}]
})

# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# EVSE Bricklet 2.0 communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function
from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 2167,
    'name': 'EVSE V2',
    'display_name': 'EVSE 2.0',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'TBD',
        'de': 'TBD'
    },
    'released': False,
    'documented': False,
    'discontinued': False,
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
'name': 'IEC61851 State',
'type': 'uint8',
'constants': [('A', 0),
              ('B', 1),
              ('C', 2),
              ('D', 3),
              ('EF', 4)]
})

com['constant_groups'].append({
'name': 'LED State',
'type': 'uint8',
'constants': [('Off', 0),
              ('On', 1),
              ('Blinking', 2),
              ('Flicker', 3),
              ('Breathing', 4)]
})

com['constant_groups'].append({
'name': 'Vehicle State',
'type': 'uint8',
'constants': [('Not Connected', 0),
              ('Connected', 1),
              ('Charging', 2),
              ('Error', 3)]
})

com['constant_groups'].append({
'name': 'Contactor State',
'type': 'uint8',
'constants': [('AC1 NLive AC2 NLive', 0),
              ('AC1 Live AC2 NLive', 1),
              ('AC1 NLive AC2 Live', 2),
              ('AC1 Live AC2 Live', 3)]
})

com['constant_groups'].append({
'name': 'Lock State',
'type': 'uint8',
'constants': [('Init', 0),
              ('Open', 1),
              ('Closing', 2),
              ('Close', 3),
              ('Opening', 4),
              ('Error', 5)]
})

com['constant_groups'].append({
'name': 'Error State',
'type': 'uint8',
'constants': [('OK', 0),
              ('Switch', 2),
              ('DC Fault', 3),
              ('Contactor', 4),
              ('Communication', 5)]
})

com['constant_groups'].append({
'name': 'Jumper Configuration',
'type': 'uint8',
'constants': [('6A', 0),
              ('10A', 1),
              ('13A', 2),
              ('16A', 3),
              ('20A', 4),
              ('25A', 5),
              ('32A', 6),
              ('Software', 7),
              ('Unconfigured', 8)]
})

com['constant_groups'].append({
'name': 'Charge Release',
'type': 'uint8',
'constants': [('Automatic', 0),
              ('Manual', 1),
              ('Deactivated', 2),
              ('Managed', 3)]
})

com['constant_groups'].append({
'name': 'DC Fault Current State',
'type': 'uint8',
'constants': [('Normal Condition', 0),
              ('6 MA Error', 1),
              ('System Error', 2),
              ('Unknown Error', 3),
              ('Calibration Error', 4)]
})

com['constant_groups'].append({
'name': 'Shutdown Input',
'type': 'uint8',
'constants': [('Ignored', 0),
              ('Shutdown On Open', 1),
              ('Shutdown On Close', 2)]
})

com['constant_groups'].append({
'name': 'Output',
'type': 'uint8',
'constants': [('Low', 0),
              ('High', 1)]
})

com['constant_groups'].append({
'name': 'Button Configuration',
'type': 'uint8',
'constants': [('Deactivated', 0),
              ('Start Charging', 1),
              ('Stop Charging', 2),
              ('Start And Stop Charging', 3)]
})

com['constant_groups'].append({
'name': 'Control Pilot',
'type': 'uint8',
'constants': [('Disconnected', 0),
              ('Connected', 1),
              ('Automatic', 2)]
})


com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('IEC61851 State', 'uint8', 1, 'out', {'constant_group': 'IEC61851 State'}),
             ('Vehicle State', 'uint8', 1, 'out', {'constant_group': 'Vehicle State'}),
             ('Contactor State', 'uint8', 1, 'out', {'constant_group': 'Contactor State'}),
             ('Contactor Error', 'uint8', 1, 'out'),
             ('Charge Release', 'uint8', 1, 'out', {'constant_group': 'Charge Release'}),
             ('Allowed Charging Current', 'uint16', 1, 'out'),
             ('Error State', 'uint8', 1, 'out', {'constant_group': 'Error State'}),
             ('Lock State', 'uint8', 1, 'out', {'constant_group': 'Lock State'}),
             ('Time Since State Change', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Uptime', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Hardware Configuration',
'elements': [('Jumper Configuration', 'uint8', 1, 'out', {'constant_group': 'Jumper Configuration'}),
             ('Has Lock Switch', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

"""
GPIO:
	response->gpio[0] = (get_bit(port0, 0)  << 0) | //  0: Config Jumper 0
	                    (get_bit(port0, 1)  << 1) | //  1: Motor Fault
	                    (get_bit(port0, 3)  << 2) | //  2: DC Error
	                    (get_bit(port0, 5)  << 3) | //  3: Config Jumper 1
	                    (get_bit(port0, 8)  << 4) | //  4: DC Test
	                    (get_bit(port0, 9)  << 5) | //  5: Enable
	                    (get_bit(port0, 12) << 6) | //  6: Switch
	                    (get_bit(port1, 0)  << 7);  //  7: CP PWM

	response->gpio[1] = (get_bit(port1, 1)  << 0) | //  8: Input Motor Switch
	                    (get_bit(port1, 2)  << 1) | //  9: Relay (Contactor)
	                    (get_bit(port1, 3)  << 2) | // 10: GP Output
	                    (get_bit(port1, 4)  << 3) | // 11: CP Disconnect
	                    (get_bit(port1, 5)  << 4) | // 12: Motor Enable
	                    (get_bit(port1, 6)  << 5) | // 13: Motor Phase
	                    (get_bit(port2, 6)  << 6) | // 14: AC 1
	                    (get_bit(port2, 7)  << 7);  // 15: AC 2

	response->gpio[2] = (get_bit(port2, 9)  << 0) | // 16: GP Input
	                    (get_bit(port4, 4)  << 1) | // 17: DC X6
	                    (get_bit(port4, 5)  << 2) | // 18: DC X30
	                    (get_bit(port4, 6)  << 3);  // 19: LED
"""
com['packets'].append({
'type': 'function',
'name': 'Get Low Level State',
'elements': [('LED State', 'uint8', 1, 'out', {'constant_group': 'LED State'}),
             ('CP PWM Duty Cycle', 'uint16', 1, 'out'),
             ('ADC Values', 'uint16', 7, 'out'), # CP/PE before resistor (PWM high), CP/PE after resistor (PWM high), CP/PE before resistor (PWM low), CP/PE after resistor (PWM low), PP/PE, +12V rail, -12V rail
             ('Voltages', 'int16', 7, 'out', {'scale': (1, 1000), 'unit': 'Volt'}), # CP/PE before resistor (PWM high), CP/PE after resistor (PWM high), CP/PE before resistor (PWM low), CP/PE after resistor (PWM low), PP/PE, +12V rail, -12V rail
             ('Resistances', 'uint32', 2, 'out', {'unit': 'Ohm'}), # CP/PE resistance, PP/PE resistance
             ('GPIO', 'bool', 24, 'out'), # TODO, all I/O (20 for now)
             ('Charging Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Max Charging Current',
'elements': [('Max Current', 'uint16', 1, 'in')], # mA (default 32A?)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Max Charging Current',
'elements': [('Max Current Configured', 'uint16', 1, 'out'),     # mA
             ('Max Current Incoming Cable', 'uint16', 1, 'out'), # mA
             ('Max Current Outgoing Cable', 'uint16', 1, 'out'), # mA
             ('Max Current Managed', 'uint16', 1, 'out')],       # mA
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
* Max Current Configured -> set with :func:`Set Max Charging Current`
* Max Current Incoming Cable -> set with jumper on EVSE
* Max Current Outgoing Cable -> set with resistor between PP/PE (if fixed cable is used)

TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Start Charging',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Stop Charging',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Charging Autostart',
'elements': [('Autostart', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Charging Autostart',
'elements': [('Autostart', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter Values',
'elements': [('Power', 'float', 1, 'out'),            # W
             ('Energy Relative', 'float', 1, 'out'),  # Wh
             ('Energy Absolute', 'float', 1, 'out'),  # Wh
             ('Phases Active', 'bool', 3, 'out'),
             ('Phases Connected', 'bool', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter Detailed Values Low Level',
'elements': [('Values Chunk Offset', 'uint16', 1, 'out', {}),
             ('Values Chunk Data', 'float', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Values', 'fixed_length': 85}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TBD
""",
'de':
"""
TBD
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Meter State',
'elements': [('Available', 'bool', 1, 'out'),
             ('Error Count', 'uint32', 6, 'out')], # local timeout, global timeout, illigal function, illegal data address, illegal data value, slave device failure
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reset Energy Meter',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get DC Fault Current State',
'elements': [('DC Fault Current State', 'uint8', 1, 'out', {'constant_group': 'DC Fault Current State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reset DC Fault Current',
'response_expected': 'true',
'elements': [('Password', 'uint32', 1, 'in')], # Password: 0xDC42FA23
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set GPIO Configuration',
'elements': [('Shutdown Input Configuration', 'uint8', 1, 'in', {'constant_group': 'Shutdown Input'}),
             ('Input Configuration', 'uint8', 1, 'in'),
             ('Output Configuration', 'uint8', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get GPIO Configuration',
'elements': [('Shutdown Input Configuration', 'uint8', 1, 'out', {'constant_group': 'Shutdown Input'}),
             ('Input Configuration', 'uint8', 1, 'out'),
             ('Output Configuration', 'uint8', 1, 'out', {'constant_group': 'Output'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Managed',
'elements': [('Managed', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Managed',
'response_expected': 'true',
'elements': [('Managed', 'bool', 1, 'in'),
             ('Password', 'uint32', 1, 'in')], # To enable: 0x00363702 (mgmt on), to disable: 0x036370FF (mgmt off)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Managed Current',
'elements': [('Current', 'uint16', 1, 'in')], # mA (default 0A)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Data Storage',
'elements': [('Page', 'uint8', 1, 'in'),
             ('Data', 'uint8', 63, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Data Storage',
'elements': [('Page', 'uint8', 1, 'in'),
             ('Data', 'uint8', 63, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Indicator LED',
'elements': [('Indication', 'int16', 1, 'out'),
             ('Duration', 'uint16', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Indicator LED',
'elements': [('Indication', 'int16', 1, 'in'), #-1 = led controled by EVSE, 0 = Off, 255 = on, 1-254 = pwm, 1001 = ack indication, 1002 = nack indication, 1003 = nag indication
             ('Duration', 'uint16', 1, 'in'), # max 2^16 ms
             ('Status', 'uint8', 1, 'out')], # OK = 0, Sonst nicht OK wegen X (Blinking=2, Flickering=3, Breathing=4)
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Button Configuration',
'elements': [('Button Configuration', 'uint8', 1, 'in', {'constant_group': 'Button Configuration'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Button Configuration',
'elements': [('Button Configuration', 'uint8', 1, 'out', {'constant_group': 'Button Configuration'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Button State',
'elements': [('Button Press Time', 'uint32', 1, 'out'),
             ('Button Release Time', 'uint32', 1, 'out'),
             ('Button Pressed', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Control Pilot Configuration',
'elements': [('Control Pilot', 'uint8', 1, 'in', {'constant_group': 'Control Pilot'})], # Default Automatic
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Control Pilot Configuration',
'elements': [('Control Pilot', 'uint8', 1, 'out', {'constant_group': 'Control Pilot'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get All Data 1',
'elements': [('IEC61851 State', 'uint8', 1, 'out', {'constant_group': 'IEC61851 State'}),
             ('Vehicle State', 'uint8', 1, 'out', {'constant_group': 'Vehicle State'}),
             ('Contactor State', 'uint8', 1, 'out', {'constant_group': 'Contactor State'}),
             ('Contactor Error', 'uint8', 1, 'out'),
             ('Charge Release', 'uint8', 1, 'out', {'constant_group': 'Charge Release'}),
             ('Allowed Charging Current', 'uint16', 1, 'out'),
             ('Error State', 'uint8', 1, 'out', {'constant_group': 'Error State'}),
             ('Lock State', 'uint8', 1, 'out', {'constant_group': 'Lock State'}),
             ('Time Since State Change', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Uptime', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Jumper Configuration', 'uint8', 1, 'out', {'constant_group': 'Jumper Configuration'}),
             ('Has Lock Switch', 'bool', 1, 'out'),
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data 2',
'elements': [('LED State', 'uint8', 1, 'out', {'constant_group': 'LED State'}),
             ('CP PWM Duty Cycle', 'uint16', 1, 'out'),
             ('ADC Values', 'uint16', 7, 'out'), # CP/PE before resistor (PWM high), CP/PE after resistor (PWM high), CP/PE before resistor (PWM low), CP/PE after resistor (PWM low), PP/PE, +12V rail, -12V rail
             ('Voltages', 'int16', 7, 'out', {'scale': (1, 1000), 'unit': 'Volt'}), # CP/PE before resistor (PWM high), CP/PE after resistor (PWM high), CP/PE before resistor (PWM low), CP/PE after resistor (PWM low), PP/PE, +12V rail, -12V rail
             ('Resistances', 'uint32', 2, 'out', {'unit': 'Ohm'}), # CP/PE resistance, PP/PE resistance
             ('GPIO', 'bool', 24, 'out'), # TODO, all I/O (20 for now)
             ('Charging Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Max Current Configured', 'uint16', 1, 'out'),     # mA
             ('Max Current Incoming Cable', 'uint16', 1, 'out'), # mA
             ('Max Current Outgoing Cable', 'uint16', 1, 'out'), # mA
             ('Max Current Managed', 'uint16', 1, 'out'),
             ('Autostart', 'bool', 1, 'out'),
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Data 3',
'elements': [('Power', 'float', 1, 'out'),            # W
             ('Energy Relative', 'float', 1, 'out'),  # Wh
             ('Energy Absolute', 'float', 1, 'out'),  # Wh
             ('Phases Active', 'bool', 3, 'out'),
             ('Phases Connected', 'bool', 3, 'out'),
             ('Available', 'bool', 1, 'out'),
             ('Error Count', 'uint32', 6, 'out'),
             ('DC Fault Current State', 'uint8', 1, 'out', {'constant_group': 'DC Fault Current State'}),
             ('Shutdown Input Configuration', 'uint8', 1, 'out', {'constant_group': 'Shutdown Input'}),
             ('Input Configuration', 'uint8', 1, 'out'),
             ('Output Configuration', 'uint8', 1, 'out', {'constant_group': 'Output'}),
             ('Managed', 'bool', 1, 'out'),
             ('Indication', 'int16', 1, 'out'),
             ('Duration', 'uint16', 1, 'out'),
             ('Button Configuration', 'uint8', 1, 'out', {'constant_group': 'Button Configuration'}),
             ('Button Press Time', 'uint32', 1, 'out'),
             ('Button Release Time', 'uint32', 1, 'out'),
             ('Button Pressed', 'bool', 1, 'out'),
             ('Control Pilot', 'uint8', 1, 'out', {'constant_group': 'Control Pilot'})
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
TODO
""",
'de':
"""
TODO
"""
}]
})

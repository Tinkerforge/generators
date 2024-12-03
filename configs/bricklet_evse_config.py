# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# EVSE Bricklet communication config

from generators.configs.commonconstants import THRESHOLD_OPTION_CONSTANT_GROUP
from generators.configs.commonconstants import add_callback_value_function
from generators.configs.openhab_commonconfig import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 2],
    'category': 'Bricklet',
    'device_identifier': 2159,
    'name': 'EVSE',
    'display_name': 'EVSE',
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
'name': 'Charger State',
'type': 'uint8',
'constants': [('Not Connected', 0),
              ('Waiting For Charge Release', 1),
              ('Ready To Charge', 2),
              ('Charging', 3),
              ('Error', 4)]
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
              ('Calibration', 3),
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

com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('IEC61851 State', 'uint8', 1, 'out', {'constant_group': 'IEC61851 State'}),
             ('Charger State', 'uint8', 1, 'out', {'constant_group': 'Charger State'}),
             ('Contactor State', 'uint8', 1, 'out', {'constant_group': 'Contactor State'}),
             ('Contactor Error', 'uint8', 1, 'out'),
             ('Allowed Charging Current', 'uint16', 1, 'out'),
             ('Error State', 'uint8', 1, 'out', {'constant_group': 'Error State'}),
             ('Lock State', 'uint8', 1, 'out', {'constant_group': 'Lock State'})],
'since_firmware': [2, 0, 5],
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
             ('Has Lock Switch', 'bool', 1, 'out'),
             ('EVSE Version', 'uint8', 1, 'out')],
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
'name': 'Get Low Level State',
'elements': [('LED State', 'uint8', 1, 'out', {'constant_group': 'LED State'}),
             ('CP PWM Duty Cycle', 'uint16', 1, 'out'),
             ('ADC Values', 'uint16', 2, 'out'),
             ('Voltages', 'int16', 3, 'out', {'scale': (1, 1000), 'unit': 'Volt'}), # pe-cp, pe-pp, high voltage pe-cp
             ('Resistances', 'uint32', 2, 'out', {'unit': 'Ohm'}),
             ('GPIO', 'bool', 5, 'out'), # XMC_GPIO_GetInput(EVSE_INPUT_GP_PIN) | (XMC_GPIO_GetInput(EVSE_OUTPUT_GP_PIN) << 1) | (XMC_GPIO_GetInput(EVSE_MOTOR_INPUT_SWITCH_PIN) << 2) | (XMC_GPIO_GetInput(EVSE_RELAY_PIN) << 3) | (XMC_GPIO_GetInput(EVSE_MOTOR_FAULT_PIN) << 4)
             ('Car Stopped Charging', 'bool', 1, 'out'),
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
'name': 'Set Charging Slot',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Max Current', 'uint16', 1, 'in'),
             ('Active', 'bool', 1, 'in'),
             ('Clear On Disconnect', 'bool', 1, 'in'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
fixed slots:
0: incoming cable (read-only, configured through slide switch)
1: outgoing cable (read-only, configured through resistor)
2: gpio input 0 (shutdown input)
3: gpio input 1 (input)
4: button (0A <-> 32A, can be controlled from web interface with start button and physical button if configured)

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Charging Slot Max Current',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Max Current', 'uint16', 1, 'in'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Charging Slot Active',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Active', 'bool', 1, 'in'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Charging Slot Clear On Disconnect',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Clear On Disconnect', 'bool', 1, 'in'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Charging Slot',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Max Current', 'uint16', 1, 'out'),
             ('Active', 'bool', 1, 'out'),
             ('Clear On Disconnect', 'bool', 1, 'out'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Charging Slots',
'elements': [('Max Current', 'uint16', 20, 'out'),
             ('Active And Clear On Disconnect', 'uint8', 20, 'out')], # bit 0 => Active, bit 1 => Clear On Disconnect
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
packed getter

""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Charging Slot Default',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Max Current', 'uint16', 1, 'in'),
             ('Active', 'bool', 1, 'in'),
             ('Clear On Disconnect', 'bool', 1, 'in'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
fixed slots:
0: incoming cable (read-only, configured through slide switch)
1: outgoing cable (read-only, configured through resistor)
2: gpio input 0 (shutdown input)
3: gpio input 1 (input)

""",
'de':
"""
TODO
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Get Charging Slot Default',
'elements': [('Slot', 'uint8', 1, 'in'),
             ('Max Current', 'uint16', 1, 'out'),
             ('Active', 'bool', 1, 'out'),
             ('Clear On Disconnect', 'bool', 1, 'out'),
],
'since_firmware': [2, 1, 0],
'doc': ['bf', {
'en':
"""
""",
'de':
"""
TODO
"""
}]
})


com['packets'].append({
'type': 'function',
'name': 'Calibrate',
'elements': [('State', 'uint8', 1, 'in'),       # 1, 2
             ('Password', 'uint32', 1, 'in'),   # state 1 = 0x0BB03201, state 2 = 0x0BB03202
             ('Value', 'int32', 1, 'in'),       # high voltage, offset
             ('Success', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get User Calibration',
'elements': [('User Calibration Active', 'bool', 1, 'out'),
             ('Voltage Diff', 'int16', 1, 'out'),
             ('Voltage Mul', 'int16', 1, 'out'),
             ('Voltage Div', 'int16', 1, 'out'),
             ('Resistance 2700', 'int16', 1, 'out'),
             ('Resistance 880', 'int16', 14, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Set User Calibration',
'response_expected': 'true',
'elements': [('Password', 'uint32', 1, 'in'), # 0xCA11B4A0
             ('User Calibration Active', 'bool', 1, 'in'),
             ('Voltage Diff', 'int16', 1, 'in'),
             ('Voltage Mul', 'int16', 1, 'in'),
             ('Voltage Div', 'int16', 1, 'in'),
             ('Resistance 2700', 'int16', 1, 'in'),
             ('Resistance 880', 'int16', 14, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['af', {
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
'name': 'Get All Data 1',
'elements': [('IEC61851 State', 'uint8', 1, 'out', {'constant_group': 'IEC61851 State'}),
             ('Charger State', 'uint8', 1, 'out', {'constant_group': 'Charger State'}),
             ('Contactor State', 'uint8', 1, 'out', {'constant_group': 'Contactor State'}),
             ('Contactor Error', 'uint8', 1, 'out'),
             ('Allowed Charging Current', 'uint16', 1, 'out'),
             ('Error State', 'uint8', 1, 'out', {'constant_group': 'Error State'}),
             ('Lock State', 'uint8', 1, 'out', {'constant_group': 'Lock State'}),
             ('Jumper Configuration', 'uint8', 1, 'out', {'constant_group': 'Jumper Configuration'}),
             ('Has Lock Switch', 'bool', 1, 'out'),
             ('EVSE Version', 'uint8', 1, 'out'),

             ('LED State', 'uint8', 1, 'out', {'constant_group': 'LED State'}),
             ('CP PWM Duty Cycle', 'uint16', 1, 'out'),
             ('ADC Values', 'uint16', 2, 'out'),
             ('Voltages', 'int16', 3, 'out', {'scale': (1, 1000), 'unit': 'Volt'}), # pe-cp, pe-pp, high voltage pe-cp
             ('Resistances', 'uint32', 2, 'out', {'unit': 'Ohm'}),
             ('GPIO', 'bool', 5, 'out'), # XMC_GPIO_GetInput(EVSE_INPUT_GP_PIN) | (XMC_GPIO_GetInput(EVSE_OUTPUT_GP_PIN) << 1) | (XMC_GPIO_GetInput(EVSE_MOTOR_INPUT_SWITCH_PIN) << 2) | (XMC_GPIO_GetInput(EVSE_RELAY_PIN) << 3) | (XMC_GPIO_GetInput(EVSE_MOTOR_FAULT_PIN) << 4)
             ('Car Stopped Charging', 'bool', 1, 'out'),
             ('Time Since State Change', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Uptime', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),

             ('Indication', 'int16', 1, 'out'),
             ('Duration', 'uint16', 1, 'out'),

             ('Button Press Time', 'uint32', 1, 'out'),
             ('Button Release Time', 'uint32', 1, 'out'),
             ('Button Pressed', 'bool', 1, 'out'),
             ('Boost Mode Enabled', 'bool', 1, 'out')],
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
'name': 'Factory Reset',
'response_expected': 'true',
'elements': [('Password', 'uint32', 1, 'in')], # Password: 0x2342FACD
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
'name': 'Set Boost Mode',
'elements': [('Boost Mode Enabled', 'bool', 1, 'in')], # default False
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
'name': 'Get Boost Mode',
'elements': [('Boost Mode Enabled', 'bool', 1, 'out')],
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

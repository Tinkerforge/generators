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
              ('AC1 Live AC2 Live', 3)] # Different in V3
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

"""
DC fault current state
state & 0b0000_0111 = [('Normal Condition', 0),
                       ('6 MA DC Error', 1),
                       ('System Error', 2),
                       ('Unknown Error', 3),
                       ('Calibration Error', 4),
                       ('20 MA AC Error', 5),
                       ('6 MA AC And 20 MA AC Error', 6)]
state & 0b0011_1000 = (state & 0b0000_0111 != 4 (calibration error)) ?
                        pins (x6 x30 err) :
                        calibration error code
state & 0b0100_0000 = sensor type (0 old, 1 new)
"""
com['constant_groups'].append({
'name': 'DC Fault Current State',
'type': 'uint8',
'constants': [('Normal Condition', 0),
              ('6 MA DC Error', 1),
              ('System Error', 2),
              ('Unknown Error', 3),
              ('Calibration Error', 4),
              ('20 MA AC Error', 5),
              ('6 MA AC And 20 MA AC Error', 6)]
})

com['constant_groups'].append({
'name': 'Shutdown Input',
'type': 'uint8',
'constants': [('Ignored', 0), # <- WARP2 default
              ('Shutdown On Open', 1),
              ('Shutdown On Close', 2),
              ('4200 Watt On Open', 3),
              ('4200 Watt On Close', 4)] # <- WARP3 default
})

com['constant_groups'].append({
'name': 'Output',
'type': 'uint8',
'constants': [('Connected To Ground', 0),
              ('High Impedance', 1)]
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
              ('DEM4A', 7)]
})

com['constant_groups'].append({
'name': 'Input',
'type': 'uint8',
'constants': [('Unconfigured', 0),
              ('Active Low Max 0A', 1),
              ('Active Low Max 6A', 2),
              ('Active Low Max 8A', 3),
              ('Active Low Max 10A', 4),
              ('Active Low Max 13A', 5),
              ('Active Low Max 16A', 6),
              ('Active Low Max 20A', 7),
              ('Active Low Max 25A', 8),
              ('Active High Max 0A', 9),
              ('Active High Max 6A', 10),
              ('Active High Max 8A', 11),
              ('Active High Max 10A', 12),
              ('Active High Max 13A', 13),
              ('Active High Max 16A', 14),
              ('Active High Max 20A', 15),
              ('Active High Max 25A', 16)]
})


"""
contactor state
state & 0b0000_0001 = contactor state  N+L1 (0 is not switched, 1 is switched)
state & 0b0000_0010 = contactor state L2+L3 (0 is not switched, 1 is switched)
state & 0b0000_0100 = pe connected (0 not connected 1 connected)
state & 0b0000_1000 = contactor control  N+L1 (0 want not switched, 1 want switched)
state & 0b0001_0000 = contactor control L2+L3 (0 want not switched, 1 want switched)

contactor error
error & 0b0000_0001 = pe error (0 ok, 1 error -> !(state & 0x04))
error & 0b1111_1110 = error state (0 ok, else earror -> contactor control/state mismatch)
"""
com['packets'].append({
'type': 'function',
'name': 'Get State',
'elements': [('IEC61851 State', 'uint8', 1, 'out', {'constant_group': 'IEC61851 State'}),
             ('Charger State', 'uint8', 1, 'out', {'constant_group': 'Charger State'}),
             ('Contactor State', 'uint8', 1, 'out', {'constant_group': 'Contactor State'}),
             ('Contactor Error', 'uint8', 1, 'out'),
             ('Allowed Charging Current', 'uint16', 1, 'out'),
             ('Error State', 'uint8', 1, 'out', {'constant_group': 'Error State'}),
             ('Lock State', 'uint8', 1, 'out', {'constant_group': 'Lock State'}),
             ('DC Fault Current State', 'uint8', 1, 'out', {'constant_group': 'DC Fault Current State'})],
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
             ('Has Lock Switch', 'bool', 1, 'out'),
             ('EVSE Version', 'uint8', 1, 'out'),
             ('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'})],
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
GPIO WARP V2:
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

GPIO WARP V3:
    response->gpio[0] = (get_bit(port0, 0)   << 0) | //  0: DC X30
                        (get_bit(port0, 1)   << 1) | //  1: DC X6
                        (get_bit(port0, 3)   << 2) | //  2: DC Error
                        (get_bit(port0, 5)   << 3) | //  3: DC Test
                        (get_bit(port0, 6)   << 4) | //  4: Status LED
                        (get_bit(port0, 12)  << 5) | //  5: Switch
                        (get_bit(port1, 0)   << 6) | //  6: LED R
                        (get_bit(port1, 2)   << 7);  //  7: LED B

    response->gpio[1] = (get_bit(port1, 3)   << 0) | //  8: LED G
                        (get_bit(port1, 4)   << 1) | //  9: CP PWM
                        (get_bit(port1, 5)   << 2) | // 10: Contactor 1
                        (get_bit(port1, 6)   << 3) | // 11: Contactor 0
                        (get_bit(port2, 6)   << 4) | // 12: Contactor 1 FB
                        (get_bit(port2, 7)   << 5) | // 13: Contactor 0 FB
                        (get_bit(port2, 8)   << 6) | // 14: PE Check
                        (get_bit(port2, 9)   << 7);  // 15: Config Jumper 1

    response->gpio[2] = (get_bit(port4, 4)   << 6) | // 16: CP Disconnect
                        (get_bit(port4, 5)   << 7) | // 17: Config Jumper 0
                        (get_bit(port4, 6)   << 0) | // 18: Enable
                        (get_bit(port4, 7)   << 1);  // 19: Version Detection
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
             ('Charging Time', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Since State Change', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Since DC Fault Check', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'since_firmware': [1, 0, 0],
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
'name': 'Get Energy Meter Values',
'elements': [('Power', 'float', 1, 'out'),            # W
             ('Current', 'float', 3, 'out'),
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
'name': 'Get All Energy Meter Values Low Level',
'elements': [('Values Chunk Offset', 'uint16', 1, 'out', {}),
             ('Values Chunk Data', 'float', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Values', 'fixed_length': 88}},
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
'name': 'Get Energy Meter Errors',
'elements': [('Error Count', 'uint32', 6, 'out')], # local timeout, global timeout, illigal function, illegal data address, illegal data value, slave device failure
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
'name': 'Reset Energy Meter Relative Energy',
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
'name': 'Reset DC Fault Current State',
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
             ('Input Configuration', 'uint8', 1, 'in', {'constant_group': 'Input'}),
             ('Output Configuration', 'uint8', 1, 'in', {'constant_group': 'Output'})],
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
             ('Input Configuration', 'uint8', 1, 'out', {'constant_group': 'Input'}),
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
             ('Duration', 'uint16', 1, 'out'),
             ('Color H', 'uint16', 1, 'out'),
             ('Color S', 'uint8', 1, 'out'),
             ('Color V', 'uint8', 1, 'out')],
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
             ('Color H', 'uint16', 1, 'in'), # Color V=0 => automatic color. In EVSE V2 always blue
             ('Color S', 'uint8', 1, 'in'),
             ('Color V', 'uint8', 1, 'in'),
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
'name': 'Set EV Wakeup',
'elements': [('EV Wakeup Enabled', 'bool', 1, 'in')],
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
'name': 'Get EV Wakuep',
'elements': [('EV Wakeup Enabled', 'bool', 1, 'out')],
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
'name': 'Set Control Pilot Disconnect',
'elements': [('Control Pilot Disconnect', 'bool', 1, 'in'),
             ('Is Control Pilot Disconnect', 'bool', 1, 'out')],
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
'name': 'Get Control Pilot Disconnect',
'elements': [('Control Pilot Disconnect', 'bool', 1, 'out')],
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
             ('DC Fault Current State', 'uint8', 1, 'out', {'constant_group': 'DC Fault Current State'}),
             ('Jumper Configuration', 'uint8', 1, 'out', {'constant_group': 'Jumper Configuration'}),
             ('Has Lock Switch', 'bool', 1, 'out'),
             ('EVSE Version', 'uint8', 1, 'out'),
             ('Energy Meter Type', 'uint8', 1, 'out', {'constant_group': 'Energy Meter Type'}),
             ('Power', 'float', 1, 'out'),            # W
             ('Current', 'float', 3, 'out'),          # A
             ('Phases Active', 'bool', 3, 'out'),
             ('Phases Connected', 'bool', 3, 'out'),
             ('Error Count', 'uint32', 6, 'out'),
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
'elements': [('Shutdown Input Configuration', 'uint8', 1, 'out', {'constant_group': 'Shutdown Input'}),
             ('Input Configuration', 'uint8', 1, 'out'),
             ('Output Configuration', 'uint8', 1, 'out', {'constant_group': 'Output'}),
             ('Indication', 'int16', 1, 'out'),
             ('Duration', 'uint16', 1, 'out'),
             ('Color H', 'uint16', 1, 'out'),
             ('Color S', 'uint8', 1, 'out'),
             ('Color V', 'uint8', 1, 'out'),
             ('Button Configuration', 'uint8', 1, 'out', {'constant_group': 'Button Configuration'}),
             ('Button Press Time', 'uint32', 1, 'out'),
             ('Button Release Time', 'uint32', 1, 'out'),
             ('Button Pressed', 'bool', 1, 'out'),
             ('EV Wakeup Enabled', 'bool', 1, 'out'),
             ('Control Pilot Disconnect', 'bool', 1, 'out'),
             ('Boost Mode Enabled', 'bool', 1, 'out'),
             ('Temperature', 'int16', 1, 'out'),
             ('Phases Current', 'uint8', 1, 'out'),  # Always three-phase for EVSE V2
             ('Phases Requested', 'uint8', 1, 'out'),
             ('Phases State', 'uint8', 1, 'out'),
             ('Phases Info', 'uint8', 1, 'out'),
             ('Phase Auto Switch Enabled', 'bool', 1, 'out'),
             ('Phases Connected', 'uint8', 1, 'out'), # 1 or 3, Ignored in EVSE V2
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
'name': 'Get Button Press Boot Time',
'elements': [('Reset', 'bool', 1, 'in'),
             ('Button Press Boot Time', 'uint32', 1, 'out')], # Amount of time button was continuously pressed during boot (in ms)
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

com['packets'].append({
'type': 'function',
'name': 'Trigger DC Fault Test',
'elements': [('Password', 'uint32', 1, 'in'), # Password: 0xDCFAE550
             ('Started', 'bool', 1, 'out')],
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
'name': 'Set GP Output',
'elements': [('GP Output', 'uint8', 1, 'in', {'constant_group': 'Output'})], # Bootup-Default set by Set GPIO Configuration
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
'name': 'Get Temperature',
'elements': [('Temperature', 'int16', 1, 'out')], # Returns 0 in EVSE V2
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
'name': 'Set Phase Control',
'elements': [('Phases', 'uint8', 1, 'in')], # No effect in EVSE V2
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
'name': 'Get Phase Control',
'elements': [('Phases Current', 'uint8', 1, 'out'),  # Always three-phase EVSE V2
             ('Phases Requested', 'uint8', 1, 'out'),
             ('Phases State', 'uint8', 1, 'out'),
             ('Phases Info', 'uint8', 1, 'out')],  # 0 = normal, 1 = 1-phase forced by auto-switch
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
'name': 'Set Phase Auto Switch',
'elements': [('Phase Auto Switch Enabled', 'bool', 1, 'in')], # Ignored in EVSE V2
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
'name': 'Get Phase Auto Switch',
'elements': [('Phase Auto Switch Enabled', 'bool', 1, 'out')], # Always false in EVSE V2
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
'name': 'Set Phases Connected',
'elements': [('Phases Connected', 'uint8', 1, 'in')], # 1 or 3, Ignored in EVSE V2
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
'name': 'Get Phases Connected',
'elements': [('Phases Connected', 'uint8', 1, 'out')], # 1 or 3, Ignored in EVSE V2
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
'type': 'callback',
'name': 'Energy Meter Values',
'elements': [('Power', 'float', 1, 'out'),            # W
             ('Current', 'float', 3, 'out'),
             ('Phases Active', 'bool', 3, 'out'),
             ('Phases Connected', 'bool', 3, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['c', {
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

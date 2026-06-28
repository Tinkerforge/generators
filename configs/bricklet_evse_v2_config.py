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
        'en': 'Controls the charging of electric vehicles according to IEC 61851',
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
              ('Start And Stop Charging', 3),
              ('Enumerate', 4)]
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
              ('DEM4A', 7),
              ('DMED341MID7ER', 8),
              ('DSZ16DZE', 9),
              ('WM3M4C', 10),
              ('WM3M4', 11)]
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

com['constant_groups'].append({
'name': 'Charging Protocol',
'type': 'uint8',
'constants': [('IEC61851 Permanent', 0),
              ('IEC61851 Temporary', 1),
              ('ISO15118', 2)]
})

com['constant_groups'].append({
'name': 'Eichrecht State',
'type': 'uint8',
'constants': [('OK', 0),
              ('Not All Info Set', 1),
              ('Busy', 2),
              ('Not Supported', 3)]
})

com['constant_groups'].append({
'name': 'Eichrecht User Assignment Identification Flag',
'type': 'uint8',
'constants': [('RFID NONE', 0),
              ('RFID PLAIN', 1),
              ('RFID RELATED', 2),
              ('RFID PSK', 3),
              ('OCPP NONE', 4),
              ('OCPP RS', 5),
              ('OCPP AUTH', 6),
              ('OCPP RS TLS', 7),
              ('OCPP AUTH TLS', 8),
              ('OCPP CACHE', 9),
              ('OCPP WHITELIST', 10),
              ('OCPP CERTIFIED', 11),
              ('ISO15118 NONE', 12),
              ('ISO15118 PNC', 13),
              ('PLMN NONE', 14),
              ('PLMN RING', 15),
              ('PLMN SMS', 16),
              ('Not Set', 17)]
})

com['constant_groups'].append({
'name': 'Eichrecht User Assignment Identification Type',
'type': 'uint8',
'constants': [('NONE', 0),
              ('DENIED', 1),
              ('UNDEFINED', 2),
              ('ISO14443', 3),
              ('ISO15693', 4),
              ('EMAID', 5),
              ('EVCCID', 6),
              ('EVCOID', 7),
              ('ISO7812', 8),
              ('CARD TXN NR', 9),
              ('CENTRAL', 10),
              ('CENTRAL 1', 11),
              ('CENTRAL 2', 12),
              ('LOCAL', 13),
              ('LOCAL 1', 14),
              ('LOCAL 2', 15),
              ('PHONE NUMBER', 16),
              ('KEY CODE', 17)]
})

com['constant_groups'].append({
'name': 'Eichrecht Charge Point Identification Type',
'type': 'uint8',
'constants': [('EVSEID', 0),
              ('CBIDC', 1)]
})

com['constant_groups'].append({
'name': 'Eichrecht Signature Status',
'type': 'uint16',
'constants': [('Not Initialised', 0),
              ('Idle', 1),
              ('Signature In Progress', 2),
              ('Signature OK', 15),
              ('Invalid Date Time', 128),
              ('Checksum Error', 129),
              ('Invalid Command', 130),
              ('Invalid State', 131),
              ('Invalid Measurement', 132),
              ('Test Mode Error', 133),
              ('Verify State Error', 243),
              ('Signature State Error', 244),
              ('Keypair Generation', 245),
              ('SHA Failed', 246),
              ('Init Failed', 247),
              ('Data Not Locked', 248),
              ('Config Not Locked', 249),
              ('Verify Error', 250),
              ('Public Key Error', 251),
              ('Invalid Message Format', 252),
              ('Invalid Message Size', 253),
              ('Signature Error', 254),
              ('Undefined Error', 255)]
})

com['constant_groups'].append({
'name': 'Eichrecht Signature Format',
'type': 'uint16',
'constants': [('ASN1', 0),
              ('Base64', 1)]
})

com['constant_groups'].append({
'name': 'Eichrecht Measurement Status',
'type': 'uint16',
'constants': [('Idle', 0),
              ('Active', 1),
              ('Active After Power Failure', 2),
              ('Active After Reset', 3)]
})

com['constant_groups'].append({
'name': 'Eichrecht Transaction Command',
'type': 'char',
'constants': [('Begin', 'B'),
              ('End', 'E'),
              ('Intermediate', 'C'),
              ('Exception', 'X'),
              ('Tariff Change', 'T'),
              ('Suspended', 'S'),
              ('End With Begin', 'r'),
              ('Fiscal Reading', 'f'),
              ('Hold Command', 'h'),
              ('Last Charge Reading', 'i')]
})

com['constant_groups'].append({
'name': 'Phase Switch Wait Time',
'type': 'uint8',
'constants': [('Default', 0)] + [(f'{15 + i * 5} Seconds', i + 1) for i in range(22)] # Default + 15s to 120s in 5s steps
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
Returns the current state of the EVSE.

* IEC61851 State: State according to IEC 61851 (A = not connected,
  B = connected, C = charging, D = unused, EF = error).
* Charger State: High level state of the charging process.
* Contactor State: State of the contactor (relays for N+L1 and L2+L3).
* Contactor Error: Error code of the contactor check, 0 means OK.
* Allowed Charging Current: Charging current that is currently allowed in mA
  (minimum over all active charging slots).
* Error State: 0 if everything is OK, otherwise the current error.
* Lock State: State of the type 2 socket lock motor.
* DC Fault Current State: State of the DC fault current protection.
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
Returns the hardware configuration of the EVSE.

* Jumper Configuration: Maximum current of the incoming cable as configured
  through the slide switch.
* Has Lock Switch: *true* if a type 2 socket lock motor is connected.
* EVSE Version: Hardware version of the EVSE (e.g. 20 for EVSE 2.0, 30 for
  3.0 and 40 for 4.0).
* Energy Meter Type: Type of the connected energy meter (Not Available if no
  energy meter is connected).
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
             ('Car Stopped Charging', 'bool', 1, 'out'),
             ('Time Since State Change', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Time Since DC Fault Check', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'}),
             ('Uptime', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the low level state of the EVSE. This is mostly useful for debugging.

* LED State: State of the status LED.
* CP PWM Duty Cycle: Duty cycle of the CP (control pilot) PWM in 1/10 %.
* ADC Values: Raw ADC values of the voltage measurements.
* Voltages: Measured voltages (CP/PE before and after the resistor for high
  and low PWM, PP/PE and the +12V and -12V rails).
* Resistances: Calculated resistances (CP/PE and PP/PE).
* GPIO: State of the GPIO pins.
* Car Stopped Charging: *true* if the car stopped the charging by itself.
* Time Since State Change: Time since the last IEC 61851 state change.
* Time Since DC Fault Check: Time since the last DC fault current check.
* Uptime: Uptime of the EVSE.
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
Sets the configuration of a charging slot. The EVSE has 20 charging slots
(0-19). The charging current that is allowed is the minimum of the maximum
current of all active slots.

* Slot: Index of the slot (0-19).
* Max Current: Maximum current of the slot in mA. 0 blocks charging.
* Active: *true* if the slot is taken into account.
* Clear On Disconnect: *true* if the slot should be deactivated when the
  cable is disconnected.

The following slots have a fixed meaning:

* 0: Incoming cable (read-only, configured through slide switch).
* 1: Outgoing cable (read-only, configured through resistor).
* 2: GPIO input 0 (shutdown input).
* 3: GPIO input 1 (input).
* 4: Button (0A <-> 32A, can be controlled from the web interface with the
  start button and the physical button if configured).
""",
'de':
"""
TODO
""",
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
Sets the maximum current of a charging slot, see :func:`Set Charging Slot`.
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
Activates/deactivates a charging slot, see :func:`Set Charging Slot`.
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
Sets the clear-on-disconnect flag of a charging slot, see
:func:`Set Charging Slot`.
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
Returns the configuration of a charging slot as set by
:func:`Set Charging Slot`.
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
Returns the configuration of all 20 charging slots, see
:func:`Set Charging Slot`.

The active and clear-on-disconnect flags are packed: bit 0 is the active flag
and bit 1 is the clear-on-disconnect flag.
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
Sets the default configuration of a charging slot. The default values are
used to initialize the charging slots on startup. Slots 0 and 1 (the cables)
have no default and can not be configured here.

See :func:`Set Charging Slot` for the meaning of the parameters.
""",
'de':
"""
TODO
""",
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
Returns the default configuration of a charging slot as set by
:func:`Set Charging Slot Default`.
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
Returns the measured values of the connected energy meter.

* Power: Total active power in W.
* Current: Current per phase (L1, L2, L3) in A.
* Phases Active: For each phase *true* if current is currently flowing.
* Phases Connected: For each phase *true* if the phase is connected.
""",
'de':
"""
TODO
""",
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get All Energy Meter Values Low Level',
'elements': [('Values Length', 'uint16', 1, 'out', {}),
             ('Values Chunk Offset', 'uint16', 1, 'out', {}),
             ('Values Chunk Data', 'float', 15, 'out', {})],
'high_level': {'stream_out': {'name': 'Values'}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all values that the connected energy meter provides. The meaning of
the values depends on the energy meter type, see
:func:`Get Hardware Configuration`.
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
Returns the Modbus communication error counters of the connected energy
meter. The counters are: local timeout, global timeout, illegal function,
illegal data address, illegal data value and slave device failure.
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
Sets the relative energy value of the energy meter to zero. This sets the
point in time from which on the relative energy meter values are counted.
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
Resets the DC fault current protection back to normal condition after a DC
fault was detected. The password is 0xDC42FA23. A new DC fault current
calibration is started immediately after the reset.

Before resetting the DC fault current protection you should make sure that
the fault is gone, otherwise the next charging session will trip it again.
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
Sets the configuration of the GPIOs.

* Shutdown Input Configuration: Defines how the shutdown input (GPIO input 0)
  reacts (e.g. shut down charging on open/close or limit to 4200 Watt).
* Input Configuration: Defines the function of GPIO input 1 (e.g. limit the
  charging current depending on the input level).
* Output Configuration: Defines the default state of the GP output (connected
  to ground or high impedance).
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
Returns the GPIO configuration as set by :func:`Set GPIO Configuration`.
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
Returns the content of the given storage page (63 bytes), see
:func:`Set Data Storage`.
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
Stores 63 bytes of data in the given storage page. This storage can be used
by the ESP32 to store its own data on the EVSE.
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
Returns the current state of the indicator LED as set by
:func:`Set Indicator LED`. The duration is the remaining duration in ms.
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
Sets the indicator LED to signal different states to the user.

* Indication: -1 leaves the control of the LED to the EVSE, 0 turns it off,
  255 turns it on, 1-254 sets a PWM value and 1001/1002/1003 show an
  acknowledge/not-acknowledge/nag indication.
* Duration: Duration of the indication in ms.
* Color H/S/V: HSV color of the LED. If the value (V) is 0 an automatic color
  is used. EVSE 2.0 only supports blue.

The returned status is 0 if the indication could be set. Otherwise the LED is
currently in use by the EVSE (e.g. blinking, flickering or breathing) and the
status is the current LED state.
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
Sets the function of the button (key switch). The button can be configured to
start charging, stop charging, both or to enumerate (see the enumerate
functions). It can also be deactivated.
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
Returns the button configuration as set by :func:`Set Button Configuration`.
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
Returns the state of the button (key switch).

The press and release time are the times (relative to the EVSE uptime) of the
last press and release. Button Pressed is *true* while the button is held down.
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
Enables/disables the EV wakeup. If enabled the EVSE adheres to IEC 61851
Annex A.5.3 and tries to wake up the electric vehicle after a long period of
inactivity. This helps with some legacy EVs that do not wake up by themselves.
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
Returns the EV wakeup setting as set by :func:`Set EV Wakeup`.
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
Disconnects/connects the control pilot (CP) from the electric vehicle. This
can be used to stop a charging session without opening the contactor.

The CP can only be disconnected in IEC 61851 state A or B and only if the
contactor is currently not active. The returned value shows whether the CP is
now disconnected.
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
Returns the control pilot disconnect state as set by
:func:`Set Control Pilot Disconnect`.
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
Returns the values of :func:`Get State`, :func:`Get Hardware Configuration`,
:func:`Get Energy Meter Values` and :func:`Get Energy Meter Errors` combined
in one call.
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
             ('Enumerate Value', 'uint8', 1, 'out'), # Returns new value if stable for > 2 seconds
             ('Enumerate Value Change Time', 'uint32', 1, 'out'), # EVSE uptime of last value change
             ('Phase Switch Wait Time', 'uint8', 1, 'out', {'constant_group': 'Phase Switch Wait Time'}),
             ('PLC Modem Enabled', 'bool', 1, 'out'),
],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the values of :func:`Get GPIO Configuration`,
:func:`Get Indicator LED`, :func:`Get Button Configuration`,
:func:`Get Button State`, :func:`Get EV Wakuep`,
:func:`Get Control Pilot Disconnect`, :func:`Get Boost Mode`,
:func:`Get Temperature`, :func:`Get Phase Control`,
:func:`Get Phase Auto Switch`, :func:`Get Phases Connected`,
:func:`Get Enumerate Value`, :func:`Get Phase Switch Wait Time` and
:func:`Get PLC Modem` combined in one call.
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
Resets the EVSE to the factory settings. The password is 0x2342FACD.
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
Returns the amount of time the button was continuously pressed during boot in
ms. This can be used to detect a long button press during startup (e.g. to
trigger a factory reset). Returns 0xFFFFFFFF if the boot press was already
reset.

If Reset is set to *true* the value is reset after it has been read.
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
Enables/disables the boost mode. In boost mode the duty cycle of the CP PWM
signal is increased by about 4µs (which stays within the IEC 61851
tolerance). This signals a slightly higher current to the car, which allows
some cars to charge a bit faster. Boost mode is disabled by default.
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
Returns the boost mode setting as set by :func:`Set Boost Mode`.
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
Triggers a test of the DC fault current protection. The password is
0xDCFAE550. This can only be started in IEC 61851 state A (not connected) and
if no calibration is currently running. The returned value shows whether the
test was started.
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
Sets the state of the general purpose output (connected to ground or high
impedance). The default state after boot is set with
:func:`Set GPIO Configuration`. Only available for EVSE 2.0.
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
Returns the temperature of the EVSE in 1/100 °C. EVSE 2.0 has no temperature
sensor and always returns 0.
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
Sets the number of phases that are used for charging (1 or 3). This requires
the hardware to support phase switching (EVSE 3.0 and newer). On EVSE 2.0 this
function has no effect.
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
Returns the current phase control state.

* Phases Current: Number of phases currently used for charging (1 or 3).
* Phases Requested: Number of phases requested by :func:`Set Phase Control`.
* Phases State: Progress state of an ongoing phase switch.
* Phases Info: 0 if normal, 1 if forced to one phase by the auto-switch.
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
Enables/disables automatic phase switching. If enabled the EVSE switches
between one and three phases depending on the available charging current. This
requires the hardware to support phase switching (EVSE 3.0 and newer) and is
ignored on EVSE 2.0.
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
Returns the phase auto switch setting as set by :func:`Set Phase Auto Switch`.
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
Sets the number of phases that are physically connected to the EVSE (1 or 3).
This is used by the phase control to know how many phases are available.
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
Returns the number of connected phases as set by :func:`Set Phases Connected`.
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
This callback is triggered with the latest energy meter values, see
:func:`Get Energy Meter Values`. It is called whenever new values are
available from the connected energy meter.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Charging Protocol',
'elements': [('Charging Protocol', 'uint8', 1, 'in', {'constant_group': 'Charging Protocol'}),
             ('CP Duty Cycle', 'uint16', 1, 'in')], # Only used when protocol is ISO15118, only 50 (5%) and 1000 (100%) are accepted
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the charging protocol that is used (IEC 61851 or ISO 15118). The CP duty
cycle is only used for ISO 15118, where only 50 (5%) and 1000 (100%) are
accepted. This requires ISO 15118 support (EVSE 4.0) and has no effect
otherwise.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Charging Protocol',
'elements': [('Charging Protocol', 'uint8', 1, 'out', {'constant_group': 'Charging Protocol'}),
             ('CP Duty Cycle', 'uint16', 1, 'out')], # Only used when protocol is ISO15118, only 50 (5%) and 1000 (100%) are accepted
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the charging protocol as set by :func:`Set Charging Protocol`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Eichrecht Gateway Identification',
'elements': [('Gateway Identification', 'char', 41, 'in'), # GI
             ('Eichrecht State', 'uint8', 1, 'out', {'constant_group': 'Eichrecht State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the gateway identification (OCMF field "GI") for the calibration law
(Eichrecht) signed metering. This requires an Eichrecht-capable energy meter
(EVSE 4.0). The returned state shows whether the value could be set.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Eichrecht Gateway Identification',
'elements': [('Gateway Identification', 'char', 41, 'out')], # GI
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the gateway identification as set by
:func:`Set Eichrecht Gateway Identification`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Eichrecht Gateway Serial',
'elements': [('Gateway Serial', 'char', 25, 'in'), # GS
             ('Eichrecht State', 'uint8', 1, 'out', {'constant_group': 'Eichrecht State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the gateway serial (OCMF field "GS") for the calibration law
(Eichrecht) signed metering. This requires an Eichrecht-capable energy meter
(EVSE 4.0). The returned state shows whether the value could be set.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Eichrecht Gateway Serial',
'elements': [('Gateway Serial', 'char', 25, 'out')], # GS
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the gateway serial as set by :func:`Set Eichrecht Gateway Serial`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Eichrecht User Assignment',
'elements': [('Identification Status', 'bool', 1, 'in'), # IS
             ('Identification Flags', 'uint8', 4, 'in', {'constant_group': 'Eichrecht User Assignment Identification Flag'}), # IF
             ('Identification Type', 'uint8', 1, 'in', {'constant_group': 'Eichrecht User Assignment Identification Type'}), # IT
             ('Identification Data', 'char', 40, 'in'), # ID
             ('Eichrecht State', 'uint8', 1, 'out', {'constant_group': 'Eichrecht State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the user assignment (OCMF fields "IS", "IF", "IT" and "ID") for the
calibration law (Eichrecht) signed metering. It identifies the user of a
charging transaction.

* Identification Status: *true* if a user is assigned.
* Identification Flags: Identification flags (up to 4 entries).
* Identification Type: Type of the identification data.
* Identification Data: The identification data itself.

This requires an Eichrecht-capable energy meter (EVSE 4.0). The returned state
shows whether the value could be set.
""",
'de':
"""
TODO
""",
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Eichrecht User Assignment',
'elements': [('Identification Status', 'bool', 1, 'out'), # IS
             ('Identification Flags', 'uint8', 4, 'out', {'constant_group': 'Eichrecht User Assignment Identification Flag'}), # IF
             ('Identification Type', 'uint8', 1, 'out', {'constant_group': 'Eichrecht User Assignment Identification Type'}), # IT
             ('Identification Data', 'char', 40, 'out')], # ID
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the user assignment as set by :func:`Set Eichrecht User Assignment`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Eichrecht Charge Point',
'elements': [('Identification Type', 'uint8', 1, 'in', {'constant_group': 'Eichrecht Charge Point Identification Type'}), # CT
             ('Identification', 'char', 20, 'in'), # CI
             ('Eichrecht State', 'uint8', 1, 'out', {'constant_group': 'Eichrecht State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the charge point identification (OCMF fields "CT" and "CI") for the
calibration law (Eichrecht) signed metering. This requires an
Eichrecht-capable energy meter (EVSE 4.0). The returned state shows whether
the value could be set.
""",
'de':
"""
TODO
""",
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Eichrecht Charge Point',
'elements': [('Identification Type', 'uint8', 1, 'out', {'constant_group': 'Eichrecht Charge Point Identification Type'}), # CT
             ('Identification', 'char', 20, 'out')], # CI
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the charge point identification as set by
:func:`Set Eichrecht Charge Point`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Eichrecht Transaction',
'elements': [('Transaction', 'char', 1, 'in', {'constant_group': 'Eichrecht Transaction Command'}),
             ('Unix Time', 'uint32', 1, 'in'), # Seconds, Iskra uses uint32 for unix time instead of standard int32, so it goes to the year 2106... good enough.
             ('UTC Time Offset', 'int16', 1, 'in', {'range': (-719, 720)}), # Minutes
             ('Signature Format', 'uint16', 1, 'in', {'constant_group': 'Eichrecht Signature Format'}),
             ('Eichrecht State', 'uint8', 1, 'out', {'constant_group': 'Eichrecht State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Starts or modifies Eichrecht transaction. A transaction
generates a signed OCMF dataset (e.g. at the begin and end of a charging
session).

* Transaction: The transaction command (e.g. begin or end).
* Unix Time: The current time as unix timestamp in seconds.
* UTC Time Offset: The local time offset to UTC in minutes.
* Signature Format: The format of the generated signature (ASN.1 or Base64).

The signed dataset and signature are returned through the
:cb:`Eichrecht Dataset Low Level` and :cb:`Eichrecht Signature Low Level`
callbacks. This requires an Eichrecht-capable energy meter (EVSE 4.0). The
returned state shows whether the transaction could be started.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Eichrecht Transaction State',
'elements': [('Transaction', 'char', 1, 'out', {'constant_group': 'Eichrecht Transaction Command'}),
             ('Transaction State', 'uint8', 1, 'out'),
             ('Transaction Inner State', 'uint8', 1, 'out'),
             ('Measurement Status', 'uint16', 1, 'out', {'constant_group': 'Eichrecht Measurement Status'}),
             ('Signature Status', 'uint16', 1, 'out', {'constant_group': 'Eichrecht Signature Status'}),
             ('Eichrecht State', 'uint8', 1, 'out', {'constant_group': 'Eichrecht State'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the state of the current Eichrecht transaction, see
:func:`Set Eichrecht Transaction`. It includes the current transaction
command, the transaction and inner state, and the measurement and signature
status of the energy meter.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Eichrecht Public Key',
'elements': [('Public Key', 'uint8', 64, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
Returns the public key of the energy meter that is used to verify the
Eichrecht signatures.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Eichrecht Dataset Low Level',
'elements': [('Message Length', 'uint16', 1, 'out', {}),
             ('Message Chunk Offset', 'uint16', 1, 'out', {}),
             ('Message Chunk Data', 'char', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered after a Eichrecht transaction was
started with :func:`Set Eichrecht Transaction`. It contains the signed OCMF
dataset. The corresponding signature is delivered through the
:cb:`Eichrecht Signature Low Level` callback.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Eichrecht Signature Low Level',
'elements': [('Message Length', 'uint16', 1, 'out', {}),
             ('Message Chunk Offset', 'uint16', 1, 'out', {}),
             ('Message Chunk Data', 'char', 60, 'out', {})],
'high_level': {'stream_out': {'name': 'Message'}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered after the :cb:`Eichrecht Dataset Low Level`
callback. It contains the signature of the signed OCMF dataset of the
Eichrecht transaction.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Enumerate Configuration',
'elements': [('Enumerator H', 'uint16', 8, 'in'), # HSV Hue; ignore entries == 0 starting at end
             ('Enumerator S', 'uint8', 8, 'in'),  # HSV Hue; ignore entries == 0 starting at end
             ('Enumerator V', 'uint8', 8, 'in')], # HSV Hue; ignore entries == 0 starting at end
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the configuration for the enumerate function of the button. The button
can step through up to 8 values, each one represented by an HSV color of the
indicator LED. Trailing entries with value (V) 0 are ignored.

The button function must be set to enumerate with
:func:`Set Button Configuration`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enumerate Configuration',
'elements': [('Enumerator H', 'uint16', 8, 'out'), # HSV Hue; ignore entries == 0 starting at end
             ('Enumerator S', 'uint8', 8, 'out'),  # HSV Hue; ignore entries == 0 starting at end
             ('Enumerator V', 'uint8', 8, 'out')], # HSV Hue; ignore entries == 0 starting at end
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the enumerate configuration as set by
:func:`Set Enumerate Configuration`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Enumerate Value',
'elements': [('Value', 'uint8', 1, 'in')], # Sets enumerate value immediately
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the current enumerate value immediately, see
:func:`Set Enumerate Configuration`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Enumerate Value',
'elements': [('Value', 'uint8', 1, 'out'), # Returns new value if stable for > 2 seconds
             ('Value Change Time', 'uint32', 1, 'out')], # EVSE uptime of last value change
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current enumerate value and the EVSE uptime (in ms) of the last
value change. A new value is only reported once it has been stable for more
than 2 seconds. See :func:`Set Enumerate Configuration`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Phase Switch Wait Time',
'elements': [('Phase Switch Wait Time', 'uint8', 1, 'in', {'constant_group': 'Phase Switch Wait Time'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the minimum wait time between two phase switches (15s to 120s, or
default). The wait time prevents the phases from being switched too often.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Phase Switch Wait Time',
'elements': [('Phase Switch Wait Time', 'uint8', 1, 'out', {'constant_group': 'Phase Switch Wait Time'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the phase switch wait time as set by
:func:`Set Phase Switch Wait Time`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set PLC Modem',
'elements': [('PLC Modem Enabled', 'bool', 1, 'in')], # default True
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables the PLC (powerline communication) modem that is used for
ISO 15118 communication. The PLC modem is enabled by default. Only available
on hardware with a PLC modem (EVSE 4.0).
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get PLC Modem',
'elements': [('PLC Modem Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the PLC modem setting as set by :func:`Set PLC Modem`.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Test Mode',
'elements': [('Test Mode Enabled', 'bool', 1, 'in'), # default False
             ('Password', 'uint32', 1, 'in')],       # 0xdeadbeef
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Enables/disables the test mode. The password is 0xDEADBEEF. The test mode is
used during production and should normally not be needed. It is disabled by
default.
""",
'de':
"""
TODO
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Test Mode',
'elements': [('Test Mode Enabled', 'bool', 1, 'out')],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the test mode setting as set by :func:`Set Test Mode`.
""",
'de':
"""
TODO
"""
}]
})

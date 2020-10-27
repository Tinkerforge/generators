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
    'device_identifier': 2152,
    'name': 'Energy Monitor',
    'display_name': 'Energy Monitor',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': 'Measures Voltage, Current, Energy, Real/Apparent/Reactive Power, Power Factor and Frequency',
        'de': 'Misst Spannung, Strom, Energie, Wirk-/Schein-/Blindleistung, Leistungsfactor und Frequenz'
    },
    'released': True,
    'documented': True,
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

com['packets'].append({
'type': 'function',
'name': 'Get Energy Data',
'elements': [('Voltage', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Volt'}),
             ('Current', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Ampere'}),
             ('Energy', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Watt Hour'}),
             ('Real Power', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Watt'}),
             ('Apparent Power', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Volt Ampere'}),
             ('Reactive Power', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Volt Ampere Reactive'}),
             ('Power Factor', 'uint16', 1, 'out', {'scale': (1, 1000)}),
             ('Frequency', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Hertz'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all of the measurements that are done by the Energy Monitor Bricklet.

* Voltage RMS
* Current RMS
* Energy (integrated over time)
* Real Power
* Apparent Power
* Reactive Power
* Power Factor
* Frequency (AC Frequency of the mains voltage)

The frequency is recalculated every 6 seconds.

All other values are integrated over 10 zero-crossings of the voltage sine wave.
With a standard AC mains voltage frequency of 50Hz this results in a 5 measurements
per second (or an integration time of 200ms per measurement).

If no voltage transformer is connected, the Bricklet will use the current waveform
to calculate the frequency and it will use an integration time of
10 zero-crossings of the current waveform.
""",
'de':
"""
Gibt alle Messdaten des Energy Monitor Bricklets zurück.

* Voltage: RMS-Spannung (Effektivwert)
* Current: RMS-Strom (Effektivwert)
* Energy: Energie (integriert über Zeit)
* Real Power: Wirkleistung
* Apparent Power: Scheinleistung
* Reactive Power: Blindleistung
* Power Factor: Leistungsfaktor
* Frequency: AC-Frequenz der Netzspannung

Die Frequenz wird alle 6 Sekunden neu berechnet.

Alle anderen Werte werden über 10 Nulldurchgänge der Spannungs-Sinuskurve integriert.
Mit einer Standard Netzspannungsfrequenz von 50Hz entspricht das 5 Messungen pro Sekunde
(oder einer Integrationszeit von 200ms pro Messung).

Wenn kein Spannungstransformator angeschlossen ist, nutzt das Bricklet den Kurvenverlauf
des Stroms, um die Frequenz zu bestimmen und die Integrationszeit beträgt 10 Nulldurchläufe
der Strom-Sinuskurve.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Reset Energy',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the energy value (see :func:`Get Energy Data`) back to 0Wh.
""",
'de':
"""
Setzt den Energiewert (siehe :func:`Get Energy Data`) zurück auf 0Wh
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Waveform Low Level',
'elements': [('Waveform Chunk Offset', 'uint16', 1, 'out', {}),
             ('Waveform Chunk Data', 'int16', 30, 'out', {})],
'high_level': {'stream_out': {'name': 'Waveform', 'fixed_length': (1024-256)*2}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns a snapshot of the voltage and current waveform. The values
in the returned array alternate between voltage and current. The data from
one getter call contains 768 data points for voltage and current, which
correspond to about 3 full sine waves.

The voltage is given with a resolution of 100mV and the current is given
with a resolution of 10mA.

This data is meant to be used for a non-realtime graphical representation of
the voltage and current waveforms.
""",
'de':
"""
Gibt eine Momentaufnahme des Spannungs- und Stromkurvenverlaufs zurück. Die
Werte im zurückgegebenen Array alternieren zwischen Spannung und Strom. Die
Daten eines Getter-Aufrufs beinhalten 768 Datenpunkte für Spannung und Strom,
diese korrespondieren zu ungefähr 3 vollen Sinuskurven.

Die Spannung hat eine Auflösung von 100mV und der Strom hat eine Auflösung
von 10mA.

Die Daten können für eine grafische Repräsentation (nicht-Realzeit) der
Kurvenverläufe genutzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Transformer Status',
'elements': [('Voltage Transformer Connected', 'bool', 1, 'out', {}),
             ('Current Transformer Connected', 'bool', 1, 'out', {})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns *true* if a voltage/current transformer is connected to the Bricklet.
""",
'de':
"""
Gibt *true* zurück wenn ein Spannungs-/Stromtransformator mit dem Bricklet verbunden ist.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Transformer Calibration',
'elements': [('Voltage Ratio', 'uint16', 1, 'in', {'default': 1923}),
             ('Current Ratio', 'uint16', 1, 'in', {'default': 3000}),
             ('Phase Shift', 'int16', 1, 'in', {'range': (0, 0), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the transformer ratio for the voltage and current transformer in 1/100 form.

Example: If your mains voltage is 230V, you use 9V voltage transformer and a
1V:30A current clamp your voltage ratio is 230/9 = 25.56 and your current ratio
is 30/1 = 30.

In this case you have to set the values 2556 and 3000 for voltage ratio and current
ratio.

The calibration is saved in non-volatile memory, you only have to set it once.

Set the phase shift to 0. It is for future use and currently not supported by the Bricklet.
""",
'de':
"""
Setzt das Transformer-Verhältnis für Strom und Spannung in Hundertstel.

Beispiel: Wenn die Netzspannung 230V beträgt und ein 9V Spannungstransformer sowie
eine 1V:30A Spannungszange verwendet wird, ergibt das ein Spannungsverhältnis von
230/9 = 25,56 und ein Stromverhältnis von 30/1 = 30.

In diesem Fall müssten also die Werte 2556 und 3000 gesetzt werden.

Die Kalibrierung wird in nicht-flüchtigem Speicher gespeichert und muss nur einmal
gesetzt werden.

Der Parameter *Phase Shift* muss auf 0 gesetzt werden. Dieser Parameter wird
aktuell von der Firmware nicht genutzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Transformer Calibration',
'elements': [('Voltage Ratio', 'uint16', 1, 'out', {'default': 1923}),
             ('Current Ratio', 'uint16', 1, 'out', {'default': 3000}),
             ('Phase Shift', 'int16', 1, 'out', {'range': (0, 0), 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the transformer calibration as set by :func:`Set Transformer Calibration`.
""",
'de':
"""
Gibt die Transformator-Kalibrierung zurück, wie von :func:`Set Transformer Calibration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Calibrate Offset',
'elements': [],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Calling this function will start an offset calibration. The offset calibration will
integrate the voltage and current waveform over a longer time period to find the 0
transition point in the sine wave.

The Bricklet comes with a factory-calibrated offset value, you should not have to
call this function.

If you want to re-calibrate the offset we recommend that you connect a load that
has a smooth sinusoidal voltage and current waveform. Alternatively you can also
short both inputs.

The calibration is saved in non-volatile memory, you only have to set it once.
""",
'de':
"""
Ein Aufruf dieser Funktion startet eine Offset-Kalibrierung. Dazu werden die
Spannungs- und Stromkurvenverläufe über einen längeren Zeitraum aufsummiert, um
den Nulldurchgangspunkt der Sinuskurve zu finden.

Der Offset für das Bricklet wird von Tinkerforge ab Werk kalibriert. Ein Aufruf dieser
Funktion sollte also nicht notwendig sein.

Wenn der Offset rekalibriert werden soll, empfehlen wir entweder eine Last
anzuschließen, die eine glatte Sinuskurve für Spannung und Strom erzeugt, oder
die beiden Eingänge kurzzuschließen.

Die Kalibrierung wird in nicht-flüchtigem Speicher gespeichert und muss nur einmal
gesetzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Energy Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'in', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period is the period with which the :cb:`Energy Data`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.
""",
'de':
"""
Die Periode ist die Periode mit der der :cb:`Energy Data`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out', {'scale': (1, 1000), 'unit': 'Second', 'default': 0}),
             ('Value Has To Change', 'bool', 1, 'out', {'default': False})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the callback configuration as set by
:func:`Set Energy Data Callback Configuration`.
""",
'de':
"""
Gibt die Callback-Konfiguration zurück, wie mittels
:func:`Set Energy Data Callback Configuration` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Energy Data',
'elements': [('Voltage', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Volt'}),
             ('Current', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Ampere'}),
             ('Energy', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Watt Hour'}),
             ('Real Power', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Watt'}),
             ('Apparent Power', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Volt Ampere'}),
             ('Reactive Power', 'int32', 1, 'out', {'scale': (1, 100), 'unit': 'Volt Ampere Reactive'}),
             ('Power Factor', 'uint16', 1, 'out', {'scale': (1, 1000)}),
             ('Frequency', 'uint16', 1, 'out', {'scale': (1, 100), 'unit': 'Hertz'})],
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered periodically according to the configuration set by
:func:`Set Energy Data Callback Configuration`.

The :word:`parameters` are the same as :func:`Get Energy Data`.
""",
'de':
"""
Dieser Callback wird periodisch ausgelöst abhängig von der mittels
:func:`Set Energy Data Callback Configuration` gesetzten Konfiguration

Die :word:`parameters` sind der gleiche wie :func:`Get Energy Data`.
"""
}]
})

com['examples'].append({
'name': 'Simple',
'functions': [('getter', ('Get Energy Data', 'energy data'), [(('Voltage', 'Voltage'), 'int32', 1, 100, 'V', None),
                                                              (('Current', 'Current'), 'int32', 1, 100, 'A', None),
                                                              (('Energy', 'Energy'), 'int32', 1, 100, 'Wh', None),
                                                              (('Real Power', 'Real Power'), 'int32', 1, 100, 'h', None),
                                                              (('Apparent Power', 'Apparent Power'), 'int32', 1, 100, 'VA', None),
                                                              (('Reactive Power', 'Reactive Power'), 'int32', 1, 100, 'var', None),
                                                              (('Power Factor', 'Power Factor'), 'uint16', 1, 1000, None, None),
                                                              (('Frequency', 'Frequency'), 'uint16', 1, 100, 'Hz', None)
], [])]})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Energy Data', 'energy data'), [(('Voltage', 'Voltage'), 'int32', 1, 100, 'V', None),
                                                            (('Current', 'Current'), 'int32', 1, 100, 'A', None),
                                                            (('Energy', 'Energy'), 'int32', 1, 100, 'Wh', None),
                                                            (('Real Power', 'Real Power'), 'int32', 1, 100, 'h', None),
                                                            (('Apparent Power', 'Apparent Power'), 'int32', 1, 100, 'VA', None),
                                                            (('Reactive Power', 'Reactive Power'), 'int32', 1, 100, 'var', None),
                                                            (('Power Factor', 'Power Factor'), 'uint16', 1, 1000, None, None),
                                                            (('Frequency', 'Frequency'), 'uint16', 1, 100, 'Hz', None)], None, None),
              ('callback_configuration', ('Energy Data', 'energy data'), [], 1000, False, None, [])]
})


integration_info_en = 'Integrated over 10 zero-crossings of the voltage sine wave. With a standard AC mains voltage frequency of 50Hz this results in a 5 measurements per second (or an integration time of 200ms per measurement). If no voltage transformer is connected, the Bricklet will use the current waveform to calculate the frequency and it will use an integration time of 10 zero-crossings of the current waveform.'
integration_info_de = 'Über 10 Nulldurchgänge der Spannungs-Sinuskurve integriert. Mit einer Standard Netzspannungsfrequenz von 50Hz entspricht das 5 Messungen pro Sekunde (oder einer Integrationszeit von 200ms pro Messung). Wenn kein Spannungstransformator angeschlossen ist, nutzt das Bricklet den Kurvenverlauf des Stroms, um die Frequenz zu bestimmen und die Integrationszeit beträgt 10 Nulldurchläufe der Strom-Sinuskurve.'

def energyDataChannel(id_, type_):
    return {
        'id': id_,
        'type': type_,
        'getters': [{
            'packet': 'Get Energy Data',
            'element': '{title_words}',
            'packet_params': [],
            'transform': 'new {number_type}(value.{headless}{divisor}{unit})'}],
        'callbacks': [{
            'packet': 'Energy Data',
            'element': '{title_words}',
            'transform': 'new {number_type}({headless}{divisor}{unit})'}],

    }

com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.StringType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [
        update_interval('Set Energy Data Callback Configuration', 'Period', 'Energy Data', 'all energy data')
    ],
    'init_code': """this.setEnergyDataCallbackConfiguration(cfg.energyDataUpdateInterval, true);""",
    'dispose_code': """this.setEnergyDataCallbackConfiguration(0, true);""",
    'channels': [
        energyDataChannel('Voltage', 'Voltage'),
        energyDataChannel('Current', 'Current'),
        energyDataChannel('Energy', 'Energy'),
        energyDataChannel('Real Power', 'RealPower'),
        energyDataChannel('Apparent Power', 'AppPower'),
        energyDataChannel('Reactive Power', 'ReacPower'),
        energyDataChannel('Power Factor', 'Factor'),
        energyDataChannel('Frequency', 'Frequency'),
        {
            'id': 'Reset Energy',
            'type': 'Reset',

            'setters': [{
                'packet': 'Reset Energy',
                'command_type': "StringType"
            }],
        }
    ],
    'channel_types': [
        oh_generic_channel_type('Voltage', 'Number', {'en': 'Voltage', 'de': 'Spannung'},
                    update_style=None,
                    description={'en': 'Root mean square voltage.\n\n'+integration_info_en,
                                 'de': 'Effektivwert der Spannung.\n\n' + integration_info_de}),
        oh_generic_channel_type('Current', 'Number', {'en': 'Current', 'de': 'Stromstärke'},
                    update_style=None,
                    description={'en': 'Root mean square current.\n\n'+integration_info_en,
                                 'de': 'Effektivwert der Stromstärke.\n\n' + integration_info_de}),
        oh_generic_channel_type('Energy', 'Number', {'en': 'Energy', 'de': 'Energie'},
                    update_style=None,
                    description={'en': 'Energy (integrated over time)\n\n'+integration_info_en,
                                 'de': 'Energie (integriert über Zeit)\n\n'+integration_info_de}),
        oh_generic_channel_type('RealPower', 'Number', {'en': 'Real Power','de': 'Wirkleistung'},
                    update_style=None,
                    description={'en': 'Real Power\n\n'+integration_info_en,
                                 'de': 'Wirkleistung\n\n'+integration_info_de}),
        oh_generic_channel_type('AppPower', 'Number', {'en': 'Apparent Power', 'de': 'Scheinleistung'},
                    update_style=None,
                    description={'en': 'Apparent Power\n\n'+integration_info_en,
                                 'de': 'Scheinleistung\n\n'+integration_info_de},
                    pattern='%.2f VA'),
        oh_generic_channel_type('ReacPower', 'Number', {'en': 'Reactive Power', 'de': 'Blindleistung'},
                    update_style=None,
                    description={'en': 'Reactive Power\n\n'+integration_info_en,
                                 'de': 'Blindleistung\n\n'+integration_info_de},
                    pattern='%.2f var'),
        oh_generic_channel_type('Factor', 'Number', {'en': 'Power Factor', 'de': 'Leistungsfaktor'},
                    update_style=None,
                    description={'en': 'Power Factor\n\n'+integration_info_en,
                                 'de': 'Leistungsfaktor\n\n'+integration_info_de}),
        oh_generic_channel_type('Frequency', 'Number', {'en': 'Frequency', 'de': 'Frequenz'},
                    update_style=None,
                    description={'en': 'AC Frequency of the mains voltage\n\nThe frequency is recalculated every 6 seconds.',
                                 'de': 'AC-Frequenz der Netzspannung\n\nDie Frequenz wird alle 6 Sekunden neu berechnet'}),
        oh_generic_channel_type('Reset', 'String', {'en': 'Reset Energy Value', 'de': 'Energiewert zurücksetzen'},
                    update_style=None,
                    description={'en': 'Sets the energy value back to 0 Wh',
                                 'de': 'Setzt den Energiewert zurück auf 0Wh'},
                    command_options=[('Reset', 'RESET')])
    ],
    'actions': ['Get Energy Data', 'Reset Energy', 'Get Waveform', 'Get Transformer Status', 'Get Transformer Calibration']
}

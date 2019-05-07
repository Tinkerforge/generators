# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Energy Monitor Bricklet communication config

from commonconstants import THRESHOLD_OPTION_CONSTANTS
from commonconstants import add_callback_value_function

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
    'released': False,
    'documented': False,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'packets': [],
    'examples': []
}


com['packets'].append({
'type': 'function',
'name': 'Get Energy Data',
'elements': [('Voltage', 'int32', 1, 'out'),        # 10mV RMS
             ('Current', 'int32', 1, 'out'),        # 10mA RMS
             ('Energy', 'int32', 1, 'out'),         # 10mWh
             ('Real Power', 'int32', 1, 'out'),     # 10mW
             ('Apparent Power', 'int32', 1, 'out'), # 10mVA
             ('Reactive Power', 'int32', 1, 'out'), # 10mVAR
             ('Power Factor', 'uint16', 1, 'out'),  # 1/1000
             ('Frequency', 'uint16', 1, 'out')],    # 1/100Hz
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns all of the measurements that are done by the Energy Monitor Bricklet.

* Voltage (V): Voltage RMS with a resolution of 10mV (example: 230.05V = 23005)
* Current (A): Current RMS with a resolution of 10mA (example: 1.42A = 142)
* Energy (Wh): Energy (integrated over time) with a resoluton of 10mWh (example: 1.1kWh = 110000)
* Real Power (W): Real Power with a resolution of 10mW (example: 1234.56W = 123456)
* Apparent Power (VA): Apparent Power with a resolution of 10mVA (example: 1234.56VA = 123456)
* Reactive Power (VAR): Reactive Power with a resolution of 10mVAR (example: 1234.56VAR = 123456)
* Power Factor: Power Factor with a resolution of 1/1000 (example: PF 0.995 = 995)
* Frequency (Hz): AC Frequency of the mains voltage with a resolution of 1/100 Hz (example: 50Hz = 5000)

The frequency is recalculated every 6s.

All other values are integrated over 10 zero-crossings of the voltage sine wave.
With a standard AC mains voltage frequecy of 50Hz this results in a 5 measurements
per second (or an integration time of 200ms per measurement).

If no voltage transformer is connected, the Bricklet will use the current waveform
to calculate the frequency and it will use an integration time of
10 zero-crossings of the current waveform.
""",
'de':
"""
Gibt alle Messdaten des Energy Monitor Bricklets zurück.

* Voltage (V): RMS-Spannung (Effektivwert) mit einer Auflösung von 10mV (Beispiel: 230,05V = 23005)
* Current (A): RMS-Strom (Effektivwert) mit einer Auflösung von 10mA (Beispiel: 1,42A = 142)
* Energy (Wh): Energie (integriert über Zeit) mit einer Auflösung von 10mWh (Beispiel: 1,1kWh = 110000)
* Real Power (W): Wirkleistung mit einer Auflösung von 10mW (Beispiel: 1234,56W = 123456)
* Apparent Power (VA): Scheinleistung mit einer Auflösung von 10mVA (Beispiel: 1234,56VA = 123456)
* Reactive Power (VAR): Blindleistung mit einer Auflösung von 10mVAR (Beispiel: 1234,56VAR = 123456)
* Power Factor: Leistungsfaktor mit einer Auflösung von 1/1000 (Beispiel: PF 0,995 = 995)
* Frequency (Hz): AC-Frequenz der Netzspannung mit einer Auflösung von 1/100 Hz (Beispiel: 50Hz = 5000)

Die Frequenz wird alle 6s neu berechnet.

Alle anderen Werte werden integriert über 10 Nulldurchgänge der Spannungs-Sinuskurve.
Mit einer Standard AC-Netzspannungsfrequenz von 50Hz entspricht das 5 Messungen pro Sekunde
(oder eine Integrationszeit von 200ms pro Messung).

Wenn kein Spannungstransformator angeschlossen ist, nutzt das Bricklet den Kurvenverlauf
des Stroms um die Frequenz zu bestimmen und die Integrationszeit beträgt 10 Nulldurchläufe
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
'elements': [('Waveform Chunk Offset', 'uint16', 1, 'out'),
             ('Waveform Chunk Data', 'int16', 30, 'out')],
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
Daten eines Getter-Aufrufs beinhalten 768 Datenpunkte für Spannnung und Strom,
diese korrespondieren zu ungefähr 3 vollen Sinuskurven.

Die Spannung hat eine Auflösung von 100mV und der Strom hat eine Auflösung
von 10mA.

Die Daten können für eine grafische Repräsentation (nicht-realzeit) der 
Kurvenverläufe genutzt werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Transformer Status',
'elements': [('Voltage Transformer Connected', 'bool', 1, 'out'),
             ('Current Transformer Connected', 'bool', 1, 'out')],
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
'elements': [('Voltage Ratio', 'uint16', 1, 'in'),
             ('Current Ratio', 'uint16', 1, 'in'),
             ('Phase Shift', 'int16', 1, 'in')],
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

By default the voltage ratio is set to 1923 and the current ratio is set to 3000.

Set the phase shift to 0. It is for future use and currently not supported by the Bricklet.
""",
'de':
"""
Setzt das Transformer-Verhältnis für Strom und Spanning in hunderstel.

Beispiel: Wenn die Netzspannung 230V beträgt und ein 9V Spannungstransformer sowie
eine 1V:30A Spannungszange verwendet wird, ergibt das ein Spannungsverhältnis von
230/9 = 25,56 und ein Stromverhältnis von 30/1 = 30.

In diesem Fall müssten also die Werte 2556 und 3000 gesetzt werden.

Die Kalibrierung wird in nicht-flüchtigen Speicher gespeichert und muss nur einmal
gesetzt werden.

Im Auslieferungszustand ist das Spanungsverhältnis auf 1923 und das Stromverhältnis auf 3000
gesetzt.

Der Parameter *Phase Shift* muss auf 0 gesetzt werden. Dieser Parameter wird
aktuell von der Firmware nicht genutzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Transformer Calibration',
'elements': [('Voltage Ratio', 'uint16', 1, 'out'),
             ('Current Ratio', 'uint16', 1, 'out'),
             ('Phase Shift', 'int16', 1, 'out')],
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
""",
'de':
"""
Ein Aufruf dieser Funktion startet eine Offset-Kalibrierung. Dazu werden die
Spannungs- und Stromkurvenverläufe über einen längeren Zeitraum aufsummiert um
den Nulldurchgangspunkt der Sinuskurve zu finden.

Der Offset wird für das Bricklet von Tinkerforge werkskalibriert. Ein Aufruf dieser
Funktion sollte also nicht notwendig sein.

Wenn der Offset re-kalibriert werden soll empfehlen wir entweder eine Last
anzuschließen die eine glatte Sinuskurve für Spannung und Strom erzeugt oder
die beiden Eingänge kurzzuschließen.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Energy Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'in'),
             ('Value Has To Change', 'bool', 1, 'in')],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The period in ms is the period with which the :cb:`Energy Data`
callback is triggered periodically. A value of 0 turns the callback off.

If the `value has to change`-parameter is set to true, the callback is only
triggered after the value has changed. If the value didn't change within the
period, the callback is triggered immediately on change.

If it is set to false, the callback is continuously triggered with the period,
independent of the value.

The default value is (0, false).
""",
'de':
"""
Die Periode in ms ist die Periode mit der der :cb:`Energy Data`
Callback ausgelöst wird. Ein Wert von 0 schaltet den Callback ab.

Wenn der `value has to change`-Parameter auf True gesetzt wird, wird der
Callback nur ausgelöst, wenn der Wert sich im Vergleich zum letzten mal geändert
hat. Ändert der Wert sich nicht innerhalb der Periode, so wird der Callback
sofort ausgelöst, wenn der Wert sich das nächste mal ändert.

Wird der Parameter auf False gesetzt, so wird der Callback dauerhaft mit der
festen Periode ausgelöst unabhängig von den Änderungen des Werts.

Der Standardwert ist (0, false).
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Energy Data Callback Configuration',
'elements': [('Period', 'uint32', 1, 'out'),
             ('Value Has To Change', 'bool', 1, 'out')],
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
'elements': [('Voltage', 'int32', 1, 'out'),
             ('Current', 'int32', 1, 'out'),
             ('Energy', 'int32', 1, 'out'),
             ('Real Power', 'int32', 1, 'out'),
             ('Apparent Power', 'int32', 1, 'out'),
             ('Reactive Power', 'int32', 1, 'out'),
             ('Power Factor', 'uint16', 1, 'out'),
             ('Frequency', 'uint16', 1, 'out')],
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
'functions': [('getter', ('Get Energy Data', 'Energy Data'), [(('Voltage', 'Voltage'), 'int32', 1, 100, 'V', None),
                                                              (('Current', 'Current'), 'int32', 1, 100, 'A', None),
                                                              (('Energy', 'Energy'), 'int32', 1, 100, 'Wh', None),
                                                              (('Real Power', 'Real Power'), 'int32', 1, 100, 'h', None),
                                                              (('Apparent Power', 'Apparent Power'), 'int32', 1, 100, 'VA', None),
                                                              (('Reactive Power', 'Reactive Power'), 'int32', 1, 100, 'VAR', None),
                                                              (('Power Factor', 'Power Factor'), 'uint16', 1, 1000, None, None),
                                                              (('Frequecy', 'Frequency'), 'uint16', 1, 100, 'Hz', None)
], [])]})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('Energy Data', 'Energy Data'), [(('Voltage', 'Voltage'), 'int32', 1, 100, 'V', None),
                                                            (('Current', 'Current'), 'int32', 1, 100, 'A', None),
                                                            (('Energy', 'Energy'), 'int32', 1, 100, 'Wh', None),
                                                            (('Real Power', 'Real Power'), 'int32', 1, 100, 'h', None),
                                                            (('Apparent Power', 'Apparent Power'), 'int32', 1, 100, 'VA', None),
                                                            (('Reactive Power', 'Reactive Power'), 'int32', 1, 100, 'VAR', None),
                                                            (('Power Factor', 'Power Factor'), 'uint16', 1, 1000, None, None),
                                                            (('Frequecy', 'Frequency'), 'uint16', 1, 100, 'Hz', None)], None, None),
              ('callback_configuration', ('Energy Data', 'Energy Data'), [], 1000, False, None, [])]
})

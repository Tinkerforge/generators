# -*- coding: utf-8 -*-

# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# Thermal Imaging Bricklet communication config

from openhab_common import *

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'api_version': [2, 0, 0],
    'category': 'Bricklet',
    'device_identifier': 278,
    'name': 'Thermal Imaging',
    'display_name': 'Thermal Imaging',
    'manufacturer': 'Tinkerforge',
    'description': {
        'en': '80x60 pixel thermal imaging camera',
        'de': '80x60 Pixel Wärmebildkamera'
    },
    'released': True,
    'documented': True,
    'discontinued': False,
    'features': [
        'comcu_bricklet',
        'bricklet_get_identity'
    ],
    'constant_groups': [],
    'packets': [],
    'examples': []
}

com['constant_groups'].append({
'name': 'Resolution',
'type': 'uint8',
'constants': [('0 To 6553 Kelvin', 0),
              ('0 To 655 Kelvin', 1)]
})

com['constant_groups'].append({
'name': 'FFC Status',
'type': 'uint8',
'constants': [('Never Commanded', 0),
              ('Imminent', 1),
              ('In Progress', 2),
              ('Complete', 3)]
})

com['constant_groups'].append({
'name': 'Image Transfer',
'type': 'uint8',
'constants': [('Manual High Contrast Image', 0),
              ('Manual Temperature Image', 1),
              ('Callback High Contrast Image', 2),
              ('Callback Temperature Image', 3)]
})

com['packets'].append({
'type': 'function',
'name': 'Get High Contrast Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out', {}),
             ('Image Chunk Data', 'uint8', 62, 'out', {})],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current high contrast image. See `here <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
for the difference between
High Contrast and Temperature Image. If you don't know what to use
the High Contrast Image is probably right for you.

The data is organized as a 8-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 8-bit value represents one gray-scale image pixel that can directly be
shown to a user on a display.

Before you can use this function you have to enable it with
:func:`Set Image Transfer Config`.
""",
'de':
"""
Gibt das aktuelle *High Contrast Image* zurück. Siehe `hier <https://www.tinkerforge.com/de/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
für eine Beschreibung des Unterschieds zwischen
*High Contrast Image* und einem *Temperature Image*. Wenn unbekannt ist
welche Darstellungsform genutzt werden soll, ist vermutlich das
*High Contrast Image* die richtige form.

Die Daten der 80x60 Pixel-Matrix werden als ein eindimensionales
Array bestehend aus 8-Bit Werten dargestellt. Die Daten sind Zeile für Zeile
von oben links bis unten rechts angeordnet.

Jeder 8-Bit Wert stellt ein Pixel aus dem Grauwertbild dar und kann als
solcher direkt dargestellt werden.

Bevor die Funktion genutzt werden kann muss diese mittels
:func:`Set Image Transfer Config` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Temperature Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out', {}),
             ('Image Chunk Data', 'uint16', 31, 'out', {'scale': 'dynamic', 'unit': 'Kelvin', 'range': (-1000, 1400)})],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the current temperature image. See `here <https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
for the difference between High Contrast and Temperature Image.
If you don't know what to use the High Contrast Image is probably right for you.

The data is organized as a 16-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 16-bit value represents one temperature measurement in either
Kelvin/10 or Kelvin/100 (depending on the resolution set with :func:`Set Resolution`).

Before you can use this function you have to enable it with
:func:`Set Image Transfer Config`.
""",
'de':
"""
Gibt das aktuelle *Temperature Image* zurück. See `hier <https://www.tinkerforge.com/de/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image>`__
für eine Beschreibung des Unterschieds zwischen *High Contrast*
und *Temperature Image*. Wenn unbekannt ist
welche Darstellungsform genutzt werden soll, ist vermutlich das
*High Contrast Image* die richtige Form.

Die Daten der 80x60 Pixel-Matrix werden als ein eindimensionales
Array bestehend aus 16-Bit Werten dargestellt. Die Daten sind Zeile für Zeile
von oben links bis unten rechts angeordnet.

Jeder 16-Bit Wert stellt eine Temperaturmessung in entweder Kelvin/10 oder
Kelvin/100 dar (abhängig von der Auflösung die mittels :func:`Set Resolution`
eingestellt wurde).

Bevor die Funktion genutzt werden kann muss diese mittels
:func:`Set Image Transfer Config` aktiviert werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Statistics',
'elements': [('Spotmeter Statistics', 'uint16', 4, 'out', {'scale': 'dynamic', 'unit': 'dynamic'}), # mean, max, min, pixel count
             ('Temperatures', 'uint16', 4, 'out', {'scale': 'dynamic', 'unit': 'Kelvin'}), # focal plain array, focal plain array at last ffc, housing, housing at last ffc
             ('Resolution', 'uint8', 1, 'out', {'constant_group': 'Resolution'}),
             ('FFC Status', 'uint8', 1, 'out', {'constant_group': 'FFC Status'}),
             ('Temperature Warning', 'bool', 2, 'out', {}) # shutter lockout, overtemp
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

FFC (Flat Field Correction) Status:

* FFC Never Commanded: Only seen on startup before first FFC.
* FFC Imminent: This state is entered 2 seconds prior to initiating FFC.
* FFC In Progress: Flat field correction is started (shutter moves in front of lens and back). Takes about 1 second.
* FFC Complete: Shutter is in waiting position again, FFC done.

Temperature warning bits:

* Index 0: Shutter lockout (if true shutter is locked out because temperature is outside -10°C to +65°C)
* Index 1: Overtemperature shut down imminent (goes true 10 seconds before shutdown)
""",
'de':
"""
Gibt die Spotmeter Statistiken, verschiedene Temperaturen, die aktuelle Auflösung und Status-Bits zurück.

Die Spotmeter Statistiken bestehen aus:

* Index 0: Durchschnittstemperatur.
* Index 1: Maximal Temperatur.
* Index 2: Minimal Temperatur.
* Index 3: Pixel Anzahl der Spotmeter Region (Spotmeter Region of Interest).

Die Temperaturen sind:

* Index 0: Sensorflächen Temperatur (Focal Plain Array Temperature).
* Index 1: Sensorflächen Temperatur bei der letzten FFC (Flat Field Correction).
* Index 2: Gehäusetemperatur.
* Index 3: Gehäusetemperatur bei der letzten FFC.

Die Auflösung ist entweder `0 bis 6553 Kelvin` oder `0 bis 655 Kelvin`. Ist die Auflösung
ersteres, so ist die Auflösung Kelvin/10. Ansonsten ist sie Kelvin/100.

FFC (Flat Field Correction) Status:

* FFC Never Commanded: FFC wurde niemals ausgeführt. Dies ist nur nach dem Start vor dem ersten FFC der Fall.
* FFC Imminent: Dieser Zustand wird zwei Sekunden vor einem FFC angenommen.
* FFC In Progress: FFC wird ausgeführt (Der Shutter bewegt sich vor die Linse und wieder zurück). Dies benötigt ca. 1 Sekunde.
* FFC Complete: FFC ist ausgeführt worden. Der Shutter ist wieder in der Warteposition.

Temperaturwarnungs-Status:

* Index 0: Shutter-Sperre (shutter lockout). Wenn True, ist der Shutter gesperrt, da die Temperatur außerhalb des Bereichs -10°C bis +65°C liegt.
* Index 1: Übertemperaturabschaltung steht bevor, wenn dieses Bit True ist. Bit wird 10 Sekunden vor der Abschaltung gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Resolution',
'elements': [('Resolution', 'uint8', 1, 'in', {'constant_group': 'Resolution', 'default': 1})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the resolution. The Thermal Imaging Bricklet can either measure

* from 0 to 6553 Kelvin (-273.15°C to +6279.85°C) with 0.1°C resolution or
* from 0 to 655 Kelvin (-273.15°C to +381.85°C) with 0.01°C resolution.

The accuracy is specified for -10°C to 450°C in the
first range and -10°C and 140°C in the second range.
""",
'de':
"""
Setzt die Auflösung. Das Thermal Imaging Bricklet kann entweder

* von 0 bis 6553 Kelvin (-273,15°C bis +6279,85°C) mit 0,1°C Auflösung oder
* von 0 bis 655 Kelvin (-273,15°C bis +381,85°C) mit 0,01°C Auflösung messen.

Die Genauigkeit ist spezifiziert von -10°C bis 450°C im ersten Auflösungsbereich
und von -10°C bis 140°C im zweiten Bereich.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Resolution',
'elements': [('Resolution', 'uint8', 1, 'out', {'constant_group': 'Resolution'})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the resolution as set by :func:`Set Resolution`.
""",
'de':
"""
Gibt die Auflösung zurück, wie von :func:`Set Resolution` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Spotmeter Config',
'elements': [('Region Of Interest', 'uint8', 4, 'in', {'range': 'dynamic', 'default' : [39, 29, 40, 30]})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the spotmeter region of interest. The 4 values are

* Index 0: Column start (has to be smaller then Column end).
* Index 1: Row start (has to be smaller then Row end).
* Index 2: Column end (has to be smaller then 80).
* Index 3: Row end (has to be smaller then 60).

The spotmeter statistics can be read out with :func:`Get Statistics`.
""",
'de':
"""
Setzt die Spotmeter Region (*Spotmeter Region of Interest*). Die 4 Werte sind

* Index 0: Spaltenstart (muss kleiner als das Spaltenende sein).
* Index 1: Zeilenstart (muss kleiner als das Zeilenende sein).
* Index 2: Spaltenende (muss kleiner als 80 sein).
* Index 3: Zeilenende (muss kleiner als 60 sein).

Die Spotmeter Statistiken können mittels :func:`Get Statistics` ausgelesen werden.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Spotmeter Config',
'elements': [('Region Of Interest', 'uint8', 4, 'out', {'range': 'dynamic', 'default' : [39, 29, 40, 30]})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the spotmeter config as set by :func:`Set Spotmeter Config`.
""",
'de':
"""
Gibt die Spotmeter Konfiguration zurück, wie von :func:`Set Spotmeter Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set High Contrast Config',
'elements': [('Region Of Interest', 'uint8', 4, 'in', {'range': 'dynamic', 'default': [0, 0, 79, 59]}),
             ('Dampening Factor', 'uint16', 1, 'in', {'range': (0, 256), 'default': 64}),
             ('Clip Limit', 'uint16', 2, 'in', {'range': 'dynamic', 'default': [4800, 512]}),
             ('Empty Counts', 'uint16', 1, 'in', {'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Sets the high contrast region of interest, dampening factor, clip limit and empty counts.
This config is only used in high contrast mode (see :func:`Set Image Transfer Config`).

The high contrast region of interest consists of four values:

* Index 0: Column start (has to be smaller or equal then Column end).
* Index 1: Row start (has to be smaller then Row end).
* Index 2: Column end (has to be smaller then 80).
* Index 3: Row end (has to be smaller then 60).

The algorithm to generate the high contrast image is applied to this region.

Dampening Factor: This parameter is the amount of temporal dampening applied to the HEQ
(history equalization) transformation function. An IIR filter of the form::

 (N / 256) * previous + ((256 - N) / 256) * current

is applied, and the HEQ dampening factor
represents the value N in the equation, i.e., a value that applies to the amount of
influence the previous HEQ transformation function has on the current function. The
lower the value of N the higher the influence of the current video frame whereas
the higher the value of N the more influence the previous damped transfer function has.

Clip Limit Index 0 (AGC HEQ Clip Limit High): This parameter defines the maximum number of pixels allowed
to accumulate in any given histogram bin. Any additional pixels in a given bin are clipped.
The effect of this parameter is to limit the influence of highly-populated bins on the
resulting HEQ transformation function.

Clip Limit Index 1 (AGC HEQ Clip Limit Low): This parameter defines an artificial population that is added to
every non-empty histogram bin. In other words, if the Clip Limit Low is set to L, a bin
with an actual population of X will have an effective population of L + X. Any empty bin
that is nearby a populated bin will be given an artificial population of L. The effect of
higher values is to provide a more linear transfer function; lower values provide a more
non-linear (equalized) transfer function.

Empty Counts: This parameter specifies the maximum number of pixels in a bin that will be
interpreted as an empty bin. Histogram bins with this number of pixels or less will be
processed as an empty bin.
""",
'de':
"""
Setzt die Region of Interest für das High Contrast Image, den Dampening Faktor, das
Clip Limit und die Empty Counts. Diese Konfiguration wird nur im High Contrast Modus
genutzt (siehe :func:`Set Image Transfer Config`).

Die High Contrast Region of Interest besteht aus vier Werten:

* Index 0: Spaltenstart (muss kleiner sein wie Spaltenende).
* Index 1: Zeilenstart (muss kleiner sein wie Zeilenende).
* Index 2: Spaltenende (muss kleiner sein wie 80).
* Index 3: Zeilenende (muss kleiner sein wie 60).

Der Algorithmus zum Erzeugen eines High Contrast Images wird auf diese Region angewandt.

Dampening Factor: Dieser Parameter stellt die Stärke der zeitlichen Dämpfung dar, die auf der
HEQ (History Equalization) Transformationsfunktion angewendet wird. Ein IIR-Filter der
Form::

 (N / 256) * transformation_zuvor + ((256 - N) / 256) * transformation_aktuell

wird dort
angewendet. Der HEQ Dämpfungsfaktor stellt dabei den Wert N in der Gleichung dar.
Der Faktor stellt also ein, wie stark der Einfluss der vorherigen HEQ Transformation
auf die aktuelle ist. Umso niedriger der Wert von N um so größer ist der Einfluss des
aktuellen Bildes. Umso größer der Wert von N umso kleiner ist der Einfluss der vorherigen
Dämpfungs-Transferfunktion.

Clip Limit Index 0 (AGC HEQ Clip Limit High): Dieser Parameter definiert die maximale Anzahl
an Pixeln, die sich in jeder Histogrammklasse sammeln dürfen. Jedes weitere Pixel wird verworfen.
Der Effekt dieses Parameters ist den Einfluss von stark gefüllten Klassen in der HEQ Transformation
zu beschränken.

Clip Limit Index 1 (AGC HEQ Clip Limit Low): Dieser Parameter definiert einen künstliche Menge,
die jeder nicht leeren Histogrammklasse hinzugefügt wird. Wenn Clip Limit Low mit L dargestellt
wird, so erhält jede Klasse mit der aktuellen Menge X die effektive Menge L + X. Jede Klasse, die
nahe einer gefüllten Klasse ist erhält die Menge L. Der Effekt von höheren Werten ist eine stärkere
lineare Transferfunktion bereitzustellen. Niedrigere Werte führen zu einer nichtlinearen
Transferfunktion.

Empty Counts: Dieser Parameter spezifiziert die maximale Anzahl von Pixeln in einer Klasse, damit
die Klasse als leere Klasse interpretiert wird. Jede Histogrammklasse mit dieser Anzahl an Pixeln oder
weniger wird als leere Klasse behandelt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get High Contrast Config',
'elements': [('Region Of Interest', 'uint8', 4, 'out', {'range': 'dynamic', 'default': [0, 0, 79, 59]}),
             ('Dampening Factor', 'uint16', 1, 'out', {'range': (0, 256), 'default': 64}),
             ('Clip Limit', 'uint16', 2, 'out', {'range': 'dynamic', 'default': [4800, 512]}),
             ('Empty Counts', 'uint16', 1, 'out', {'default': 2})],
'since_firmware': [1, 0, 0],
'doc': ['bf', {
'en':
"""
Returns the high contrast config as set by :func:`Set High Contrast Config`.
""",
'de':
"""
Gibt die High Contrast Konfiguration zurück, wie von
:func:`Set High Contrast Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Set Image Transfer Config',
'elements': [('Config', 'uint8', 1, 'in', {'constant_group': 'Image Transfer', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
The necessary bandwidth of this Bricklet is too high to use getter/callback or
high contrast/temperature image at the same time. You have to configure the one
you want to use, the Bricklet will optimize the internal configuration accordingly.

Corresponding functions:

* Manual High Contrast Image: :func:`Get High Contrast Image`.
* Manual Temperature Image: :func:`Get Temperature Image`.
* Callback High Contrast Image: :cb:`High Contrast Image` callback.
* Callback Temperature Image: :cb:`Temperature Image` callback.
""",
'de':
"""
Die notwendige Bandbreite für dieses Bricklet ist zu groß um Getter/Callbacks
oder High Contrast/Temperature Images gleichzeitig zu nutzen. Daher muss konfiguriert
werden was genutzt werden soll. Das Bricklet optimiert seine interne Konfiguration
anschließend dahingehend.

Zugehörige Funktionen:

* Manual High Contrast Image: :func:`Get High Contrast Image`.
* Manual Temperature Image: :func:`Get Temperature Image`.
* Callback High Contrast Image: :cb:`High Contrast Image` callback.
* Callback Temperature Image: :cb:`Temperature Image` callback.
"""
}]
})

com['packets'].append({
'type': 'function',
'name': 'Get Image Transfer Config',
'elements': [('Config', 'uint8', 1, 'out', {'constant_group': 'Image Transfer', 'default': 0})],
'since_firmware': [1, 0, 0],
'doc': ['ccf', {
'en':
"""
Returns the image transfer config, as set by :func:`Set Image Transfer Config`.
""",
'de':
"""
Gibt die Image Transfer Konfiguration zurück, wie von :func:`Set Image Transfer Config` gesetzt.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'High Contrast Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out', {}),
             ('Image Chunk Data', 'uint8', 62, 'out', {})],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered with every new high contrast image if the transfer image
config is configured for high contrast callback (see :func:`Set Image Transfer Config`).

The data is organized as a 8-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 8-bit value represents one gray-scale image pixel that can directly be
shown to a user on a display.
""",
'de':
"""
Dieser Callback wird für jedes neue High Contrast Image ausgelöst, wenn die
*Transfer Image Config* für diesen Callback konfiguriert wurde (siehe
:func:`Set Image Transfer Config`).

Die Daten der 80x60 Pixel-Matrix werden als ein eindimensionales
Array bestehend aus 8-Bit Werten dargestellt. Die Daten sind Zeile für Zeile
von oben links bis unten rechts angeordnet.

Jeder 8-Bit Wert stellt ein Pixel aus dem Grauwertbild dar und kann als
solcher direkt dargestellt werden.
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': 'Temperature Image Low Level',
'elements': [('Image Chunk Offset', 'uint16', 1, 'out', {}),
             ('Image Chunk Data', 'uint16', 31, 'out', {'scale': 'dynamic', 'unit': 'Kelvin', 'range': (-1000, 1400)})],
'high_level': {'stream_out': {'name': 'Image', 'fixed_length': 80*60}},
'since_firmware': [1, 0, 0],
'doc': ['c', {
'en':
"""
This callback is triggered with every new temperature image if the transfer image
config is configured for temperature callback (see :func:`Set Image Transfer Config`).

The data is organized as a 16-bit value 80x60 pixel matrix linearized in
a one-dimensional array. The data is arranged line by line from top left to
bottom right.

Each 16-bit value represents one temperature measurement in either
Kelvin/10 or Kelvin/100 (depending on the resolution set with :func:`Set Resolution`).
""",
'de':
"""
Dieser Callback wird für jedes neue Temperature Image ausgelöst, wenn die *Transfer
Image Config* für diesen Callback konfiguriert wurde (siehe
:func:`Set Image Transfer Config`).

Die Daten der 80x60 Pixel-Matrix werden als ein eindimensionales
Array bestehend aus 16-Bit Werten dargestellt. Die Daten sind Zeile für Zeile
von oben links bis unten rechts angeordnet.

Jeder 16-Bit Wert stellt ein Pixel aus dem Temperatur Bild dar und kann als
solcher direkt dargestellt werden.
"""
}]
})

com['examples'].append({
'name': 'Callback',
'functions': [('callback', ('High Contrast Image', 'high contrast image'), [(('Image', None), 'uint8', -4800, None, None, None)], None, None),
              ('setter', 'Set Image Transfer Config', [('uint8:constant', 2)], 'Enable high contrast image transfer for callback', None)],
'incomplete': True # because of callback with array parameters
})


com['openhab'] = {
    'imports': oh_generic_channel_imports() + ['org.eclipse.smarthome.core.library.types.RawType', 'org.eclipse.smarthome.core.library.types.OnOffType'],
    'param_groups': oh_generic_channel_param_groups(),
    'params': [{
            'name': 'Image Type',
            'type': 'integer',
            'options': [('High Contrast Image', 0),
                        ('Linear Temperature Image', 1)],
            'limitToOptions': 'true',
            'default': '0',

            'label': 'Image Type',
            'description': 'The necessary bandwidth of this Bricklet is too high to use the high contrast and temperature image at the same time. You have to configure the one you want to use, the Bricklet will optimize the internal configuration accordingly.',
        }, {
            'name': 'Resolution',
            'type': 'integer',
            'options': [('0 To 6553 Kelvin', 0),
                        ('0 To 655 Kelvin', 1)],
            'limitToOptions': 'true',
            'default': '1',

            'label': 'Resolution',
            'description': 'The Thermal Imaging Bricklet can either measure<ul><li>from 0 to 6553 Kelvin (-273.15°C to +6279.85°C) with 0.1°C resolution or</li><li>from 0 to 655 Kelvin (-273.15°C to +381.85°C) with 0.01°C resolution.</li></ul><br/>The accuracy is specified for -10°C to 450°C in the first range and -10°C and 140°C in the second range.',
        }, {
            'name': 'Spotmeter Column Start',
            'type': 'integer',
            'min': '0',
            'max': '79',
            'default': '39',

            'label': 'Spotmeter Column Start',
            'description': 'First column of the spotmeter region of interest.',
        }, {
            'name': 'Spotmeter Row Start',
            'type': 'integer',
            'min': '0',
            'max': '59',
            'default': '29',

            'label': 'Spotmeter Row Start',
            'description': 'First row of the spotmeter region of interest.',
        }, {
            'name': 'Spotmeter Column End',
            'type': 'integer',
            'min': '0',
            'max': '79',
            'default': '40',

            'label': 'Spotmeter Column End',
            'description': 'Last column of the spotmeter region of interest.',
        }, {
            'name': 'Spotmeter Row End',
            'type': 'integer',
            'min': '0',
            'max': '59',
            'default': '30',

            'label': 'Spotmeter Row End',
            'description': 'Last row of the spotmeter region of interest.',
        }],
    'init_code': """this.setImageTransferConfig(cfg.imageType);
    this.setResolution(cfg.resolution);
    this.setSpotmeterConfig(new int[]{cfg.spotmeterColumnStart, cfg.spotmeterRowStart, cfg.spotmeterColumnEnd, cfg.spotmeterRowEnd});""",
    'channels': [{
        'predicate': 'cfg.imageType == 0',
        'id': 'High Contrast Image',
        'label': 'High Contrast Image',
        'type': 'High Contrast Image',

        'init_code': """this.setHighContrastConfig(new int[]{{channelCfg.highContrastColumnStart, channelCfg.highContrastRowStart, channelCfg.highContrastColumnEnd, channelCfg.highContrastRowEnd}}, channelCfg.dampeningFactor, new int[]{{channelCfg.clipLimitHigh, channelCfg.clipLimitLow}}, channelCfg.emptyCounts);""",

        'getters': [{
            'packet': 'Get {title_words}',
            'packet_params': [],
            'transform': 'new RawType(Helper.convertThermalHighContrastImage(value, logger), "image/png")'}],
        'is_trigger_channel': False
    }, {
        'predicate': 'cfg.imageType == 1',
        'id': 'Temperature Image',
        'label': 'Temperature Image',
        'type': 'Temperature Image',

        'getters': [{
            'packet': 'Get {title_words}',
            'packet_params': [],
            'transform': 'new RawType(Helper.convertThermalTemperatureImage(value, logger), "image/png")'}],
        'is_trigger_channel': False
    }, {
        'id': 'Spotmeter Mean Temperature',
        'label': 'Spotmeter Mean Temperature',
        'type': 'Temperature',


        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.spotmeterStatistics[0] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    }, {
        'id': 'Spotmeter Maximum Temperature',
        'label': 'Spotmeter Maximum Temperature',
        'type': 'Temperature',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.spotmeterStatistics[1] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    }, {
        'id': 'Spotmeter Minimum Temperature',
        'label': 'Spotmeter Minimum Temperature',
        'type': 'Temperature',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.spotmeterStatistics[2] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    }, {
        'id': 'Spotmeter ROI Pixel Count',
        'type': 'Spotmeter ROI Pixel Count',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.spotmeterStatistics[3], {unit})'}],
        'java_unit': 'SmartHomeUnits.ONE',
        'is_trigger_channel': False
    }, {
        'id': 'Focal Plain Array Temperature',
        'label': 'Focal Plain Array Temperature',
        'type': 'Temperature',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.temperatures[0] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    }, {
        'id': 'Focal Plain Array Temperature FFC',
        'label': 'Focal Plain Array Temperature (last FFC)',
        'type': 'Temperature',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.temperatures[1] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    },  {
        'id': 'Housing Temperature',
        'label': 'Housing Temperature',
        'type': 'Temperature',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.temperatures[2] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    }, {
        'id': 'Housing Temperature FFC',
        'label': 'Housing Temperature (last FFC)',
        'type': 'Temperature',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.temperatures[3] / (cfg.resolution == 0 ? 10.0 : 100.0), {unit})'}],
        'java_unit': 'SmartHomeUnits.KELVIN',
        'is_trigger_channel': False
    }, {
        'id': 'FFC Status',
        'label': 'Flat Field Correction Status',
        'type': 'FFC Status',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'new QuantityType(value.ffcStatus, {unit})'}],
        'java_unit': 'SmartHomeUnits.ONE',
        'is_trigger_channel': False
    }, {
        'id': 'Shutter Lockout',
        'type': 'Shutter Lockout',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'value.temperatureWarning[0] ? OnOffType.ON : OnOffType.OFF'}],
        'is_trigger_channel': False
    }, {
        'id': 'Overtemperature Shutdown Imminent',
        'type': 'Overtemperature Shutdown Imminent',

        'getters': [{
            'packet': 'Get Statistics',
            'packet_params': [],
            'transform': 'value.temperatureWarning[1] ? OnOffType.ON : OnOffType.OFF'}],
        'is_trigger_channel': False
    },


    ],
    'channel_types': [
        oh_generic_channel_type('High Contrast Image', 'Image', 'High Contrast Image',
                    description="The current high contrast image. See <a href=\\\"https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image\\\">here</a> for the difference between High Contrast and Temperature Image. If you don't know what to use the High Contrast Image is probably right for you.",
                    read_only=True,
                    params=[{
                            'name': 'High Contrast Column Start',
                            'type': 'integer',
                            'min': '0',
                            'max': '79',
                            'default': '39',

                            'label': 'High Contrast Column Start',
                            'description': 'First column of the high contrast region of interest.',
                        }, {
                            'name': 'High Contrast Row Start',
                            'type': 'integer',
                            'min': '0',
                            'max': '59',
                            'default': '29',

                            'label': 'High Contrast Row Start',
                            'description': 'First row of the high contrast region of interest.',
                        }, {
                            'name': 'High Contrast Column End',
                            'type': 'integer',
                            'min': '0',
                            'max': '79',
                            'default': '40',

                            'label': 'High Contrast Column End',
                            'description': 'Last column of the high contrast region of interest.',
                        }, {
                            'name': 'High Contrast Row End',
                            'type': 'integer',
                            'min': '0',
                            'max': '59',
                            'default': '30',

                            'label': 'High Contrast Row End',
                            'description': 'Last row of the high contrast region of interest.',
                        }, {
                            'name': 'Dampening Factor',
                            'type': 'integer',
                            'min': '0',
                            'max': '256',
                            'default': '64',

                            'label': 'Dampening Factor',
                            'description': 'This parameter is the amount of temporal dampening applied to the HEQ (history equalization) transformation function. An IIR filter of the form:<pre>(N / 256) * previous + ((256 - N) / 256) * current</pre>is applied, and the HEQ dampening factor represents the value N in the equation, i.e., a value that applies to the amount of influence the previous HEQ transformation function has on the current function. The lower the value of N the higher the influence of the current video frame whereas the higher the value of N the more influence the previous damped transfer function has.',
                        }, {
                            'name': 'Clip Limit Low',
                            'type': 'integer',
                            'min': '0',
                            'max': '1024',
                            'default': '512',

                            'label': 'AGC HEQ Clip Limit Low',
                            'description': 'This parameter defines an artificial population that is added to every non-empty histogram bin. In other words, if the Clip Limit Low is set to L, a bin with an actual population of X will have an effective population of L + X. Any empty bin that is nearby a populated bin will be given an artificial population of L. The effect of higher values is to provide a more linear transfer function; lower values provide a more non-linear (equalized) transfer function.',
                        },  {
                            'name': 'Clip Limit High',
                            'type': 'integer',
                            'min': '0',
                            'max': '4800',
                            'default': '4800',

                            'label': 'AGC HEQ Clip Limit High',
                            'description': 'This parameter defines the maximum number of pixels allowed to accumulate in any given histogram bin. Any additional pixels in a given bin are clipped. The effect of this parameter is to limit the influence of highly-populated bins on the resulting HEQ transformation function.',
                        },   {
                            'name': 'Empty Counts',
                            'type': 'integer',
                            'min': '0',
                            'max': '16383',
                            'default': '2',

                            'label': 'Empty Counts',
                            'description': ' This parameter specifies the maximum number of pixels in a bin that will be interpreted as an empty bin. Histogram bins with this number of pixels or less will be processed as an empty bin.',
                        },
                    ]),
        oh_generic_channel_type('Temperature Image', 'Image', 'Temperature Image',
                    description="The current temperature image. See <a href=\\\"https://www.tinkerforge.com/en/doc/Hardware/Bricklets/Thermal_Imaging.html#high-contrast-image-vs-temperature-image\\\">here</a> for the difference between High Contrast and Temperature Image. If you don't know what to use the High Contrast Image is probably right for you.",
                    read_only=True),
        oh_generic_channel_type('Temperature', 'Number:Temperature', 'NOT USED',
                    pattern='%.3f %unit%',
                    read_only=True),
        oh_generic_channel_type('Spotmeter ROI Pixel Count', 'Number:Dimensionless', 'Spotmeter ROI Pixel Count',
                    pattern='%.3f %unit%',
                    read_only=True),
        {
            'id': 'FFC Status',
            'item_type': 'Number:Dimensionless',
            'label': 'FFC Status',
            'description': 'Flat Field Correction Status',
            'read_only': True,
            'min': 0,
            'max': 3,
            'is_trigger_channel': False,
            'options': [('Never Commanded', 0),
                        ('Imminent', 1),
                        ('In Progress', 2),
                        ('Complete', 3)]
        },
        oh_generic_channel_type('Shutter Lockout', 'Switch', 'Shutter Lockout',
                     description='If enabled, shutter is locked out because temperature is outside -10°C to +65°C',
                     read_only=True),
        oh_generic_channel_type('Overtemperature Shutdown Imminent', 'Switch', 'Overtemperature Shutdown Imminent',
                     description='Gets enabled 10 seconds before shutdown.',
                     read_only=True),
    ],
    'actions': ['Get High Contrast Image', 'Get Temperature Image', 'Get Statistics', 'Get Resolution', 'Get Spotmeter Config', 'Get High Contrast Config']
}

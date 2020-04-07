#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
openHAB Documentation Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_openhab_doc.py: Generator for openHAB documentation

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
General Public License for more details.

You should have received a copy of the GNU General Public
License along with this program; if not, write to the
Free Software Foundation, Inc., 59 Temple Place - Suite 330,
Boston, MA 02111-1307, USA.
"""

import sys
import os

sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'java'))
import common
import java_common
import openhab_common

import re

def unescape(s):
    return s.replace('<', '⟨').replace('>', '⟩').replace('"', '«')

class OpenHABDocDevice(openhab_common.OpenHABDevice):
    def __init__(self, raw_data, generator):
        openhab_common.OpenHABDevice.__init__(self, raw_data, generator)

        self.read_openhab_config()

    # Override common implementation to be able to replace text in the specializer
    def specialize_doc_rst_links(self, text, specializer, prefix=None):
        for keyword, type_ in [('func', 'function'), ('cb', 'callback')]:
            for packet in self.get_packets(type_):
                names = [packet.get_name().space]

                if packet.has_high_level():
                    names.append(packet.get_name(skip=-2).space)

                for name in names:
                    generic_name = ':{0}:`{1}`'.format(keyword, name)
                    special_name, text = specializer(text, packet, packet.has_high_level() and not name.endswith(' Low Level'))

                    text = text.replace(generic_name, special_name)

            if prefix != None:
                p = '(?<!:' + prefix + ')(:' + keyword + ':`[^`]*`)'
            else:
                p = '(:' + keyword + ':`[^`]*`)'

            m = re.search(p, text)

            if m != None:
                raise common.GeneratorError('Unknown :{0}: found: {1}'.format(keyword, m.group(1)))

        return text

    def specialize_java_doc_function_links(self, text):
        def specializer(text, packet, high_level):
            # Device, link to be removed (the replacement will only fail if this is in text), replacements
            special_cases = [
('CAN', ':cb:`Frame Read`', [
("""
Instead of polling with this function, you can also use callbacks. See the
:func:`Enable Frame Read Callback` function and the :cb:`Frame Read` callback.
""", ''),

("""
Instead of polling with this function, you can also use callbacks. See the
:func:`Set Frame Read Callback Configuration` function and the :cb:`Frame Read`
callback.
""", ''),

("""  function. Using the :cb:`Frame Read` callback ensures that the read buffer
  can not overflow.
""", """  function.
"""),

("""  function. Using the :cb:`Frame Read` callback ensures that the read backlog
  can not overflow.
""", """  function.
""")
]),

('RS232', ':cb:`Read`', [("""
Instead of polling with this function, you can also use
callbacks. See :func:`Enable Read Callback` and :cb:`Read` callback.
""", ''),

("""
Instead of polling with this function, you can also use
callbacks. But note that this function will return available
data only when the read callback is disabled.
See :func:`Enable Read Callback` and :cb:`Read` callback.
""", "")]),

('RS485', ':cb:`Read`', [("""

Instead of polling with this function, you can also use
callbacks. But note that this function will return available
data only when the read callback is disabled.
See :func:`Enable Read Callback` and :cb:`Read` callback.
""", '')]),

('DMX', ':cb:`Frame`', [("""Instead of polling this function you can also use the :cb:`Frame` callback.
You can enable it with :func:`Set Frame Callback Config`.

""", '')]),

('Industrial Digital In 4', ':func:`Set Group`', [("""
If no groups are used (see :func:`Set Group`), the pins correspond to the
markings on the IndustrialDigital In 4 Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""", ''),

("""
The edge counters use the grouping as set by :func:`Set Group`.
""", '')]),

('Industrial Digital Out 4', ':func:`Set Group`', [("""
If no groups are used (see :func:`Set Group`), the pins correspond to the
markings on the Industrial Digital Out 4 Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""", '')]),

('Industrial Quad Relay', ':func:`Set Group`', [("""
If no groups are used (see :func:`Set Group`), the pins correspond to the
markings on the Industrial Quad Relay Bricklet.

If groups are used, the pins correspond to the element in the group.
Element 1 in the group will get pins 0-3, element 2 pins 4-7, element 3
pins 8-11 and element 4 pins 12-15.
""", '')]),

('PTC V2', ':func:`Set Sensor Connected Callback Configuration`', [(""" You can set the callback configuration
with :func:`Set Sensor Connected Callback Configuration`.""", '')]),

('Joystick V2', ':func:`Set Pressed Callback Configuration`', [(""" and set the period with
:func:`Set Pressed Callback Configuration`""", '')])
            ]

            for dev, link, replacements in special_cases:
                if dev not in self.get_name().space:
                    continue
                if link not in text:
                    continue
                for to_replace, replacement in replacements:
                    if to_replace in text:
                        text = text.replace(to_replace, replacement)
                        break
                else:
                    raise common.GeneratorError("openhab: {} {} No replacement found!".format(dev, link))

            channel = None

            # Handle 'All Data/Values' cases: Cut out the complete paragraph mentioning the callback.
            needle = ':cb:`{}`'.format(packet.get_name(skip=-2 if high_level else 0).space)
            if 'All' in packet.name.words and needle in text:
                channel = 'All'
                if packet.get_type() == 'callback':
                    needle_idx = text.find(needle)
                    paragraph_start = text.rfind('\n\n', 0, needle_idx)
                    paragraph_end = text.rfind('\n\n', needle_idx)
                    if paragraph_start < 0:
                        paragraph_start = 0
                    if paragraph_end < 0:
                        paragraph_end = len(text) - 1
                    text = text[:paragraph_start] + text[paragraph_end:]
                    return '', text
                else:
                    return ':openhab:func:`{1}() <{0}::{2}{1}>`'.format(packet.get_device().get_java_class_name(),
                                                              packet.get_name(skip=-2 if high_level else 0).camel,
                                                              packet.get_device().get_category().headless+packet.get_device().get_name().camel), text

            # Handle EEPROM/Flash cases: Remove link, add note instead.
            to_remove = [('BrickletAirQuality', 'SetBackgroundCalibrationDuration'),
                         ('BrickletAnalogInV3', 'SetCalibration'),
                         ('BrickletCompass', 'SetCalibration'),
                         ('BrickletCO2V2', 'SetTemperatureOffset'),
                         ('BrickletDistanceIRV2', 'SetSensorType'),
                         ('BrickletDistanceIR', 'SetSamplingPoint'),
                         ('BrickletEnergyMonitor', 'SetTransformerCalibration'),
                         ('BrickletIndustrialDualAnalogInV2', 'SetCalibration'),
                         ('BrickletIndustrialDualAnalogInV2', 'SetCalibration'),
                         ('BrickletIndustrialDualAnalogIn', 'SetCalibration'),
                         ('BrickletIndustrialDualAnalogIn', 'SetCalibration'),
                         ('BrickletJoystickV2', 'Calibrate'),
                         ('BrickletJoystick', 'Calibrate'),
                         ('BrickletLaserRangeFinderV2', 'SetOffsetCalibration'),
                         ('BrickletRGBLEDButton', 'SetColorCalibration'),
                         ('BrickletRealTimeClockV2', 'SetOffset'),
                         ('BrickletRealTimeClock', 'SetOffset'),
                         ('BrickletTemperatureIRV2', 'SetEmissivity'),
                         ('BrickletTemperatureIRV2', 'SetEmissivity'),
                         ('BrickletTemperatureIR', 'SetEmissivity'),
                         ('BrickletTemperatureIR', 'SetEmissivity'),
                         ('BrickletVoltageCurrentV2', 'SetCalibration'),
                         ('BrickletVoltageCurrent', 'SetCalibration'),
                         ('BrickIMU', 'SetCalibration'),
                         ('BrickMaster', 'SetExtensionType'),
                         ('BrickMaster', 'SetChibiAddress'),
                         ('BrickMaster', 'SetChibiMasterAddress'),
                         ('BrickMaster', 'SetChibiSlaveAddress'),
                         ('BrickMaster', 'SetChibiFrequency'),
                         ('BrickMaster', 'SetChibiChannel'),
                         ('BrickMaster', 'SetRS485Address'),
                         ('BrickMaster', 'SetRS485SlaveAddress'),
                         ('BrickMaster', 'SetRS485Configuration'),
                         ('BrickMaster', 'SetWifiConfiguration'),
                         ('BrickMaster', 'SetWifiEncryption'),
                         ('BrickMaster', 'SetWifiCertificate'),
                         ('BrickMaster', 'SetWifiPowerMode'),
                         ('BrickMaster', 'SetWifiRegulatoryDomain'),
                         ('BrickMaster', 'SetLongWifiKey'),
                         ('BrickMaster', 'SetWifiHostname'),
                         ('BrickMaster', 'SetWifiAuthenticationSecret'),
                         ('BrickMaster', 'SetEthernetConfiguration'),
                         ('BrickMaster', 'SetEthernetConfiguration'),
                         ('BrickMaster', 'SetEthernetAuthenticationSecret'),
                         ('BrickMaster', 'SetWifi2AuthenticationSecret'),
                         ('BrickMaster', 'SetWifi2Configuration'),
                         ('BrickMaster', 'SetWifi2ClientConfiguration'),
                         ('BrickMaster', 'SetWifi2ClientHostname'),
                         ('BrickMaster', 'SetWifi2APConfiguration'),
                         ('BrickMaster', 'SetWifi2MeshConfiguration'),
                         ('BrickMaster', 'SetWifi2MeshRouterSSID'),
                         ('BrickletLoadCell', 'SetConfiguration'),
                         ('BrickletPiezoSpeaker', 'Calibrate')]

            current_dev = self.get_category().camel + self.get_name().camel
            current_fn = packet.get_name().camel

            for dev, fn in to_remove:
                if dev != current_dev:
                    continue
                if fn != current_fn:
                    continue
                return '*This function is not available in openHAB*. *Please use Brick Viewer to change persistant device settings*', text


            # Try to find a channel for the link
            def match_name(gp, sp, cp, skip_haystack, skip_needle, skipped):
                return any(x.get_name(skip=skip_haystack).space == 'Get ' + packet.get_name(skip_needle).space for x in gp if skipped in x.get_name().space) or \
                       any(x.get_name(skip=skip_haystack).space == 'Set ' + packet.get_name(skip_needle).space for x in sp if skipped in x.get_name().space) or \
                       any(x.get_name(skip=skip_haystack).space == packet.get_name(skip_needle).space for x in gp if skipped in x.get_name().space) or \
                       any(x.get_name(skip=skip_haystack).space == packet.get_name(skip_needle).space for x in sp if skipped in x.get_name().space) or \
                       any(x.get_name(skip=skip_haystack).space == packet.get_name(skip_needle).space for x in cp if skipped in x.get_name().space)

            for c in self.oh.channels:
                # skip=-2 for low level, skip=-1 for reached
                gp = [x.packet for x in c.getters]
                sp = [x.packet for x in c.setters]
                cp = [x.packet for x in c.callbacks]
                if match_name(gp, sp, cp, skip_haystack=0, skip_needle=0, skipped=''):
                    channel = c
                    break

                if 'Low Level' in packet.get_name().space:
                    if match_name(gp, sp, cp, skip_haystack=-2, skip_needle=-2, skipped='Low Level'):
                        channel = c
                        break

                if 'Reached' in packet.get_name().space:
                    if match_name(gp, sp, cp, skip_haystack=0, skip_needle=-1, skipped='Reached'):
                        channel = c
                        break

            if channel is not None:
                return ':openhab:chan:`{label} <{device}::{label}>`'.format(label=channel.get_label(),
                                                                            device=packet.get_device().get_java_class_name()), text

            # Check if the function is used by the thing itself for configuration.
            for p in self.oh.params:
                if p.packet is not None and p.packet.get_name().space == packet.get_name().space:
                    if p is not None:
                        return 'the thing configuration', text


            # Try to find a channel that uses the linked function for configuration.
            for c in self.oh.channels:
                for p in c.type.params:
                    if p.packet is not None and p.packet.get_name().space == packet.get_name().space:
                        return 'the configuration of :openhab:chan:`{label} <{device}::{label}>`'.format(label=c.get_label(),
                                                                            device=packet.get_device().get_java_class_name()), text

            # Try to map function to an action
            for a in self.oh.actions:
                if a.fn.get_name().space == packet.get_name().space:
                    return ':openhab:func:`{1}() <{0}::{2}{1}>`'.format(packet.get_device().get_java_class_name(),
                                                              packet.get_name(skip=-2 if high_level else 0).camel,
                                                              packet.get_device().get_category().headless+packet.get_device().get_name().camel), text

            # This is the last resort, typically only used for links that will not show up in the documentation anyway.
            if packet.get_type() == 'callback':
                if channel is None:
                    return '', text
                return ':openhab:chan:`{label} <{device}::{label}>`'.format(label=channel.get_label(),
                                                                            device=packet.get_device().get_java_class_name()), text
            else:
                return ':openhab:func:`{1}() <{0}::{2}{1}>`'.format(packet.get_device().get_java_class_name(),
                                                              packet.get_name(skip=-2 if high_level else 0).camel,
                                                              packet.get_device().get_category().headless+packet.get_device().get_name().camel), text

        return self.specialize_doc_rst_links(text, specializer, prefix='openhab')

    def get_java_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.java', '')
            return common.camel_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_openhab_channels(self):

        #functions = []
        channels = []
        template = '.. openhab:channel:: {device}::{label}\n\n{desc}\n\n{meta_table}\n\n'
        description = {
            'de': """
.. _{0}_openhab_channels:

Channel
-------

""",
            'en': """
.. _{0}_openhab_channels:

Channels
--------

"""
        }
        #cls = self.get_java_class_name()

        for c in self.oh.channels:
            meta_table_entries = []
            item_type = c.type.item_type
            if item_type == 'Color':
                item_type += ' - Only HSBType commands are accepted. Updating the brightness without changing the hue (e.g. by sending a PercentType) may fail.'

            meta_table_entries.append(('plain', 'UID', 'tinkerforge:{device_lower}:[UID]:{channel_camel}'.format(device_lower=self.get_thing_type_name(),
                            channel_camel=c.id.camel,)))
            meta_table_entries.append(('plain', 'Read only', 'Yes' if c.type.read_only else 'No'))
            if c.predicate != 'true':
                meta_table_entries.append(('plain', 'Predicate', common.select_lang(c.predicate_description)))

            if c.type.options is not None:
                item_type = 'Choice'
                meta_table_entries.append(('plain', 'Options', ', '.join([name for name, value in c.type.options])))
            elif c.type.command_options is not None:
                item_type = 'Commands ({})'.format(item_type)
                meta_table_entries.append(('plain', 'Commands', [x[0] for x in c.type.command_options] if len(c.type.command_options) > 1 else 'Accepts any string'))
            elif c.type.is_trigger_channel:
                item_type = 'Trigger ({})'.format(c.type.id.space)

            meta_table_entries.insert(0, ('plain', 'Type', item_type))

            desc = c.get_description().replace('|', '\|')

            if '<ul>' in desc:
                desc = desc.replace('<ul>', '\n\n').replace('<li>', '* ').replace('</li>', '\n').replace('</ul>', '')

            if not c.automatic_update:
                desc += '\n\nThis channel will only update after the configured update interval, not on changed values.'

            unit_name = ''
            if c.java_unit is not None and c.java_unit != 'SmartHomeUnits.ONE':
                unit_name = ' ' + c.java_unit.split('.')[1].replace('_', ' ').title().replace('Metre', 'Meter')
                meta_table_entries.append(('plain', 'Unit', unit_name))

            if c.type.min is not None and c.type.max is not None:
                if c.type.step is not None:
                    s = '{min}{unit} to {max}{unit} (Step {step}{unit})'.format(min=c.type.min, max=c.type.max, unit=common.wrap_non_empty(' ', unit_name, ''), step=c.type.step)
                else:
                    s = '{min}{unit} to {max}{unit}'.format(min=c.type.min, max=c.type.max, unit=common.wrap_non_empty(' ', unit_name, ''))
                meta_table_entries.append(('plain', 'Range', s))

            if c.type.params is not None:
                meta_table_entries += self.get_openhab_param_entries(c.type.params)

            channels.append(template.format(device=self.get_java_class_name(),
                                label=c.get_label(),
                                meta_table=common.make_rst_meta_table(common.merge_meta_sections(meta_table_entries)),
                                desc=desc))
        return common.select_lang(description).format(self.get_doc_rst_ref_name()) + '\n\n'.join(channels)

    def get_openhab_param_entries(self, params):
        meta_table_entries = []

        for i, p in enumerate(params):
            param_meta = []
            entries = [('Type', p.type if p.options is None else 'Choice'),
                        ('Default', p.default if p.options is None else [x[0] for x in p.options if x[1] == p.default][0]),
                        ('Unit', p.unit),
                        ('Min', p.min),
                        ('Max', p.max),
                        ('Step', p.step)]
            for l, r in entries:
                if r is not None:
                    param_meta.append('{}: {}'.format(l, r))

            if p.description is None:
                raise common.GeneratorError("Parameter {} has no description.".format(p.label))
            else:
                entry_tup = ('plain', 'Parameters', [('plain', p.label, ', '.join(param_meta)), common.shift_right(unescape(p.description), 2)])
            if p.options is not None:
                entry_tup[2].append('{}: {}'.format('Options', ', '.join([x[0] for x in p.options])))
            if i != len(params) - 1:
                entry_tup[2].append(unescape('<br/>'))
            meta_table_entries.append(entry_tup)
        return meta_table_entries

    def get_openhab_configuration(self):
        meta_table_entries = []

        meta_table_entries.append(('plain', 'UID', 'tinkerforge:{device_lower}:[UID]'.format(device_lower=self.get_thing_type_name())))
        meta_table_entries.append(('plain', 'Required firmware version', self.oh.required_firmware_version))
        meta_table_entries.append(('plain', 'Firmware update supported', 'yes' if self.oh.firmware_update_supported else 'no'))


        channels = [unescape('<a href="#{device}::{label}">{label}</a>'.format(label=c.get_label(), device=self.get_java_class_name())) for c in self.oh.channels]
        meta_table_entries.append(('plain', 'Channels', channels))

        actions = [unescape('<a href="#{0}::{2}{1}">{1}</a>'.format(self.get_java_class_name(),
                                                                    a.fn.get_name(skip = -2 if a.fn.has_high_level() else 0).camel,
                                                                    self.get_category().headless+self.get_name().camel)) for a in self.oh.actions]
        meta_table_entries.append(('plain', 'Actions', actions))

        if self.oh.params is not None:
            meta_table_entries += self.get_openhab_param_entries(self.oh.params)

        desc = """.. _{0}_openhab_api:

Thing
-----

"""

        return desc.format(self.get_name().under + '_' + self.get_category().under) + common.make_rst_meta_table(common.merge_meta_sections(meta_table_entries))

    def get_openhab_actions(self, type_):
        functions = []
        template = '.. openhab:function:: {device}::{fn}({params})\n\n{table}\n{desc}\n'

        if self.oh.actions == 'custom':
            return ''

        for action in self.oh.actions:
            packet = action.fn
            if packet.get_doc_type() != type_:
                continue

            skip = -2 if packet.has_high_level() else 0
            name = self.get_category().headless + self.get_name().camel + packet.get_name(skip=skip).camel
            params = packet.get_java_parameters(high_level=True)
            meta = packet.get_formatted_element_meta(lambda element, cardinality=None: element.get_java_type(cardinality=cardinality),
                                                     lambda element, index=None: element.get_name(index=index).headless,
                                                     return_object='always',
                                                     explicit_string_cardinality=True,
                                                     explicit_variable_stream_cardinality=True,
                                                     explicit_fixed_stream_cardinality=True,
                                                     explicit_common_cardinality=True,
                                                     high_level=True,
                                                     return_object_label_override={'de': 'TODO', 'en': 'Return Map'})
            meta_table = common.make_rst_meta_table(meta)
            desc = packet.get_java_formatted_doc(1)

            functions.append(template.format(device=self.get_java_class_name(), fn=name, params=params, table=meta_table, desc=desc))

        return ''.join(functions)

    def get_openhab_examples(self):
        def title_from_filename(filename):
            filename = filename.replace('Example', '').replace('.rules', '')
            return common.camel_to_space(filename)

        return common.make_rst_examples(title_from_filename, self)

    def get_openhab_doc(self):
        doc  = common.make_rst_header(self, has_device_identifier_constant=False)
        doc += common.make_rst_summary(self)
        if self.oh.doc is not None:
            doc += self.oh.doc
            doc += '\n\n'
        doc += self.get_openhab_examples()
        doc += '\n\n'
        doc += self.get_openhab_configuration()
        doc += '\n\n'
        doc += self.get_openhab_channels()
        doc += '\n\n'
        doc += """Actions
-------

Actions can be used in rules by creating an action object. All actions return a Map<String, Object>.
Returned values can be accessed by name, sometimes the type deduction needs some hints, as shown below:

.. code-block:: none

 val actions = getActions("tinkerforge", "tinkerforge:{device_lower}:[UID]")
 val hwVersion = actions.{device_headless}GetIdentity().get("hardwareVersion") as short[]
 logInfo("Example", "Hardware version: " + hwVersion.get(0) + "." + hwVersion.get(1) + "." + hwVersion.get(2))

""".format(device_lower=self.get_category().lower_no_space + self.get_name().lower_no_space,
           device_headless=self.get_category().headless + self.get_name().camel)

        for type_, caption in [ ('bf', 'Basic Actions'),
                                ('af', 'Advanced Actions'),
                                ('ccf', 'Trigger Channel Configuration Actions'),
                                ('vf', 'Virtual Actions'),
                                ('if', 'Internal Actions')]:
            actions = self.get_openhab_actions(type_)
            if len(actions) > 0:
                doc += "{}\n{}\n\n".format(caption, '^' * len(caption))
                doc += actions

        return doc

class JavaDocPacket(java_common.JavaPacket):
    def get_java_formatted_doc(self, shift_right):
        text = common.select_lang(self.get_doc_text())
        text = self.get_device().specialize_java_doc_function_links(text)

        text = text.replace('Callback ', 'Channel ')
        text = text.replace(' Callback', ' Channel')
        text = text.replace('callback ', 'channel ')
        text = text.replace(' callback', ' channel')

        def format_parameter(name):
            return '``{0}``'.format(name) # FIXME

        text = common.handle_rst_param(text, format_parameter)
        text = common.handle_rst_word(text)
        text = common.handle_rst_substitutions(text, self)

        prefix = 'val '

        def format_element_name(element, index):
            if index == None:
                return element.get_name().headless

            return '{0}[{1}]'.format(element.get_name().headless, index)

        text += common.format_constants(prefix, self, format_element_name)
        text += common.format_since_firmware(self.get_device(), self)

        return common.shift_right(text, shift_right)

class OpenHABDocGenerator(openhab_common.OpenHABGeneratorTrait, common.DocGenerator):
    is_openhab_doc_generator = True

    def get_bindings_name(self):
        return 'openhab'

    def get_bindings_display_name(self):
        return 'openHAB'

    def get_doc_rst_filename_part(self):
        return 'openHAB'

    def get_doc_example_regex(self):
        return r'^Example.*\.rules$'

    def get_device_class(self):
        return OpenHABDocDevice

    def get_packet_class(self):
        return JavaDocPacket

    def get_element_class(self):
        return java_common.JavaElement

    def generate(self, device):
        with open(device.get_doc_rst_path(), 'w') as f:
            f.write(device.get_openhab_doc())

    def is_matlab(self):
        return False

    def is_octave(self):
        return False

def generate(root_dir, language):
    if language != 'en':
        print("Generating {} is not implemented yet.".format(language))
        return
    common.generate(root_dir, language, OpenHABDocGenerator)

if __name__ == '__main__':
    for language in ['en', 'de']:
        print('=== Generating %s ===' % language)
        generate(os.getcwd(), language)

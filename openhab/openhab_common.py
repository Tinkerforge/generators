import copy
import os
import re
import sys
import math

sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'java'))
import common
import java_common


class OpenHABGeneratorTrait:
    def get_bindings_display_name(self):
        return 'openHAB'

    def get_bindings_name(self):
        return 'openhab'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().camel

class OpenHABUnit:
    def __init__(self, tf_unit, java_unit, java_number_type, tf_to_oh_divisor=1):
        self.tf_unit = tf_unit
        self.java_unit = java_unit
        self.java_number_type = java_number_type
        self.tf_to_oh_divisor = tf_to_oh_divisor

openHABUnits = [
    OpenHABUnit('Ampere', 'SmartHomeUnits.AMPERE', 'ElectricCurrent'),
    #OpenHABUnit('Bar', 'SmartHomeUnits.BAR', ''),
    OpenHABUnit('Bit Per Second', 'SmartHomeUnits.BIT_PER_SECOND', 'DataTransferRate'),
    OpenHABUnit('Byte', 'SmartHomeUnits.BYTE', 'DataAmount'),
    OpenHABUnit('Degree Celsius', 'SIUnits.CELSIUS', 'Temperature'),
    OpenHABUnit('Decibel', 'SmartHomeUnits.DECIBEL', 'Dimensionless'),
    OpenHABUnit('Degree', 'SmartHomeUnits.DEGREE_ANGLE', 'Angle'),
    OpenHABUnit('Degree Per Second', 'SmartHomeUnits.ONE', 'Dimensionless'),
    OpenHABUnit('Gram Per Cubic Meter', 'SmartHomeUnits.MICROGRAM_PER_CUBICMETRE', 'Density', tf_to_oh_divisor=1/(10**6)),
    OpenHABUnit('Gram', 'SIUnits.GRAM', 'Mass'),
    OpenHABUnit('Hertz', 'SmartHomeUnits.HERTZ', 'Frequency'),
    OpenHABUnit('Kelvin', 'SmartHomeUnits.KELVIN', 'Temperature'),
    OpenHABUnit('Kilometer Per Hour', 'SIUnits.KILOMETRE_PER_HOUR', 'Speed'),
    OpenHABUnit('Lux', 'SmartHomeUnits.LUX', 'Illuminance'),
    OpenHABUnit('Meter Per Second Squared', 'SmartHomeUnits.METRE_PER_SQUARE_SECOND', 'Acceleration'),
    OpenHABUnit('Meter Per Second', 'SmartHomeUnits.METRE_PER_SECOND', 'Speed'),
    OpenHABUnit('Meter', 'SIUnits.METRE', 'Length'),
    OpenHABUnit('Parts Per Million', 'SmartHomeUnits.PARTS_PER_MILLION', 'Dimensionless'),
    OpenHABUnit('Particles Per Cubic Meter', 'SmartHomeUnits.ONE', 'Dimensionless'),
    OpenHABUnit('Pascal', 'SIUnits.PASCAL', 'Pressure'),
    OpenHABUnit('Percent Relative Humidity', 'SmartHomeUnits.PERCENT', 'Dimensionless'),
    OpenHABUnit('Percent', 'SmartHomeUnits.PERCENT', 'Dimensionless'),
    OpenHABUnit('Ohm', 'SmartHomeUnits.OHM', 'ElectricResistance'),
    OpenHABUnit('Second', 'SmartHomeUnits.SECOND', 'Time'),
    OpenHABUnit('Standard Gravity', 'SmartHomeUnits.STANDARD_GRAVITY', 'Acceleration'),
    OpenHABUnit('Steps Per Second', 'SmartHomeUnits.ONE', 'Dimensionless'),
    OpenHABUnit('Tesla', 'SmartHomeUnits.TESLA', 'MagneticFluxDensity'),
    OpenHABUnit('Volt', 'SmartHomeUnits.VOLT', 'ElectricPotential'),
    OpenHABUnit('Volt-Ampere', 'SmartHomeUnits.ONE', 'Dimensionless'),
    OpenHABUnit('Volt-Ampere Reactive', 'SmartHomeUnits.ONE', 'Dimensionless'),
    OpenHABUnit('Watt-Hour', 'SmartHomeUnits.WATT_HOUR', 'Energy'),
    OpenHABUnit('Watt Per Square Meter', 'SmartHomeUnits.IRRADIANCE', 'Intensity'),
    OpenHABUnit('Watt', 'SmartHomeUnits.WATT', 'Power'),
    OpenHABUnit('UV Index', 'SmartHomeUnits.ONE', 'Dimensionless'),
    OpenHABUnit('None', 'SmartHomeUnits.ONE', 'Dimensionless'),
]

def long_literal(x):
    return 'L' if isinstance(x, int) and (x < -2**31 or x > 2**31 - 1) else ''

def check_for_unknown_keys(obj, dictionary, name):
    unknown_keys = [k for k in dictionary.keys() if k not in obj.__dict__.keys()]
    if len(unknown_keys) > 0:
        raise common.GeneratorError("Unknown openHAB {} configuration keys {}.".format(name, unknown_keys))

class OpenHAB:
    def __init__(self, **kwargs):
        self.channels = kwargs.get('channels', [])
        self.channel_types = kwargs.get('channel_types', [])
        self.imports = kwargs.get('imports', [])
        self.params = kwargs.get('params', [])
        self.param_groups = kwargs.get('param_groups', [])
        self.init_code = kwargs.get('init_code', '')
        self.dispose_code = kwargs.get('dispose_code', '')
        self.category = kwargs.get('category', None)
        self.custom = kwargs.get('custom', False)
        self.actions = kwargs.get('actions', [])
        self.is_bridge = kwargs.get('is_bridge', False)
        self.required_firmware_version = kwargs.get('required_firmware_version', False)
        self.firmware_update_supported = kwargs.get('firmware_update_supported', False)
        self.implemented_interfaces = kwargs.get('implemented_interfaces', [])

        check_for_unknown_keys(self, kwargs, 'top level')

class Channel:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.type = kwargs['type']
        self.init_code = kwargs.get('init_code', '')
        self.dispose_code = kwargs.get('dispose_code', '')
        self.java_unit = kwargs.get('java_unit', None)
        self.divisor = kwargs.get('divisor', 1)
        self.getters = kwargs.get('getters', [])
        self.setters = kwargs.get('setters', [])
        self.setter_refreshs = kwargs.get('setter_refreshs', [])
        self.callbacks = kwargs.get('callbacks', [])
        self.predicate = kwargs.get('predicate', 'true')
        self.predicate_description = kwargs.get('predicate_description', None)
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.automatic_update = kwargs.get('automatic_update', True)

        check_for_unknown_keys(self, kwargs, 'channel')

    def get_builder_call(self):
        template = """new ChannelDefinitionBuilder("{channel_id}", new ChannelTypeUID("{binding}", "{channel_type_id}")){with_calls}.build()"""
        with_calls = ['.withLabel("{}")'.format(self.get_label())]

        if self.description is not None:
            with_calls.append('.withDescription("{}")'.format(self.description))

        if self.type.is_system_type():
            binding = 'system'
            channel_type_id = self.type.id.camel.replace('system.', '')
        else:
            binding = 'tinkerforge'
            channel_type_id = self.type.id.camel

        return template.format(channel_id=self.id.camel, binding=binding, channel_type_id=channel_type_id, with_calls=''.join(with_calls))

    def get_label(self):
        return self.label if self.label is not None else self.type.label

    def get_description(self):
        return self.description if self.description is not None else self.type.description

class ChannelType:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.params = kwargs.get('params', [])
        self.param_groups = kwargs.get('param_groups', [])
        self.item_type = kwargs.get('item_type', None)
        self.category = kwargs.get('category', None)
        self.read_only = kwargs.get('read_only', None)
        self.pattern = kwargs.get('pattern', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.step = kwargs.get('step', None)
        self.options = kwargs.get('options', None)
        self.is_trigger_channel = kwargs.get('is_trigger_channel', False)
        self.command_options = kwargs.get('command_options', None)
        self.tags = kwargs.get('tags', [])

        check_for_unknown_keys(self, kwargs, 'channel type')

    def is_system_type(self):
        return self.id.space.startswith('system.')

    def get_builder_call(self):
        def get_state_description(min_=None, max_=None, options=None, pattern=None, readOnly=None, step=None):
            template = """StateDescriptionFragmentBuilder.create(){with_calls}.build().toStateDescription()"""
            with_calls = []

            if min_ is not None:
                with_calls.append(".withMinimum(BigDecimal.valueOf({}{}))".format(min_, long_literal(min_)))
            if max_ is not None:
                with_calls.append(".withMaximum(BigDecimal.valueOf({}{}))".format(max_, long_literal(max_)))
            if step is not None:
                with_calls.append(".withStep(BigDecimal.valueOf({}{}))".format(step, long_literal(step)))
            if pattern is not None:
                with_calls.append('.withPattern("{}")'.format(pattern))
            if readOnly is not None:
                with_calls.append('.withReadOnly({})'.format(str(readOnly).lower()))
            if options is not None:
                opts = []
                for name, value in options:
                    opts.append('new StateOption("{}", "{}")'.format(value, name))
                with_calls.append('.withOptions(Arrays.asList({}))'.format(', '.join(opts)))

            return template.format(with_calls=''.join(with_calls))

        template = """ChannelTypeBuilder.{state_or_trigger}(new ChannelTypeUID("tinkerforge", "{type_id_camel}"), "{label}"{state_item_type}).withConfigDescriptionURI(URI.create("channel-type:tinkerforge:{type_id_camel}")){with_calls}.build()"""
        with_calls = []

        if self.category is not None:
            with_calls.append('.withCategory("{}")'.format(self.category))

        if self.description is not None:
            with_calls.append('.withDescription("{}")'.format(self.description))

        with_calls += ['.withTag("{}")'.format(tag) for tag in self.tags]

        if not self.is_trigger_channel and any(x is not None for x in [self.min, self.max, self.pattern, self.read_only, self.options, self.step]):
            with_calls.append('.withStateDescription({})'.format(get_state_description(self.min, self.max, self.options, self.pattern, self.read_only, self.step)))

        if self.command_options is not None:
            with_calls.append('.withCommandDescription(CommandDescriptionBuilder.create(){}.build())'.format(''.join('.withCommandOption(new CommandOption("{}", "{}"))'.format(command, label) for label, command in self.command_options)))

        return template.format(state_or_trigger='trigger' if self.is_trigger_channel else 'state',
                               type_id_camel=self.id.camel,
                               label=self.label,
                               state_item_type='' if self.is_trigger_channel else ', "{}"'.format(self.item_type),
                               with_calls='\n'.join(with_calls))

class Setter:
    def __init__(self, **kwargs):
        self.packet = kwargs.get('packet', None)
        self.element = kwargs.get('element', None)
        self.packet_params = kwargs.get('packet_params', [])
        self.predicate = kwargs.get('predicate', 'true')
        self.command_type = kwargs.get('command_type', None)

        check_for_unknown_keys(self, kwargs, 'setter')

class Getter:
    def __init__(self, **kwargs):
        self.packet = kwargs.get('packet', None)
        self.element = kwargs.get('element', None)
        self.packet_params = kwargs.get('packet_params', [])
        self.predicate = kwargs.get('predicate', 'true')
        self.transform = kwargs.get('transform', None)

        check_for_unknown_keys(self, kwargs, 'getter')

class Callback:
    def __init__(self, **kwargs):
        self.packet = kwargs.get('packet', None)
        self.element = kwargs.get('element', None)
        self.filter = kwargs.get('filter', 'true')
        self.transform = kwargs.get('transform', None)

        check_for_unknown_keys(self, kwargs, 'callback')

class SetterRefresh:
    def __init__(self, **kwargs):
        self.channel = kwargs['channel']
        self.delay = kwargs['delay']

        check_for_unknown_keys(self, kwargs, 'setter refresh')

class Param:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.type = kwargs['type']
        self.context = kwargs.get('context', None)
        self.default = kwargs.get('default', None)
        self.description = kwargs.get('description', None)
        self.groupName = kwargs.get('groupName', None)
        self.label = kwargs.get('label', None)
        self.unit = kwargs.get('unit', None)
        self.unitLabel = kwargs.get('unitLabel', None)
        self.advanced = kwargs.get('advanced', None)
        self.limit_to_options = {None: None, 'true': True, 'false': False}[kwargs.get('limit_to_options', None)]
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.step = kwargs.get('step', None)
        self.options = kwargs.get('options', None)
        self.packet = kwargs.get('packet', None)
        self.element = kwargs.get('element', None)
        self.element_index = kwargs.get('element_index', None)
        self.virtual = kwargs.get('virtual', False)

        check_for_unknown_keys(self, kwargs, 'param')

    def get_builder_call(self, channel_name=None):
        template = """ConfigDescriptionParameterBuilder.create("{name}", Type.{type_upper}){with_calls}.build()"""

        if channel_name is not None:
            name = channel_name + self.name.camel
        else:
            name = self.name.headless

        with_calls = []

        if self.context is not None:
            with_calls.append('.withContext("{val}")'.format(val=self.context))

        if self.default is not None:
            with_calls.append('.withDefault("{val}")'.format(val=self.default))

        if self.description is not None:
            with_calls.append('.withDescription("{val}")'.format(val=self.description))

        if self.groupName is not None:
            with_calls.append('.withGroupName("{val}")'.format(val=self.groupName))

        if self.label is not None:
            with_calls.append('.withLabel("{val}")'.format(val=self.label))

        if self.unit is not None:
            with_calls.append('.withUnit("{val}")'.format(val=self.unit))

        if self.unitLabel is not None:
            with_calls.append('.withUnitLabel("{val}")'.format(val=self.unitLabel))

        if self.advanced is not None:
            with_calls.append('.withAdvanced({val})'.format(val='true' if self.advanced else 'false'))

        if self.limit_to_options is not None:
            with_calls.append('.withLimitToOptions({val})'.format(val='true' if self.limit_to_options else 'false'))

        if self.min is not None:
            with_calls.append('.withMinimum(BigDecimal.valueOf({}{}))'.format(self.min, long_literal(self.min)))

        if self.max is not None:
            with_calls.append('.withMaximum(BigDecimal.valueOf({}{}))'.format(self.max, long_literal(self.max)))

        if self.step is not None:
            with_calls.append('.withStepSize(BigDecimal.valueOf({}{}))'.format(self.step, long_literal(self.step)))

        if self.options is not None:
            with_calls.append('.withOptions(Arrays.asList({}))'.format(', '.join('new ParameterOption("{}", "{}")'.format(val, label) for label, val in self.options)))

        return template.format(name=name, type_upper=self.type.upper(), with_calls=''.join(with_calls))

class ParamGroup:
    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.context = kwargs.get('context', None)
        self.advanced = kwargs.get('advanced', 'false')
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)

        check_for_unknown_keys(self, kwargs, 'param group')

class Action:
    def __init__(self, **kwargs):
        self.fn = kwargs['fn']
        self.refreshs = kwargs.get('refreshs', [])

        check_for_unknown_keys(self, kwargs, 'action')


class OpenHABDevice(java_common.JavaDevice):
    def get_thing_type_name(self):
        return self.get_category().lower_no_space + self.get_name().lower_no_space


    def apply_defaults(self, oh):
        param_defaults = {
            'context': None,
            'default': None,
            'description': None,
            'groupName': None,
            'label': None,
            'unit': None,
            'unitLabel': None,
            'advanced': None,
            'limit_to_options': None,
            'min': None,
            'max': None,
            'step': None,
            'options': None,
            'packet': None,
            'element': None,
            'element_index': None,
            'virtual': False
        }

        channel_defaults = {
            'init_code': '',
            'dispose_code': '',

            'getters': [],
            'setters': [],
            'callbacks': [],

            'setter_refreshs': [],

            'java_unit': None,
            'divisor': 1,
            'predicate': 'true',

            'label': None,
            'description': None
        }

        getter_defaults = {
            'packet': None,
            'packet_params': [],
            'predicate': 'true',
            'transform': None
        }

        setter_defaults = {
            'packet': None,
            'packet_params': [],
            'predicate': 'true',
            'command_type': None
        }

        callback_defaults = {
            'packet': None,
            'filter': 'true',
            'transform': None,
        }

        channel_type_defaults = {
            'params': [],
            'param_groups': [],
            'category': None,
            'item_type': None,
            'pattern': None,
            'min': None,
            'max': None,
            'step': None,
            'options': None,
            'read_only': None,
            'is_trigger_channel': False,
            'command_options': None
        }

        param_group_defaults = {
            'label': None,
            'description': None,
            'context': None,
            'advanced': 'false',
        }

        oh_defaults = {
            'params': [],
            'param_groups': [],
            'channels': [],
            'channel_types': [],
            'imports': [],
            'init_code': '',
            'dispose_code': '',
            'category': None,
            'custom': False,
            'actions': [],
            'implemented_interfaces': []
        }

        action_defaults = {
            'refreshs': []
        }

        tmp = oh_defaults.copy()
        tmp.update(oh)
        oh = tmp

        for c_idx, channel in enumerate(oh['channels']):
            if 'divisor' in channel and channel['divisor'] != 1:
                for setter in channel.get('setters', []):
                    if '{divisor}' not in ', '.join(setter['packet_params']):
                        raise common.GeneratorError("Divisor not used in setter of channel {}".format(channel['id']))
                for getter in channel.get('getters', []):
                    if '{divisor}' not in getter['transform']:
                        raise common.GeneratorError("Divisor not used in getter of channel {}".format(channel['id']))
                for callback in channel.get('callbacks', []):
                    if '{divisor}' not in callback['transform']:
                        raise common.GeneratorError("Divisor not used in callback of channel {}".format(channel['id']))

            tmp_channel = channel_defaults.copy()
            tmp_channel.update(channel)

            for g_idx, getter in enumerate(tmp_channel['getters']):
                tmp_getter = getter_defaults.copy()
                tmp_getter.update(getter)
                tmp_channel['getters'][g_idx] = tmp_getter

            for s_idx, setter in enumerate(tmp_channel['setters']):
                tmp_setter = setter_defaults.copy()
                tmp_setter.update(setter)
                tmp_channel['setters'][s_idx] = tmp_setter

            for cb_idx, callback in enumerate(tmp_channel['callbacks']):
                tmp_callback = callback_defaults.copy()
                tmp_callback.update(callback)
                tmp_channel['callbacks'][cb_idx] = tmp_callback

            oh['channels'][c_idx] = tmp_channel

        for p_idx, param in enumerate(oh['params']):
            tmp = param_defaults.copy()
            tmp.update(param)
            oh['params'][p_idx] = tmp

        for ct_idx, channel_type in enumerate(oh['channel_types']):
            tmp_channel_type = channel_type_defaults.copy()
            tmp_channel_type.update(channel_type)

            for p_idx, param in enumerate(tmp_channel_type['params']):
                tmp_param = param_defaults.copy()
                tmp_param.update(param)
                tmp_channel_type['params'][p_idx] = tmp_param

            oh['channel_types'][ct_idx] = tmp_channel_type

        for pg_idx, param_group in enumerate(oh['param_groups']):
            tmp = param_group_defaults.copy()
            tmp.update(param_group)
            oh['param_groups'][pg_idx] = tmp

        if oh['actions'] != 'custom':
            for a_idx, action in enumerate(oh['actions']):
                if not isinstance(action, dict):
                    action = {'fn': action}

                tmp = action_defaults.copy()
                tmp.update(action)
                oh['actions'][a_idx] = tmp

        return oh

    def apply_features(self, oh):
        common_openhab = copy.deepcopy(__import__('device_commonconfig').common_openhab)
        iface_map = {
            'comcu_bricklet': 'CoMCUFlashable',
            'standard_bricklet_host_2_ports': 'StandardFlashHost',
            'standard_bricklet_host_4_ports': 'StandardFlashHost',
            'tng': 'TngFlashable'
        }
        for feature in self.raw_data['features']:
            if feature in iface_map:
                oh['implemented_interfaces'].append(iface_map[feature])
            if feature not in common_openhab:
                continue
            for key, value in common_openhab[feature].items():
                if key == 'actions' and oh[key] == 'custom':
                    continue
                if key == 'init_code' or key == 'dispose_code':
                    oh[key] += '\n' + value
                else:
                    oh[key] += value
        if len(oh['implemented_interfaces']) == 0 and self.get_category().space == 'Bricklet':
            oh['implemented_interfaces'].append('StandardFlashable')
        if any('Flashable' in x for x in oh['implemented_interfaces']):
            oh['firmware_update_supported'] = True
        return oh

    def find_unit_with_prefix(self, unit):
        for openHABUnit in openHABUnits:
            if unit.get_base_title().lower() in openHABUnit.tf_unit.lower():
                if openHABUnit.tf_unit.lower() == unit.get_title().lower():
                    return 1, openHABUnit
                for prefix in unit.get_allowed_prefixes():
                    for inv_prefix in unit.get_allowed_inverse_prefixes():
                        result = unit.clone(prefix, inv_prefix)
                        if openHABUnit.tf_unit.lower() == result.get_title().lower():
                            return 10**result.get_numerator_exponent() / 10**result.get_denominator_exponent(), openHABUnit
        return None

    def apply_packet_info(self, oh):
        for c in oh.channels:
            elements = [x.element for x in c.getters + c.setters + c.callbacks if x.element is not None]

            if len(elements) == 0:
                continue

            skip = False
            for name, fn in [('scale', lambda x: x.get_scale()), ('unit', lambda x: x.get_unit()), ('range', lambda x: x.get_range()), ('constants', lambda x: x.get_constant_group()), ('type', lambda x: x.get_type())]:
                if not all(fn(x) == fn(elements[0]) for x in elements):
                    print("openhab: Not all elements had same {}! Device {} Channel {} ".format(name, self.get_long_display_name(), c.id.space))
                    skip = True
            if skip:
                continue

            e = elements[0]
            # Deduce unit and divisor
            if not c.type.is_trigger_channel and c.java_unit is None and (c.type.item_type is None or 'Number' in c.type.item_type):
                if e.get_unit() is not None:
                    _, tf_unit = self.find_unit_with_prefix(e.get_unit())
                    c.java_unit = tf_unit.java_unit
                    c.type.item_type = 'Number:' + tf_unit.java_number_type
                else:
                    c.java_unit = 'SmartHomeUnits.ONE'
                    c.type.item_type = 'Number:Dimensionless'

            if not c.type.is_trigger_channel and c.divisor == 1 and isinstance(e.get_scale(), tuple):
                if e.get_unit() is not None:
                    factor, tf_unit = self.find_unit_with_prefix(e.get_unit())
                    c.divisor = tf_unit.tf_to_oh_divisor / factor * e.get_scale()[1] / e.get_scale()[0]
                else:
                    c.divisor = e.get_scale()[1] / e.get_scale()[0]

        def deduce_min_max(p, divisor):
            if divisor is None:
                return
            if p.element.get_constant_group() is None:
                if isinstance(p.element.get_range(), list):
                    new_min = min(r[0] for r in p.element.get_range())
                    new_max = max(r[1] for r in p.element.get_range())
                elif p.element.get_range() == 'type':
                    new_min, new_max = p.element.get_type_range()
                else:
                    return
                new_min /= divisor
                new_max /= divisor

                # with python 2 these can be integers
                if isinstance(new_min, float) and new_min.is_integer():
                    new_min = int(new_min)
                if isinstance(new_min, float) and new_max.is_integer():
                    new_max = int(new_max)

                if p.min is None:
                    p.min = new_min
                if p.max is None:
                    p.max = new_max
            else:
                pass

        def deduce_default(p, divisor):
            if divisor is None:
                if p.element.get_default() is not None:
                    new_default = 'true' if p.element.get_default() else 'false'
                else:
                    new_default = None
            else:
                if p.element.get_default() is not None:
                    new_default = p.element.get_default() / divisor
                elif p.default is None:
                    new_default = p.min if p.min is not None and p.min >= 0 else 0.0
                else:
                    return
                if isinstance(new_default, float) and new_default.is_integer():
                    new_default = int(new_default)

            if p.default is None:
                p.default = new_default

        def deduce_options(p):
            if p.element.get_constant_group() is None or p.element.get_range() != 'constants' or p.options is not None or p.type != 'integer':
                return
            p.options = p.element.get_constant_group().raw_data['constants']
            p.limit_to_options = 'true'

        for p in oh.params + [p for c in oh.channels for p in c.type.params]:
            if p.virtual and p.default is None:
                raise common.GeneratorError('openhab: Device {}: Parameter "{}" is virtual but no default is set.'.format(self.get_long_display_name(), p.label))

            if p.element is None or p.element.is_struct():
                continue

            if p.element.get_packet().get_doc_type() == 'af':
                p.advanced = True

            if p.type == 'integer':
                divisor = 1
            elif p.type == 'decimal':
                divisor = p.element.get_scale()[1] / p.element.get_scale()[0]
            else:
                divisor = None

            deduce_min_max(p, divisor)
            deduce_default(p, divisor)
            deduce_options(p)

        def get_min(element):
            if not isinstance(element.get_range(), list):
                return None

            return min([x[0] for x in element.get_range()])

        def get_max(element):
            if not isinstance(element.get_range(), list):
                return None

            return max([x[1] for x in element.get_range()])


        type_to_channels = {ct: [c for c in self.oh.channels if c.type == ct] for ct in self.oh.channel_types}
        for ct, channels in type_to_channels.items():
            div = channels[0].divisor if isinstance(channels[0].divisor, (int, float)) else 1
            elements = [x.element for c in channels for x in c.getters + c.setters + c.callbacks if x.element is not None]
            if 'Number' not in ct.item_type:
                continue
            mins = [get_min(e) for e in elements if get_min(e) is not None]
            maxs = [get_max(e) for e in elements if get_max(e) is not None]
            unscaled_min = None
            unscaled_max = None

            if len(mins) > 0:
                unscaled_min = min(mins)
                min_ = unscaled_min / div
                if isinstance(min_, float) and min_.is_integer():
                    min_ = int(min_)
                if ct.min is None:
                    ct.min = min_
            if len(maxs) > 0:
                unscaled_max = max(maxs)
                max_ = unscaled_max / div
                if isinstance(max_, float) and max_.is_integer():
                    max_ = int(max_)
                if ct.max is None:
                    ct.max = max_

            if ct.step is None and unscaled_min is not None and unscaled_max is not None:
                step = (ct.max - ct.min) / (unscaled_max - unscaled_min)
                if isinstance(step, float) and step.is_integer():
                    step = int(step)
                ct.step = step

            if ct.read_only is None:
                ct.read_only = len([x for c in channels for x in c.setters]) == 0

            digits = math.ceil(math.log10(div))

            if any(e.get_type() == 'float' for e in elements):
                number_placeholder = "%f"
            elif div != 1:
                number_placeholder = "%.{}f".format(digits)
            else:
                number_placeholder = "%d"

            if ct.item_type != 'Number:Dimensionless' or channels[0].java_unit != 'SmartHomeUnits.ONE':
                unit = '%unit%'
            else:
                unit = ''

            pattern = number_placeholder + common.wrap_non_empty(' ', unit, '')
            if ct.pattern is None:
                ct.pattern = pattern

        def deduce_predicate_description(c):
            # Try to extract referenced config param
            splt = c.predicate.split(' ')
            cfg_param = splt[0].split('.')[1]
            try:
                cfg_param = next(p for p in self.oh.params if p.name.headless == cfg_param)
            except StopIteration:
                return None

            if len(splt) == 1:
                return {'de': 'TODO', 'en': 'This channel will only be available if {} is enabled.'.format(cfg_param.label)}
            if len(splt) != 3:
                return None

            cmp = { '==': lambda l, r: str(l) == str(r),
                    '!=': lambda l, r: str(l) != str(r),
                    '<':  lambda l, r: float(l) < float(r),
                    '>':  lambda l, r: float(l) >  float(r),
                    '<=': lambda l, r: float(l) <= float(r),
                    '>=': lambda l, r: float(l) >= float(r)
                }.get(splt[1], None)
            if cmp is None:
                return None

            rhs = [x[0] for x in cfg_param.options if cmp(x[1], splt[2])]
            if len(rhs) == 0:
                return None
            rhs = rhs[0] if len(rhs) == 1 else ('one of ' + ', '.join(rhs))
            return {
                'de': 'TODO',
                'en': 'This channel will only be available if {} is {}.'.format(cfg_param.label, rhs)
            }


        for c in self.oh.channels:
            if c.predicate == 'true' or c.predicate_description is not None:
                continue

            desc = deduce_predicate_description(c)
            if desc is None:
                raise common.GeneratorError('openhab: Channel {} has a predicate, no configured predicate description and deducing a description failed!'.format(c.id.space))
            c.predicate_description = desc


    def sanity_check_config(self, oh):
        # Channels must have a label or inherit one
        for c in oh.channels:
            if c.get_label() is None:
                raise common.GeneratorError('openhab: Device {} Channel {} has no label and does not inherit one from its channel type.'.format(self.get_long_display_name(), c.id.space))

        # Channels must have a description or inherit one
        for c in oh.channels:
            if c.description is None and c.type.description is None:
                raise common.GeneratorError('openhab: Device {} Channel {} has no description and does not inherit one from its channel type.'.format(self.get_long_display_name(), c.id.space))

        # Channel labels must be title case
        for c in self.oh.channels:
            if any(word[0].islower() for word in c.get_label().split(' ')):
                raise common.GeneratorError('openhab: Device {}: Channel Label "{}" is not in title case.'.format(self.get_long_display_name(), c.get_label()))

        # Parameter labels must be title case
        for param in oh.params:
            if any(word[0].islower() for word in param.label.split(' ')):
                raise common.GeneratorError('openhab: Device {}: Parameter label "{}" is not in title case.'.format(self.get_long_display_name(), param.label))

        for ct in self.oh.channel_types:
            for param in ct.params:
                if any(word[0].islower() for word in param.label.split(' ')):
                    raise common.GeneratorError('openhab: Device {}: Channel Type {}: Parameter label "{}" is not in title case.'.format(self.get_long_display_name(), ct.id.space, param.label))

        # Params must have associated packet and element or be virtual
        for param in oh.params:
            if param.virtual or param.element is not None:
                continue
            raise common.GeneratorError('openhab: Device {}: Config parameter {} has no associated packet and element and is not marked virtual.'.format(self.get_long_display_name(), param.name.space))

        # Param must be marked virtual or have an associated element
        for c in oh.channels:
            if c.type.params is None:
                continue
            for param in c.type.params:
                if param.virtual or param.element is not None:
                    continue
                raise common.GeneratorError('openhab: Device {}: Channel {}: Config parameter {} has no associated element but is not marked virtual.'.format(self.get_long_display_name(), c.name.space, param.name.space))

         # Setters/Getters must have string params
        for c in oh.channels:
            for s in c.setters:
                for param in s.packet_params:
                    if not isinstance(param, str):
                        raise common.GeneratorError('openhab: Device "{}" Channel "{}" Setter "{}" Param "{}" is not a string'.format(self.get_long_display_name(), c.id.space, s.packet.get_name().space, param))
            for g in c.getters:
                for param in g.packet_params:
                    if not isinstance(param, str):
                        raise common.GeneratorError('openhab: Device "{}" Channel "{}" Getter "{}" Param "{}" is not a string'.format(self.get_long_display_name(), c.id.space, g.packet.get_name().space, param))

        # Params must be used
        for param in oh.params:
            needle = 'cfg.{}'.format(param.name.headless)
            init_code_uses_param = needle in oh.init_code
            channel_init_code_uses_param = any(c.init_code is not None and needle in c.init_code for c in oh.channels)
            channel_setters_use_param = any(needle in p for c in oh.channels for s in c.setters for p in s.packet_params if s.packet_params is not None)
            channel_getter_params_use_param = any(needle in p for c in oh.channels for g in c.getters for p in g.packet_params if g.packet_params is not None)
            channel_getter_transforms_use_param = any(needle in g.transform for c in oh.channels for g in c.getters if g.transform is not None)
            channel_predicate_uses_param = any(needle in c.predicate for c in oh.channels if c.predicate is not None)

            if not any([init_code_uses_param,
                        channel_init_code_uses_param,
                        channel_setters_use_param,
                        channel_getter_params_use_param,
                        channel_getter_transforms_use_param,
                        channel_predicate_uses_param]):
                raise common.GeneratorError('openhab: Device {}: Config parameter {} is not used in init_code or param mappings.'.format(self.get_long_display_name(), param.name.space))

        # Channel Params must be used in the channel
        for c in oh.channels:
            if c.type.params is None:
                continue
            for param in c.type.params:
                needle = 'channelCfg.{}'.format(param.name.headless)

                channel_init_code_uses_param = c.init_code is not None and needle in c.init_code
                channel_setters_use_param = any(needle in p for s in c.setters for p in s.packet_params if s.packet_params is not None)
                channel_getters_use_param = any(needle in p for g in c.getters for p in g.packet_params if g.packet_params is not None)
                channel_getter_params_use_param = any(needle in p for g in c.getters for p in g.packet_params if g.packet_params is not None)
                channel_getter_transforms_use_param = any(needle in g.transform for g in c.getters if g.transform is not None)
                channel_predicate_uses_param = c.predicate is not None and needle in c.predicate

                if not any([channel_init_code_uses_param,
                            channel_setters_use_param,
                            channel_getter_params_use_param,
                            channel_getter_transforms_use_param,
                            channel_predicate_uses_param]):
                    raise common.GeneratorError('openhab: Device {}: Channel {}: Config parameter {} is not used in init_code or param mappings.'.format(self.get_long_display_name(), c.id.space, param.name.space))


        # Use only one of command options, state description and trigger channel per channel type
        for ct in oh.channel_types:
            has_command_description = ct.command_options is not None
            has_state_description = any(x is not None for x in [ct.min, ct.max, ct.pattern, ct.read_only, ct.options, ct.step])
            is_trigger_channel = ct.is_trigger_channel

            if has_command_description and is_trigger_channel:
                raise common.GeneratorError('openhab: Device {} Channel Type {} has command description, but is flagged as trigger channel (which is the opposite).'.format(self.get_long_display_name(), ct.id))

            if has_command_description and has_state_description:
                raise common.GeneratorError('openhab: Device {} Channel Type {} has command description and state description (that would override the commands).'.format(self.get_long_display_name(), ct.id))

            if has_state_description and is_trigger_channel:
                raise common.GeneratorError('openhab: Device {} Channel Type {} has state description, but is flagged as trigger channel (which is stateless).'.format(self.get_long_display_name(), ct.id))

        # SetterRefreshs must refresh a known channel
        ids = [c.id for c in oh.channels]
        for c in oh.channels:
            for r in c.setter_refreshs:
                if not r.channel in ids:
                    raise common.GeneratorError('openhab: Device "{}" Channel "{}" has setter refresh for channel "{}" but no such channel was found.'.format(self.get_long_display_name(), c.id.space, r.channel.space))

        # Channels must have a command type per setter
        for c in oh.channels:
            for s in c.setters:
                if s.command_type is None:
                    raise common.GeneratorError('openhab: Device "{}" Channel "{}" Setter "{}" has no command_type.'.format(self.get_long_display_name(), c.id.space, s.packet.get_name().space))

        # Trigger channels must be of system. type (for now)
        for ct in self.oh.channel_types:
            if ct.is_trigger_channel and "system." in ct.id:
                raise common.GeneratorError('openhab: Device {} Channel Type {} is marked as trigger channel, but uses a custom type (not system.trigger or similar). This is theoretically supported, but the device handler currently assumes (when sending initial refreshs), that all trigger channels are of system-wide type.'.format(self.get_long_display_name(), ct.id))

        # QuantityType should only be used if the value has a unit
        for c in self.oh.channels:
            if c.java_unit == 'SmartHomeUnits.ONE' and any('QuantityType' in x.transform for x in c.getters + c.callbacks):
                raise common.GeneratorError('openhab: Device {} Channel {} uses a QuantityType but with SmartHomeUnits.ONE (i.e. is dimensionless). Let the generator decide which type to insert by using the {number_type} placeholder or use a DecimalType in this case.'.format(self.get_long_display_name(), c.id.space))

        # system.trigger channels should not use specific CommonTriggerEvents
        for c in self.oh.channels:
            if c.type.id.space == 'system.trigger' and any('CommonTriggerEvents.' in x.transform for x in c.getters + c.callbacks):
                raise common.GeneratorError('openhab: Device {} Channel {} has type system.trigger, but specific CommonTriggerEvents are used. These are only to be used with the other trigger channel types (e.g. system.rawbutton).'.format(self.get_long_display_name(), c.id.space))

    def find_channel_type(self, channel, channel_types):
        if channel['type'].startswith('system.'):
            system_type = ChannelType(**{'id': common.FlavoredName(channel['type']).get(), 'is_trigger_channel': True})
            #system_type = self.apply_defaults({'channel_types': {'id': common.FlavoredName(channel['type']).get()}})['channel_types'][0]
            return system_type
            #return ChannelType._make([common.FlavoredName(channel['type']).get()] + [None] * (len(ChannelType._fields) - 1))
        try:
            return next(ct for ct in channel_types if ct.id.space.replace(self.get_category().space + ' ' + self.get_name().space + ' ', '', 1) == channel['type'])
        except StopIteration:
            raise common.GeneratorError('openhab: Device "{}" Channel "{}" has type {}, but no such channel type was found.'.format(self.get_long_display_name(), channel['id'].space, channel['type']))

    def format_unit_element(self):
        def fmt(format_str, unit, divisor, is_setter):
            if unit is None or unit == 'SmartHomeUnits.ONE':
                number_type = 'DecimalType'
                unit = ''
            else:
                number_type = 'QuantityType<>'
                unit = ', ' + unit
            if divisor == 1:
                div = ''
            elif is_setter:
                div = ' * ' + str(divisor)
            else:
                div = ' / ' + str(divisor)
            return format_str.format(number_type=number_type,
                                     unit=unit,
                                     divisor=div)

        def fmt_dict(d, unit, divisor, is_setter):
            for k, v in d.items():
                if isinstance(v, str):
                    d[k] = fmt(v, unit, divisor, is_setter)

        for c in self.oh.channels:
            fmt_dict(c.__dict__, c.java_unit, c.divisor, False)
            for setter in c.setters:
                fmt_dict(setter.__dict__, c.java_unit, c.divisor, True)
                setter.packet_params = [fmt(x, c.java_unit, c.divisor, True) for x in setter.packet_params]

            for getter in c.getters:
                fmt_dict(getter.__dict__, c.java_unit, c.divisor, False)
            for callback in c.callbacks:
                fmt_dict(callback.__dict__, c.java_unit, c.divisor, False)

        for ct in self.oh.channel_types:
            for param in ct.params:
                fmt_dict(param.__dict__, param.unit, 1, False)


    def read_openhab_config(self):
        if 'openhab' in self.raw_data:
            oh = self.apply_defaults(self.raw_data['openhab'])
        else:
            oh = self.apply_defaults({})

        oh = self.apply_features(oh)
        oh = self.apply_defaults(oh)

        # Replace config placeholders
        def fmt(format_str, base_name):
            if not isinstance(format_str, str):
                return format_str
            name = common.FlavoredName(base_name).get()

            return format_str.format(title_words=name.space,#.title(),
                                     lower_words=name.lower,
                                     camel=name.camel,
                                     headless=name.headless,
                                     number_type='{number_type}',
                                     divisor='{divisor}',
                                     unit='{unit}')

        def fmt_dict(d, base_name):
            return {k: fmt(v, base_name) for k, v in d.items()}

        for c_idx, channel in enumerate(oh['channels']):
            oh['channels'][c_idx] = fmt_dict(channel, channel['id'])
            oh['channels'][c_idx]['getters'] = [fmt_dict(getter, channel['id']) for getter in oh['channels'][c_idx]['getters']]
            oh['channels'][c_idx]['setters'] = [fmt_dict(setter, channel['id']) for setter in oh['channels'][c_idx]['setters']]
            oh['channels'][c_idx]['callbacks'] = [fmt_dict(callback, channel['id']) for callback in oh['channels'][c_idx]['callbacks']]

        for ct_idx, channel_type in enumerate(oh['channel_types']):
            for p_idx, param in enumerate(channel_type['params']):
                channel_type['params'][p_idx] = fmt_dict(param, channel_type['id'])
            oh['channel_types'][ct_idx] = fmt_dict(channel_type, channel_type['id'])

        used_packets = []

        # Search possible packet usage in init_code etc.
        used_packet_names = re.findall("this\.([a-zA-Z0-9]+)\(", str(oh))
        for packet in self.get_packets():
            if packet.get_name().headless in used_packet_names:
                used_packets.append(packet)
            if packet.has_high_level() and packet.get_name(skip=-2).headless in used_packet_names:
                used_packets.append(packet)


        def find_packet(name):
            if name is None:
                return None
            for p in self.get_packets():
                if p.get_name().space == name:
                    used_packets.append(p)
                    return p
                if p.has_high_level() and p.get_name(skip=-2).space == name:
                    used_packets.append(p)
                    return p
            raise common.GeneratorError('openhab: Device {}: Packet {} not found.'.format(self.get_long_display_name(), name))

        def find_element(name, packet):
            for e in packet.get_elements(high_level=True):
                if e.get_name().space == name:
                    return e
            raise common.GeneratorError("Element {} not found in packet {}.".format(name, packet.get_name().space))


        # Convert from dicts to objects
        for ct_idx, channel_type in enumerate(oh['channel_types']):
            if channel_type['id'].startswith('system.'):
                channel_type['id'] = common.FlavoredName(channel_type['id']).get()
            else:
                channel_type['id'] = common.FlavoredName(self.get_category().space + ' ' + self.get_name().space + ' ' + channel_type['id']).get()

            for param in channel_type['params']:
                param['name'] = common.FlavoredName(param['name']).get()
                if param['packet'] is not None:
                    param['packet'] = find_packet(param['packet'])
                    param['element'] = find_element(param['element'], param['packet'])

            channel_type['params'] = [Param(**p) for p in channel_type['params']]
            oh['channel_types'][ct_idx] = ChannelType(**channel_type)

        for c_idx, channel in enumerate(oh['channels']):
            if channel['id'].startswith('system.'):
                channel['id'] = common.FlavoredName(channel['id']).get()
            else:
                channel['id'] = common.FlavoredName(self.get_category().space + ' ' + self.get_name().space + ' ' + channel['id']).get()

            for g_idx, getter in enumerate(oh['channels'][c_idx]['getters']):
                getter['packet'] = find_packet(getter['packet'])
                if 'element' in getter:
                    getter['element'] = find_element(getter['element'], getter['packet'])
                oh['channels'][c_idx]['getters'][g_idx] = Getter(**getter)
            for s_idx, setter in enumerate(oh['channels'][c_idx]['setters']):
                setter['packet'] = find_packet(setter['packet'])
                if 'element' in setter:
                    setter['element'] = find_element(setter['element'], setter['packet'])
                oh['channels'][c_idx]['setters'][s_idx] = Setter(**setter)
            for cb_idx, callback in enumerate(oh['channels'][c_idx]['callbacks']):
                callback['packet'] = find_packet(callback['packet'])
                if 'element' in callback:
                    callback['element'] = find_element(callback['element'], callback['packet'])
                oh['channels'][c_idx]['callbacks'][cb_idx] = Callback(**callback)

            oh['channels'][c_idx]['setter_refreshs'] = [SetterRefresh(**{'channel':common.FlavoredName(self.get_category().space + ' ' + self.get_name().space + ' ' + r['channel']).get(), 'delay': r['delay']}) for r in oh['channels'][c_idx]['setter_refreshs']]
            oh['channels'][c_idx]['type'] = self.find_channel_type(oh['channels'][c_idx], oh['channel_types'])
            oh['channels'][c_idx] = Channel(**channel)


        for p_idx, param in enumerate(oh['params']):
            param['name'] = common.FlavoredName(param['name']).get()
            if param['packet'] is not None:
                param['packet'] = find_packet(param['packet'])
                if not param['virtual']: # Allow configuring packets for virtual params: The documentation generator can use the packet as link hint.
                    param['element'] = [e for e in param['packet'].get_elements() if e.get_name().space == param['element']][0] # TODO: handle high-level parameters?
            oh['params'][p_idx] = Param(**param)

        for g_idx, group in enumerate(oh['param_groups']):
            oh['param_groups'][g_idx] = ParamGroup(**group)

        if oh['actions'] != 'custom':
            for a_idx, action in enumerate(oh['actions']):
                action['fn'] = find_packet(action['fn'])
                oh['actions'][a_idx] = Action(**action)

        if 'required_firmware_version' not in oh:
            oh['required_firmware_version'] = [2, 0, 0]

        req_version = max([packet.get_since_firmware() for packet in used_packets] + [oh['required_firmware_version']])
        oh['required_firmware_version'] = "{}.{}.{}".format(*req_version)

        self.oh = OpenHAB(**oh)
        self.apply_packet_info(self.oh)
        self.format_unit_element()
        self.sanity_check_config(self.oh)

        # Add update interval param to channels updated by the scheduler.
        # This must happen after the sanity checks, as they would
        # raise unused parameter errors:
        # The init code where the params are used is generated later.
        for c in self.oh.channels:
            if len(c.setters) == 0 and len(c.callbacks) == 0 and len(c.getters) > 0:
                c.automatic_update = False
                if len([p for p in c.type.params if p.label == 'Update Interval']) == 0:
                    c.type.params.append(Param(**{
                        'virtual': True,
                        'name': common.FlavoredName('Update Interval').get(),
                        'type': 'integer',
                        'unit': 'ms',
                        'label': 'Update Interval',
                        'description': 'Specifies the update interval in milliseconds. A value of 0 disables automatic updates.',
                        'default': 1000,
                    }))

        if self.oh.actions != 'custom':
            for action in self.oh.actions:
                for i, refresh in enumerate(action.refreshs):
                    try:
                        action.refreshs[i] = next(c for c in self.oh.channels if c.id.space.replace(self.get_category().space + ' ' + self.get_name().space + ' ', '', 1) == refresh)
                    except StopIteration:
                        raise common.GeneratorError('openhab: Device {}: Action {}: Unknown channel {}.'.format(self.get_long_display_name(), action.fn.get_name().space, refresh))




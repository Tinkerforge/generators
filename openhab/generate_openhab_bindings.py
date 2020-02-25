#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
MATLAB/Octave Bindings Generator
Copyright (C) 2019 Erik Fleckstein <erik@tinkerforge.com>

generate_openhab_bindings.py: Generator for OpenHAB bindings

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

from collections import namedtuple
import copy
import os
import shutil
import sys
import re

sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'java'))
import common
from java.generate_java_bindings import JavaBindingsGenerator, JavaBindingsDevice

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
        self.implemented_interfaces = kwargs.get('implemented_interfaces', [])

class Channel:
    def __init__(self, **kwargs):
        self.id = kwargs['id']
        self.type = kwargs['type']
        self.init_code = kwargs.get('init_code', '')
        self.dispose_code = kwargs.get('dispose_code', '')
        self.java_unit = kwargs.get('java_unit', None)
        self.divisor = kwargs.get('divisor', 1)
        self.is_trigger_channel = kwargs.get('is_trigger_channel', False)
        self.getters = kwargs.get('getters', [])
        self.setters = kwargs.get('setters', [])
        self.setter_refreshs = kwargs.get('setter_refreshs', [])
        self.callbacks = kwargs.get('callbacks', [])
        self.predicate = kwargs.get('predicate', 'true')
        self.label = kwargs.get('label', None)
        self.description = kwargs.get('description', None)
        self.automatic_update = kwargs.get('automatic_update', True)

    def get_builder_call(self):
        template = """new ChannelDefinitionBuilder("{channel_id}", new ChannelTypeUID("{binding}", "{channel_type_id}")){with_calls}.build()"""
        with_calls = []
        if self.label is not None:
            with_calls.append('.withLabel("{}")'.format(self.label))
        elif not self.type.is_system_type():
            with_calls.append('.withLabel("{}")'.format(self.type.label))
        if self.description is not None:
            with_calls.append('.withDescription("{}")'.format(self.description))

        if self.type.is_system_type():
            binding = 'system'
            channel_type_id = self.type.id.camel.replace('system.', '')
        else:
            binding = 'tinkerforge'
            channel_type_id = self.type.id.camel

        return template.format(channel_id=self.id.camel, binding=binding, channel_type_id=channel_type_id, with_calls=''.join(with_calls))

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

    def is_system_type(self):
        return self.id.space.startswith('system.')

    def get_builder_call(self):
        def get_state_description(min_=None, max_=None, options=None, pattern=None, readOnly=None, step=None):
            template = """StateDescriptionFragmentBuilder.create(){with_calls}.build().toStateDescription()"""
            with_calls = []

            if min_ is not None:
                with_calls.append(".withMinimum(BigDecimal.valueOf({}))".format(min_))
            if max_ is not None:
                with_calls.append(".withMaximum(BigDecimal.valueOf({}))".format(max_))
            if step is not None:
                with_calls.append(".withStep(BigDecimal.valueOf({}))".format(step))
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
        self.packet_params = kwargs.get('packet_params', [])
        self.predicate = kwargs.get('predicate', 'true')
        self.command_type = kwargs.get('command_type', None)

class Getter:
    def __init__(self, **kwargs):
        self.packet = kwargs.get('packet', None)
        self.packet_params = kwargs.get('packet_params', [])
        self.predicate = kwargs.get('predicate', 'true')
        self.transform = kwargs.get('transform', None)

class Callback:
    def __init__(self, **kwargs):
        self.packet = kwargs.get('packet', None)
        self.filter = kwargs.get('filter', 'true')
        self.transform = kwargs.get('transform', None)

class SetterRefresh:
    def __init__(self, **kwargs):
        self.channel = kwargs['channel']
        self.delay = kwargs['delay']

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
        self.limitToOptions = kwargs.get('limitToOptions', None)
        self.min = kwargs.get('min', None)
        self.max = kwargs.get('max', None)
        self.step = kwargs.get('step', None)
        self.options = kwargs.get('options', None)
        self.packet = kwargs.get('packet', None)
        self.element = kwargs.get('element', None)
        self.element_index = kwargs.get('element_index', None)
        self.virtual = kwargs.get('virtual', False)

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

        if self.limitToOptions is not None:
            with_calls.append('.withLimitToOptions({val})'.format(val='true' if self.advanced else 'false'))

        if self.min is not None:
            with_calls.append('.withMinimum(BigDecimal.valueOf({val}))'.format(val=self.min))

        if self.max is not None:
            with_calls.append('.withMaximum(BigDecimal.valueOf({val}))'.format(val=self.max))

        if self.step is not None:
            with_calls.append('.withStepSize(BigDecimal.valueOf({val}))'.format(val=self.step))

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

class Action:
    def __init__(self, **kwargs):
        self.fn = kwargs['fn']
        self.refreshs = kwargs.get('refreshs', [])

class OpenHABBindingsDevice(JavaBindingsDevice):
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
            'limitToOptions': None,
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
            'is_trigger_channel': False,
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
        if len(oh['implemented_interfaces']) == 0:
            oh['implemented_interfaces'].append('StandardFlashable')
        return oh

    def sanity_check_config(self, oh):
        # Channels must have a label or inherit one
        for c in oh.channels:
            if c.label is None and  c.type.label is None:
                raise common.GeneratorError('openhab: Device {} Channel {} has no label and does not inherit one from its channel type.'.format(self.get_long_display_name(), c.id.space))

        # Channels must have a description or inherit one
        for c in oh.channels:
            if c.description is None and c.type.description is None:
                raise common.GeneratorError('openhab: Device {} Channel {} has no description and does not inherit one from its channel type.'.format(self.get_long_display_name(), c.id.space))

        # Channel labels must be title case
        for c in self.oh.channels:
            label = c.label if c.label is not None else c.type.label
            if any(word[0].islower() for word in label.split(' ')):
                raise common.GeneratorError('openhab: Device {}: Channel Label "{}" is not in title case.'.format(self.get_long_display_name(), label))

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

        for c in oh.channels:
            if c.type.params is None:
                continue
            for param in c.type.params:
                if param.virtual or param.element is not None:
                    continue
                raise common.GeneratorError('openhab: Device {}: Channel {}: Config parameter {} is not used in init_code or param mappings.'.format(self.get_long_display_name(), c.name.space, param.name.space))

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
                    raise common.GeneratorError('openhab: Device {}: Channel {}: Config parameter {} is not used in init_code or param mappings.'.format(self.get_long_display_name(), c.name.space, param.name.space))


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


    def add_packet_info(self, param):
        if param['virtual']:
            return param

        if param['element'].get_packet().get_doc_type() == 'af':
            param['advanced'] = True

        return param


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

    def __init__(self, *args, **kwargs):
        JavaBindingsDevice.__init__(self, *args, **kwargs)

        if 'openhab' in self.raw_data:
            oh = self.apply_defaults(self.raw_data['openhab'])
        else:
            oh = self.apply_defaults({})

        oh = self.apply_features(oh)
        oh = self.apply_defaults(oh)

        # Replace config placeholders
        def fmt(format_str, base_name, unit, divisor):
            if not isinstance(format_str, str):
                return format_str
            name = common.FlavoredName(base_name).get()
            return format_str.format(title_words=name.space,#.title(),
                                     lower_words=name.lower,
                                     camel=name.camel,
                                     headless=name.headless,
                                     unit=unit,
                                     divisor=' / ' + str(divisor) if divisor != 1 else '')

        def fmt_dict(d, base_name, unit, divisor):
            return {k: fmt(v, base_name, unit, divisor) for k, v in d.items()}

        for c_idx, channel in enumerate(oh['channels']):
            oh['channels'][c_idx] = fmt_dict(channel, channel['id'], channel['java_unit'], channel['divisor'])
            oh['channels'][c_idx]['getters'] = [fmt_dict(getter, channel['id'], channel['java_unit'], channel['divisor']) for getter in oh['channels'][c_idx]['getters']]
            oh['channels'][c_idx]['setters'] = [fmt_dict(setter, channel['id'], channel['java_unit'], channel['divisor']) for setter in oh['channels'][c_idx]['setters']]
            oh['channels'][c_idx]['callbacks'] = [fmt_dict(callback, channel['id'], channel['java_unit'], channel['divisor']) for callback in oh['channels'][c_idx]['callbacks']]

        for ct_idx, channel_type in enumerate(oh['channel_types']):
            for p_idx, param in enumerate(channel_type['params']):
                channel_type['params'][p_idx] = fmt_dict(param, channel_type['id'], param['unit'], 1)
            oh['channel_types'][ct_idx] = fmt_dict(channel_type, channel_type['id'], None, None)

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
                    try:
                        param['element'] = [e for e in param['packet'].get_elements() if e.get_name().space == param['element']][0] # TODO: handle high-level parameters?
                    except:
                        raise common.GeneratorError("Element {} not found in packet {}.".format(param['element'], param['packet'].get_name().space))

            channel_type['params'] = [Param(**self.add_packet_info(p)) for p in channel_type['params']]
            oh['channel_types'][ct_idx] = ChannelType(**channel_type)

        for c_idx, channel in enumerate(oh['channels']):
            if channel['id'].startswith('system.'):
                channel['id'] = common.FlavoredName(channel['id']).get()
            else:
                channel['id'] = common.FlavoredName(self.get_category().space + ' ' + self.get_name().space + ' ' + channel['id']).get()

            for g_idx, getter in enumerate(oh['channels'][c_idx]['getters']):
                getter['packet'] = find_packet(getter['packet'])
                oh['channels'][c_idx]['getters'][g_idx] = Getter(**getter)
            for s_idx, setter in enumerate(oh['channels'][c_idx]['setters']):
                setter['packet'] = find_packet(setter['packet'])
                oh['channels'][c_idx]['setters'][s_idx] = Setter(**setter)
            for cb_idx, callback in enumerate(oh['channels'][c_idx]['callbacks']):
                callback['packet'] = find_packet(callback['packet'])
                oh['channels'][c_idx]['callbacks'][cb_idx] = Callback(**callback)

            oh['channels'][c_idx]['setter_refreshs'] = [SetterRefresh(**{'channel':common.FlavoredName(self.get_category().space + ' ' + self.get_name().space + ' ' + r['channel']).get(), 'delay': r['delay']}) for r in oh['channels'][c_idx]['setter_refreshs']]
            oh['channels'][c_idx]['type'] = self.find_channel_type(oh['channels'][c_idx], oh['channel_types'])
            oh['channels'][c_idx] = Channel(**channel)


        for p_idx, param in enumerate(oh['params']):
            param['name'] = common.FlavoredName(param['name']).get()
            if param['packet'] is not None:
                param['packet'] = find_packet(param['packet'])
                param['element'] = [e for e in param['packet'].get_elements() if e.get_name().space == param['element']][0] # TODO: handle high-level parameters?
            oh['params'][p_idx] = Param(**self.add_packet_info(param))

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

    def get_openhab_imports(self):
        oh_imports = ['java.net.URI',
                      'java.math.BigDecimal',
                      'java.util.ArrayList',
                      'java.util.Arrays',
                      'java.util.Collections',
                      'java.util.HashMap',
                      'java.util.List',
                      'java.util.Map',
                      'java.util.function.Function',
                      'java.util.function.BiConsumer',
                      'java.util.concurrent.ScheduledExecutorService',
                      'java.util.concurrent.ScheduledFuture',
                      'java.util.concurrent.TimeUnit',
                      'org.eclipse.smarthome.config.core.Configuration',
                      'org.eclipse.smarthome.config.core.ConfigDescription',
                      'org.eclipse.smarthome.config.core.ConfigDescriptionBuilder',
                      'org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type',
                      'org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder',
                      'org.eclipse.smarthome.config.core.ConfigDescriptionParameterGroup',
                      'org.eclipse.smarthome.config.core.ParameterOption',
                      'org.eclipse.smarthome.core.types.State',
                      'org.eclipse.smarthome.core.types.StateOption',
                      'org.eclipse.smarthome.core.types.Command',
                      'org.eclipse.smarthome.core.types.CommandDescriptionBuilder',
                      'org.eclipse.smarthome.core.types.CommandOption',
                      'org.eclipse.smarthome.core.thing.ChannelUID',
                      'org.eclipse.smarthome.core.thing.ThingStatus',
                      'org.eclipse.smarthome.core.thing.ThingTypeUID',
                      'org.eclipse.smarthome.core.thing.binding.BaseThingHandler',
                      'org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder',
                      'org.eclipse.smarthome.core.thing.type.ChannelType',
                      'org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder',
                      'org.eclipse.smarthome.core.thing.type.ChannelTypeUID',
                      'org.eclipse.smarthome.core.types.RefreshType',
                      'org.eclipse.smarthome.core.thing.type.ThingType',
                      'org.eclipse.smarthome.core.thing.type.ThingTypeBuilder',
                      'org.eclipse.smarthome.core.types.StateDescriptionFragmentBuilder',
                      'org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants',
                      'org.slf4j.Logger',
                      'org.slf4j.LoggerFactory'] + self.oh.imports

        return '\n'.join('import {};'.format(i) for i in oh_imports) + '\n'

    def get_openhab_device_wrapper_functions(self):
        func_template = """public {device_class}{return_type} {name}({params_signature}) throws TinkerforgeException {{
    {return_}this.dev.{name}({params});
}}"""

        cb_template = """public void add{0}Listener({1}.{0}Listener l) {{
    this.dev.add{0}Listener(l);
}}

public void remove{0}Listener({1}.{0}Listener l) {{
    this.dev.remove{0}Listener(l);
}}"""
        funcs = []
        for packet in self.get_packets('function'):
            ret_count = len(packet.get_elements(direction='out', high_level=True))
            ret_type = packet.get_java_return_type(high_level=True)
            funcs.append(func_template.format(device_class=self.get_java_class_name()+'.' if ret_count > 1 else '',
                                              return_type=ret_type,
                                              name=packet.get_name().headless if not packet.has_high_level() else packet.get_name(skip=-2).headless,
                                              params_signature=packet.get_java_parameters(high_level=True),
                                              params=packet.get_java_parameters(high_level=True, context='call'),
                                              return_='return ' if ret_count > 0 else ''))

        for packet in self.get_packets('callback'):
            funcs.append(cb_template.format(packet.get_name().camel if not packet.has_high_level() else packet.get_name(skip=-2).camel,
                                            self.get_java_class_name()))

        return '\n\n'.join(funcs)

    def get_openhab_device_wrapper(self):
        template = """{header}
package org.eclipse.smarthome.binding.tinkerforge.internal.device;

{imports}
import com.tinkerforge.{device_camel};
import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;

public class {device_camel}Wrapper extends DeviceWrapper {interfaces}{{
    {device_camel} dev;

    {device_info}

    public {device_camel}Wrapper(String uid, IPConnection ipcon) {{
        super();
        this.dev = new {device_camel}(uid, ipcon);
    }}

    {wrapper_consts}

    {wrapper_funcs}

    {device_impl}
}}"""

        dev_info_template = 'public final static DeviceInfo DEVICE_INFO = new DeviceInfo({device_camel}.DEVICE_DISPLAY_NAME, "{device_lower}", {device_camel}.DEVICE_IDENTIFIER, {device_camel}Wrapper.class, {actions}Actions.class, "{version}", {isCoMCU});'

        dev_info = dev_info_template.format(device_lower=self.get_category().lower_no_space + self.get_name().lower_no_space,
                                            device_camel=self.get_java_class_name(),
                                            actions='Default' if len(self.oh.actions) == 0 else self.get_java_class_name(),
                                            version=self.oh.required_firmware_version,
                                            isCoMCU='true' if self.has_comcu() else 'false')

        return template.format(header=self.get_generator().get_header_comment('asterisk'),
                               imports=self.get_openhab_imports(),
                               device_camel=self.get_category().camel + self.get_name().camel,
                               interfaces=common.wrap_non_empty('implements ', ', '.join(self.oh.implemented_interfaces), ''),
                               device_info=dev_info,
                               wrapper_consts=self.get_java_constants(),
                               wrapper_funcs=self.get_openhab_device_wrapper_functions(),
                               device_impl=self.get_openhab_device_impl())

    def get_filtered_elements_and_type(self, packet, elements, out_of_class=False):
        if len(elements) > 1:
            type_ = packet.get_java_object_name(packet.has_high_level())
            if out_of_class:
                type_ = packet.get_device().get_java_class_name() + '.' + type_
        else:
            type_ = elements[0].get_java_type()

        return elements, type_

    def get_openhab_channel_init_code(self):
        manual_update_template = """if(channelCfg.updateInterval > 0) {{
    this.manualChannelUpdates.add(scheduler.scheduleWithFixedDelay(() -> {{if(handler.getThing().getStatus() == ThingStatus.ONLINE) {{handler.handleCommand(new ChannelUID(handler.getThing().getUID(), "{channel_name_camel}"), RefreshType.REFRESH);}}}}, channelCfg.updateInterval, channelCfg.updateInterval, TimeUnit.MILLISECONDS));
}}"""

        init_code = []
        for c in self.oh.channels:
            channel_cfg = ['{channel_type_name_camel}Config channelCfg = getChannelConfigFn.apply("{channel_name_camel}").as({channel_type_name_camel}Config.class);'
                               .format(channel_name_camel=c.id.camel,
                                       channel_type_name_camel=c.type.id.camel)]
            if c.type.is_system_type():
                channel_cfg = []
            if c.predicate != 'true':
                init_code += ['if ({}) {{'.format(c.predicate)]
            else:
                init_code += ['{']

            init_code +=  channel_cfg + c.init_code.split('\n')
            if not c.automatic_update:
                init_code += [manual_update_template.format(channel_name_camel=c.id.camel)]
            init_code += ['}']
        return init_code

    def get_openhab_callback_impl(self):
        transformation_template = """    private {state_or_string} transform{camel}Callback{i}({callback_args}{device_camel}Config cfg) {{
        return {transform};
    }}"""
        cb_registration = '{predicate}this.add{camel}Listener(this.reg(({args}) -> {{if({filter}) {{{updateFn}.accept("{channel_camel}", transform{channel_camel}Callback{i}({args}{comma}cfg));}}}}, this.dev::remove{camel}Listener));{end_predicate}'

        regs = []

        dispose_template = '{predicate}{code}{end_predicate}'

        dispose_code = []
        lambda_transforms = []
        for c in self.oh.channels:
            if len(c.callbacks) == 0:
                continue

            for i, callback in enumerate(c.callbacks):
                elements = callback.packet.get_elements(direction='out', high_level=True)
                regs.append(cb_registration.format(
                                                predicate='if({}) {{\n'.format(c.predicate) if c.predicate != 'true' else '',
                                                camel=callback.packet.get_name().camel,
                                                filter=callback.filter,
                                                channel_camel=c.id.camel,
                                                args=', '.join(e.get_name().headless for e in elements),
                                                updateFn='triggerChannelFn' if c.is_trigger_channel else 'updateStateFn',
                                                i=i,
                                                comma=', ' if len(elements) > 0 else '',
                                                end_predicate='}' if c.predicate != 'true' else ''))

                packet_name = callback.packet.get_name().camel if not callback.packet.has_high_level() else callback.packet.get_name(skip=-2).camel
                if len(c.dispose_code) > 0:
                    dispose_code += [dispose_template.format(predicate='if({}) {{\n'.format(c.predicate) if c.predicate != 'true' else '',
                                                            code=c.dispose_code,
                                                            end_predicate='}' if c.predicate != 'true' else '')]
                lambda_transforms.append(transformation_template.format(state_or_string='String' if c.is_trigger_channel else 'org.eclipse.smarthome.core.types.State',
                                                                camel=c.id.camel,
                                                                callback_args=common.wrap_non_empty('', ', '.join(e.get_java_type() + ' ' + e.get_name().headless for e in elements), ', '),
                                                                transform=callback.transform,
                                                                i=i,
                                                                device_camel=self.get_category().camel + self.get_name().camel))

        return (regs,  dispose_code, lambda_transforms)

    def get_openhab_getter_impl(self):
        func_template = """    @Override
    public void refreshValue(String channel, org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {{
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        switch(channel) {{
            {channel_cases}
            default:
                logger.warn("Refresh for unknown channel {{}}", channel);
                break;
        }}
    }}
    """

        getter_template = """{{
            {type_} value = this.{getter}({getter_params});
            if({predicate})
                {updateFn}.accept(channel, transform{camel}Getter{i}(value, cfg));
        }}"""

        transformation_template = """    private {state_or_string} transform{camel}Getter{i}({type_} value, {device_camel}Config cfg) {{
        return {transform};
    }}"""

        case_template_with_config = """case "{camel}": {{
                   {channel_type_camel}Config channelCfg = channelConfig.as({channel_type_camel}Config.class);
                   {getters}
                   return;
               }}"""
        case_template = """case "{camel}":
                   {getters}
                   return;"""
        empty_case_template = """case "{camel}":
               return;"""



        channel_cases = []
        transforms = []
        for c in self.oh.channels:
            if len(c.getters) == 0:
                channel_cases.append(empty_case_template.format(camel=c.id.camel))
                continue


            template = case_template if c.type.is_system_type() else case_template_with_config
            channel_getters = []
            for i, getter in enumerate(c.getters):
                packet_name = getter.packet.get_name().headless if not getter.packet.has_high_level() else getter.packet.get_name(skip=-2).headless
                elements = getter.packet.get_elements(direction='out', high_level=True)
                _, type_ = self.get_filtered_elements_and_type(getter.packet, elements, out_of_class=True)

                channel_getters.append(getter_template.format(updateFn='triggerChannelFn' if c.is_trigger_channel else 'updateStateFn',
                                                              camel=c.id.camel,
                                                              getter=packet_name,
                                                              getter_params=', '.join(getter.packet_params),
                                                              i=i,
                                                              type_=type_,
                                                              predicate=getter.predicate))



                transforms.append(transformation_template.format(device_camel=self.get_category().camel + self.get_name().camel,
                                                                 state_or_string='String' if c.is_trigger_channel else 'org.eclipse.smarthome.core.types.State',
                                                                 camel=c.id.camel,
                                                                 type_=type_,
                                                                 transform=getter.transform,
                                                                 i=i))

            channel_cases.append(template.format(camel=c.id.camel,
                                                 channel_type_camel=c.type.id.camel,
                                                 getters='\n                   '.join(channel_getters)))

        return (func_template.format(name_camel=self.get_category().camel + self.get_name().camel,
                                     channel_cases='\n            '.join(channel_cases)), transforms)


    def get_openhab_setter_impl(self):
        template = """    @Override
    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command) throws TinkerforgeException {{
        List<SetterRefresh> result = {refresh_init};
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        switch(channel) {{
            {channel_cases}
            default:
                logger.warn("Command for unknown channel {{}}", channel);
        }}
        return result;
    }}"""

        setter_template = "this.{setter}({setter_params});"
        setter_with_predicate_template = """if({pred}) {{
    this.{setter}({setter_params});
}}"""
        command_template = """if (command instanceof {command_type}) {{
                    {channel_type_camel}Config channelCfg = channelConfig.as({channel_type_camel}Config.class);
                    {command_type} cmd = ({command_type}) command;
                    {setter}
                }}
        """
        case_template = """case "{camel}":
                {commands}
                else {{
                    logger.warn("Command type {{}} not supported for channel {{}}. Please use one of {command_types}.", command.getClass().getName(), channel);
                }}
                {setter_refreshs}
                break;"""
        channel_cases = []
        for c in self.oh.channels:
            if len(c.setters) == 0:
                continue
            refresh_template = 'result.add(new SetterRefresh("{}", {}));'

            refreshs = '\n\t\t\t\t'.join(refresh_template.format(r.channel.camel, r.delay) for r in c.setter_refreshs)

            commands = []
            first = True
            for s in c.setters:
                packet_name = s.packet.get_name().headless if not s.packet.has_high_level() else s.packet.get_name(skip=-2).headless

                if s.predicate == 'true':
                    setter = setter_template.format(setter=packet_name, setter_params=', '.join(s.packet_params))
                else:
                    setter = setter_with_predicate_template.format(setter=packet_name,
                                                                         setter_params=', '.join(s.packet_params),
                                                                         pred=s.predicate)

                commands.append(command_template.format(channel_type_camel=c.type.id.camel,
                                                       command_type=s.command_type,
                                                       setter=setter))
                first = False

            channel_cases.append(
                case_template.format(camel=c.id.camel,
                                     command_types=', '.join(s.command_type for s in c.setters),
                                     commands='\n'.join(commands),
                                     setter_refreshs=refreshs))

        if any(len(c.setter_refreshs) > 0 for c in self.oh.channels):
            refresh_init = 'new ArrayList<SetterRefresh>()'
        else:
            refresh_init = 'Collections.emptyList()'

        return template.format(refresh_init=refresh_init,
                              name_camel=self.get_category().camel + self.get_name().camel,
                              channel_cases='\n            '.join(channel_cases))

    def get_openhab_channel_enablers(self):
        template = """if ({pred}) {{
                result.add("{channel_camel}");
            }}"""

        enablers = []
        for c in self.oh.channels:
            name = c.id.camel
            if c.predicate == 'true':
                enablers.append('result.add("{channel_camel}");'.format(channel_camel=name))
            else:
                enablers.append(template.format(pred=c.predicate, channel_camel=name))

        return enablers

    def get_openhab_device_impl(self):
        template = """
    private final Logger logger = LoggerFactory.getLogger({name_camel}Wrapper.class);
    private final static Logger static_logger = LoggerFactory.getLogger({name_camel}Wrapper.class);

    @Override
    public void initialize(org.eclipse.smarthome.config.core.Configuration config, Function<String, org.eclipse.smarthome.config.core.Configuration> getChannelConfigFn, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn, ScheduledExecutorService scheduler, BaseThingHandler handler) throws TinkerforgeException {{
        this.dev.setResponseExpectedAll(true);
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        {callback_registrations}
        {init_code}
    }}

    @Override
    public void dispose(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException {{
        super.dispose(config);
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        {dispose_code}
    }}

    @Override
    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException{{
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        List<String> result = new ArrayList<String>();
        {channel_enablers}
        return result;
    }}

    {get_channel_type}

    {get_thing_type}

    {get_config_description}

    {refresh_value}

    {handle_command}

    {transforms}
"""

        init_code = self.oh.init_code.split('\n') + self.get_openhab_channel_init_code()
        dispose_code = self.oh.dispose_code.split('\n')
        callback_regs, callback_dispose_code, lambda_transforms = self.get_openhab_callback_impl()
        refresh_value, getter_transforms = self.get_openhab_getter_impl()
        handle_command = self.get_openhab_setter_impl()
        channel_enablers = self.get_openhab_channel_enablers()

        return template.format(name_camel=self.get_category().camel + self.get_name().camel,
                               init_code='\n\t\t'.join(init_code),
                               callback_registrations='\n\t\t'.join(callback_regs),
                               dispose_code='\n\t\t'.join(callback_dispose_code + dispose_code),
                               channel_enablers='\n\t\t'.join(channel_enablers),
                               get_channel_type=self.get_openhab_get_channel_type_impl(),
                               get_thing_type=self.get_openhab_get_thing_type_impl(),
                               get_config_description=self.get_openhab_get_config_description_impl(),
                               refresh_value=refresh_value,
                               handle_command=handle_command,
                               transforms='\n\t'.join(lambda_transforms + getter_transforms))

    def get_openhab_get_channel_type_impl(self):
        template = """public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {{
        switch(channelTypeUID.getId()) {{
            {}
            default:
                static_logger.debug("Unknown channel type ID {{}}", channelTypeUID.getId());
                break;
        }}

        return null;
    }}"""

        case_template = """case "{channel_type_id}":
                return {channel_type_builder_call};"""

        cases = [case_template.format(channel_type_id=ct.id.camel,
                                      channel_type_builder_call=ct.get_builder_call())
                 for ct in self.oh.channel_types]
        return template.format('\n            '.join(cases))



    def get_openhab_get_thing_type_impl(self):
        template = """ThingTypeBuilder.instance(thingTypeUID, "{label}").isListed(false).withSupportedBridgeTypeUIDs(Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICK_DAEMON.toString())).withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId())){with_calls}.build{bridge}()"""

        with_calls = []
        if self.oh.category is not None:
            with_calls.append('.withCategory("{}")'.format(self.oh.category))
        with_calls.append('.withDescription("{}")'.format(common.select_lang(self.get_description()).replace('"', '\\"')))
        with_calls.append('.withChannelDefinitions(Arrays.asList({}))'.format(', '.join(c.get_builder_call() for c in self.oh.channels)))
        with_calls.append('.withProperties(props)')
        label = 'Tinkerforge ' + self.get_long_display_name()
        not_supported = len(self.oh.channels) == 0 and len(self.oh.actions) == 0
        if not_supported:
            label += ' - This device is not supported yet.'

        builder_call = template.format(label=label, with_calls=''.join(with_calls), bridge='Bridge' if self.oh.is_bridge else '')

        return """public static ThingType getThingType(ThingTypeUID thingTypeUID) {{
             Map<String, String> thingTypeProperties = ThingTypeBuilder.instance(thingTypeUID, "unused").build().getProperties();
             Map<String, String> props = new HashMap<String, String>(thingTypeProperties);
             props.putIfAbsent(TinkerforgeBindingConstants.PROPERTY_MINIMUM_FIRMWARE_VERSION, DEVICE_INFO.minimum_fw_version);
        return {};
    }}""".format(builder_call)



    def get_openhab_parameter_group_ctor_list(self, param_groups):
        ctor_template = 'new ConfigDescriptionParameterGroup("{}", "{}", {}, "{}", "{}")'

        ctors = []
        for pg in param_groups:
            ctor_params = (item if item is not None else 'null' for item in [pg.name, pg.context, pg.advanced, pg.label, pg.description])
            ctors.append(ctor_template.format(*ctor_params))

        return ', '.join(ctors)

    def get_openhab_get_config_description_impl(self):
        template = """public static ConfigDescription getConfigDescription(URI uri) {{
        switch(uri.toASCIIString()) {{
            {cases}
            default:
                static_logger.debug("Unknown config description URI {{}}", uri.toASCIIString());
                break;
        }}
        return null;
    }}"""

        case_template = """case "{uri}":
                return ConfigDescriptionBuilder.create(uri).withParameters(Arrays.asList({builder_calls})).withParameterGroups(Arrays.asList({groups})).build();"""

        cases = [case_template.format(uri='thing-type:tinkerforge:' + self.get_category().lower_no_space + self.get_name().lower_no_space,
                                      builder_calls=', '.join(p.get_builder_call() for p in self.oh.params),
                                      groups=self.get_openhab_parameter_group_ctor_list(self.oh.param_groups))
                ] + \
                [case_template.format(uri='channel-type:tinkerforge:' + ct.id.camel,
                                      builder_calls=', '.join(p.get_builder_call() for p in ct.params),
                                      groups=self.get_openhab_parameter_group_ctor_list(ct.param_groups)) for ct in self.oh.channel_types
                ]

        return template.format(cases='\n            '.join(cases))

    def get_openhab_actions_class(self):
        template = """package org.eclipse.smarthome.binding.tinkerforge.internal.device;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;
import org.eclipse.smarthome.binding.tinkerforge.internal.handler.DeviceHandler;
import org.eclipse.smarthome.core.thing.binding.ThingActions;
import org.eclipse.smarthome.core.thing.binding.ThingActionsScope;
import org.eclipse.smarthome.core.thing.binding.ThingHandler;
import org.eclipse.smarthome.core.types.RefreshType;
import org.eclipse.smarthome.core.thing.ChannelUID;
import org.openhab.core.automation.annotation.ActionInput;
import org.openhab.core.automation.annotation.ActionOutput;
import org.openhab.core.automation.annotation.RuleAction;

import java.util.Map;
import java.util.HashMap;

import com.tinkerforge.TinkerforgeException;
import com.tinkerforge.{device_camel};

@ThingActionsScope(name = "tinkerforge")
@NonNullByDefault
public class {device_camel}Actions implements ThingActions {{

    private @Nullable DeviceHandler handler;

    @Override
    public void setThingHandler(@Nullable ThingHandler handler) {{ this.handler = (DeviceHandler) handler; }}

    @Override
    public @Nullable ThingHandler getThingHandler() {{ return handler; }}

    {actions}
}}
"""
        input_action_template = """    @RuleAction(label = "{label}")
    public void {device_headless}{id_camel}(
            {annotated_inputs}) throws TinkerforgeException {{
        (({device_camel}Wrapper)this.handler.getDevice()).{packet_headless}({packet_params});
        {refreshs}
    }}

    public static void {device_headless}{id_camel}(@Nullable ThingActions actions{typed_inputs}) throws TinkerforgeException {{
        if (actions instanceof {device_camel}Actions) {{
            (({device_camel}Actions) actions).{device_headless}{id_camel}({inputs});
        }} else {{
            throw new IllegalArgumentException("Instance is not an {device_camel}Actions class.");
        }}
    }}"""

        output_action_template = """    @RuleAction(label = "{label}")
    public {output_annotations}
           Map<String, Object> {device_headless}{id_camel}(
            {annotated_inputs}) throws TinkerforgeException {{
        Map<String, Object> result = new HashMap<>();
        {result_type} value = (({device_camel}Wrapper)this.handler.getDevice()).{packet_headless}({packet_params});
        {refreshs}
        {transforms}
        return result;
    }}

    public static Map<String, Object> {device_headless}{id_camel}(@Nullable ThingActions actions{typed_inputs}) throws TinkerforgeException {{
        if (actions instanceof {device_camel}Actions) {{
            return (({device_camel}Actions) actions).{device_headless}{id_camel}({inputs});
        }} else {{
            throw new IllegalArgumentException("Instance is not an {device_camel}Actions class.");
        }}
    }}"""

        input_template = """@ActionInput(name = "{id}") {type} {id}"""

        output_template = """@ActionOutput(name = "{id}", type="{type}")"""

        transform_template = """result.put("{id}", {transform});"""

        refresh_template = """if(handler.getThing().getChannel(new ChannelUID(handler.getThing().getUID(), "{channel_name}")) != null){{\n\tthis.handler.handleCommand(new ChannelUID(handler.getThing().getUID(), "{channel_name}"), RefreshType.REFRESH);\n}}"""

        actions = []
        for action in self.oh.actions:
            packet = action.fn
            inputs = packet.get_elements(direction='in', high_level=True)
            outputs = packet.get_elements(direction='out', high_level=True)

            annotated_inputs = [input_template.format(id=elem.get_name().headless,
                                                      type=elem.get_java_type()) for elem in inputs]
            typed_inputs = ["{type} {id}".format(id=elem.get_name().headless,
                                                 type=elem.get_java_type()) for elem in inputs]
            input_names = [elem.get_name().headless for elem in inputs]

            refreshs = [refresh_template.format(channel_name=c.id.camel) for c in action.refreshs]

            packet_name = packet.get_name() if not packet.has_high_level() else packet.get_name(skip=-2)

            if len(outputs) == 0:
                actions.append(input_action_template.format(label=packet_name.space,
                                                    id_headless=packet_name.headless,
                                                    device_headless=self.get_category().headless + self.get_name().camel,
                                                    id_camel=packet_name.camel,
                                                    annotated_inputs=',\n            '.join(annotated_inputs),
                                                    device_camel=self.get_category().camel + self.get_name().camel,
                                                    packet_headless=packet_name.headless,
                                                    packet_params=', '.join(input_names),
                                                    refreshs='\n'.join(refreshs),
                                                    typed_inputs=common.wrap_non_empty(', ', ', '.join(typed_inputs), ''),
                                                    inputs=', '.join(input_names)))
            else:

                output_annotations = [output_template.format(id=elem.get_name().headless,
                                                      type=elem.get_java_type()) for elem in outputs]

                _, result_type = self.get_filtered_elements_and_type(packet, outputs, out_of_class=True)

                if len(outputs) == 1:
                    transforms = [transform_template.format(id=outputs[0].get_name().headless, transform='value')]
                else:
                    transforms = [transform_template.format(id=elem.get_name().headless, transform='value.' + elem.get_name().headless) for elem in outputs]

                actions.append(output_action_template.format(label=packet_name.space,
                                                    id_headless=packet_name.headless,
                                                    device_headless=self.get_category().headless + self.get_name().camel,
                                                    id_camel=packet_name.camel,
                                                    annotated_inputs=',\n            '.join(annotated_inputs),
                                                    device_camel=self.get_category().camel + self.get_name().camel,
                                                    packet_headless=packet_name.headless,
                                                    packet_params=', '.join(input_names),
                                                    typed_inputs=common.wrap_non_empty(', ', ', '.join(typed_inputs), ''),
                                                    inputs=', '.join(input_names),
                                                    output_annotations='\n           '.join(output_annotations),
                                                    result_type=result_type,
                                                    refreshs='\n'.join(refreshs),
                                                    transforms='\n        '.join(transforms)
                                                    ))

        return template.format(device_camel=self.get_category().camel + self.get_name().camel,
                               actions='\n\n'.join(actions))

    def get_openhab_config_classes(self):
        template = """package org.eclipse.smarthome.binding.tinkerforge.internal.device;{imports}

public class {name_camel} {{
    {parameters}

    public {name_camel}() {{}}
}}"""

        parameter_template = "{type} {name} = {ctor}{default}{ctor2};"

        param_types = {
            'integer': 'Integer',
            'decimal': 'BigDecimal',
            'boolean': 'Boolean',
            'text': 'String'
        }


        classes = []
        imports = '\n\nimport java.math.BigDecimal;' if 'decimal' in [p.type for p in self.oh.params] else ''
        class_name = self.get_category().camel + self.get_name().camel + 'Config'
        classes.append((class_name,
                        template.format(imports=imports,
                               name_camel=class_name,
                               parameters="\n\t".join(parameter_template.format(type=param_types[p.type],
                                                                                name=p.name.headless,
                                                                                ctor='new BigDecimal(' if p.type == 'decimal' else '',
                                                                                ctor2=')' if p.type == 'decimal' else '',
                                                                                default=p.default if p.type != 'text' else '"' + p.default + '"') for p in self.oh.params))))
        for ct in self.oh.channel_types:
            imports = '\n\nimport java.math.BigDecimal;' if 'decimal' in [p.type for p in ct.params] else ''
            class_name = ct.id.camel + 'Config'
            classes.append((class_name,
                            template.format(imports=imports,
                               name_camel=class_name,
                               parameters="\n\t".join(parameter_template.format(type=param_types[p.type],
                                                                                name=p.name.headless,
                                                                                ctor='new BigDecimal(' if p.type == 'decimal' else '',
                                                                                ctor2=')' if p.type == 'decimal' else '',
                                                                                default=p.default if p.type != 'text' else '"' + p.default + '"') for p in ct.params))))

        return classes

    def get_openhab_binding_constant(self):
        thing_type_template = """public static final ThingTypeUID {} = new ThingTypeUID(BINDING_ID, "{}");"""
        thing_type_caps = 'THING_TYPE_' + self.get_category().upper + "_" + self.get_name().upper
        thing_type_decl = thing_type_template.format(thing_type_caps, self.get_category().lower_no_space + self.get_name().lower_no_space)

        channel_type_template = """public static final ChannelTypeUID {} = new ChannelTypeUID(BINDING_ID, "{}");"""
        channel_types_caps = ['CHANNEL_TYPE_' + ct.id.upper for ct in self.oh.channel_types]
        channel_type_decls = [channel_type_template.format(caps, id_) for caps, id_ in zip(channel_types_caps, [ct.id.camel for ct in self.oh.channel_types])]

        config_description_type_template = """public static final URI {name} = URI.create("{thing_or_channel}-type:"+{type_caps}.toString());"""
        config_description_types_caps = ['CONFIG_DESCRIPTION_URI_' + ct.id.upper for ct in self.oh.channel_types if not ct.is_system_type()]
        config_description_type_decls = [config_description_type_template.format(name=caps, thing_or_channel='channel', type_caps='CHANNEL_TYPE_' + ct.id.upper) for caps, ct in zip(config_description_types_caps, [ct for ct in self.oh.channel_types]) if not ct.is_system_type()]

        config_description_type_caps = 'CONFIG_DESCRIPTION_URI_' + self.get_category().upper + "_" + self.get_name().upper
        config_description_types_caps.append(config_description_type_caps)
        config_description_type_decls.append(config_description_type_template.format(name=config_description_type_caps, thing_or_channel='thing', type_caps=thing_type_caps))

        return (thing_type_caps, thing_type_decl, channel_types_caps, channel_type_decls, config_description_types_caps, config_description_type_decls)

    def get_openhab_docs(self):
        not_supported = len(self.oh.channels) == 0
        if not_supported:
            return None

        template = """{device}: {description}
    Configuration
    {cfg}
    Channels
    {channels}
    Actions
    {actions}
"""
        param_template = """        {name} ({type}):
                {description}"""
        cfg = []
        for p in self.oh.params:
            if p.description is not None:
                desc = p.description
            else:
                try:
                    group = [g for g in self.oh.param_groups if g.name == p.groupName][0]
                except:
                    print(self.get_long_display_name())
                    print(p.name.space)
                desc = group.description
            desc = desc.replace('<br/>', '\n                ').replace('\\\\', '\\')

            cfg.append(param_template.format(name=p.label, type=p.type if p.limitToOptions != 'true' else 'choice', description=desc))

        channel_template = """        {name} ({type})
                {description}"""
        channels = []
        for c in self.oh.channels:
            if c.description is not None:
                desc = c.description
            elif c.type.description is not None:
                desc = c.type.description
            elif c.type.is_system_type():
                desc = 'Default ' + c.type.id.under.replace('system.', '') + ' channel.'
            else:
                print(self.get_long_display_name())
                print(c.id.space)

            desc = desc.replace('<br/>', '\n                ').replace('\\\\', '\\')
            channels.append(channel_template.format(name=c.label if c.label is not None else c.type.label,
                                                    description=desc,
                                                    type=c.type.item_type if c.type.item_type is not None else 'trigger channel'))

        return template.format(device=self.get_long_display_name(),
                               description=self.get_description()['en'],
                               cfg='\n\n    '.join(cfg),
                               channels='\n\n    '.join(channels),
                               actions=', '.join(self.get_category().headless + self.get_name().camel + a.fn.get_name().camel for a in self.oh.actions) if self.oh.actions != 'custom' else 'custom')

class OpenHABBindingsGenerator(JavaBindingsGenerator):
    def get_bindings_name(self):
        return 'openhab'

    def get_bindings_display_name(self):
        return 'OpenHAB'

    def get_doc_null_value_name(self):
        return 'null'

    def get_doc_formatted_param(self, element):
        return element.get_name().headless

    def get_device_class(self):
        return OpenHABBindingsDevice

    def is_openhab(self):
        return True

    def prepare(self):
        JavaBindingsGenerator.prepare(self)
        self.released_devices = []

    def generate(self, device):
        if device.oh.custom:
            return
        class_name = device.get_java_class_name()

        with open(os.path.join(self.get_bindings_dir(), class_name + '.java'), 'w') as f:
            f.write(device.get_java_source())

        with open(os.path.join(self.get_bindings_dir(), class_name + 'Wrapper.java'), 'w') as f:
            f.write(device.get_openhab_device_wrapper())

        config_classes = device.get_openhab_config_classes()
        for config_class_name, config_class in config_classes:
            with open(os.path.join(self.get_bindings_dir(), config_class_name + '.java'), 'w') as f:
                f.write(config_class)

        if device.oh.actions == 'custom':
            shutil.copy(class_name + 'Actions.java', os.path.join(self.get_bindings_dir(), class_name + 'Actions.java'))
        elif len(device.oh.actions) > 0:
            with open(os.path.join(self.get_bindings_dir(), class_name + 'Actions.java'), 'w') as f:
                f.write(device.get_openhab_actions_class())

        if device.is_released():
            self.released_devices.append(device)
            self.released_files.append(class_name + '.java')
            self.released_files.append(class_name + 'Config.java')

    def finish(self):
        JavaBindingsGenerator.finish(self)
        consts = [d.get_openhab_binding_constant() for d in self.released_devices]
        thing_types = [x[0] for x in consts]
        thing_type_decls = [x[1] for x in consts]

        channel_types = [x[2] for x in consts]
        channel_type_decls = common.flatten([x[3] for x in consts])

        config_descs = [x[4] for x in consts]
        config_desc_decls = common.flatten([x[5] for x in consts])

        common.specialize_template(os.path.join(self.get_root_dir(), 'TinkerforgeBindingConstants.java.template'),
                                    os.path.join(self.get_bindings_dir(), 'TinkerforgeBindingConstants.java'),
                                    {
                                        '{thing_type_decls}': '\n\t'.join(thing_type_decls),
                                        '{thing_types}': ',\n\t\t'.join(thing_types),
                                        '{channel_type_decls}': '\n\t'.join(channel_type_decls),
                                        '{channel_type_assigns}': '\n\t\t'.join('SUPPORTED_CHANNELS.put({}, {});'.format(ctype, ttype) for ctypes, ttype in zip(channel_types, thing_types) for ctype in ctypes),
                                        '{config_description_decls}': '\n\t'.join(config_desc_decls),
                                        '{config_description_assigns}': '\n\t\t'.join('SUPPORTED_CONFIG_DESCRIPTIONS.put({}, {});'.format(ctype, ttype) for ctypes, ttype in zip(config_descs, thing_types) for ctype in ctypes)
                                    })
        common.specialize_template(os.path.join(self.get_root_dir(), 'DeviceWrapperFactory.java.template'),
                                    os.path.join(self.get_bindings_dir(), 'DeviceWrapperFactory.java'),
                                    {
                                        '{devices}': ',\n\t\t\t'.join(d.get_java_class_name() + 'Wrapper.DEVICE_INFO' for d in self.released_devices)
                                    })

        docs = [(d.get_name().under + '_' + d.get_category().under, d.get_openhab_docs()) for d in self.released_devices if d.get_openhab_docs() is not None]
        doc_folder = os.path.join(self.get_bindings_dir(), '..', 'doc')
        shutil.rmtree(doc_folder, ignore_errors=True)
        os.makedirs(doc_folder)

        for file, content in docs:
            with open(os.path.join(doc_folder, file + '.txt'), 'w') as f:
                f.write(content)

def generate(root_dir):
    common.generate(root_dir, 'en', OpenHABBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())

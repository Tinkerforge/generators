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
import os
import sys

sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'java'))
import common
from java.generate_java_bindings import JavaBindingsGenerator, JavaBindingsDevice



OpenHAB = namedtuple('OpenHAB', 'channels channel_types imports params param_groups init_code dispose_code category')
Channel = namedtuple('Channel', ['id', 'type', 'init_code', 'dispose_code',
                                    'java_unit', 'divisor', 'is_trigger_channel',
                                    'getter_packet', 'getter_packet_params', 'getter_transform',
                                    'setter_packet', 'setter_packet_params', 'setter_command_type', 'setter_refreshs',
                                    'callback_packet', 'callback_filter', 'callback_transform',
                                    'predicate',
                                    'label', 'description'])

ChannelType = namedtuple('ChannelType', ['id', 'params', 'item_type', 'category', 'label', 'description',
                                            'read_only', 'pattern', 'min', 'max', 'step', 'options',
                                            'is_trigger_channel', 'command_options'])
SetterRefresh = namedtuple('SetterRefresh', ['channel', 'delay'])

Param = namedtuple('Param', ['name', 'type', 'context', 'default', 'description', 'groupName', 'label',
                                'pattern', 'unit', 'unitLabel', 'advanced', 'limitToOptions', 'multiple',
                                'readOnly', 'required', 'verify', 'min', 'max', 'step', 'options', 'filter'])
ParamGroup = namedtuple('ParamGroup', 'name elements')

class OpenHABBindingsDevice(JavaBindingsDevice):
    def apply_defaults(self, oh):
        oh = self.raw_data['openhab']

        param_defaults = {
            'context': None,
            'default': None,
            'description': None,
            'groupName': None,
            'label': None,
            'pattern': None,
            'unit': None,
            'unitLabel': None,
            'advanced': None,
            'limitToOptions': None,
            'multiple': None,
            'readOnly': None,
            'required': None,
            'verify': None,
            'min': None,
            'max': None,
            'step': None,
            'options': None,
            'filter': None,
        }

        channel_defaults = {
            'init_code': '',
            'dispose_code': '',
            'getter_packet': None,
            'getter_packet_params': [],

            'setter_packet': None,
            'setter_packet_params': [],
            'setter_command_type': None,
            'setter_refreshs': [],

            'callback_packet': None,
            'callback_filter': 'true',
            'callback_transform': None,

            'java_unit': None,
            'divisor': 1,
            'is_trigger_channel': False,
            'predicate': 'true',

            'label': None,
            'description': None
        }

        channel_type_defaults = {
            'params': [],
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
            'advanced': None,
        }

        oh_defaults = {
            'params': [],
            'param_groups': [],
            'init_code': '',
            'dispose_code': '',
            'category': None
        }

        tmp = oh_defaults.copy()
        tmp.update(oh)
        oh = tmp

        for c_idx, channel in enumerate(oh['channels']):
            tmp_channel = channel_defaults.copy()
            tmp_channel.update(channel)
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

        return oh

    def sanity_check_config(self, oh):
        # Params must be used
        for param in oh.params:
            needle = 'cfg.{}'.format(param.name.headless)
            init_code_uses_param = needle in oh.init_code
            channel_init_code_uses_param = any(c.init_code is not None and needle in c.init_code for c in oh.channels)
            channel_setters_use_param = any(needle in p for c in oh.channels for p in c.setter_packet_params if c.setter_packet_params is not None)
            channel_getters_use_param = any(needle in p for c in oh.channels for p in c.getter_packet_params if c.getter_packet_params is not None)

            if not any([init_code_uses_param,
                        channel_init_code_uses_param,
                        channel_setters_use_param,
                        channel_getters_use_param]):
                raise common.GeneratorError('openhab: Device {}: Config parameter {} is not used in init_code or param mappings.'.format(self.get_long_display_name(), param.name))

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

        #for c in oh.channels:
        #    if len(c.params) > 0:
        #        print('openhab: Device {} Channel {} has config params. This is not supported yet, as the UI seems to render them incorrectly.'.format(self.get_long_display_name(), ct.id))

    def find_channel_type(self, channel, channel_types):
        if channel['type'].startswith('system.'):
            return ChannelType._make([common.FlavoredName(channel['type']).get()] + [None] * (len(ChannelType._fields) - 1))
        try:
            return next(ct for ct in channel_types if ct.id.space.replace(self.get_name().space + ' ', '') == channel['type'])
        except StopIteration:
            raise common.GeneratorError('openhab: Device "{}" Channel "{}" has type {}, but no such channel type was found.'.format(self.get_long_display_name(), channel['id'].space, channel['type']))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if not 'openhab' in self.raw_data:
            return

        oh = self.apply_defaults(self.raw_data['openhab'])

        # Replace config placeholders
        def fmt(format_str, base_name, unit, divisor):
            if not isinstance(format_str, str):
                return format_str
            name = common.FlavoredName(base_name).get()
            return format_str.format(title_words=name.space.title(),
                                     lower_words=name.lower,
                                     camel=name.camel,
                                     headless=name.headless,
                                     unit=unit,
                                     divisor=' / ' + str(divisor) if divisor != 1 else '')

        for c_idx, channel in enumerate(oh['channels']):
            oh['channels'][c_idx] = {k: fmt(v, channel['id'], channel['java_unit'], channel['divisor']) for k, v in oh['channels'][c_idx].items()}

        for ct_idx, channel_type in enumerate(oh['channel_types']):
            for p_idx, param in enumerate(channel_type['params']):
                channel_type['params'][p_idx] = {k: fmt(v, channel_type['id'], param['unit'], 1) for k, v in channel_type['params'][p_idx].items()}
            oh['channel_types'][ct_idx] = {k: fmt(v, channel_type['id'], None, None) for k, v in oh['channel_types'][ct_idx].items()}


        def find_packet(name):
            if name is None:
                return None
            return next(p for p in self.get_packets() if p.get_name().space == name)

        # Convert from dicts to namedtuples
        for ct_idx, channel_type in enumerate(oh['channel_types']):
            if channel_type['id'].startswith('system.'):
                channel_type['id'] = common.FlavoredName(channel_type['id']).get()
            else:
                channel_type['id'] = common.FlavoredName(self.get_name().space + ' ' + channel_type['id']).get()

            for param in channel_type['params']:
                param['name'] = common.FlavoredName(param['name']).get()

            channel_type['params'] = [Param(**p) for p in channel_type['params']]
            oh['channel_types'][ct_idx] = ChannelType(**channel_type)

        for c_idx, channel in enumerate(oh['channels']):
            if channel['id'].startswith('system.'):
                channel['id'] = common.FlavoredName(channel['id']).get()
            else:
                channel['id'] = common.FlavoredName(self.get_name().space + ' ' + channel['id']).get()

            for packet in ['getter_packet', 'setter_packet', 'callback_packet']:
                oh['channels'][c_idx][packet] = find_packet(oh['channels'][c_idx][packet])

            oh['channels'][c_idx]['setter_refreshs'] = [SetterRefresh(common.FlavoredName(self.get_name().space + ' ' + r['channel']).get(), r['delay']) for r in oh['channels'][c_idx]['setter_refreshs']]
            oh['channels'][c_idx]['type'] = self.find_channel_type(oh['channels'][c_idx], oh['channel_types'])
            oh['channels'][c_idx] = Channel(**channel)


        for p_idx, param in enumerate(oh['params']):
            param['name'] = common.FlavoredName(param['name']).get()
            oh['params'][p_idx] = Param(**param)

        for g_idx, group in enumerate(oh['param_groups']):
            oh['param_groups'][g_idx] = ParamGroup(name=group['name'],
                                                   elements={k: v for k, v in group.items() if v is not None})

        self.oh = OpenHAB(**oh)
        self.sanity_check_config(self.oh)

    def get_java_import(self):
        java_imports = super().get_java_import()
        oh_imports = ['java.net.URI',
                      'java.math.BigDecimal',
                      'java.util.ArrayList',
                      'java.util.Collections',
                      'java.util.function.Function',
                      'java.util.function.BiConsumer',
                      'org.eclipse.smarthome.config.core.Configuration',
                      'org.eclipse.smarthome.config.core.ConfigDescription',
                      'org.eclipse.smarthome.config.core.ConfigDescriptionParameter.Type',
                      'org.eclipse.smarthome.config.core.ConfigDescriptionParameterBuilder',
                      'org.eclipse.smarthome.config.core.ParameterOption',
                      'org.eclipse.smarthome.core.types.State',
                      'org.eclipse.smarthome.core.types.Command',
                      'org.eclipse.smarthome.core.types.CommandDescriptionBuilder',
                      'org.eclipse.smarthome.core.types.CommandOption',
                      'org.eclipse.smarthome.core.thing.ThingTypeUID',
                      'org.eclipse.smarthome.core.thing.type.ChannelDefinitionBuilder',
                      'org.eclipse.smarthome.core.thing.type.ChannelType',
                      'org.eclipse.smarthome.core.thing.type.ChannelTypeBuilder',
                      'org.eclipse.smarthome.core.thing.type.ChannelTypeUID',
                      'org.eclipse.smarthome.core.thing.type.ThingType',
                      'org.eclipse.smarthome.core.thing.type.ThingTypeBuilder',
                      'org.eclipse.smarthome.core.types.StateDescriptionFragmentBuilder',
                      'org.eclipse.smarthome.binding.tinkerforge.internal.TinkerforgeBindingConstants'] + self.oh.imports

        java_imports += '\n'.join('import {};'.format(i) for i in oh_imports) + '\n'

        return java_imports

    def get_java_class(self):
        java_class = super().get_java_class()
        java_class += '    public final static DeviceInfo DEVICE_INFO = new DeviceInfo(DEVICE_DISPLAY_NAME, "{}", DEVICE_IDENTIFIER, {}.class);\n\n'.format(self.get_name().lower_no_space, self.get_java_class_name())
        return java_class

    def get_filtered_elements_and_type(self, packet, elements):
        if len(elements) > 1:
            type_ = packet.get_java_object_name(skip=-2 if packet.has_high_level() else 0)
        else:
            type_ = elements[0].get_java_type()

        return elements, type_

    def get_openhab_channel_init_code(self):
        init_code = []
        for c in self.oh.channels:
            channel_cfg = ['{channel_type_name_camel}Config channelCfg = getChannelConfigFn.apply("{channel_name_camel}").as({channel_type_name_camel}Config.class);'
                               .format(channel_name_camel=c.id.camel,
                                       channel_type_name_camel=self.get_category().camel + c.type.id.camel)]
            if c.type.id.space.startswith('system.'):
                channel_cfg = []
            if c.predicate != 'true':
                init_code += ['if ({}) {{'.format(c.predicate)]
                init_code += c.init_code.split('\n')
                init_code += ['}']
            else:
                init_code += ['{'] + channel_cfg + c.init_code.split('\n') + ['}']
        return init_code

    def get_openhab_callback_impl(self):
        transformation_template = """    private {state_or_string} transform{camel}Callback({callback_args}) {{
        return {transform};
    }}"""
        # To init
        cb_registration = 'this.add{camel}Listener(({args}) -> {{if({filter}) {{{updateFn}.accept("{channel_camel}", transform{channel_camel}Callback({args}));}}}});'
        # To dispose
        cb_deregistration = 'this.listener{camel}.clear();'

        regs = []

        deregs = []
        dispose_code = []
        lambda_transforms = []
        for c in self.oh.channels:
            if c.callback_packet is None:
                continue
            elements = c.callback_packet.get_elements(direction='out', high_level=True)
            regs.append(cb_registration.format(camel=c.callback_packet.get_name().camel,
                                               filter=c.callback_filter,
                                               channel_camel=c.id.camel,
                                               args=', '.join(e.get_name().headless for e in elements),
                                               updateFn='triggerChannelFn' if c.is_trigger_channel else 'updateStateFn'))

            deregs.append(cb_deregistration.format(camel=c.callback_packet.get_name().camel))
            dispose_code += c.dispose_code.split('\n')

            filtered_elements, type_ = self.get_filtered_elements_and_type(c.getter_packet, elements)


            lambda_transforms.append(transformation_template.format(state_or_string='String' if c.is_trigger_channel else 'State',
                                                             camel=c.id.camel,
                                                             callback_args=', '.join(e.get_java_type() + ' ' + e.get_name().headless for e in elements),
                                                             transform=c.callback_transform))

        return (regs, deregs, dispose_code, lambda_transforms)

    def get_openhab_getter_impl(self):
        template = """    @Override
    public void refreshValue(String value, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {{
        switch(value) {{
            {channel_cases}
        }}
        throw new RuntimeException("Refresh for unknown or trigger channel " + value + ". Should never happen.");
    }}
    """

        case_template = """case "{camel}":
               {updateFn}.accept(value, transform{camel}Getter(this.{getter}({getter_params})));
               return;"""
        empty_case_template = """case "{camel}":
               return;"""

        transformation_template = """    private {state_or_string} transform{camel}Getter({type_} value) {{
        return {transform};
    }}"""

        channel_cases = []
        transforms = []
        for c in self.oh.channels:
            if c.getter_packet is None:
                channel_cases.append(empty_case_template.format(camel=c.id.camel))
                continue

            channel_cases.append(case_template.format(camel=c.id.camel,
                                                      updateFn='triggerChannelFn' if c.is_trigger_channel else 'updateStateFn',
                                                      getter=c.getter_packet.get_name().headless,
                                                      getter_params=', '.join(c.getter_packet_params)))

            elements = c.getter_packet.get_elements(direction='out', high_level=True)
            _, type_ = self.get_filtered_elements_and_type(c.getter_packet, elements)

            transforms.append(transformation_template.format(state_or_string='String' if c.is_trigger_channel else 'State',
                                                             camel=c.id.camel,
                                                             type_=type_,
                                                             transform=c.getter_transform))

        return (template.format(channel_cases='\n            '.join(channel_cases)), transforms)


    def get_openhab_setter_impl(self):
        template = """    @Override
    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command) throws TinkerforgeException {{
        List<SetterRefresh> result = {refresh_init};
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        switch(channel) {{
            {channel_cases}
        }}
        return result;
    }}"""

        case_template = """case "{camel}":
                if (command instanceof {command_type}) {{
                    {category_camel}{channel_type_camel}Config channelCfg = channelConfig.as({category_camel}{channel_type_camel}Config.class);
                    {command_type} cmd = ({command_type}) command;
                    this.{setter}({setter_params});
                    {setter_refreshs}
                }}
                break;"""
        channel_cases = []
        for c in self.oh.channels:
            if c.setter_packet is None:
                continue
            refresh_template = 'result.add(new SetterRefresh("{}", {}));'

            refreshs = '\n\t\t\t\t'.join(refresh_template.format(r.channel.camel, r.delay) for r in c.setter_refreshs)
            channel_cases.append(
                case_template.format(category_camel=self.get_category().camel,
                                     channel_type_camel=c.type.id.camel,
                                     camel=c.id.camel,
                                     command_type=c.setter_command_type,
                                     setter=c.setter_packet.get_name().headless,
                                     setter_params=', '.join(c.setter_packet_params),
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
    @Override
    public void initialize(org.eclipse.smarthome.config.core.Configuration config, Function<String, org.eclipse.smarthome.config.core.Configuration> getChannelConfigFn, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {{
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        {callback_registrations}
        {init_code}
    }}

    @Override
    public void dispose(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException {{
        {name_camel}Config cfg = ({name_camel}Config) config.as({name_camel}Config.class);
        {callback_deregistrations}
        {dispose_code}
    }}

    @Override
    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config) {{
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
        callback_regs, callback_deregs, callback_dispose_code, lambda_transforms = self.get_openhab_callback_impl()
        refresh_value, getter_transforms = self.get_openhab_getter_impl()
        handle_command = self.get_openhab_setter_impl()
        channel_enablers = self.get_openhab_channel_enablers()

        return template.format(name_camel=self.get_category().camel + self.get_name().camel,
                               init_code='\n\t\t'.join(init_code),
                               callback_registrations='\n\t\t'.join(callback_regs),
                               callback_deregistrations='\n\t\t'.join(callback_deregs),
                               dispose_code='\n\t\t'.join(callback_dispose_code + dispose_code),
                               channel_enablers='\n\t\t'.join(channel_enablers),
                               get_channel_type=self.get_openhab_get_channel_type_impl(),
                               get_thing_type=self.get_openhab_get_thing_type_impl(),
                               get_config_description=self.get_openhab_get_config_description_impl(),
                               refresh_value=refresh_value,
                               handle_command=handle_command,
                               transforms='\n\t'.join(lambda_transforms + getter_transforms))


    def get_openhab_channel_type_builder_call(self, ct):
        template = """ChannelTypeBuilder.{state_or_trigger}(new ChannelTypeUID("tinkerforge", "{type_id_camel}"), "{label}"{state_item_type}).withConfigDescriptionURI(URI.create("channel-type:tinkerforge:{type_id_camel}")){with_calls}.build()"""

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
                with_calls.append('.withOptions(Arrays.asList({})))'.format(', '.join(opts)))

            return template.format(with_calls=''.join(with_calls))

        with_calls = []

        for item in ['Category', 'Description']:
            name = common.FlavoredName(item).get()
            if name.under in ct._asdict() and ct._asdict()[name.under] is not None:
                with_calls.append('.with{}("{}")'.format(name.camel, ct._asdict()[name.under]))
        if 'tags' in ct._asdict() and ct.tags is not None:
            for tag in ct.tags:
                with_calls.append('.withTag("{}")'.format(tag))

        if not ct.is_trigger_channel and any(x is not None for x in [ct.min, ct.max, ct.pattern, ct.read_only, ct.options, ct.step]):
            with_calls.append('.withStateDescription({})'.format(get_state_description(ct.min, ct.max, ct.options, ct.pattern, ct.read_only, ct.step)))

        if ct.command_options is not None:
            with_calls.append('.withCommandDescription(CommandDescriptionBuilder.create(){}.build())'.format(''.join('.withCommandOption(new CommandOption("{}", "{}"))'.format(command, label) for label, command in ct.command_options)))

        return template.format(state_or_trigger='trigger' if ct.is_trigger_channel else 'state',
                               type_id_camel=ct.id.camel,
                               label=ct.label,
                               state_item_type='' if ct.is_trigger_channel else ', "{}"'.format(ct.item_type),
                               with_calls='\n'.join(with_calls))

    #region get_openhab_get_channel_type_impl
    def get_openhab_get_channel_type_impl(self):
        template = """public static ChannelType getChannelType(ChannelTypeUID channelTypeUID) {{
        switch(channelTypeUID.getId()) {{
            {}
        }}
        return null;
    }}"""

        case_template = """case "{channel_type_id}":
                return {channel_type_builder_call};"""

        cases = [case_template.format(channel_type_id=ct.id.camel,
                                      channel_type_builder_call=self.get_openhab_channel_type_builder_call(ct))
                 for ct in self.oh.channel_types]
        return template.format('\n            '.join(cases))
    #endregion

    def get_openhab_channel_definition_builder_call(self, c):
        template = """new ChannelDefinitionBuilder("{channel_id}", new ChannelTypeUID("{binding}", "{channel_type_id}")){with_calls}.build()"""
        with_calls = []
        if c.label is not None:
            with_calls.append('.withLabel("{}")'.format(c.label))
        if c.description is not None:
            with_calls.append('.withDescription("{}")'.format(c.description))

        binding = 'tinkerforge'
        channel_type_id = c.type.id.camel
        if channel_type_id.startswith('system.'):
            binding = 'system'
            channel_type_id = channel_type_id.replace('system.', '')

        return template.format(channel_id=c.id.camel, binding=binding, channel_type_id=channel_type_id, with_calls=''.join(with_calls))

    def get_openhab_thing_type_builder_call(self):
        template = """ThingTypeBuilder.instance(thingTypeUID, "{label}").isListed(false).withSupportedBridgeTypeUIDs(Arrays.asList(TinkerforgeBindingConstants.THING_TYPE_BRICK_DAEMON.getId())).withConfigDescriptionURI(URI.create("thing-type:tinkerforge:" + thingTypeUID.getId())){with_calls}.build()"""

        with_calls = []
        if self.oh.category is not None:
            with_calls.append('.withCategory("{}")'.format(self.oh.category))
        with_calls.append('.withDescription("{}")'.format(common.select_lang(self.get_description())))
        with_calls.append('.withChannelDefinitions(Arrays.asList({}))'.format(', '.join(self.get_openhab_channel_definition_builder_call(c) for c in self.oh.channels)))

        return template.format(label='Tinkerforge ' + self.get_long_display_name(), with_calls=''.join(with_calls))

    def get_openhab_get_thing_type_impl(self):
         return """public static ThingType getThingType(ThingTypeUID thingTypeUID) {{
        return {};
    }}""".format(self.get_openhab_thing_type_builder_call())

    def get_openhab_config_description_parameter_builder_call(self, param, channel_name=None):
        template = """ConfigDescriptionParameterBuilder.create("{name}", Type.{type_upper}){with_calls}.build()"""

        if channel_name is not None:
            name = channel_name + param.name.camel
        else:
            name = param.name.headless

        with_calls = []
        # Strings
        for x in ['context', 'default', 'description', 'groupName', 'label', 'pattern', 'unit', 'unitLabel']:
            if param._asdict()[x] is not None:
                with_calls.append('.with{camel}("{val}")'.format(camel=x[0].upper() + x[1:], val=param._asdict()[x]))

        # Bools
        for x in ['advanced', 'limitToOptions', 'multiple', 'readOnly', 'required', 'verify']:
            if param._asdict()[x] is not None:
                with_calls.append('.with{camel}({val})'.format(camel=x[0].upper() + x[1:], val=str(param._asdict()[x]).lower()))

        # BigInts
        for x, camel in [('min', 'Minimum'), ('max', 'Maximum'), ('step', 'StepSize')]:
            if param._asdict()[x] is not None:
                with_calls.append('.with{camel}(BigDecimal.valueOf({val}))'.format(camel=camel, val=param._asdict()[x]))

        if param.options is not None:
            with_calls.append('.withOptions(Arrays.asList({}))'.format(', '.join('new ParameterOption("{}", "{}")'.format(val, label) for label, val in param.options)))

        if param.filter is not None:
            with_calls.append('.withFilterCriteria(Arrays.asList({}))'.format(', '.join('new FilterCriteria({}, {})'.format(val, label) for label, val in param.options)))

        return template.format(name=name, type_upper=param.type.upper(), with_calls=''.join(with_calls))

    def get_openhab_get_config_description_impl(self):
        template = """public static ConfigDescription getConfigDescription(URI uri) {{
        switch(uri.toASCIIString()) {{
            {cases}
        }}
        return null;
    }}"""

        case_template = """case "{uri}":
                return new ConfigDescription(uri, Arrays.asList({builder_calls}));"""

        cases = [case_template.format(uri='thing-type:tinkerforge:' + self.get_name().lower_no_space,
                                      builder_calls=', '.join(self.get_openhab_config_description_parameter_builder_call(p) for p in self.oh.params))
                ] + \
                [case_template.format(uri='channel-type:tinkerforge:' + ct.id.camel,
                                      builder_calls=', '.join(self.get_openhab_config_description_parameter_builder_call(p) for p in ct.params)) for ct in self.oh.channel_types
                ] #+ \
                #[case_template.format(uri='channel:tinkerforge:' + self.get_name().under + '_' + c.id.headless,
                #                      builder_calls=', '.join(self.get_openhab_config_description_parameter_builder_call(p) for p in c.params)) for c in self.oh.channels]

        return template.format(cases='\n            '.join(cases))

    def get_java_source(self, close_device_class=False):
        source =  super().get_java_source(close_device_class=False)
        source += self.get_openhab_device_impl()
        source += '}\n'
        return source

    def get_openhab_config_classes(self):
        template = """package com.tinkerforge;{imports}

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
                                                                                default=p.default) for p in self.oh.params))))
        for ct in self.oh.channel_types:
            imports = '\n\nimport java.math.BigDecimal;' if 'decimal' in [p.type for p in ct.params] else ''
            class_name = self.get_category().camel + ct.id.camel + 'Config'
            classes.append((class_name,
                            template.format(imports=imports,
                               name_camel=class_name,
                               parameters="\n\t".join(parameter_template.format(type=param_types[p.type],
                                                                                name=p.name.headless,
                                                                                ctor='new BigDecimal(' if p.type == 'decimal' else '',
                                                                                ctor2=')' if p.type == 'decimal' else '',
                                                                                default=p.default) for p in ct.params))))

        return classes

    def get_openhab_binding_constant(self):
        thing_type_template = """public static final ThingTypeUID {} = new ThingTypeUID(BINDING_ID, "{}");"""
        thing_type_caps = 'THING_TYPE_' + self.get_name().upper
        thing_type_decl = thing_type_template.format(thing_type_caps, self.get_name().lower_no_space)

        channel_type_template = """public static final ChannelTypeUID {} = new ChannelTypeUID(BINDING_ID, "{}");"""
        channel_types_caps = ['CHANNEL_TYPE_' + ct.id.upper for ct in self.oh.channel_types]
        channel_type_decls = [channel_type_template.format(caps, id_) for caps, id_ in zip(channel_types_caps, [ct.id.camel for ct in self.oh.channel_types])]

        config_description_type_template = """public static final URI {name} = URI.create("{thing_or_channel}-type:"+{type_caps}.toString());"""
        config_description_types_caps = ['CONFIG_DESCRIPTION_URI_' + ct.id.upper for ct in self.oh.channel_types if not ct.id.space.startswith('system.')]
        config_description_type_decls = [config_description_type_template.format(name=caps, thing_or_channel='channel', type_caps='CHANNEL_TYPE_' + ct.id.upper) for caps, ct in zip(config_description_types_caps, [ct for ct in self.oh.channel_types]) if not ct.id.space.startswith('system.')]

        config_description_types_caps.append('CONFIG_DESCRIPTION_URI_' + self.get_name().upper)
        config_description_type_decls.append(config_description_type_template.format(name='CONFIG_DESCRIPTION_URI_' + self.get_name().upper, thing_or_channel='thing', type_caps=thing_type_caps))

        return (thing_type_caps, thing_type_decl, channel_types_caps, channel_type_decls, config_description_types_caps, config_description_type_decls)


class OpenHABBindingsGenerator(JavaBindingsGenerator):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.released_devices = []

    def get_device_class(self):
        return OpenHABBindingsDevice

    def get_bindings_name(self):
        return 'openhab'

    def get_bindings_display_name(self):
        return 'OpenHAB'

    def is_openhab(self):
        return True

    def generate(self, device):
        if not 'openhab' in device.raw_data:
            return

        class_name = device.get_java_class_name()

        with open(os.path.join(self.get_bindings_dir(), class_name + '.java'), 'w') as f:
            f.write(device.get_java_source())

        config_classes = device.get_openhab_config_classes()
        for config_class_name, config_class in config_classes:
            with open(os.path.join(self.get_bindings_dir(), config_class_name + '.java'), 'w') as f:
                f.write(config_class)

        if device.is_released():
            self.released_devices.append(device)
            self.released_files.append(class_name + '.java')
            self.released_files.append(class_name + 'Config.java')

    def finish(self):
        super().finish()
        consts = [d.get_openhab_binding_constant() for d in self.released_devices]
        thing_types = [x[0] for x in consts]
        thing_type_decls = [x[1] for x in consts]

        channel_types = [x[2] for x in consts]
        channel_type_decls = common.flatten([x[3] for x in consts])

        config_descs = [x[4] for x in consts]
        config_desc_decls = common.flatten([x[5] for x in consts])

        common.specialize_template('TinkerforgeBindingConstants.java.template',
                                    os.path.join(self.get_bindings_dir(), 'TinkerforgeBindingConstants.java'),
                                    {
                                        '{thing_type_decls}': '\n\t'.join(thing_type_decls),
                                        '{thing_types}': ',\n\t\t'.join(thing_types),
                                        '{channel_type_decls}': '\n\t'.join(channel_type_decls),
                                        '{channel_type_assigns}': '\n\t\t'.join('SUPPORTED_CHANNELS.put({}, {});'.format(ctype, ttype) for ctypes, ttype in zip(channel_types, thing_types) for ctype in ctypes),
                                        '{config_description_decls}': '\n\t'.join(config_desc_decls),
                                        '{config_description_assigns}': '\n\t\t'.join('SUPPORTED_CONFIG_DESCRIPTIONS.put({}, {});'.format(ctype, ttype) for ctypes, ttype in zip(config_descs, thing_types) for ctype in ctypes)
                                    })
        common.specialize_template('DeviceFactory.java.template',
                                    os.path.join(self.get_bindings_dir(), 'DeviceFactory.java'),
                                    {
                                        '{devices}': ',\n\t\t\t'.join(d.get_java_class_name() + '.DEVICE_INFO' for d in self.released_devices)
                                    })

def generate(root_dir):
    common.generate(root_dir, 'en', OpenHABBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())

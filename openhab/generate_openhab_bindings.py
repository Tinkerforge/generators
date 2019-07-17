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
            'params': [],
            'init_code': '',
            'dispose_code': '',
            'getter_packet': None,
            'getter_packet_params': [],

            'setter_packet': None,
            'setter_packet_params': [],
            'setter_command_type': None,

            'callback_packet': None,
            'callback_param_mapping': None,
            'callback_filter': 'true',

            'java_unit': None,
            'divisor': 1,
            'is_trigger_channel': False,
            'predicate': 'true',

            'label': None,
            'description': None
        }

        channel_type_defaults = {
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

            for p_idx, param in enumerate(tmp_channel['params']):
                tmp_param = param_defaults.copy()
                tmp_param.update(param)
                tmp_channel['params'][p_idx] = tmp_param

            oh['channels'][c_idx] = tmp_channel

        for p_idx, param in enumerate(oh['params']):
            tmp = param_defaults.copy()
            tmp.update(param)
            oh['params'][p_idx] = tmp

        for ct_idx, channel_type in enumerate(oh['channel_types']):
            tmp = channel_type_defaults.copy()
            tmp.update(channel_type)
            oh['channel_types'][ct_idx] = tmp

        for pg_idx, param_group in enumerate(oh['param_groups']):
            tmp = param_group_defaults.copy()
            tmp.update(param_group)
            oh['param_groups'][pg_idx] = tmp

        return oh

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
            for p_idx, param in enumerate(channel['params']):
                channel['params'][p_idx] = {k: fmt(v, channel['id'], param['unit'], 1) for k, v in channel['params'][p_idx].items()}
            oh['channels'][c_idx] = {k: fmt(v, channel['id'], channel['java_unit'], channel['divisor']) for k, v in oh['channels'][c_idx].items()}

        # Convert from dicts to namedtuples
        OpenHAB = namedtuple('OpenHAB', 'channels channel_types imports params param_groups init_code dispose_code category')
        Channel = namedtuple('Channel', ['id', 'type_id', 'params', 'init_code', 'dispose_code',
                                         'java_unit', 'divisor', 'is_trigger_channel', 'transform',
                                         'getter_packet', 'getter_packet_params',
                                         'setter_packet', 'setter_packet_params', 'setter_command_type',
                                         'callback_packet', 'callback_param_mapping', 'callback_filter',
                                         'predicate',
                                         'label', 'description'])

        Param = namedtuple('Param', ['name', 'type', 'context', 'default', 'description', 'groupName', 'label', 'pattern', 'unit', 'unitLabel', 'advanced', 'limitToOptions', 'multiple', 'readOnly', 'required', 'verify', 'min', 'max', 'step', 'options', 'filter'])
        ParamGroup = namedtuple('ParamGroup', 'name elements')
        ChannelType = namedtuple('ChannelType', 'type_id item_type category label description read_only pattern min max step options is_trigger_channel command_options')

        def find_packet(name):
            if name is None:
                return None
            return next(p for p in self.get_packets() if p.get_name().space == name)

        for c_idx, channel in enumerate(oh['channels']):
            if not channel['type_id'].startswith('system.'):
                channel['type_id'] = self.get_name().under + '_' + channel['type_id']
            for p_idx, param in enumerate(channel['params']):
                channel['params'][p_idx] = Param(**param)
            for packet in ['getter_packet', 'setter_packet', 'callback_packet']:
                oh['channels'][c_idx][packet] = find_packet(oh['channels'][c_idx][packet])
            if oh['channels'][c_idx]['callback_param_mapping'] is not None:
                oh['channels'][c_idx]['callback_param_mapping'] = {common.FlavoredName(k).get(): (common.FlavoredName(v).get() if v is not None else None) for k, v in oh['channels'][c_idx]['callback_param_mapping'].items()}
            oh['channels'][c_idx] = Channel(**channel)

        for ct_idx, channel_type in enumerate(oh['channel_types']):
            if not channel_type['type_id'].startswith('system.'):
                channel_type['type_id'] = self.get_name().under + '_' + channel_type['type_id']
            oh['channel_types'][ct_idx] = ChannelType(**channel_type)

        for p_idx, param in enumerate(oh['params']):
            oh['params'][p_idx] = Param(**param)

        for g_idx, group in enumerate(oh['param_groups']):
            oh['param_groups'][g_idx] = ParamGroup(name=group['name'],
                                                   elements={k: v for k, v in group.items() if v is not None})

        self.oh = OpenHAB(**oh)

    def get_java_import(self):
        java_imports = super().get_java_import()
        oh_imports = ['java.net.URI',
                      'java.math.BigDecimal',
                      'java.util.ArrayList',
                      'java.util.function.BiConsumer',
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

    def get_filtered_elements_and_type(self, packet, elements, mapping):
        if mapping is not None:
            def f(e):
                val = mapping[e.get_name()]
                return val is not None
            filtered_elements = [e for e in elements if f(e)]
        else:
            filtered_elements = elements

        if len(filtered_elements) > 1:
            type_ = packet.get_java_object_name(skip=-2 if packet.has_high_level() else 0)
        else:
            type_ = filtered_elements[0].get_java_type()

        return filtered_elements, type_

    def get_openhab_channel_init_code(self):
        init_code = []
        for c in self.oh.channels:
            if c.predicate != 'true':
                init_code += ['if ({}) {{'.format(c.predicate)]
                init_code += c.init_code.split('\n')
                init_code += ['}']
            else:
                init_code += c.init_code.split('\n')
        return init_code
    def get_openhab_callback_impl(self):
        lambda_transformation_template = """    private {type_} lambdaArgsTo{channel_camel}({callback_args}) {{
        {type_} lambda_transform_result{init};
        {assignments}
        return lambda_transform_result;
    }}"""

        # To init
        cb_registration = 'this.add{camel}Listener(({args}) -> {{if({filter}) {{{updateFn}.accept("{channel_camel}", transform{channel_camel}(lambdaArgsTo{channel_camel}({args})));}}}});'
        # To dispose
        cb_deregistration = 'this.listener{camel}.clear();'

        regs = []

        deregs = []
        dispose_code = []
        lambda_transforms = []
        for c in self.oh.channels:
            if c.callback_packet is None:
                continue
            name = common.FlavoredName(c.id).get()
            elements = c.callback_packet.get_elements(direction='out', high_level=True)
            regs.append(cb_registration.format(camel=c.callback_packet.get_name().camel,
                                               filter=c.callback_filter,
                                               channel_camel=common.FlavoredName(c.id).get().camel,
                                               args=', '.join(e.get_name().headless for e in elements),
                                               updateFn='triggerChannelFn' if c.is_trigger_channel else 'updateStateFn'))

            deregs.append(cb_deregistration.format(camel=c.callback_packet.get_name().camel))
            dispose_code += c.dispose_code.split('\n')

            filtered_elements, type_ = self.get_filtered_elements_and_type(c.getter_packet, elements, c.callback_param_mapping)

            if len(filtered_elements) > 1:
                init = ' = new {}()'.format(type_)
                if c.callback_param_mapping is None:
                    assignments = '\n\t\t'.join('lambda_transform_result.{0} = {0};'.format(e.get_name().headless) for e in filtered_elements)
                else:
                    assignments = []
                    for k, v in c.callback_param_mapping.items():
                        if v is None:
                            continue
                        assignments.append('lambda_transform_result.{} = {};'.format(k.headless, v.headless))
                    assignments = '\n\t\t'.join(assignments)
            else:
                init = ''
                if c.callback_param_mapping is None:
                    assignments = 'lambda_transform_result = {};'.format(filtered_elements[0].get_name().headless)
                else:
                    assignments = 'lambda_transform_result = {};'.format(c.callback_param_mapping[filtered_elements[0].get_name()].headless)

            lambda_transforms.append(lambda_transformation_template.format(type_=type_,
                                                                           channel_camel=name.camel,
                                                                           callback_args=', '.join(e.get_java_type() + ' ' + e.get_name().headless for e in elements),
                                                                           init=init,
                                                                           assignments=assignments))

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
               {updateFn}.accept(value, transform{camel}(this.{getter}({getter_params})));
               return;"""
        empty_case_template = """case "{camel}":
               return;"""

        transformation_template = """    private {state_or_string} transform{camel}({type_} value) {{
        return {transform};
    }}"""

        channel_cases = []
        transforms = []
        for c in self.oh.channels:
            name = common.FlavoredName(c.id).get()
            if c.getter_packet is None:
                channel_cases.append(empty_case_template.format(camel=name.camel))
                continue

            channel_cases.append(case_template.format(camel=name.camel,
                                                      updateFn='triggerChannelFn' if c.is_trigger_channel else 'updateStateFn',
                                                      getter=c.getter_packet.get_name().headless,
                                                      getter_params=', '.join(c.getter_packet_params)))

            if c.callback_packet is not None:
                elements = c.callback_packet.get_elements(direction='out', high_level=True)
            else:
                elements = c.getter_packet.get_elements(direction='out', high_level=True)
            _, type_ = self.get_filtered_elements_and_type(c.getter_packet, elements, c.callback_param_mapping)

            transforms.append(transformation_template.format(state_or_string='String' if c.is_trigger_channel else 'State',
                                                             camel=name.camel,
                                                             type_=type_,
                                                             transform=c.transform))

        return (template.format(channel_cases='\n            '.join(channel_cases)), transforms)


    def get_openhab_setter_impl(self):
        template = """    @Override
    public void handleCommand(Object config, String channel, Command command) throws TinkerforgeException {{
        {name_camel}Config cfg = ({name_camel}Config) config;
        switch(channel) {{
            {channel_cases}
        }}
    }}"""

        case_template = """case "{camel}":
                if (command instanceof {command_type}) {{
                    {command_type} cmd = ({command_type}) command;
                    this.{setter}({setter_params});
                }}
                break;"""
        channel_cases = []
        for c in self.oh.channels:
            if c.setter_packet is None:
                continue
            name = common.FlavoredName(c.id).get()
            channel_cases.append(
                case_template.format(camel=name.camel,
                                     command_type=c.setter_command_type,
                                     setter=c.setter_packet.get_name().headless,
                                     setter_params=', '.join(c.setter_packet_params)))

        return template.format(name_camel=self.get_category().camel + self.get_name().camel, channel_cases='\n            '.join(channel_cases))

    def get_openhab_channel_enablers(self):
        template = """if ({pred}) {{
                result.add("{channel_camel}");
            }}"""

        enablers = []
        for c in self.oh.channels:
            name = common.FlavoredName(c.id).get().camel
            if c.predicate == 'true':
                enablers.append('result.add("{channel_camel}");'.format(channel_camel=name))
            else:
                enablers.append(template.format(pred=c.predicate, channel_camel=name))

        return enablers

    def get_openhab_device_impl(self):
        template = """
    @Override
    public void initialize(Object config, BiConsumer<String, State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {{
        {name_camel}Config cfg = ({name_camel}Config) config;
        {callback_registrations}
        {init_code}
    }}

    @Override
    public Class<{name_camel}Config> getConfigurationClass() {{
        return {name_camel}Config.class;
    }}

    @Override
    public void dispose(Object config) throws TinkerforgeException {{
        {callback_deregistrations}
        {dispose_code}
    }}

    @Override
    public List<String> getEnabledChannels(Object config) {{
        {name_camel}Config cfg = ({name_camel}Config) config;
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
        template = """ChannelTypeBuilder.{state_or_trigger}(new ChannelTypeUID("tinkerforge", "{type_id}"), "{label}"{state_item_type}).withConfigDescriptionURI(URI.create("channel-type:tinkerforge:{type_id}")){with_calls}.build()"""

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
                               type_id=ct.type_id,
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

        cases = [case_template.format(channel_type_id=ct.type_id,
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
        channel_type_id = c.type_id
        if channel_type_id.startswith('system.'):
            binding = 'system'
            channel_type_id = channel_type_id.replace('system.', '')

        return template.format(channel_id=common.FlavoredName(c.id).get().camel, binding=binding, channel_type_id=channel_type_id, with_calls=''.join(with_calls))

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

    def get_openhab_config_description_parameter_builder_call(self, param):
        template = """ConfigDescriptionParameterBuilder.create("{name}", Type.{type_upper}){with_calls}.build()"""

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

        return template.format(name=common.FlavoredName(param.name).get().headless, type_upper=param.type.upper(), with_calls=''.join(with_calls))

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
                [case_template.format(uri='channel-type:tinkerforge:' + self.get_name().under + '_' + common.FlavoredName(c.id).get().headless,
                                      builder_calls=', '.join(self.get_openhab_config_description_parameter_builder_call(p) for p in c.params)) for c in self.oh.channels]

        return template.format(cases='\n            '.join(cases))

    def get_java_source(self, close_device_class=False):
        source =  super().get_java_source(close_device_class=False)
        source += self.get_openhab_device_impl()
        source += '}\n'
        return source

    def get_openhab_config_class(self):
        template = """package com.tinkerforge;{imports}

public class {name_camel}Config {{
    {parameters}

    public {name_camel}Config() {{}}
}}"""

        parameter_template = "{type} {name} = {ctor}{default}{ctor2};"

        params = self.oh.params + [p for c in self.oh.channels for p in c.params]

        param_types = {
            'integer': 'Integer',
            'decimal': 'BigDecimal',
            'boolean': 'Boolean',
            'text': 'String'
        }

        return template.format(imports='\n\nimport java.math.BigDecimal;' if 'decimal' in [p.type for p in params] else '',
                               name_camel=self.get_category().camel + self.get_name().camel,
                               parameters="\n\t".join(parameter_template.format(type=param_types[p.type],
                                                                                name=common.FlavoredName(p.name).get().headless,
                                                                                ctor='new BigDecimal(' if p.type == 'decimal' else '',
                                                                                ctor2=')' if p.type == 'decimal' else '',
                                                                                default=p.default) for p in params))

    def get_openhab_binding_constant(self):
        thing_type_template = """public static final ThingTypeUID {} = new ThingTypeUID(BINDING_ID, "{}");"""
        thing_type_caps = 'THING_TYPE_' + self.get_name().upper
        thing_type_decl = thing_type_template.format(thing_type_caps, self.get_name().lower_no_space)

        channel_type_template = """public static final ChannelTypeUID {} = new ChannelTypeUID(BINDING_ID, "{}");"""
        channel_types_caps = ['CHANNEL_TYPE_' + common.FlavoredName(ct.type_id).get().upper for ct in self.oh.channel_types]
        channel_type_decls = [channel_type_template.format(caps, id_) for caps, id_ in zip(channel_types_caps, [ct.type_id for ct in self.oh.channel_types])]

        config_description_type_template = """public static final URI {name} = URI.create("{thing_or_channel}-type:"+{type_caps}.toString());"""
        config_description_types_caps = ['CONFIG_DESCRIPTION_URI_' + self.get_name().upper + '_' + common.FlavoredName(c.id).get().upper for c in self.oh.channels if not c.type_id.startswith('system.')]
        config_description_type_decls = [config_description_type_template.format(name=caps, thing_or_channel='channel', type_caps='CHANNEL_TYPE_' + common.FlavoredName(c.type_id).get().upper) for caps, c in zip(config_description_types_caps, [c for c in self.oh.channels]) if not c.type_id.startswith('system.')]

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

        with open(os.path.join(self.get_bindings_dir(), class_name + 'Config.java'), 'w') as f:
            f.write(device.get_openhab_config_class())

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

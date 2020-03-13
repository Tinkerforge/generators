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
import shutil
import sys


sys.path.append(os.path.split(os.getcwd())[0])
sys.path.append(os.path.join(os.path.split(os.getcwd())[0], 'java'))
import common
from java.generate_java_bindings import JavaBindingsGenerator, JavaBindingsDevice
import openhab_common

class OpenHABBindingsDevice(openhab_common.OpenHABDevice, JavaBindingsDevice):
    def __init__(self, *args, **kwargs):
        JavaBindingsDevice.__init__(self, *args, **kwargs)
        self.read_openhab_config()

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
                      'java.util.function.Consumer',
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

    def get_openhab_device_wrapper(self):
        template = """{header}
package org.eclipse.smarthome.binding.tinkerforge.internal.device;

{imports}
import com.tinkerforge.{device_camel};
import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;

import org.eclipse.jdt.annotation.NonNullByDefault;
import org.eclipse.jdt.annotation.Nullable;

@NonNullByDefault
public class {device_camel}Wrapper extends {device_camel} {interfaces}{{
    {device_info}

    public {device_camel}Wrapper(String uid, IPConnection ipcon) {{
        super(uid, ipcon);
    }}

    private List<ScheduledFuture<?>> manualChannelUpdates = new ArrayList<>();
    private List<ListenerReg<?>> listenerRegs = new ArrayList<>();

    public void cancelManualUpdates() {{
        manualChannelUpdates.forEach(f -> f.cancel(true));
    }}

    public <T> T reg(T listener, Consumer<T> toRemove) {{
        listenerRegs.add(new ListenerReg<T>(listener, toRemove));
        return listener;
    }}

    {device_impl}
}}"""

        dev_info_template = 'public final static DeviceInfo DEVICE_INFO = new DeviceInfo({device_camel}.DEVICE_DISPLAY_NAME, "{device_lower}", {device_camel}.DEVICE_IDENTIFIER, {device_camel}Wrapper.class, {actions}Actions.class, "{version}", {isCoMCU});'

        dev_info = dev_info_template.format(device_lower=self.get_thing_type_name(),
                                            device_camel=self.get_java_class_name(),
                                            actions='Default' if len(self.oh.actions) == 0 else self.get_java_class_name(),
                                            version=self.oh.required_firmware_version,
                                            isCoMCU='true' if self.has_comcu() else 'false')

        return template.format(header=self.get_generator().get_header_comment('asterisk'),
                               imports=self.get_openhab_imports(),
                               device_camel=self.get_category().camel + self.get_name().camel,
                               interfaces=common.wrap_non_empty('implements ', ', '.join(self.oh.implemented_interfaces + ['DeviceWrapper']), ' '),
                               device_info=dev_info,
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
            if c.automatic_update and len(c.init_code) == 0:
                continue
            channel_cfg = ['{channel_type_name_camel}Config channelCfg = getChannelConfigFn.apply("{channel_name_camel}").as({channel_type_name_camel}Config.class);'
                               .format(channel_name_camel=c.id.camel,
                                       channel_type_name_camel=c.type.id.camel)]

            if 'channelCfg.' not in c.predicate and 'channelCfg.' not in c.init_code and c.automatic_update:
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
        cb_registration = '{predicate}this.add{camel}Listener(this.reg(({args}) -> {{if({filter}) {{{updateFn}.accept("{channel_camel}", transform{channel_camel}Callback{i}({args}{comma}cfg));}}}}, this::remove{camel}Listener));{end_predicate}'

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
                                                updateFn='triggerChannelFn' if c.type.is_trigger_channel else 'updateStateFn',
                                                i=i,
                                                comma=', ' if len(elements) > 0 else '',
                                                end_predicate='}' if c.predicate != 'true' else ''))

                packet_name = callback.packet.get_name().camel if not callback.packet.has_high_level() else callback.packet.get_name(skip=-2).camel
                if len(c.dispose_code) > 0:
                    dispose_code += [dispose_template.format(predicate='if({}) {{\n'.format(c.predicate) if c.predicate != 'true' else '',
                                                            code=c.dispose_code,
                                                            end_predicate='}' if c.predicate != 'true' else '')]
                lambda_transforms.append(transformation_template.format(state_or_string='String' if c.type.is_trigger_channel else 'org.eclipse.smarthome.core.types.State',
                                                                camel=c.id.camel,
                                                                callback_args=common.wrap_non_empty('', ', '.join(e.get_java_type() + ' ' + e.get_name().headless for e in elements), ', '),
                                                                transform=callback.transform,
                                                                i=i,
                                                                device_camel=self.get_category().camel + self.get_name().camel))

        return (regs,  dispose_code, lambda_transforms)

    def get_openhab_getter_impl(self):
        func_template = """    @Override
    public void refreshValue(String channel, org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, BiConsumer<String, org.eclipse.smarthome.core.types.State> updateStateFn, BiConsumer<String, String> triggerChannelFn) throws TinkerforgeException {{
        {config}
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

        config = "{0}Config cfg = ({0}Config) config.as({0}Config.class);".format(self.get_category().camel + self.get_name().camel);
        config = '' if all(len(c.getters) == 0 for c in self.oh.channels) else config

        channel_cases = []
        transforms = []
        for c in self.oh.channels:
            if len(c.getters) == 0:
                channel_cases.append(empty_case_template.format(camel=c.id.camel))
                continue

            channel_getters = []
            for i, getter in enumerate(c.getters):
                packet_name = getter.packet.get_name().headless if not getter.packet.has_high_level() else getter.packet.get_name(skip=-2).headless
                elements = getter.packet.get_elements(direction='out', high_level=True)
                _, type_ = self.get_filtered_elements_and_type(getter.packet, elements, out_of_class=True)

                channel_getters.append(getter_template.format(updateFn='triggerChannelFn' if c.type.is_trigger_channel else 'updateStateFn',
                                                              camel=c.id.camel,
                                                              getter=packet_name,
                                                              getter_params=', '.join(getter.packet_params),
                                                              i=i,
                                                              type_=type_,
                                                              predicate=getter.predicate))



                transforms.append(transformation_template.format(device_camel=self.get_category().camel + self.get_name().camel,
                                                                 state_or_string='String' if c.type.is_trigger_channel else 'org.eclipse.smarthome.core.types.State',
                                                                 camel=c.id.camel,
                                                                 type_=type_,
                                                                 transform=getter.transform,
                                                                 i=i))
            getters = '\n                   '.join(channel_getters)
            template = case_template if 'channelCfg.' not in getters else case_template_with_config
            channel_cases.append(template.format(camel=c.id.camel,
                                                 channel_type_camel=c.type.id.camel,
                                                 getters=getters))

        return (func_template.format(name_camel=self.get_category().camel + self.get_name().camel,
                                     config=config,
                                     channel_cases='\n            '.join(channel_cases)), transforms)


    def get_openhab_setter_impl(self):
        template = """    @Override
    public List<SetterRefresh> handleCommand(org.eclipse.smarthome.config.core.Configuration config, org.eclipse.smarthome.config.core.Configuration channelConfig, String channel, Command command) throws TinkerforgeException {{
        List<SetterRefresh> result = {refresh_init};
        {config}
        switch(channel) {{
            {channel_cases}
            default:
                logger.warn("Command for unknown channel {{}}", channel);
        }}
        return result;
    }}"""

        config = "{0}Config cfg = ({0}Config) config.as({0}Config.class);".format(self.get_category().camel + self.get_name().camel)

        setter_template = "this.{setter}({setter_params});"
        setter_with_predicate_template = """if({pred}) {{
    this.{setter}({setter_params});
}}"""
        command_template = """if (command instanceof {command_type}) {{
                    {channel_config}
                    {command}
                    {setter}
                }}
        """
        channel_config_template = "{0}Config channelCfg = channelConfig.as({0}Config.class);"
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
                command = "{0} cmd = ({0}) command;".format(s.command_type) if not (s.command_type == 'StringType' and c.type.command_options is not None and len(c.type.command_options) == 1) else ''
                commands.append(command_template.format(channel_type_camel=c.type.id.camel,
                                                        channel_config=channel_config_template.format(c.type.id.camel) if 'channelCfg.' in setter else '',
                                                        command_type=s.command_type,
                                                        command=command,
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
        channel_cases = '\n            '.join(channel_cases)
        return template.format(refresh_init=refresh_init,
                               name_camel=self.get_category().camel + self.get_name().camel,
                               config=config if 'cfg.' in channel_cases else '',
                               channel_cases=channel_cases)

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
        this.setResponseExpectedAll(true);
        {init_config}
        {callback_registrations}
        {init_code}
    }}

    @Override
    public void dispose(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException {{
        listenerRegs.forEach(ListenerReg::deregister);

        {dispose_config}
        {dispose_code}
    }}

    @Override
    public List<String> getEnabledChannels(org.eclipse.smarthome.config.core.Configuration config) throws TinkerforgeException{{
        {enabled_channels_config}
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

        config = "{0}Config cfg = ({0}Config) config.as({0}Config.class);".format(self.get_category().camel + self.get_name().camel)

        init_code = self.oh.init_code.split('\n') + self.get_openhab_channel_init_code()
        dispose_code = self.oh.dispose_code.split('\n')
        callback_regs, callback_dispose_code, lambda_transforms = self.get_openhab_callback_impl()
        refresh_value, getter_transforms = self.get_openhab_getter_impl()
        handle_command = self.get_openhab_setter_impl()
        channel_enablers = self.get_openhab_channel_enablers()

        init_code = '\n\t\t'.join(init_code)
        callback_regs = '\n\t\t'.join(callback_regs)
        dispose_code = '\n\t\t'.join(callback_dispose_code + dispose_code)
        channel_enablers = '\n\t\t'.join(channel_enablers)

        return template.format(name_camel=self.get_category().camel + self.get_name().camel,
                               init_config=config if 'cfg.' in init_code or callback_regs != '' else '',
                               init_code=init_code,
                               callback_registrations=callback_regs,
                               dispose_config=config if 'cfg.' in dispose_code else '',
                               dispose_code=dispose_code,
                               enabled_channels_config=config if 'cfg.' in channel_enablers else '',
                               channel_enablers=channel_enablers,
                               get_channel_type=self.get_openhab_get_channel_type_impl(),
                               get_thing_type=self.get_openhab_get_thing_type_impl(),
                               get_config_description=self.get_openhab_get_config_description_impl(),
                               refresh_value=refresh_value,
                               handle_command=handle_command,
                               transforms='\n\t'.join(lambda_transforms + getter_transforms))

    def get_openhab_get_channel_type_impl(self):
        template = """public static @Nullable ChannelType getChannelType(ChannelTypeUID channelTypeUID) {{
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
        template = """public static @Nullable ConfigDescription getConfigDescription(URI uri) {{
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

        cases = [case_template.format(uri='thing-type:tinkerforge:' + self.get_thing_type_name(),
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
        thing_type_decl = thing_type_template.format(thing_type_caps, self.get_thing_type_name())

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

            cfg.append(param_template.format(name=p.label, type=p.type if not p.limit_to_options else 'choice', description=desc))

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
            channels.append(channel_template.format(name=c.get_label(),
                                                    description=desc,
                                                    type=c.type.item_type if c.type.item_type is not None else 'trigger channel'))

        return template.format(device=self.get_long_display_name(),
                               description=self.get_description()['en'],
                               cfg='\n\n    '.join(cfg),
                               channels='\n\n    '.join(channels),
                               actions=', '.join(self.get_category().headless + self.get_name().camel + a.fn.get_name().camel for a in self.oh.actions) if self.oh.actions != 'custom' else 'custom')

class OpenHABBindingsGenerator(openhab_common.OpenHABGeneratorTrait, JavaBindingsGenerator):
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
            shutil.copy(os.path.join(self.get_root_dir(), class_name + 'Actions.java'), os.path.join(self.get_bindings_dir(), class_name + 'Actions.java'))
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
        doc_folder = os.path.join(self.get_bindings_dir(), '..', 'beta', 'doc')
        shutil.rmtree(doc_folder, ignore_errors=True)
        os.makedirs(doc_folder)

        for file, content in docs:
            with open(os.path.join(doc_folder, file + '.txt'), 'w') as f:
                f.write(content)

def generate(root_dir):
    common.generate(root_dir, 'en', OpenHABBindingsGenerator)

if __name__ == '__main__':
    generate(os.getcwd())

def oh_generic_channel_imports():
    return ['org.eclipse.smarthome.core.library.types.QuantityType',
            'org.eclipse.smarthome.core.library.unit.MetricPrefix',
            'org.eclipse.smarthome.core.library.unit.SIUnits',
            'org.eclipse.smarthome.core.library.unit.SmartHomeUnits']


def oh_generic_channel(id_, type_, unit, divisor=1.0, label=None, description=None):
    return {
        'id': id_,
        'label': label,
        'description': description,
        'type': type_,
        'init_code':"""this.set{camel}CallbackConfiguration(channelCfg.updateInterval, true, \'x\', 0, 0);""",
        'dispose_code': """this.set{camel}CallbackConfiguration(0, true, \'x\', 0, 0);""",

        'getters': [{
            'packet': 'Get {title_words}',
            'packet_params': [],
            'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

        'callbacks': [{
            'packet': '{title_words}',
            'transform': 'new QuantityType<>({headless}{divisor}, {unit})',
            'filter': 'true'}],

        'java_unit': unit,
        'divisor': divisor,
        'is_trigger_channel': False
    }

def oh_generic_old_style_channel(id_, type_, unit, divisor=1.0, cast_literal=''):
    return {
        'id': id_,
        'type': type_,
        'init_code':"""this.set{{camel}}CallbackPeriod(channelCfg.updateInterval);
this.set{{camel}}CallbackThreshold(\'x\', {cast_literal}0, {cast_literal}0);""".format(cast_literal=cast_literal),
        'dispose_code': """this.set{camel}CallbackPeriod(0);""",
        'getters': [{
            'packet': 'Get {title_words}',
            'packet_params': [],
            'transform': 'new QuantityType<>(value{divisor}, {unit})'}],

        'callbacks': [{
            'packet': '{title_words}',
            'transform': 'new QuantityType<>({headless}{divisor}, {unit})',
            'filter': 'true'}],

        'java_unit': unit,
        'divisor': divisor,
        'is_trigger_channel': False
    }

def oh_generic_channel_param_groups():
    return [{
        'name': 'update_intervals',
        'label': 'Update Intervals',
        'description': 'Update Intervals',
        'advanced': 'true'
    }]

def oh_generic_trigger_channel_imports():
    return ["org.eclipse.smarthome.core.thing.CommonTriggerEvents"]

def oh_generic_channel_type(id_, item_type, label, description=None, read_only=None, pattern=None, min_=None, max_=None, is_trigger_channel=False, command_options=None, params=()):
    return {
        'id': id_,
        'item_type': item_type,
        'params':[{
            'name': 'Update Interval',
            'type': 'integer',
            'unit': 'ms',
            'label': 'Update Interval',
            'description': 'Specifies the update interval in milliseconds. A value of 0 disables automatic updates.',
            'default': 1000,
            'groupName': 'update_intervals'
        }] + list(params), # Use tuple as default for params to silence pylint warning "Dangerous default value [] as argument" (as a list could be mutated, changing the default)
        'label': label,
        'description': description,
        'read_only': read_only,
        'pattern': pattern,
        'min': min_,
        'max': max_,
        'is_trigger_channel': is_trigger_channel,
        'command_options': command_options
    }

def update_interval(prefix, description_name):
    return {
        'name': prefix + ' Update Interval',
        'type': 'integer',
        'unit': 'ms',
        'label': prefix + ' Update Interval',
        'description': 'Specifies the update interval for {} in milliseconds. A value of 0 disables automatic updates.'.format(description_name),
        'default': 1000,
        'groupName': 'update_intervals'
    }

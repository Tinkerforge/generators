# -*- coding: utf-8 -*-

# IO-4 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 1],
    'category': 'Bricklet',
    'name': ('IO4', 'io4', 'IO-4'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling up to 4 general purpose input/output pins',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetValue', 'set_value'),
'elements': [('value_mask', 'uint8', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the output value (high or low) with a bit mask. The bit mask
is 4 bit long, "true" refers to high and "false" refers to low.

For example: The value 0b0011 will turn the pins 0-1 high and the
pins 2-3 low.

.. note::
 This function does nothing for pins that are configured as input.
 Pull up resistors can be switched on with :func:`SetConfiguration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetValue', 'get_value'),
'elements': [('value_mask', 'uint8', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns a bit mask of the values that are currently measured.
This function works if the pin is configured to input
as well as if it is configured to output.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetConfiguration', 'set_configuration'),
'elements': [('pin_mask', 'uint8', 1, 'in'),
             ('direction', 'char', 1, 'in'),
             ('value', 'bool', 1, 'in')],
'doc': ['bm', {
'en':
"""
Configures the value and direction of the specified pins. Possible directions
are "i" and "o" for input and output.

If the direction is configured as output, the value is either high or low
(set as true or false).

If the direction is configured as input, the value is either pull up or
default (set as true or false).

For example:

* (15, 'i', true) will set all pins of as input pull up.
* (8, 'i', false) will set pin 3 of as input default (floating if nothing is connected).
* (3, 'o', false) will set pins 0 and 1 as output low.
* (4, 'o', true) will set pin 2 of as output high.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetConfiguration', 'get_configuration'),
'elements': [('direction_mask', 'uint8', 1, 'out'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns a value bit mask and a direction bit mask.

For example: A return value of 0b0011 and 0b0101 for
direction and value means that:

* pin 0 is configured as input pull up,
* pin 1 is configured as input default,
* pin 2 is configured as output high
* and pin 3 is are configured as output low.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetDebouncePeriod', 'set_debounce_period'),
'elements': [('debounce', 'uint32', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the debounce period of the :func:`Interrupt` callback in ms.

For example: If you set this value to 100, you will get the interrupt
maximal every 100ms. This is necessary if something that bounces is
connected to the IO-4 Bricklet, such as a button.

The default value is 100.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetDebouncePeriod', 'get_debounce_period'),
'elements': [('debounce', 'uint32', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the debounce period as set by :func:`SetDebouncePeriod`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetInterrupt', 'set_interrupt'),
'elements': [('interrupt_mask', 'uint8', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the pins on which an interrupt is activated with a bit mask.
Interrupts are triggered on changes of the voltage level of the pin,
i.e. changes from high to low and low to high.

For example: An interrupt bit mask of 9 will enable the interrupt for
pins 0 and 3.

The interrupt is delivered with the callback :func:`Interrupt`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetInterrupt', 'get_interrupt'),
'elements': [('interrupt_mask', 'uint8', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the interrupt bit mask as set by :func:`SetInterrupt`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Interrupt', 'interrupt'),
'elements': [('interrupt_mask', 'uint8', 1, 'out'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a change of the voltage level is detected
on pins where the interrupt was activated with :func:`SetInterrupt`.

The values are a bit mask that specifies which interrupts occurred
and the current value bit mask.

For example:

* (1, 1) means that an interrupt on pin 0 occurred and
  currently pin 0 is high and pins 1-3 are low.
* (9, 14) means that an interrupt on pins 0 and 3
  occurred and currently pin 0 is low and pins 1-3 are high.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetMonoflop', 'set_monoflop'),
'elements': [('pin_mask', 'uint8', 1, 'in'),
             ('value_mask', 'uint8', 1, 'in'),
             ('time', 'uint32', 1, 'in')],
'doc': ['am', {
'en':
"""
Configures a monoflop of the pins specified by the first parameter as 4 bit
long bit mask. The specified pins must be configured for output. Non-output
pins will be ignored.

The second parameter is a bit mask with the desired value of the specified
output pins (*true* means high and *false* means low).

The third parameter indicates the time (in ms) that the pins should hold
the value.

If this function is called with the parameters ((1 << 0) | (1 << 3), (1 << 0), 1500):
Pin 0 will get high and Pin 3 will get low. In 1.5s Pin 0 will get low and Pin
3 will get high again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and an IO-4 Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and Pin 0 set to high. Pin 0 will be high all the time. If now
the RS485 connection is lost, then Pin 0 will get low in at most two seconds.

.. versionadded:: 1.1.1
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetMonoflop', 'get_monoflop'),
'elements': [('pin', 'uint8', 1, 'in'),
             ('value', 'uint8', 1, 'out'),
             ('time', 'uint32', 1, 'out'),
             ('time_remaining', 'uint32', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns (for the given pin) the current value and the time as set by
:func:`SetMonoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.

.. versionadded:: 1.1.1
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('MonoflopDone', 'monoflop_done'),
'elements': [('pin_mask', 'uint8', 1, 'out'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the pins and the current value of the pins
(the value after the monoflop).

.. versionadded:: 1.1.1
""",
'de':
"""
"""
}]
})

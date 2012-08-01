# -*- coding: utf-8 -*-

# IO-16 Bricklet communication config

com = {
    'author': 'Olaf Lüke <olaf@tinkerforge.com>',
    'version': [1, 0, 1],
    'category': 'Bricklet',
    'name': ('IO16', 'io16', 'IO-16'),
    'manufacturer': 'Tinkerforge',
    'description': 'Device for controlling up to 16 general purpose input/output pins',
    'packets': []
}

com['packets'].append({
'type': 'function',
'name': ('SetPort', 'set_port'), 
'elements': [('port', 'char', 1, 'in'),
             ('value_mask', 'uint8', 1, 'in')],
'doc': ['bm', {
'en':
"""
Sets the output value (high or low) for a port ("a" or "b") with a bit mask. 
The bit mask is 8 bit long, "true" refers to high and "false" refers to low.

For example: The value 0b00001111 will turn the pins 0-3 high and the
pins 4-7 low for the specified port.

.. note::
 This function does nothing for pins that are configured as input.
 Pull up resistors can be switched on with :func:`SetPortConfiguration`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPort', 'get_port'), 
'elements': [('port', 'char', 1, 'in'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns a bit mask of the values that are currently measured on the
specified port. This function works if the pin is configured to input
as well as if it is configured to output.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPortConfiguration', 'set_port_configuration'), 
'elements': [('port', 'char', 1, 'in'),
             ('pin_mask', 'uint8', 1, 'in'),
             ('direction', 'char', 1, 'in'),
             ('value', 'bool', 1, 'in')],
'doc': ['bm', {
'en':
"""
Configures the value and direction of a specified port. Possible directions
are "i" and "o" for input and output.

If the direction is configured as output, the value is either high or low
(set as true or false).

If the direction is configured as input, the value is either pull up or
default (set as true or false).

For example:

* ("a", 0xFF, 'i', true) will set all pins of port a as input pull up.
* ("a", 128, 'i', false) will set pin 7 of port a as input default (floating if nothing is connected).
* ("b", 3, 'o', false) will set pins 0 and 1 of port b as output low.
* ("b", 4, 'o', true) will set pin 2 of port b as output high.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPortConfiguration', 'get_port_configuration'), 
'elements': [('port', 'char', 1, 'in'),
             ('direction_mask', 'uint8', 1, 'out'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['bm', {
'en':
"""
Returns a value bit mask and a direction bit mask for the specified port.

For example: A return value of 0b00001111 and 0b00110011 for
direction and value means that:

* pins 0 and 1 are configured as input pull up,
* pins 2 and 3 are configured as input default,
* pins 4 and 5 are configured as output high
* and pins 6 and 7 are configured as output low.
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
connected to the IO-16 Bricklet, such as a button.

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
'name': ('SetPortInterrupt', 'set_port_interrupt'), 
'elements': [('port', 'char', 1, 'in'),
             ('interrupt_mask', 'uint8', 1, 'in')],
'doc': ['ccm', {
'en':
"""
Sets the pins on which an interrupt is activated with a bit mask. 
Interrupts are triggered on changes of the voltage level of the pin,
i.e. changes from high to low and low to high.

For example: ('a', 129) will enable the interrupt for pins 0 and 7 of
port a.

The interrupt is delivered with the callback :func:`Interrupt`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPortInterrupt', 'get_port_interrupt'), 
'elements': [('port', 'char', 1, 'in'),
             ('interrupt_mask', 'uint8', 1, 'out')],
'doc': ['ccm', {
'en':
"""
Returns the interrupt bit mask for the specified port as set by
:func:`SetPortInterrupt`.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('Interrupt', 'interrupt'), 
'elements': [('port', 'char', 1, 'out'),
             ('interrupt_mask', 'uint8', 1, 'out'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a change of the voltage level is detected
on pins where the interrupt was activated with :func:`SetPortInterrupt`.

The values are the port, a bit mask that specifies which interrupts occurred
and the current value bit mask of the port.

For example:

* ("a", 1, 1) means that on port a an interrupt on pin 0 occurred and
  currently pin 0 is high and pins 1-7 are low.
* ("b", 128, 254) means that on port b an interrupt on pins 0 and 7
  occurred and currently pin 0 is low and pins 1-7 are high.
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('SetPortMonoflop', 'set_port_monoflop'),
'elements': [('port', 'char', 1, 'in'),
             ('pin_mask', 'uint8', 1, 'in'),
             ('value_mask', 'uint8', 1, 'in'),
             ('time', 'uint32', 1, 'in')],
'doc': ['am', {
'en':
"""
Configures a monoflop of the pins specified by the second parameter as 4 bit
long bit mask. The specified pins must be configured for output. Non-output
pins will be ignored.

The third parameter is a bit mask with the desired value of the specified
output pins (*true* means high and *false* means low).

The forth parameter indicates the time (in ms) that the pins should hold
the value.

If this function is called with the parameters ('a', (1 << 0) | (1 << 3), (1 << 0), 1500):
Pin 0 will get high and Pin 3 will get low on port 'a'. In 1.5s Pin 0 will get
low and Pin 3 will get high again.

A monoflop can be used as a failsafe mechanism. For example: Lets assume you
have a RS485 bus and an IO-16 Bricklet connected to one of the slave
stacks. You can now call this function every second, with a time parameter
of two seconds and Pin 0 set to high. Pin 0 will be high all the time. If now
the RS485 connection is lost, then Pin 0 will get low in at most two seconds.

.. versionadded:: 1.1.2
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'function',
'name': ('GetPortMonoflop', 'get_port_monoflop'),
'elements': [('port', 'char', 1, 'in'),
             ('pin', 'uint8', 1, 'in'),
             ('value', 'uint8', 1, 'out'),
             ('time', 'uint32', 1, 'out'),
             ('time_remaining', 'uint32', 1, 'out')],
'doc': ['am', {
'en':
"""
Returns (for the given pin) the current value and the time as set by
:func:`SetPortMonoflop` as well as the remaining time until the value flips.

If the timer is not running currently, the remaining time will be returned
as 0.

.. versionadded:: 1.1.2
""",
'de':
"""
"""
}]
})

com['packets'].append({
'type': 'callback',
'name': ('MonoflopDone', 'monoflop_done'),
'elements': [('port', 'char', 1, 'out'),
             ('pin_mask', 'uint8', 1, 'out'),
             ('value_mask', 'uint8', 1, 'out')],
'doc': ['c', {
'en':
"""
This callback is triggered whenever a monoflop timer reaches 0. The
:word:`parameters` contain the port, the pins and the current value of the pins
(the value after the monoflop).

.. versionadded:: 1.1.2
""",
'de':
"""
"""
}]
})

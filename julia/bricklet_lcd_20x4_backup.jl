


export BrickletLCD20x4Config
struct BrickletLCD20x4Config
    cursor::Bool
    blinking::Bool
end

export BrickletLCD20x4Identity
struct BrickletLCD20x4Identity
    uid::String
    connected_uid::String
    position::Char
    hardware_version::Vector{Integer}
    firmware_version::Vector{Integer}
    device_identifier::Integer
end

export BrickletLCD20x4
"""
20x4 character alphanumeric display with blue backlight
"""
mutable struct BrickletLCD20x4 <: TinkerforgeDevice
    replaced::Bool
	uid::Union{Integer, Missing}
	uid_string::String
	ipcon::IPConnection
	device_identifier::Integer
	device_display_name::String
    device_url_part::String
	device_identifier_lock::Base.AbstractLock
	device_identifier_check::DeviceIdentifierCheck # protected by device_identifier_lock
	wrong_device_display_name::String # protected by device_identifier_lock
	api_version::Tuple{Integer, Integer, Integer}
	registered_callbacks::Dict{Integer, Function}
	expected_response_function_id::Union{Integer, Nothing} # protected by request_lock
	expected_response_sequence_number::Union{Integer, Nothing} # protected by request_lock
	response_queue::DataStructures.Queue{Symbol}
	request_lock::Base.AbstractLock
	stream_lock::Base.AbstractLock

    callbacks::Dict{Symbol, Integer}
    callback_formats::Dict{Symbol, Tuple{Integer, String}}
    high_level_callbacks::Dict{Symbol, Integer}
    id_definitions::Dict{Symbol, Integer}
    constants::Dict{Symbol, Integer}
    response_expected::DefaultDict{Symbol, ResponseExpected}

    """
    Creates an object with the unique device ID *uid* and adds it to
    the IP Connection *ipcon*.
    """
    function BrickletLCD20x4(uid::String, ipcon::IPConnection)
        replaced = false
        uid_string = uid
        device_identifier = 212
        device_display_name = "LCD 20x4 Bricklet"
        device_url_part = "lcd_20x4" # internal
        device_identifier_lock = Base.ReentrantLock()
        device_identifier_check = DEVICE_IDENTIFIER_CHECK_PENDING # protected by device_identifier_lock
        wrong_device_display_name = "?" # protected by device_identifier_lock
        api_version = (0, 0, 0)
        registered_callbacks = Dict{Integer, Function}()
        expected_response_function_id = nothing # protected by request_lock
        expected_response_sequence_number = nothing # protected by request_lock
        response_queue = DataStructures.Queue{Symbol}()
        request_lock = Base.ReentrantLock()
        stream_lock = Base.ReentrantLock()

        callbacks = Dict{Symbol, Integer}()
        callback_formats = Dict{Symbol, Tuple{Integer, String}}()
        high_level_callbacks = Dict{Symbol, Integer}()
        id_definitions = Dict{Symbol, Integer}()
        constants = Dict{Symbol, Integer}()
        response_expected = DefaultDict{Symbol, ResponseExpected}(RESPONSE_EXPECTED_INVALID_FUNCTION_ID)

        device = new(
            replaced,
            missing,
            uid_string,
            ipcon,
            device_identifier,
            device_display_name,
            device_url_part,
            device_identifier_lock,
            device_identifier_check,
            wrong_device_display_name,
            api_version,
            registered_callbacks,
            expected_response_function_id,
            expected_response_sequence_number,
            response_queue,
            request_lock,
            stream_lock,
            callbacks,
            callback_formats,
            high_level_callbacks,
            id_definitions,
            constants,
            response_expected
        )
        _initDevice(device)

        device.api_version = (2, 0, 2)

        device.callbacks[:CALLBACK_BUTTON_PRESSED] = 9
        device.callbacks[:CALLBACK_BUTTON_RELEASED] = 10

        device.id_definitions[:FUNCTION_WRITE_LINE] = 1
        device.id_definitions[:FUNCTION_CLEAR_DISPLAY] = 2
        device.id_definitions[:FUNCTION_BACKLIGHT_ON] = 3
        device.id_definitions[:FUNCTION_BACKLIGHT_OFF] = 4
        device.id_definitions[:FUNCTION_IS_BACKLIGHT_ON] = 5
        device.id_definitions[:FUNCTION_SET_CONFIG] = 6
        device.id_definitions[:FUNCTION_GET_CONFIG] = 7
        device.id_definitions[:FUNCTION_IS_BUTTON_PRESSED] = 8
        device.id_definitions[:FUNCTION_SET_CUSTOM_CHARACTER] = 11
        device.id_definitions[:FUNCTION_GET_CUSTOM_CHARACTER] = 12
        device.id_definitions[:FUNCTION_SET_DEFAULT_TEXT] = 13
        device.id_definitions[:FUNCTION_GET_DEFAULT_TEXT] = 14
        device.id_definitions[:FUNCTION_SET_DEFAULT_TEXT_COUNTER] = 15
        device.id_definitions[:FUNCTION_GET_DEFAULT_TEXT_COUNTER] = 16
        device.id_definitions[:FUNCTION_GET_IDENTITY] = 255


        device.response_expected[:FUNCTION_WRITE_LINE] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_CLEAR_DISPLAY] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_BACKLIGHT_ON] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_BACKLIGHT_OFF] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_IS_BACKLIGHT_ON] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_SET_CONFIG] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_GET_CONFIG] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_IS_BUTTON_PRESSED] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_SET_CUSTOM_CHARACTER] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_GET_CUSTOM_CHARACTER] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_SET_DEFAULT_TEXT] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_GET_DEFAULT_TEXT] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_SET_DEFAULT_TEXT_COUNTER] = RESPONSE_EXPECTED_FALSE
        device.response_expected[:FUNCTION_GET_DEFAULT_TEXT_COUNTER] = RESPONSE_EXPECTED_ALWAYS_TRUE
        device.response_expected[:FUNCTION_GET_IDENTITY] = RESPONSE_EXPECTED_ALWAYS_TRUE

        device.callback_formats[:CALLBACK_BUTTON_PRESSED] = (9, "B")
        device.callback_formats[:CALLBACK_BUTTON_RELEASED] = (9, "B")

        add_device(ipcon, device)

        return device
    end
end

export write_line
"""
    $(SIGNATURES)

Writes text to a specific line with a specific position.
The text can have a maximum of 20 characters.

For example: (0, 7, "Hello") will write *Hello* in the middle of the
first line of the display.

The display uses a special charset that includes all ASCII characters except
backslash and tilde. The LCD charset also includes several other non-ASCII characters, see
the `charset specification <https://github.com/Tinkerforge/lcd-20x4-bricklet/raw/master/datasheets/standard_charset.pdf>`__
for details. The Unicode example above shows how to specify non-ASCII characters
and how to translate from Unicode to the LCD charset.
"""
function write_line(brick::BrickletLCD20x4, line, position, text)
    check_validity(brick)

    line = Int64(line)
    position = Int64(position)
    text = create_string(text)

    send_request(brick.ipcon, :FUNCTION_WRITE_LINE, (line, position, text), "B B 20s", 0, "")
end

export clear_display
"""
    $(SIGNATURES)

Deletes all characters from the display.
"""
function clear_display(brick::BrickletLCD20x4)
    check_validity(brick)


    send_request(brick.ipcon, :FUNCTION_CLEAR_DISPLAY, (), "", 0, "")
end

export backlight_on
"""
    $(SIGNATURES)

Turns the backlight on.
"""
function backlight_on(brick::BrickletLCD20x4)
    check_validity(brick)


    send_request(brick, :FUNCTION_BACKLIGHT_ON, (), "", 0, "")
end

export backlight_off
"""
    $(SIGNATURES)

Turns the backlight off.
"""
function backlight_off(brick::BrickletLCD20x4)
    check_validity(brick)


    send_request(brick, :FUNCTION_BACKLIGHT_OFF, (), "", 0, "")
end

export is_backlight_on
"""
    $(SIGNATURES)

Returns *true* if the backlight is on and *false* otherwise.
"""
function is_backlight_on(brick::BrickletLCD20x4)
    check_validity(brick)


    return send_request(brick.ipcon, :FUNCTION_IS_BACKLIGHT_ON, (), "", 9, "!")
end

export set_config
"""
    $(SIGNATURES)

Configures if the cursor (shown as "_") should be visible and if it
should be blinking (shown as a blinking block). The cursor position
is one character behind the the last text written with
:func:`Write Line`.
"""
function set_config(brick::BrickletLCD20x4, cursor, blinking)
    check_validity(brick)

    cursor = bool(cursor)
    blinking = bool(blinking)

    send_request(brick.ipcon, :FUNCTION_SET_CONFIG, (cursor, blinking), "! !", 0, "")
end

export get_config
"""
    $(SIGNATURES)

Returns the configuration as set by :func:`Set Config`.
"""
function get_config(brick::BrickletLCD20x4)
    check_validity(brick)


    return GetConfig(send_request(brick.ipcon, :FUNCTION_GET_CONFIG, (), "", 10, "! !"))
end

export is_button_pressed
"""
    $(SIGNATURES)

Returns *true* if the button (0 to 2 or 0 to 3 since hardware version 1.2)
is pressed.

If you want to react on button presses and releases it is recommended to use
the :cb:`Button Pressed` and :cb:`Button Released` callbacks.
"""
function is_button_pressed(brick::BrickletLCD20x4, button)
    check_validity(brick)

    button = int(button)

    return send_request(brick.ipcon, :FUNCTION_IS_BUTTON_PRESSED, (button,), "B", 9, "!")
end

export set_custom_character
"""
    $(SIGNATURES)

The LCD 20x4 Bricklet can store up to 8 custom characters. The characters
consist of 5x8 pixels and can be addressed with the index 0-7. To describe
the pixels, the first 5 bits of 8 bytes are used. For example, to make
a custom character "H", you should transfer the following:

* ``character[0] = 0b00010001`` (decimal value 17)
* ``character[1] = 0b00010001`` (decimal value 17)
* ``character[2] = 0b00010001`` (decimal value 17)
* ``character[3] = 0b00011111`` (decimal value 31)
* ``character[4] = 0b00010001`` (decimal value 17)
* ``character[5] = 0b00010001`` (decimal value 17)
* ``character[6] = 0b00010001`` (decimal value 17)
* ``character[7] = 0b00000000`` (decimal value 0)

The characters can later be written with :func:`Write Line` by using the
characters with the byte representation 8 ("\\\\x08" or "\\\\u0008") to 15
("\\\\x0F" or "\\\\u000F").

You can play around with the custom characters in Brick Viewer version
since 2.0.1.

Custom characters are stored by the LCD in RAM, so they have to be set
after each startup.

.. versionadded:: 2.0.1\$nbsp;(Plugin)
"""
function set_custom_character(brick::BrickletLCD20x4, index, character)
    check_validity(brick)

    index = int(index)
    character = list(map(int, character))

    send_request(brick.ipcon, :FUNCTION_SET_CUSTOM_CHARACTER, (index, character), "B 8B", 0, "")
end

export get_custom_character
"""
    $(SIGNATURES)

Returns the custom character for a given index, as set with
:func:`Set Custom Character`.

.. versionadded:: 2.0.1\$nbsp;(Plugin)
"""
function get_custom_character(brick::BrickletLCD20x4, index)
    check_validity(brick)

    index = int(index)

    return send_request(brick.ipcon, :FUNCTION_GET_CUSTOM_CHARACTER, (index,), "B", 16, "8B")
end

export set_default_text
"""
    $(SIGNATURES)

Sets the default text for lines 0-3. The max number of characters
per line is 20.

The default text is shown on the LCD, if the default text counter
expires, see :func:`Set Default Text Counter`.

.. versionadded:: 2.0.2\$nbsp;(Plugin)
"""
function set_default_text(brick::BrickletLCD20x4, line, text)
    check_validity(brick)

    line = int(line)
    text = create_string(text)

    send_request(brick.ipcon, :FUNCTION_SET_DEFAULT_TEXT, (line, text), "B 20s", 0, "")
end

export get_default_text
"""
    $(SIGNATURES)

Returns the default text for a given line (0-3) as set by
:func:`Set Default Text`.

.. versionadded:: 2.0.2\$nbsp;(Plugin)
"""
function get_default_text(brick::BrickletLCD20x4, line)
    check_validity(brick)

    line = int(line)

    return send_request(brick.ipcon, :FUNCTION_GET_DEFAULT_TEXT, (line,), "B", 28, "20s")
end

export set_default_text_counter
"""
    $(SIGNATURES)

Sets the default text counter. This counter is decremented each
ms by the LCD firmware. If the counter reaches 0, the default text
(see :func:`Set Default Text`) is shown on the LCD.

This functionality can be used to show a default text if the controlling
program crashes or the connection is interrupted.

A possible approach is to call :func:`Set Default Text Counter` every
minute with the parameter 1000*60*2 (2 minutes). In this case the
default text will be shown no later than 2 minutes after the
controlling program crashes.

A negative counter turns the default text functionality off.

.. versionadded:: 2.0.2\$nbsp;(Plugin)
"""
function set_default_text_counter(brick::BrickletLCD20x4, counter)
    check_validity(brick)

    counter = int(counter)

    send_request(brick.ipcon, :FUNCTION_SET_DEFAULT_TEXT_COUNTER, (counter,), "i", 0, "")
end

export get_default_text_counter
"""
    $(SIGNATURES)

Returns the current value of the default text counter.

.. versionadded:: 2.0.2\$nbsp;(Plugin)
"""
function get_default_text_counter(brick::BrickletLCD20x4)
    check_validity(brick)


    return send_request(brick.ipcon, :FUNCTION_GET_DEFAULT_TEXT_COUNTER, (), "", 12, "i")
end

export get_identity
"""
    $(SIGNATURES)

Returns the UID, the UID where the Bricklet is connected to,
the position, the hardware and firmware version as well as the
device identifier.

The position can be 'a', 'b', 'c', 'd', 'e', 'f', 'g' or 'h' (Bricklet Port).
A Bricklet connected to an :ref:`Isolator Bricklet <isolator_bricklet>` is always at
position 'z'.

The device identifier numbers can be found :ref:`here <device_identifier>`.
|device_identifier_constant|
"""
function get_identity(brick::BrickletLCD20x4)


    return GetIdentity(send_request(brick.ipcon, :FUNCTION_GET_IDENTITY, (), "", 33, "8s 8s c 3B 3B H"))
end

export register_callback
"""
Registers the given *function* with the given *callback_id*.
"""
function register_callback(device::BrickletLCD20x4, callback_id, function_)
    if isnothing(function_)
        device.registered_callbacks.pop(callback_id, None)
    else
        device.registered_callbacks[callback_id] = function_
    end
end

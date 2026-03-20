# -*- coding: utf-8 -*-
# Created by René Rohner
# Copyright (C) 2026 Tinkerforge GmbH
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

# MicroPython IP Connection implementation.
# Designed for ESP32 and other MicroPython-capable boards.
# Uses synchronous/blocking I/O with explicit callback dispatch,
# following the same pattern as the PHP bindings.

import struct
import socket
import sys
import time
import math
import hashlib

try:
    import hmac
except ImportError:
    hmac = None

try:
    import os
except ImportError:
    os = None

try:
    from collections import namedtuple
except ImportError:
    pass

def get_uid_from_data(data):
    return struct.unpack('<I', data[0:4])[0]

def get_length_from_data(data):
    return struct.unpack('<B', data[4:5])[0]

def get_function_id_from_data(data):
    return struct.unpack('<B', data[5:6])[0]

def get_sequence_number_from_data(data):
    return (struct.unpack('<B', data[6:7])[0] >> 4) & 0x0F

def get_error_code_from_data(data):
    return (struct.unpack('<B', data[7:8])[0] >> 6) & 0x03

BASE58 = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

def base58encode(value):
    encoded = ''

    while value >= 58:
        div, mod = divmod(value, 58)
        encoded = BASE58[mod] + encoded
        value = div

    return BASE58[value] + encoded

def base58decode(encoded):
    value = 0
    column_multiplier = 1

    for c in reversed(encoded):
        try:
            column = BASE58.index(c)
        except ValueError:
            raise Error(Error.INVALID_UID, 'UID "{0}" contains invalid character'.format(encoded))

        value += column * column_multiplier
        column_multiplier *= 58

    return value

def uid64_to_uid32(uid64):
    value1 = uid64 & 0xFFFFFFFF
    value2 = (uid64 >> 32) & 0xFFFFFFFF

    uid32  = (value1 & 0x00000FFF)
    uid32 |= (value1 & 0x0F000000) >> 12
    uid32 |= (value2 & 0x0000003F) << 16
    uid32 |= (value2 & 0x000F0000) << 6
    uid32 |= (value2 & 0x3F000000) << 2

    return uid32

def create_chunk_data(data, chunk_offset, chunk_length, chunk_padding):
    chunk_data = data[chunk_offset:chunk_offset + chunk_length]

    if len(chunk_data) < chunk_length:
        chunk_data += [chunk_padding] * (chunk_length - len(chunk_data))

    return chunk_data

def create_char(value):
    if isinstance(value, str) and len(value) == 1 and ord(value) <= 255:
        return value
    elif isinstance(value, (bytes, bytearray)) and len(value) == 1:
        return chr(value[0])
    elif isinstance(value, int) and value >= 0 and value <= 255:
        return chr(value)
    else:
        raise ValueError('Invalid char value: ' + repr(value))

def create_char_list(value, expected_type='char list'):
    if isinstance(value, list):
        return list(map(create_char, value))
    elif isinstance(value, str):
        chars = list(value)

        for char in chars:
            if ord(char) > 255:
                raise ValueError('Invalid {0} value: {1}'.format(expected_type, repr(value)))

        return chars
    elif isinstance(value, (bytes, bytearray)):
        return list(map(chr, value))
    else:
        raise ValueError('Invalid {0} value: {1}'.format(expected_type, repr(value)))

def create_string(value):
    if isinstance(value, str):
        for char in value:
            if ord(char) > 255:
                raise ValueError('Invalid string value: {0}'.format(repr(value)))

        return value
    elif isinstance(value, (bytes, bytearray)):
        return ''.join(map(chr, value))
    else:
        return ''.join(create_char_list(value, expected_type='string'))

def pack_payload(data, form):
    packed = b''

    for f, d in zip(form.split(' '), data):
        if '!' in f:
            if len(f) > 1:
                if int(f.replace('!', '')) != len(d):
                    raise ValueError('Incorrect bool list length')

                p = [0] * int(math.ceil(len(d) / 8.0))

                for i, b in enumerate(d):
                    if b:
                        p[i // 8] |= 1 << (i % 8)

                packed += struct.pack('<{0}B'.format(len(p)), *p)
            else:
                packed += struct.pack('<B', 1 if d else 0)
        elif 'c' in f:
            # MicroPython struct doesn't support 'c', use 'B' (unsigned byte) instead
            bf = f.replace('c', 'B')
            if len(f) > 1:
                packed += struct.pack('<' + bf, *list(map(lambda char: ord(char), d)))
            else:
                packed += struct.pack('<' + bf, ord(d))
        elif 's' in f:
            packed += struct.pack('<' + f, bytes(map(ord, d)))
        elif len(f) > 1:
            packed += struct.pack('<' + f, *d)
        else:
            packed += struct.pack('<' + f, d)

    return packed

def unpack_payload(data, form):
    ret = []

    for f in form.split(' '):
        o = f

        if '!' in f:
            if len(f) > 1:
                f = '{0}B'.format(int(math.ceil(int(f.replace('!', '')) / 8.0)))
            else:
                f = 'B'

        # MicroPython struct doesn't support 'c', use 'B' (unsigned byte) instead
        f = '<' + f.replace('c', 'B')
        length = struct.calcsize(f)
        x = struct.unpack(f, data[:length])

        if '!' in o:
            y = []

            if len(o) > 1:
                for i in range(int(o.replace('!', ''))):
                    y.append(x[i // 8] & (1 << (i % 8)) != 0)
            else:
                y.append(x[0] != 0)

            x = tuple(y)

        if 'c' in o:
            if len(o) > 1:
                ret.append(tuple(map(lambda item: chr(item), x)))
            else:
                ret.append(chr(x[0]))
        elif 's' in f:
            s = ''.join(map(chr, x[0]))

            i = s.find('\x00')

            if i >= 0:
                s = s[:i]

            ret.append(s)
        elif len(x) > 1:
            ret.append(x)
        else:
            ret.append(x[0])

        data = data[length:]

    if len(ret) == 1:
        return ret[0]
    else:
        return ret

class Error(Exception):
    TIMEOUT = -1
    NOT_ADDED = -6 # obsolete since v2.0
    ALREADY_CONNECTED = -7
    NOT_CONNECTED = -8
    INVALID_PARAMETER = -9
    NOT_SUPPORTED = -10
    UNKNOWN_ERROR_CODE = -11
    STREAM_OUT_OF_SYNC = -12
    INVALID_UID = -13
    NON_ASCII_CHAR_IN_SECRET = -14
    WRONG_DEVICE_TYPE = -15
    DEVICE_REPLACED = -16
    WRONG_RESPONSE_LENGTH = -17

    def __init__(self, value, description):
        super().__init__('{0} ({1})'.format(description, value))

        self.value = value
        self.description = description

class Device:
    DEVICE_IDENTIFIER_CHECK_PENDING = 0
    DEVICE_IDENTIFIER_CHECK_MATCH = 1
    DEVICE_IDENTIFIER_CHECK_MISMATCH = 2

    RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0
    RESPONSE_EXPECTED_ALWAYS_TRUE = 1 # getter
    RESPONSE_EXPECTED_TRUE = 2 # setter
    RESPONSE_EXPECTED_FALSE = 3 # setter, default

    def __init__(self, uid, ipcon, device_identifier, device_display_name):
        uid_ = base58decode(uid)

        if uid_ > (1 << 64) - 1:
            raise Error(Error.INVALID_UID, 'UID "{0}" is too big'.format(uid))

        if uid_ > (1 << 32) - 1:
            uid_ = uid64_to_uid32(uid_)

        if uid_ == 0:
            raise Error(Error.INVALID_UID, 'UID "{0}" is empty or maps to zero'.format(uid))

        self.replaced = False
        self.uid = uid_
        self.uid_string = uid
        self.ipcon = ipcon
        self.device_identifier = device_identifier
        self.device_display_name = device_display_name
        self.device_identifier_check = Device.DEVICE_IDENTIFIER_CHECK_PENDING
        self.wrong_device_display_name = '?'
        self.api_version = (0, 0, 0)
        self.registered_callbacks = {}
        self.callback_formats = {}
        self.high_level_callbacks = {}
        self.pending_callbacks = []
        self.expected_response_function_id = None
        self.expected_response_sequence_number = None
        self.received_response = None

        self.response_expected = [Device.RESPONSE_EXPECTED_INVALID_FUNCTION_ID] * 256
        self.response_expected[IPConnection.FUNCTION_ADC_CALIBRATE] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnection.FUNCTION_GET_ADC_CALIBRATION] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnection.FUNCTION_READ_BRICKLET_UID] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[IPConnection.FUNCTION_WRITE_BRICKLET_UID] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE

    def get_api_version(self):
        """
        Returns the API version (major, minor, revision) of the bindings for
        this device.
        """
        return self.api_version

    def get_response_expected(self, function_id):
        """
        Returns the response expected flag for the function specified by the
        *function_id* parameter. It is *true* if the function is expected to
        send a response, *false* otherwise.
        """
        if function_id < 0 or function_id >= len(self.response_expected):
            raise ValueError('Function ID {0} out of range'.format(function_id))

        flag = self.response_expected[function_id]

        if flag == Device.RESPONSE_EXPECTED_INVALID_FUNCTION_ID:
            raise ValueError('Invalid function ID {0}'.format(function_id))

        return flag in [Device.RESPONSE_EXPECTED_ALWAYS_TRUE, Device.RESPONSE_EXPECTED_TRUE]

    def set_response_expected(self, function_id, response_expected):
        """
        Changes the response expected flag of the function specified by the
        *function_id* parameter. This flag can only be changed for setter
        (default value: *false*) and callback configuration functions
        (default value: *true*). For getter functions it is always enabled.
        """
        if function_id < 0 or function_id >= len(self.response_expected):
            raise ValueError('Function ID {0} out of range'.format(function_id))

        flag = self.response_expected[function_id]

        if flag == Device.RESPONSE_EXPECTED_INVALID_FUNCTION_ID:
            raise ValueError('Invalid function ID {0}'.format(function_id))

        if flag == Device.RESPONSE_EXPECTED_ALWAYS_TRUE:
            raise ValueError('Response Expected flag cannot be changed for function ID {0}'.format(function_id))

        if bool(response_expected):
            self.response_expected[function_id] = Device.RESPONSE_EXPECTED_TRUE
        else:
            self.response_expected[function_id] = Device.RESPONSE_EXPECTED_FALSE

    def set_response_expected_all(self, response_expected):
        """
        Changes the response expected flag for all setter and callback
        configuration functions of this device at once.
        """
        if bool(response_expected):
            flag = Device.RESPONSE_EXPECTED_TRUE
        else:
            flag = Device.RESPONSE_EXPECTED_FALSE

        for i in range(len(self.response_expected)):
            if self.response_expected[i] in [Device.RESPONSE_EXPECTED_TRUE, Device.RESPONSE_EXPECTED_FALSE]:
                self.response_expected[i] = flag

    def check_validity(self):
        if self.replaced:
            raise Error(Error.DEVICE_REPLACED, 'Device has been replaced')

        if self.device_identifier < 0:
            return

        if self.device_identifier_check == Device.DEVICE_IDENTIFIER_CHECK_MATCH:
            return

        if self.device_identifier_check == Device.DEVICE_IDENTIFIER_CHECK_PENDING:
            device_identifier = self.ipcon.send_request(self, 255, (), '', 33, '8s 8s c 3B 3B H')[5] # <device>.get_identity

            if device_identifier == self.device_identifier:
                self.device_identifier_check = Device.DEVICE_IDENTIFIER_CHECK_MATCH
            else:
                self.device_identifier_check = Device.DEVICE_IDENTIFIER_CHECK_MISMATCH
                self.wrong_device_display_name = str(device_identifier)

        if self.device_identifier_check == Device.DEVICE_IDENTIFIER_CHECK_MISMATCH:
            raise Error(Error.WRONG_DEVICE_TYPE,
                        'UID {0} belongs to a {1} instead of the expected {2}'
                        .format(self.uid_string, self.wrong_device_display_name, self.device_display_name))

    def _dispatch_pending_callbacks(self):
        """Dispatch all pending callbacks for this device."""
        pending = self.pending_callbacks
        self.pending_callbacks = []

        for packet in pending:
            if self.ipcon.socket is None:
                break

            try:
                self.check_validity()
            except:
                continue # silently ignoring callbacks from mismatching devices

            self.ipcon.dispatch_packet(packet)

class BrickDaemon(Device):
    FUNCTION_GET_AUTHENTICATION_NONCE = 1
    FUNCTION_AUTHENTICATE = 2

    def __init__(self, uid, ipcon):
        Device.__init__(self, uid, ipcon, 0, 'Brick Daemon')

        self.api_version = (2, 0, 0)

        self.response_expected[BrickDaemon.FUNCTION_GET_AUTHENTICATION_NONCE] = BrickDaemon.RESPONSE_EXPECTED_ALWAYS_TRUE
        self.response_expected[BrickDaemon.FUNCTION_AUTHENTICATE] = BrickDaemon.RESPONSE_EXPECTED_TRUE

        ipcon.add_device(self)

    def get_authentication_nonce(self):
        return self.ipcon.send_request(self, BrickDaemon.FUNCTION_GET_AUTHENTICATION_NONCE, (), '', 12, '4B')

    def authenticate(self, client_nonce, digest):
        self.ipcon.send_request(self, BrickDaemon.FUNCTION_AUTHENTICATE, (client_nonce, digest), '4B 20B', 0, '')

class IPConnection:
    FUNCTION_ENUMERATE = 254
    FUNCTION_ADC_CALIBRATE = 251
    FUNCTION_GET_ADC_CALIBRATION = 250
    FUNCTION_READ_BRICKLET_UID = 249
    FUNCTION_WRITE_BRICKLET_UID = 248
    FUNCTION_DISCONNECT_PROBE = 128

    CALLBACK_ENUMERATE = 253
    CALLBACK_CONNECTED = 0
    CALLBACK_DISCONNECTED = 1

    BROADCAST_UID = 0

    # enumeration_type parameter to the enumerate callback
    ENUMERATION_TYPE_AVAILABLE = 0
    ENUMERATION_TYPE_CONNECTED = 1
    ENUMERATION_TYPE_DISCONNECTED = 2

    # connect_reason parameter to the connected callback
    CONNECT_REASON_REQUEST = 0

    # disconnect_reason parameter to the disconnected callback
    DISCONNECT_REASON_REQUEST = 0
    DISCONNECT_REASON_ERROR = 1
    DISCONNECT_REASON_SHUTDOWN = 2

    # returned by get_connection_state
    CONNECTION_STATE_DISCONNECTED = 0
    CONNECTION_STATE_CONNECTED = 1

    DISCONNECT_PROBE_INTERVAL = 5

    def __init__(self):
        """
        Creates an IP Connection object that can be used to enumerate the
        available devices. It is also required for the constructor of Bricks
        and Bricklets.
        """
        self.host = None
        self.port = None
        self.timeout = 2.5
        self.next_sequence_number = 0
        self.next_authentication_nonce = 0
        self.devices = {}
        self.registered_callbacks = {}
        self.socket = None
        self.pending_data = b''
        self.pending_callbacks = [] # for enumerate callbacks
        self.next_disconnect_probe = 0
        self.disconnect_probe_request = None
        self.brickd = BrickDaemon('2', self)

    def connect(self, host, port):
        """
        Creates a TCP/IP connection to the given *host* and *port*. The host
        and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.

        Devices can only be controlled when the connection was established
        successfully.

        Blocks until the connection is established and throws an exception if
        there is no Brick Daemon or WIFI/Ethernet Extension listening at the
        given host and port.
        """
        if self.socket is not None:
            raise Error(Error.ALREADY_CONNECTED,
                        'Already connected to {0}:{1}'.format(self.host, self.port))

        self.host = host
        self.port = port

        try:
            addr = socket.getaddrinfo(host, port)[0][-1]
            self.socket = socket.socket()
            self.socket.connect(addr)
        except Exception as e:
            if self.socket is not None:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            raise

        # Pre-build disconnect probe request
        self.disconnect_probe_request, _, _ = self.create_packet_header(None, 8, IPConnection.FUNCTION_DISCONNECT_PROBE)
        self.next_disconnect_probe = time.time() + IPConnection.DISCONNECT_PROBE_INTERVAL
        self.pending_data = b''

        cb = self.registered_callbacks.get(IPConnection.CALLBACK_CONNECTED)
        if cb is not None:
            cb(IPConnection.CONNECT_REASON_REQUEST)

    def disconnect(self):
        """
        Disconnects the TCP/IP connection from the Brick Daemon or the
        WIFI/Ethernet Extension.
        """
        if self.socket is None:
            raise Error(Error.NOT_CONNECTED, 'Not connected')

        disconnect_reason = IPConnection.DISCONNECT_REASON_REQUEST

        try:
            self.socket.close()
        except:
            pass

        self.socket = None

        cb = self.registered_callbacks.get(IPConnection.CALLBACK_DISCONNECTED)
        if cb is not None:
            cb(disconnect_reason)

    def authenticate(self, secret):
        """
        Performs an authentication handshake with the connected Brick Daemon or
        WIFI/Ethernet Extension.
        """
        if hmac is None:
            raise Error(Error.NOT_SUPPORTED, 'authenticate requires the hmac module which is not available in this MicroPython build')

        try:
            secret_bytes = secret.encode('ascii')
        except UnicodeEncodeError:
            raise Error(Error.NON_ASCII_CHAR_IN_SECRET, 'Authentication secret contains non-ASCII characters')

        if self.next_authentication_nonce == 0:
            try:
                self.next_authentication_nonce = struct.unpack('<I', os.urandom(4))[0]
            except (NotImplementedError, AttributeError):
                subseconds, seconds = math.modf(time.time())
                seconds = int(seconds)
                subseconds = int(subseconds * 1000000)
                self.next_authentication_nonce = ((seconds << 26 | seconds >> 6) & 0xFFFFFFFF) + subseconds

        server_nonce = self.brickd.get_authentication_nonce()
        client_nonce = struct.unpack('<4B', struct.pack('<I', self.next_authentication_nonce))
        self.next_authentication_nonce = (self.next_authentication_nonce + 1) % (1 << 32)

        h = hmac.new(secret_bytes, digestmod=hashlib.sha1)

        h.update(struct.pack('<4B', *server_nonce))
        h.update(struct.pack('<4B', *client_nonce))

        digest = struct.unpack('<20B', h.digest())

        self.brickd.authenticate(client_nonce, digest)

    def get_connection_state(self):
        """
        Can return the following states:

        - CONNECTION_STATE_DISCONNECTED: No connection is established.
        - CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
          the WIFI/Ethernet Extension is established.
        """
        if self.socket is not None:
            return IPConnection.CONNECTION_STATE_CONNECTED
        else:
            return IPConnection.CONNECTION_STATE_DISCONNECTED

    def set_timeout(self, timeout):
        """
        Sets the timeout in seconds for getters and for setters for which the
        response expected flag is activated.

        Default timeout is 2.5.
        """
        timeout = float(timeout)

        if timeout < 0:
            raise ValueError('Timeout cannot be negative')

        self.timeout = timeout

    def get_timeout(self):
        """
        Returns the timeout as set by set_timeout.
        """
        return self.timeout

    def enumerate(self):
        """
        Broadcasts an enumerate request. All devices will respond with an
        enumerate callback.
        """
        request, _, _ = self.create_packet_header(None, 8, IPConnection.FUNCTION_ENUMERATE)

        self._send(request)

    def register_callback(self, callback_id, function):
        """
        Registers the given *function* with the given *callback_id*.
        """
        if function is None:
            self.registered_callbacks.pop(callback_id, None)
        else:
            self.registered_callbacks[callback_id] = function

    def dispatch_callbacks(self, seconds):
        """
        Dispatches incoming callbacks for the given amount of time in seconds
        (negative value means infinity). Because MicroPython doesn't support
        threads you need to call this method periodically to ensure that
        incoming callbacks are handled. If you don't use callbacks you don't
        need to call this method.

        The recommended dispatch time is 0. This will just dispatch all pending
        callbacks without waiting for further callbacks.
        """
        # Dispatch all pending callbacks
        self._dispatch_pending_callbacks()

        if seconds < 0:
            while True:
                self._receive(self.timeout, None, True)
                self._dispatch_pending_callbacks()
        else:
            self._receive(seconds, None, True)

    def add_device(self, device):
        replaced_device = self.devices.get(device.uid)

        if replaced_device is not None:
            replaced_device.replaced = True

        self.devices[device.uid] = device

    def send_request(self, device, function_id, data, form, length_ret, form_ret):
        if len(form) > 0:
            payload = pack_payload(data, form)
        else:
            payload = b''

        header, response_expected, sequence_number = self.create_packet_header(device, 8 + len(payload), function_id)
        request = header + payload

        if response_expected:
            device.expected_response_function_id = function_id
            device.expected_response_sequence_number = sequence_number
            device.received_response = None

            try:
                self._send(request)
                self._receive(self.timeout, device, False)
            finally:
                device.expected_response_function_id = None
                device.expected_response_sequence_number = None

            if device.received_response is None:
                msg = 'Did not receive response for function {0} in time'.format(function_id)
                raise Error(Error.TIMEOUT, msg)

            response = device.received_response
            device.received_response = None

            error_code = get_error_code_from_data(response)

            if error_code == 0:
                if length_ret == 0:
                    length_ret = 8 # setter with response-expected enabled

                if len(response) != length_ret:
                    msg = 'Expected response of {0} byte for function ID {1}, got {2} byte instead' \
                          .format(length_ret, function_id, len(response))
                    raise Error(Error.WRONG_RESPONSE_LENGTH, msg)
            elif error_code == 1:
                msg = 'Got invalid parameter for function {0}'.format(function_id)
                raise Error(Error.INVALID_PARAMETER, msg)
            elif error_code == 2:
                msg = 'Function {0} is not supported'.format(function_id)
                raise Error(Error.NOT_SUPPORTED, msg)
            else:
                msg = 'Function {0} returned an unknown error'.format(function_id)
                raise Error(Error.UNKNOWN_ERROR_CODE, msg)

            if len(form_ret) > 0:
                return unpack_payload(response[8:], form_ret)
        else:
            self._send(request)

    def _send(self, packet):
        if self.socket is None:
            raise Error(Error.NOT_CONNECTED, 'Not connected')

        try:
            self.socket.send(packet)
        except OSError:
            self._handle_disconnect(IPConnection.DISCONNECT_REASON_ERROR)
            raise Error(Error.NOT_CONNECTED, 'Not connected')

        self.next_disconnect_probe = time.time() + IPConnection.DISCONNECT_PROBE_INTERVAL

    def _receive(self, seconds, device, direct_callback_dispatch):
        if seconds < 0:
            seconds = 0

        start = time.time()
        end = start + seconds

        while True:
            if self.socket is None:
                return

            now = time.time()

            # Send disconnect probe if needed
            if self.disconnect_probe_request is not None and \
               (self.next_disconnect_probe < now or
                (self.next_disconnect_probe - now) > IPConnection.DISCONNECT_PROBE_INTERVAL):
                try:
                    self.socket.send(self.disconnect_probe_request)
                except OSError:
                    self._handle_disconnect(IPConnection.DISCONNECT_REASON_ERROR)
                    return

                now = time.time()
                self.next_disconnect_probe = now + IPConnection.DISCONNECT_PROBE_INTERVAL

            timeout = end - now

            if timeout < 0:
                timeout = 0

            # Set socket timeout for this receive cycle
            try:
                self.socket.settimeout(timeout)
            except OSError:
                self._handle_disconnect(IPConnection.DISCONNECT_REASON_ERROR)
                return

            try:
                data = self.socket.recv(8192)
            except OSError as e:
                # Check for timeout
                if hasattr(e, 'errno'):
                    import errno
                    if e.errno == errno.ETIMEDOUT or e.errno == errno.EAGAIN:
                        if device is not None and device.received_response is not None:
                            return
                        now = time.time()
                        if now >= end and now >= start:
                            return
                        continue
                # On MicroPython, timeout raises OSError with ETIMEDOUT
                # Try to detect timeout by checking time
                now = time.time()
                if now >= end and now >= start:
                    return
                continue

            if len(data) == 0:
                self._handle_disconnect(IPConnection.DISCONNECT_REASON_SHUTDOWN)
                return

            self.pending_data += data

            while True:
                if len(self.pending_data) < 8:
                    break

                length = get_length_from_data(self.pending_data)

                if len(self.pending_data) < length:
                    break

                packet = self.pending_data[0:length]
                self.pending_data = self.pending_data[length:]

                self._handle_response(packet, direct_callback_dispatch)

            if device is not None and device.received_response is not None:
                return

            now = time.time()
            if now >= end and now >= start:
                return

    def _handle_response(self, packet, direct_callback_dispatch):
        self.next_disconnect_probe = time.time() + IPConnection.DISCONNECT_PROBE_INTERVAL

        function_id = get_function_id_from_data(packet)
        sequence_number = get_sequence_number_from_data(packet)

        if sequence_number == 0 and function_id == IPConnection.CALLBACK_ENUMERATE:
            if IPConnection.CALLBACK_ENUMERATE in self.registered_callbacks:
                if direct_callback_dispatch:
                    if self.socket is None:
                        return
                    self.dispatch_packet(packet)
                else:
                    self.pending_callbacks.append(packet)
            return

        uid = get_uid_from_data(packet)
        device = self.devices.get(uid)

        if device is None:
            return # Response from an unknown device, ignoring it

        if sequence_number == 0:
            if function_id in device.registered_callbacks or \
               -function_id in device.high_level_callbacks:
                if direct_callback_dispatch:
                    if self.socket is None:
                        return
                    self.dispatch_packet(packet)
                else:
                    device.pending_callbacks.append(packet)
            return

        if device.expected_response_function_id == function_id and \
           device.expected_response_sequence_number == sequence_number:
            device.received_response = packet
            return

        # Response seems to be OK, but can't be handled

    def dispatch_packet(self, packet):
        uid = get_uid_from_data(packet)
        function_id = get_function_id_from_data(packet)
        payload = packet[8:]

        if function_id == IPConnection.CALLBACK_ENUMERATE:
            cb = self.registered_callbacks.get(IPConnection.CALLBACK_ENUMERATE)

            if cb is None:
                return

            if len(packet) != 34:
                return # silently ignoring callback with wrong length

            uid_str, connected_uid, position, hardware_version, \
                firmware_version, device_identifier, enumeration_type = \
                unpack_payload(payload, '8s 8s c 3B 3B H B')

            cb(uid_str, connected_uid, position, hardware_version,
               firmware_version, device_identifier, enumeration_type)

            return

        device = self.devices.get(uid)

        if device is None:
            return

        try:
            device.check_validity()
        except Error:
            return # silently ignoring callback for invalid device

        if -function_id in device.high_level_callbacks:
            hlcb = device.high_level_callbacks[-function_id] # [roles, options, data]
            length, form = device.callback_formats[function_id]

            if len(packet) != length:
                return # silently ignoring callback with wrong length

            llvalues = unpack_payload(payload, form)
            has_data = False
            data = None

            if hlcb[1]['fixed_length'] is not None:
                length = hlcb[1]['fixed_length']
            else:
                length = llvalues[hlcb[0].index('stream_length')]

            if not hlcb[1]['single_chunk']:
                chunk_offset = llvalues[hlcb[0].index('stream_chunk_offset')]
            else:
                chunk_offset = 0

            chunk_data = llvalues[hlcb[0].index('stream_chunk_data')]

            if hlcb[2] is None: # no stream in-progress
                if chunk_offset == 0: # stream starts
                    hlcb[2] = chunk_data

                    if len(hlcb[2]) >= length: # stream complete
                        has_data = True
                        data = hlcb[2][:length]
                        hlcb[2] = None
                else: # ignore tail of current stream, wait for next stream start
                    pass
            else: # stream in-progress
                if chunk_offset != len(hlcb[2]): # stream out-of-sync
                    has_data = True
                    data = None
                    hlcb[2] = None
                else: # stream in-sync
                    hlcb[2] += chunk_data

                    if len(hlcb[2]) >= length: # stream complete
                        has_data = True
                        data = hlcb[2][:length]
                        hlcb[2] = None

            cb = device.registered_callbacks.get(-function_id)

            if has_data and cb is not None:
                result = []

                for role, llvalue in zip(hlcb[0], llvalues):
                    if role == 'stream_chunk_data':
                        result.append(data)
                    elif role is None:
                        result.append(llvalue)

                cb(*tuple(result))

        cb = device.registered_callbacks.get(function_id)

        if cb is not None:
            length, form = device.callback_formats.get(function_id, (None, None))

            if length is None:
                return # silently ignore registered but unknown callback

            if len(packet) != length:
                return # silently ignoring callback with wrong length

            if len(form) == 0:
                cb()
            elif ' ' not in form:
                cb(unpack_payload(payload, form))
            else:
                cb(*unpack_payload(payload, form))

    def _dispatch_pending_callbacks(self):
        """Dispatch all pending IPConnection-level and device-level callbacks."""
        # Dispatch IPConnection-level pending callbacks (enumerate)
        pending = self.pending_callbacks
        self.pending_callbacks = []

        for packet in pending:
            if self.socket is None:
                break
            self.dispatch_packet(packet)

        # Dispatch device-level pending callbacks
        for device in list(self.devices.values()):
            if self.socket is None:
                break
            device._dispatch_pending_callbacks()

    def _handle_disconnect(self, disconnect_reason):
        if self.socket is not None:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None

        cb = self.registered_callbacks.get(IPConnection.CALLBACK_DISCONNECTED)
        if cb is not None:
            cb(disconnect_reason)

    def get_next_sequence_number(self):
        sequence_number = self.next_sequence_number + 1
        self.next_sequence_number = sequence_number % 15
        return sequence_number

    def create_packet_header(self, device, length, function_id):
        uid = IPConnection.BROADCAST_UID
        sequence_number = self.get_next_sequence_number()
        r_bit = 0

        if device is not None:
            uid = device.uid

            if device.get_response_expected(function_id):
                r_bit = 1

        sequence_number_and_options = (sequence_number << 4) | (r_bit << 3)

        return (struct.pack('<IBBBB', uid, length, function_id,
                            sequence_number_and_options, 0),
                bool(r_bit),
                sequence_number)

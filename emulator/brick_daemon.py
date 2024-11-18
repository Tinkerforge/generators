# Copyright (C) 2021 Matthias Bolte <matthias@tinkerforge.com>
#
# Redistribution and use in source and binary forms of this file,
# with or without modification, are permitted. See the Creative
# Commons Zero (CC0 1.0) License for more details.

import sys

if sys.hexversion < 0x3070000:
    raise Exception('Python >= 3.7 required')

import struct
import math
import re
import asyncio
import logging
import inspect
import functools
from collections import namedtuple

_logger = logging.getLogger('tinkerforge_emulator')

class GenericError(Exception):
    pass

class InvalidUIDError(GenericError):
    pass

class PackingError(GenericError):
    pass

class GenericResult(Exception):
    pass

class NoSupport(GenericResult):
    pass

class NoResponse(GenericResult):
    pass

class Passthrough(GenericResult):
    pass

_FunctionSpec = namedtuple('FunctionSpec', 'input_format output_format callable')
_PassthroughSpec = namedtuple('PassthroughSpec', 'format name callable')
_Request = namedtuple('Request', 'source trace data')
_Response = namedtuple('Response', 'source trace data')
_Callback = namedtuple('Callback', 'source trace data')
_RequestMatch = namedtuple('RequestMatch', 'uid_number function_id sequence_number')
_PendingRequest = namedtuple('PendingRequest', 'request_match request response_queue')

_BASE58_ALPHABET = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ'

_global_debug = False

def set_global_debug(debug):
    global _global_debug

    _global_debug = debug

def _base58_to_number(base58):
    number = 0
    column_multiplier = 1

    for c in base58[::-1]:
        try:
            column = _BASE58_ALPHABET.index(c)
        except ValueError as e:
            raise InvalidUIDError('"{0}" contains invalid character'.format(base58)) from e

        number += column * column_multiplier
        column_multiplier *= 58

    return number

def _number_to_base58(number):
    base58 = ''

    while number >= 58:
        div, mod = divmod(number, 58)
        base58 = _BASE58_ALPHABET[mod] + base58
        number = div

    return _BASE58_ALPHABET[number] + base58

def _exception_to_str(e):
    return '[{0}] {1}'.format(type(e).__name__, e)

def _get_uid_number_from_data(data):
    return struct.unpack('<I', data[0:4])[0]

def _get_length_from_data(data):
    return struct.unpack('<B', data[4:5])[0]

def _get_function_id_from_data(data):
    return struct.unpack('<B', data[5:6])[0]

def _get_sequence_number_from_data(data):
    return (struct.unpack('<B', data[6:7])[0] >> 4) & 0x0F

def _get_response_expected_from_data(data):
    return (struct.unpack('<B', data[6:7])[0] >> 3) & 0x01

def _unpack_payload(format_, payload):
    values = []

    for f in format_:
        o = f

        if '!' in f:
            if len(f) > 1:
                f = '{0}B'.format(int(math.ceil(int(f.replace('!', '')) / 8)))
            else:
                f = 'B'

        f = '<' + f
        length = struct.calcsize(f)
        x = struct.unpack(f, payload[:length])

        if '!' in o:
            y = []

            if len(o) > 1:
                for i in range(int(o.replace('!', ''))):
                    y.append(x[i // 8] & (1 << (i % 8)) != 0)
            else:
                y.append(x[0] != 0)

            x = tuple(y)

        if 'c' in f:
            if len(x) > 1:
                values.append(tuple(map(lambda item: chr(ord(item)), x)))
            else:
                values.append(chr(ord(x[0])))
        elif 's' in f:
            s = ''.join(map(chr, x[0]))

            i = s.find('\x00')

            if i >= 0:
                s = s[:i]

            values.append(s)
        elif len(x) > 1:
            values.append(x)
        else:
            values.append(x[0])

        payload = payload[length:]

    if len(payload) != 0:
        raise ValueError('Non-unpacked payload left over')

    return tuple(values)

def _pack_payload(format_, values):
    payload = b''

    if len(format_) != len(values):
        raise ValueError('Mismatch between pack-format length and payload length: {0} != {1}'.format(len(format_), len(values)))

    for f, v in zip(format_, values):
        if '!' in f:
            if len(f) > 1:
                if int(f.replace('!', '')) != len(v):
                    raise ValueError('Incorrect bool-list length in pack-format')

                p = [0] * int(math.ceil(len(v) / 8))

                for i, b in enumerate(v):
                    if b:
                        p[i // 8] |= 1 << (i % 8)

                payload += struct.pack('<{0}B'.format(len(p)), *p)
            else:
                payload += struct.pack('<?', v)
        elif 'c' in f:
            if len(f) > 1:
                payload += struct.pack('<' + f, *list(map(lambda char: bytes([ord(char)]), v)))
            else:
                payload += struct.pack('<' + f, bytes([ord(v)]))
        elif 's' in f:
            payload += struct.pack('<' + f, bytes(map(ord, v)))
        elif len(f) > 1:
            payload += struct.pack('<' + f, *v)
        else:
            payload += struct.pack('<' + f, v)

    return payload

def _create_error_response(request, error_code):
    header = list(request.data[:8])
    header[4] = 8
    header[7] |= error_code << 6

    return _Response('emulator', request.trace, bytes(header))

async def _cancel_task(task):
    if task.done():
        try:
            task.result() # propagate exception
        except asyncio.CancelledError:
            pass
    else:
        task.cancel()

        try:
            await task
        except asyncio.CancelledError:
            pass

class _InterruptThing:
    pass

async def _run(get_things, create_thing_coroutine, create_interrupt_coroutine=None):
    tasks = {} # by thing
    things = {} # by task
    interrupt_thing = _InterruptThing()
    interrupt_event = asyncio.Event()

    if create_interrupt_coroutine == None:
        # ensure that there is always something to wait for because
        # asyncio.wait doesn't work on an empty set
        create_interrupt_coroutine = interrupt_event.wait

    while True:
        old_things = list(things.values())
        new_things = list(get_things())

        for thing in new_things:
            try:
                old_things.remove(thing)
            except ValueError:
                pass

            if thing in tasks:
                continue

            task = asyncio.create_task(create_thing_coroutine(thing), name='run:thing')

            tasks[thing] = task
            things[task] = thing

        if interrupt_thing not in tasks:
            task = asyncio.create_task(create_interrupt_coroutine(), name='run:interrupt')

            tasks[interrupt_thing] = task
            things[task] = interrupt_thing

        try:
            old_things.remove(interrupt_thing)
        except ValueError:
            pass

        for old_thing in old_things:
            old_task = tasks.pop(old_thing)

            await _cancel_task(old_task) # FIXME: what to do if awaiting cancellation gets cancelled?

        try:
            done, _ = await asyncio.wait(set(tasks.values()), return_when=asyncio.FIRST_COMPLETED)
        except asyncio.CancelledError:
            for task in tasks.values():
                await _cancel_task(task) # FIXME: what to do if awaiting cancellation gets cancelled?

            raise

        for task in done:
            thing = things.pop(task)

            tasks.pop(thing)

            task.result() # propagate exception

# decorator
def autorun(callable_):
    assert inspect.iscoroutinefunction(callable_)

    callable_._is_autorun = True

    return callable_

# decorator
def function(function_id, input_format, output_format):
    assert function_id >= 1 and function_id <= 255, function_id

    def helper(callable_):
        assert inspect.iscoroutinefunction(callable_)

        callable_._is_function = True
        callable_._function_id = function_id
        callable_._input_format = input_format
        callable_._output_format = output_format

        return callable_

    return helper

# decorator
def passthrough(function_id, format_):
    assert function_id >= 1 and function_id <= 255, function_id

    def helper(callable_):
        assert inspect.iscoroutinefunction(callable_)

        m = re.match('^passthrough_([a-z][a-z0-9_]*)_(request|response|callback)$', callable_.__name__)

        assert m != None, callable_.__name__

        callable_._is_passthrough = True
        callable_._function_id = function_id
        callable_._format = format_
        callable_._name = m.group(1)
        callable_._category = m.group(2)

        return callable_

    return helper

class MetaDevice(type):
    def __new__(mcls, name, bases, attrs):
        cls = super().__new__(mcls, name, bases, attrs)

        cls._AUTORUN_CALLABLES = []
        cls._FUNCTION_SPECS = {} # by function_id
        cls._PASSTHROUGH_SPECS = {'request': {}, 'response': {}, 'callback': {}} # by function_id

        autorun_callables = {} # by callable.__name__

        for other_cls in cls.__mro__:
            for attr_name in dir(other_cls):
                attr = getattr(other_cls, attr_name)

                if not inspect.isfunction(attr):
                    continue

                if getattr(attr, '_is_autorun', False) and attr.__name__ not in autorun_callables:
                    autorun_callables[attr.__name__] = getattr(cls, attr_name)

                if getattr(attr, '_is_function', False):
                    function_id = getattr(attr, '_function_id')
                    input_format = getattr(attr, '_input_format')
                    output_format = getattr(attr, '_output_format')
                    function_spec = cls._FUNCTION_SPECS.get(function_id)

                    if function_spec == None:
                        cls._FUNCTION_SPECS[function_id] = _FunctionSpec(input_format, output_format, getattr(cls, attr_name))
                    else:
                        assert function_spec.input_format == input_format
                        assert function_spec.output_format == output_format
                        assert function_spec.callable.__name__ == attr_name

                if getattr(attr, '_is_passthrough', False):
                    function_id = getattr(attr, '_function_id')
                    format_ = getattr(attr, '_format')
                    name_ = getattr(attr, '_name')
                    category = getattr(attr, '_category')
                    passthrough_spec = cls._PASSTHROUGH_SPECS[category].get(function_id)

                    if passthrough_spec == None:
                        cls._PASSTHROUGH_SPECS[category][function_id] = _PassthroughSpec(format_, name_, getattr(cls, attr_name))
                    else:
                        assert passthrough_spec.output_format == output_format
                        assert passthrough_spec.name == name_
                        assert passthrough_spec.callable.__name__ == attr_name

        cls._AUTORUN_CALLABLES = list(autorun_callables.values())

        assert set(cls._FUNCTION_SPECS).isdisjoint(set(cls._PASSTHROUGH_SPECS['request'])), cls
        assert set(cls._PASSTHROUGH_SPECS['response']).isdisjoint(set(cls._PASSTHROUGH_SPECS['callback'])), cls

        return cls

# FIXME: add streaming support
# FIXME: add passthrough request/response manipulation support
class Device(metaclass=MetaDevice):
    _ERROR_CODE_INVALID_PARAMETER = 1
    _ERROR_CODE_FUNCTION_NOT_SUPPORTED = 2

    def __init__(self, uid, debug=None, passthrough_host=None, passthrough_port=None, passthrough_unknown_requests=False,
                 passthrough_unknown_responses=False, passthrough_unknown_callbacks=False):
        super().__init__()

        self._uid = uid
        self._passthrough_host = passthrough_host
        self._passthrough_port = passthrough_port
        self._passthrough_unknown_requests = passthrough_unknown_requests
        self._passthrough_unknown_responses = passthrough_unknown_responses
        self._passthrough_unknown_callbacks = passthrough_unknown_callbacks
        self._uid_number = _base58_to_number(uid)
        self._local_debug = debug
        self._brick_daemon_debug = None
        self._request_queue = asyncio.Queue()
        self._passthrough_queue = asyncio.Queue()
        self._get_next_trace_cb = None
        self._broadcast_response_cb = None

        if self._uid_number > (2 ** 32) - 1:
            raise InvalidUIDError('UID {0} is too big'.format(uid))

    @property
    def _debug(self):
        if self._local_debug != None:
            return self._local_debug

        if self._brick_daemon_debug != None:
            return self._brick_daemon_debug

        return _global_debug

    async def _run(self):
        await _run(lambda: self._AUTORUN_CALLABLES, lambda callable_: callable_(self)) # cancellation is okay here

    def _enqueue_request(self, request, response_queue):
        self._request_queue.put_nowait((request, response_queue))

    @autorun
    async def _handle_requests(self):
        while True:
            request, response_queue = await self._request_queue.get() # cancellation is okay here

            try:
                response = await self._handle_request(request) # cancellation is okay here
            except Passthrough:
                assert self._passthrough_host != None

                self._passthrough_queue.put_nowait((request, response_queue))

                continue

            if response != None:
                response_queue.put_nowait(response)

    def _get_request_handler(self, request):
        function_id = _get_function_id_from_data(request.data)

        # known function
        function_spec = self._FUNCTION_SPECS.get(function_id)

        if function_spec != None:
            signature = '{0}{{{1}}}.{2}'.format(self.__class__.__name__, self._uid, function_spec.callable.__name__)

            return signature, function_spec.input_format, function_spec.output_format, functools.partial(function_spec.callable, self)

        # known function passthrough
        passthrough_spec = self._PASSTHROUGH_SPECS['request'].get(function_id)

        if passthrough_spec != None:
            signature = '{0}{{{1}}}.{2}'.format(self.__class__.__name__, self._uid, passthrough_spec.name)

            async def wrapper(*args):
                if await passthrough_spec.callable(self, *args): # cancellation is okay here
                    raise Passthrough

                raise NoResponse

            return signature, passthrough_spec.format, None, wrapper

        # unknown function
        signature = '{0}{{{1}}}.<{2}>'.format(self.__class__.__name__, self._uid, function_id)

        async def wrapper():
            if self._passthrough_unknown_requests:
                raise Passthrough

            raise NoSupport

        return signature, None, None, wrapper

    async def _handle_request(self, request):
        signature, input_format, output_format, callable_ = self._get_request_handler(request)
        response_expected = _get_response_expected_from_data(request.data) != 0

        if self._debug:
            _logger.debug('Handling {0} for {1} function, {2}response expected'
                          .format(request, signature, '' if response_expected else 'no '))

        # unpack request
        if input_format == None:
            input_values = tuple()
        else:
            try:
                input_values = _unpack_payload(input_format, request.data[8:])
            except Exception as e:
                if not response_expected:
                    if self._debug:
                        _logger.error('Error while unpacking {0} for {1} function as "{2}", no response expected: {3}'
                                      .format(request, signature, ' '.join(input_format), _exception_to_str(e)))

                    return None # no response

                if self._debug:
                    _logger.error('Error while unpacking {0} for {1} function as "{2}", sending invalid-parameter response: {3}'
                                  .format(request, signature, ' '.join(input_format), _exception_to_str(e)))

                return _create_error_response(request, self._ERROR_CODE_INVALID_PARAMETER)

        # call handler
        try:
            output_values = await callable_(*input_values) # cancellation is okay here
        except NoSupport:
            if not response_expected:
                if self._debug:
                    _logger.debug('No-support selected for {0} for {1} function, no response expected'
                                  .format(request, signature))

                return None # no response

            if self._debug:
                _logger.debug('No-support selected for {0} for {1} function, sending function-not-supported response'
                              .format(request, signature))

            return _create_error_response(request, self._ERROR_CODE_FUNCTION_NOT_SUPPORTED)
        except NoResponse:
            if self._debug:
                _logger.debug('No-response selected for {0} for {1} function, {2} response expected'
                              .format(request, signature, 'but' if response_expected else 'no'))

            return None # no response
        except Passthrough:
            if self._passthrough_host != None:
                if self._debug:
                    _logger.debug('Passthrough selected for {0} for {1} function'.format(request, signature))

                raise

            if not response_expected:
                if self._debug:
                    _logger.warning('Passthrough selected for {0} for {1} function, but passthrough not configured, no response expected'
                                    .format(request, signature))

                return None # no response

            if self._debug:
                _logger.warning('Passthrough selected for {0} for {1} function, but passthrough not configured, sending function-not-supported response'
                                .format(request, signature))

            return _create_error_response(request, self._ERROR_CODE_FUNCTION_NOT_SUPPORTED)
        except Exception as e:
            if not response_expected:
                if self._debug:
                    _logger.error('Error while handling {0} for {1} function, no response expected: {2}'
                                  .format(request, signature, _exception_to_str(e)))

                return None # no response

            if self._debug:
                _logger.error('Error while handling {0} for {1} function, abusing invalid-parameter response: {2}'
                              .format(request, signature, _exception_to_str(e)))

            return _create_error_response(request, self._ERROR_CODE_INVALID_PARAMETER)

        if not response_expected:
            if output_values != None and self._debug:
                _logger.warning('Dropping output {0} for {1} for {2} function, no response expected'
                                .format(repr(output_values), request, signature))

            return None # no response

        # pack response
        assert output_format != None, output_format

        if len(output_format) == 0:
            if output_values != None and self._debug:
                _logger.warning('Dropping unexpected output {0} for {1} for {2} function'
                                .format(repr(output_values), request, signature))

            output_values = tuple()
        else:
            if output_values == None:
                if self._debug:
                    _logger.warning('Missing expected output for {0} for {1} function, abusing invalid-parameter response'
                                    .format(request, signature))

                return _create_error_response(request, self._ERROR_CODE_INVALID_PARAMETER)

            if len(output_format) == 1:
                output_values = (output_values,)

            if not isinstance(output_values, tuple) or len(output_format) != len(output_values):
                if self._debug:
                    _logger.warning('Output {0} for {1} for {2} function does not match expected format "{3}", abusing invalid-parameter response'
                                    .format(repr(output_values), request, signature, ' '.join(output_format)))

                return _create_error_response(request, self._ERROR_CODE_INVALID_PARAMETER)

        try:
            payload = _pack_payload(output_format, output_values)
        except Exception as e:
            if self._debug:
                _logger.error('Error while packing output {0} for {1} for {2} function as "{3}", abusing invalid-parameter response: {4}'
                              .format(repr(output_values), request, signature, ' '.join(output_format), _exception_to_str(e)))

            return _create_error_response(request, self._ERROR_CODE_INVALID_PARAMETER)

        header = list(request.data[:8])
        header[4] = 8 + len(payload)

        return _Response('emulator', request.trace, bytes(header) + payload)

    def enqueue_callback(self, callback_id, callback_name, output_format, output_values):
        try:
            payload = _pack_payload(output_format, output_values)
        except Exception as e:
            signature = '{0}{{{1}}}.{2}'.format(self.__class__.__name__, self._uid, callback_name)

            raise PackingError('Error while packing {0} for {1} callback as "{2}": {3}'
                               .format(repr(output_values), signature, ' '.join(output_format), _exception_to_str(e))) from e

        header = struct.pack('<IBBBB', self._uid_number, 8 + len(payload), callback_id, 1 << 3, 0)
        callback = _Callback('emulator', self._get_next_trace(), header + payload)

        self._broadcast_response(callback)

    def _get_response_handler(self, response):
        function_id = _get_function_id_from_data(response.data)
        sequence_number = _get_sequence_number_from_data(response.data)

        if sequence_number != 0:
            category = 'response'
            passthrough_unknown = self._passthrough_unknown_responses
        else:
            category = 'callback'
            passthrough_unknown = self._passthrough_unknown_callbacks

        # known function/callback passthrough
        passthrough_spec = self._PASSTHROUGH_SPECS[category].get(function_id)

        if passthrough_spec != None:
            signature = '{0}{{{1}}}.{2}'.format(self.__class__.__name__, self._uid, passthrough_spec.name)

            return signature, passthrough_spec.format, functools.partial(passthrough_spec.callable, self)

        # unknown function/callback
        signature = '{0}{{{1}}}.<{2}>'.format(self.__class__.__name__, self._uid, function_id)

        async def wrapper():
            return passthrough_unknown

        return signature, None, wrapper

    @autorun
    async def _handle_passthrough(self):
        if self._passthrough_host == None:
            while True:
                await asyncio.sleep(100) # cancellation is okay here

        passthrough_signature = '{0}@{1}:{2}'.format(self._uid, self._passthrough_host, self._passthrough_port)
        cancelled = False

        while not cancelled:
            try:
                reader, writer = await asyncio.open_connection(self._passthrough_host, self._passthrough_port)
            except asyncio.CancelledError:
                break # ignore cancellation here to do proper cleanup
            except Exception as e:
                if self._debug:
                    _logger.error('Error while trying to connect to passthrough {0}: {1}'.format(passthrough_signature, _exception_to_str(e)))

                await asyncio.sleep(3) # cancellation is okay here

                continue

            if self._debug:
                _logger.info('Passthrough {0} connected'.format(passthrough_signature))

            disconnect = False
            request_task = None
            pending_requests = []
            response_task = None
            pending_data = b''

            while not disconnect:
                if request_task == None:
                    request_task = asyncio.create_task(self._passthrough_queue.get(), name='Device:passthrough_queue:get')

                if response_task == None:
                    response_task = asyncio.create_task(reader.read(8192), name='Device:passthrough_socket:read')

                try:
                    await asyncio.wait({request_task, response_task}, return_when=asyncio.FIRST_COMPLETED)
                except asyncio.CancelledError:
                    cancelled = True

                    break # ignore cancellation here to do proper cleanup

                if request_task.done():
                    request, response_queue = request_task.result()
                    request_task = None

                    if self._debug:
                        _logger.debug('Sending {0} to passthrough {1}'.format(request, passthrough_signature))

                    writer.write(request.data)

                    try:
                        await writer.drain()
                    except asyncio.CancelledError:
                        cancelled = True

                        break # ignore cancellation here to do proper cleanup

                    if _get_response_expected_from_data(request.data) != 0:
                        uid_number = _get_uid_number_from_data(request.data)
                        function_id = _get_function_id_from_data(request.data)
                        sequence_number = _get_sequence_number_from_data(request.data)
                        request_match = _RequestMatch(uid_number, function_id, sequence_number)

                        pending_requests.append(_PendingRequest(request_match, request, response_queue))

                if response_task.done():
                    try:
                        data = response_task.result()
                    except asyncio.CancelledError:
                        break # ignore cancellation here to do proper cleanup
                    except Exception as e:
                        if self._debug:
                            _logger.error('Error while receiving response data, disconnecting passthrough {0}: {1}'
                                          .format(passthrough_signature, _exception_to_str(e)))

                        break

                    response_task = None

                    if len(data) == 0:
                        if self._debug:
                            _logger.info('Passthrough {0} disconnected by peer'.format(passthrough_signature))

                        break

                    pending_data += data

                    while True:
                        if len(pending_data) < 8:
                            break # wait for complete header

                        length = _get_length_from_data(pending_data)

                        if length < 8 or length > 80:
                            if self._debug:
                                _logger.error('Received response data {0}... with invalid length {1}, disconnecting passthrough {2}'
                                              .format(pending_data[:80], length, passthrough_signature))

                            disconnect = True

                            break

                        if len(pending_data) < length:
                            break # wait for complete response

                        response_data = pending_data[:length]
                        pending_data = pending_data[length:]
                        uid_number = _get_uid_number_from_data(response_data)

                        if uid_number == 0:
                            if self._debug:
                                _logger.error('Received response data {0} with zero UID, disconnecting passthrough {1}'
                                              .format(response_data, passthrough_signature))

                            disconnect = True

                            break

                        if _get_function_id_from_data(response_data) == 0:
                            if self._debug:
                                _logger.error('Received response data {0} with zero function ID, disconnecting passthrough {1}'
                                              .format(response_data, passthrough_signature))

                            disconnect = True

                            break

                        if _get_response_expected_from_data(response_data) == 0:
                            if self._debug:
                                _logger.error('Received response data {0} without response-expected flag, disconnecting passthrough {1}'
                                              .format(response_data, passthrough_signature))

                            disconnect = True

                            break

                        if uid_number != self._uid_number:
                            continue

                        sequence_number = _get_sequence_number_from_data(response_data)

                        if sequence_number != 0:
                            kind = 'function'
                            wrapper = _Response
                        else:
                            kind = 'callback'
                            wrapper = _Callback

                        response = wrapper(passthrough_signature, self._get_next_trace(), response_data)
                        signature, output_format, callable_ = self._get_response_handler(response)

                        if self._debug:
                            _logger.debug('Received {0} for {1} {2}'.format(response, signature, kind))

                        if output_format == None:
                            output_values = tuple()
                        else:
                            try:
                                output_values = _unpack_payload(output_format, response.data[8:])
                            except Exception as e:
                                if self._debug:
                                    _logger.error('Error while unpacking {0} for {1} {2} as "{3}", disconnecting passthrough {4}: {5}'
                                                  .format(response, signature, kind, ' '.join(output_format), passthrough_signature, _exception_to_str(e)))

                                disconnect = True

                                break

                        try:
                            forward = await callable_(*output_values)
                        except asyncio.CancelledError:
                            cancelled = True
                            disconnect = True

                            break # ignore cancellation here to do proper cleanup
                        except Exception as e:
                            if self._debug:
                                if output_format != None:
                                    output_format_str = 'as "{0}"'.format(' '.join(output_format))
                                else:
                                    output_format_str = ''

                                _logger.error('Error while handling {0} for {1} {2}{3}, disconnecting passthrough {4}: {5}'
                                              .format(response, signature, kind, output_format_str, passthrough_signature, _exception_to_str(e)))

                            disconnect = True

                            break

                        if not forward:
                            if self._debug:
                                _logger.debug('Dropping {0}'.format(response))

                            continue

                        if sequence_number == 0:
                            if self._debug:
                                _logger.debug('Forwarding {0}'.format(response))

                            self._broadcast_response(response)
                        else:
                            request_match = _RequestMatch(uid_number, function_id, sequence_number)

                            for i, pending_request in enumerate(pending_requests):
                                if pending_request.request_match != request_match:
                                    continue

                                if self._debug:
                                    _logger.debug('Forwarding {0} expected by {1}'.format(response, pending_request.request))

                                pending_request.response_queue.put_nowait(response)
                                pending_requests.pop(i)

                                break
                            else:
                                if self._debug:
                                    _logger.debug('Forwarding unexpected {0}'.format(response))

                                self._broadcast_response(response)

            if request_task != None:
                await _cancel_task(request_task) # FIXME: what to do if awaiting cancellation gets cancelled?

            if response_task != None:
                await _cancel_task(response_task) # FIXME: what to do if awaiting cancellation gets cancelled?

            writer.close()

            try:
                await writer.wait_closed()
            except asyncio.CancelledError:
                raise # cancellation is okay here
            except Exception as e:
                if self._debug:
                    _logger.error('Error while disconnecting passthrough {0}: {1}'
                                  .format(passthrough_signature, _exception_to_str(e)))

    def _get_next_trace(self):
        if self._get_next_trace_cb == None:
            return None

        return self._get_next_trace_cb()

    def _broadcast_response(self, response):
        if self._broadcast_response_cb == None:
            if self._debug:
                _logger.warning('Dropping {0} to be broadcasted, device not added to a Brick Daemon'.format(response))

            return

        self._broadcast_response_cb(response)

class EnumerateFeature:
    ENUMERATION_TYPE_AVAILABLE = 0
    ENUMERATION_TYPE_CONNECTED = 1
    ENUMERATION_TYPE_DISCONNECTED = 2

    def __init__(self):
        super().__init__()

        self._connected_uid = '0'
        self._position = '?'
        self._hardware_version = (1, 0, 0)
        self._firmware_version = (2, 0, 0)
        self._device_identifier = 0

    def configure_enumerate_feature(self, connected_uid, position, hardware_version, firmware_version, device_identifier):
        self._connected_uid = connected_uid
        self._position = position
        self._hardware_version = hardware_version
        self._firmware_version = firmware_version
        self._device_identifier = device_identifier

    @function(254, [], [])
    async def enumerate(self):
        self.enqueue_enumerate_callback(self.ENUMERATION_TYPE_AVAILABLE)

    @function(255, [], ['8s', '8s', 'c', '3B', '3B', 'H'])
    async def get_identity(self):
        return self._uid, self._connected_uid, self._position, self._hardware_version, self._firmware_version, self._device_identifier

    def enqueue_enumerate_callback(self, enumeration_type):
        if enumeration_type == self.ENUMERATION_TYPE_DISCONNECTED:
            output_values = [
                self._uid,
                '',
                '\0',
                (0, 0, 0),
                (0, 0, 0),
                0,
                enumeration_type
            ]
        else:
            output_values = [
                self._uid,
                self._connected_uid,
                self._position,
                self._hardware_version,
                self._firmware_version,
                self._device_identifier,
                enumeration_type
            ]

        self.enqueue_callback(253, 'enumerate', ['8s', '8s', 'c', '3B', '3B', 'H', 'B'], output_values)

class CoMCUBrickletFeature:
    BOOTLOADER_MODE_BOOTLOADER = 0
    BOOTLOADER_MODE_FIRMWARE = 1
    BOOTLOADER_MODE_BOOTLOADER_WAIT_FOR_REBOOT = 2
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_REBOOT = 3
    BOOTLOADER_MODE_FIRMWARE_WAIT_FOR_ERASE_AND_REBOOT = 4

    STATUS_LED_CONFIG_OFF = 0
    STATUS_LED_CONFIG_ON = 1
    STATUS_LED_CONFIG_SHOW_HEARTBEAT = 2
    STATUS_LED_CONFIG_SHOW_STATUS = 3

    def __init__(self):
        super().__init__()

        self._bootloader_mode = self.BOOTLOADER_MODE_FIRMWARE
        self._status_led_config = self.STATUS_LED_CONFIG_SHOW_STATUS

    @function(236, [], ['B'])
    async def get_bootloader_mode(self):
        return self._bootloader_mode

    @function(239, ['B'], [])
    async def set_status_led_config(self, config):
        self._status_led_config = config

    @function(240, [], ['B'])
    async def get_status_led_config(self):
        return self._status_led_config

# FIXME: add authentication support
class BrickDaemon:
    _BROADCAST_UID_NUMBER = 0

    _FUNCTION_ID_DISCONNECT_PROBE = 128

    def __init__(self, host, port, debug=None, start_running=True):
        self._host = host
        self._port = port
        self._local_debug = debug
        self._next_trace = 1
        self._devices = {} # by uid_number
        self._device_change_queue = asyncio.Queue()
        self._clients = []
        self._client_addition_queue = asyncio.Queue()
        self._response_queues = []
        self._run_task = None

        if start_running:
            self.start_running()

    @property
    def _debug(self):
        if self._local_debug != None:
            return self._local_debug

        return _global_debug

    def _get_next_trace(self):
        trace = self._next_trace

        self._next_trace += 1

        return trace

    def _add_device(self, device):
        if device._uid_number in self._devices:
            if self._debug:
                _logger.warning('Device with UID {0} has already been added'.format(device._uid))

            return False

        device._brick_daemon_debug = self._local_debug
        device._get_next_trace_cb = self._get_next_trace
        device._broadcast_response_cb = self._broadcast_response

        self._devices[device._uid_number] = device

        if isinstance(device, EnumerateFeature):
            device.enqueue_enumerate_callback(device.ENUMERATION_TYPE_CONNECTED)

        return True

    async def add_device(self, device):
        if self._run_task == None:
            return self._add_device(device)

        return_queue = asyncio.Queue()

        self._device_change_queue.put_nowait((self._add_device, device, return_queue))

        success, result = await return_queue.get() # cancellation is okay here

        if not success:
            raise result

        return result

    def _remove_device(self, device):
        known_device = self._devices.get(device._uid_number)

        if known_device == None:
            if self._debug:
                _logger.warning('Device with UID {0} has not been added before'.format(device._uid))

            return False

        if known_device != device:
            if self._debug:
                _logger.warning('Device with UID {0} does not match device to be removed'.format(device._uid))

            return False

        if isinstance(device, EnumerateFeature):
            device.enqueue_enumerate_callback(device.ENUMERATION_TYPE_DISCONNECTED)

        self._devices.pop(device._uid_number)

        device._brick_daemon_debug = None
        device._get_next_trace_cb = None
        device._broadcast_response_cb = None

        return True

    async def remove_device(self, device):
        if self._run_task == None:
            return self._remove_device(device)

        return_queue = asyncio.Queue()

        self._device_change_queue.put_nowait((self._remove_device, device, return_queue))

        success, result = await return_queue.get() # cancellation is okay here

        if not success:
            raise result

        return result

    async def _handle_device_change(self):
        callable_, device, return_queue = await self._device_change_queue.get() # cancellation is okay here

        try:
            result = callable_(device)
            success = True
        except Exception as e:
            result = e
            success = False

        return_queue.put_nowait((success, result))

    def _enqueue_request(self, request, response_queue):
        uid_number = _get_uid_number_from_data(request.data)

        if uid_number == self._BROADCAST_UID_NUMBER:
            function_id = _get_function_id_from_data(request.data)

            if function_id == self._FUNCTION_ID_DISCONNECT_PROBE:
                if self._debug:
                    _logger.debug('Dropping disconnect-probe {0}'.format(request))

                return

            if self._debug:
                _logger.debug('Broadcasting {0} to all devices'.format(request))

            for device in self._devices.values():
                device._enqueue_request(request, response_queue)

            return

        device = self._devices.get(uid_number)

        if device != None:
            device._enqueue_request(request, response_queue)

            return

        if self._debug:
            _logger.warning('Dropping {0} for unknown UID {1}'.format(request, _number_to_base58(uid_number)))

    def _broadcast_response(self, response):
        if self._debug:
            _logger.debug('Broadcasting {0} to all clients'.format(response))

        for response_queue in self._response_queues:
            response_queue.put_nowait(response)

    async def _handle_client_addition(self):
        client = await self._client_addition_queue.get() # cancellation is okay here

        self._clients.append(client)

    async def _handle_client(self, client):
        reader, writer = client
        peername = writer.get_extra_info('peername')

        if peername == None:
            client_signature = '<unknown>'
        else:
            client_signature = '{0}:{1}'.format(*peername)

        if self._debug:
            _logger.info('Client {0} connected'.format(client_signature))

        disconnect = False
        request_task = None
        pending_data = b''
        response_task = None
        response_queue = asyncio.Queue()

        self._response_queues.append(response_queue)

        while not disconnect:
            if request_task == None:
                request_task = asyncio.create_task(reader.read(8192), name='Client:socket:read')

            if response_task == None:
                response_task = asyncio.create_task(response_queue.get(), name='Client:response_queue:get')

            try:
                await asyncio.wait({request_task, response_task}, return_when=asyncio.FIRST_COMPLETED)
            except asyncio.CancelledError:
                break # ignore cancellation here to do proper cleanup

            if request_task.done():
                try:
                    data = request_task.result()
                except asyncio.CancelledError:
                    break # ignore cancellation here to do proper cleanup
                except Exception as e:
                    if self._debug:
                        _logger.error('Error while receiving request data, disconnecting client {0}: {1}'
                                      .format(client_signature, _exception_to_str(e)))

                    break

                request_task = None

                if len(data) == 0:
                    if self._debug:
                        _logger.info('Client {0} disconnected by peer'.format(client_signature))

                    break

                pending_data += data

                while True:
                    if len(pending_data) < 8:
                        break # wait for complete header

                    length = _get_length_from_data(pending_data)

                    if length < 8 or length > 80:
                        if self._debug:
                            _logger.error('Received request data {0}... with invalid length {1}, disconnecting client {2}'
                                          .format(pending_data[:80], length, client_signature))

                        disconnect = True

                        break

                    if len(pending_data) < length:
                        break # wait for complete request

                    request_data = pending_data[:length]
                    pending_data = pending_data[length:]

                    if _get_sequence_number_from_data(request_data) == 0:
                        if self._debug:
                            _logger.error('Received request data {0} with zero sequence number, disconnecting client {1}'
                                          .format(request_data, client_signature))

                        disconnect = True

                        break

                    request = _Request(client_signature, self._get_next_trace(), request_data)

                    if self._debug:
                        _logger.debug('Received {0}'.format(request))

                    self._enqueue_request(request, response_queue)

            if response_task.done():
                response = response_task.result()
                response_task = None

                if not disconnect:
                    if self._debug:
                        _logger.debug('Sending {0} to client {1}'.format(response, client_signature))

                    writer.write(response.data)

                    try:
                        await writer.drain()
                    except asyncio.CancelledError:
                        break # ignore cancellation here to do proper cleanup

        self._response_queues.remove(response_queue)
        self._clients.remove(client)

        if request_task != None:
            await _cancel_task(request_task) # FIXME: what to do if awaiting cancellation gets cancelled?

        if response_task != None:
            await _cancel_task(response_task) # FIXME: what to do if awaiting cancellation gets cancelled?

        writer.close()

        try:
            await writer.wait_closed()
        except asyncio.CancelledError:
            raise # cancellation is okay here
        except Exception as e:
            if self._debug:
                _logger.error('Error while disconnecting client {0}: {1}'
                              .format(client_signature, _exception_to_str(e)))

    def start_running(self):
        if self._run_task != None:
            return

        self._run_task = asyncio.create_task(self._run(), name='BrickDaemon:run')

    async def stop_running(self):
        if self._run_task == None:
            return

        await _cancel_task(self._run_task) # FIXME: what to do if awaiting cancellation gets cancelled?

        self._run_task = None

    async def _run(self):
        server = await asyncio.start_server(lambda *client: self._client_addition_queue.put_nowait(client), self._host, self._port) # cancellation is okay here

        async with server:
            devices_task = asyncio.create_task(_run(self._devices.values, lambda device: device._run(), create_interrupt_coroutine=self._handle_device_change), name='BrickDaemon:run_devices')
            clients_task = asyncio.create_task(_run(lambda: self._clients, lambda client: self._handle_client(client), create_interrupt_coroutine=self._handle_client_addition), name='BrickDaemon:run_clients')

            try:
                # FIXME: use asyncio.gather instead here?
                await asyncio.wait({devices_task, clients_task}, return_when=asyncio.FIRST_COMPLETED)
            finally:
                await _cancel_task(clients_task) # FIXME: what to do if awaiting cancellation gets cancelled?
                await _cancel_task(devices_task) # FIXME: what to do if awaiting cancellation gets cancelled?

    async def run_forever(self):
        self.start_running()

        await self._run_task # cancellation is okay here

    async def __aenter__(self):
        return self

    async def __aexit__(self, _exc_type, _exc_value, _traceback):
        await self.stop_running() # cancellation is okay here

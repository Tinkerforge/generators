# -*- coding: utf-8 -*-
# Type stubs for MicroPython Tinkerforge IP Connection

from typing import Optional, Callable, Any, Sequence, Union

def get_uid_from_data(data: bytes) -> int: ...
def get_length_from_data(data: bytes) -> int: ...
def get_function_id_from_data(data: bytes) -> int: ...
def get_sequence_number_from_data(data: bytes) -> int: ...
def get_error_code_from_data(data: bytes) -> int: ...

def base58encode(value: int) -> str: ...
def base58decode(encoded: str) -> int: ...
def uid64_to_uid32(uid64: int) -> int: ...

def create_chunk_data(data: Sequence, chunk_offset: int, chunk_length: int, chunk_padding: Any) -> list: ...
def create_char(value: Union[str, bytes, bytearray, int]) -> str:
    """
    Tries to convert the given value to a single character string.
    """
    ...

def create_char_list(value: Union[list, str, bytes, bytearray], expected_type: str = 'char list') -> list[str]:
    """
    Tries to convert the given value to a list of single character strings.
    """
    ...

def create_string(value: Union[str, bytes, bytearray, list]) -> str:
    """
    Tries to convert the given value to a string.
    """
    ...

def pack_payload(data: tuple, form: str) -> bytes: ...
def unpack_payload(data: bytes, form: str) -> Any: ...

class Error(Exception):
    TIMEOUT: int
    NOT_ADDED: int
    ALREADY_CONNECTED: int
    NOT_CONNECTED: int
    INVALID_PARAMETER: int
    NOT_SUPPORTED: int
    UNKNOWN_ERROR_CODE: int
    STREAM_OUT_OF_SYNC: int
    INVALID_UID: int
    NON_ASCII_CHAR_IN_SECRET: int
    WRONG_DEVICE_TYPE: int
    DEVICE_REPLACED: int
    WRONG_RESPONSE_LENGTH: int

    value: int
    description: str

    def __init__(self, value: int, description: str) -> None: ...

class Device:
    DEVICE_IDENTIFIER_CHECK_PENDING: int
    DEVICE_IDENTIFIER_CHECK_MATCH: int
    DEVICE_IDENTIFIER_CHECK_MISMATCH: int

    RESPONSE_EXPECTED_INVALID_FUNCTION_ID: int
    RESPONSE_EXPECTED_ALWAYS_TRUE: int
    RESPONSE_EXPECTED_TRUE: int
    RESPONSE_EXPECTED_FALSE: int

    uid: int
    uid_string: str
    ipcon: 'IPConnection'
    device_identifier: int
    device_display_name: str
    api_version: tuple[int, int, int]
    registered_callbacks: dict
    callback_formats: dict
    high_level_callbacks: dict
    response_expected: list[int]

    def __init__(self, uid: str, ipcon: 'IPConnection', device_identifier: int, device_display_name: str) -> None: ...

    def get_api_version(self) -> tuple[int, int, int]:
        """
        Returns the API version (major, minor, revision) of the bindings for
        this device.
        """
        ...

    def get_response_expected(self, function_id: int) -> bool:
        """
        Returns the response expected flag for the function specified by the
        *function_id* parameter. It is *true* if the function is expected to
        send a response, *false* otherwise.
        """
        ...

    def set_response_expected(self, function_id: int, response_expected: bool) -> None:
        """
        Changes the response expected flag of the function specified by the
        *function_id* parameter. This flag can only be changed for setter
        (default value: *false*) and callback configuration functions
        (default value: *true*). For getter functions it is always enabled.
        """
        ...

    def set_response_expected_all(self, response_expected: bool) -> None:
        """
        Changes the response expected flag for all setter and callback
        configuration functions of this device at once.
        """
        ...

    def check_validity(self) -> None: ...

class IPConnection:
    FUNCTION_ENUMERATE: int
    FUNCTION_ADC_CALIBRATE: int
    FUNCTION_GET_ADC_CALIBRATION: int
    FUNCTION_READ_BRICKLET_UID: int
    FUNCTION_WRITE_BRICKLET_UID: int
    FUNCTION_DISCONNECT_PROBE: int

    CALLBACK_ENUMERATE: int
    CALLBACK_CONNECTED: int
    CALLBACK_DISCONNECTED: int

    BROADCAST_UID: int

    ENUMERATION_TYPE_AVAILABLE: int
    ENUMERATION_TYPE_CONNECTED: int
    ENUMERATION_TYPE_DISCONNECTED: int

    CONNECT_REASON_REQUEST: int

    DISCONNECT_REASON_REQUEST: int
    DISCONNECT_REASON_ERROR: int
    DISCONNECT_REASON_SHUTDOWN: int

    CONNECTION_STATE_DISCONNECTED: int
    CONNECTION_STATE_CONNECTED: int

    DISCONNECT_PROBE_INTERVAL: int

    host: Optional[str]
    port: Optional[int]
    timeout: float

    def __init__(self) -> None:
        """
        Creates an IP Connection object that can be used to enumerate the
        available devices. It is also required for the constructor of Bricks
        and Bricklets.
        """
        ...

    def connect(self, host: str, port: int) -> None:
        """
        Creates a TCP/IP connection to the given *host* and *port*. The host
        and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.

        Devices can only be controlled when the connection was established
        successfully.

        Blocks until the connection is established and throws an exception if
        there is no Brick Daemon or WIFI/Ethernet Extension listening at the
        given host and port.
        """
        ...

    def disconnect(self) -> None:
        """
        Disconnects the TCP/IP connection from the Brick Daemon or the
        WIFI/Ethernet Extension.
        """
        ...

    def authenticate(self, secret: str) -> None:
        """
        Performs an authentication handshake with the connected Brick Daemon or
        WIFI/Ethernet Extension.
        """
        ...

    def get_connection_state(self) -> int:
        """
        Can return the following states:

        - CONNECTION_STATE_DISCONNECTED: No connection is established.
        - CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
          the WIFI/Ethernet Extension is established.
        """
        ...

    def set_timeout(self, timeout: float) -> None:
        """
        Sets the timeout in seconds for getters and for setters for which the
        response expected flag is activated.

        Default timeout is 2.5.
        """
        ...

    def get_timeout(self) -> float:
        """
        Returns the timeout as set by set_timeout.
        """
        ...

    def enumerate(self) -> None:
        """
        Broadcasts an enumerate request. All devices will respond with an
        enumerate callback.
        """
        ...

    def register_callback(self, callback_id: int, function: Optional[Callable]) -> None:
        """
        Registers the given *function* with the given *callback_id*.
        """
        ...

    def dispatch_callbacks(self, seconds: float) -> None:
        """
        Dispatches incoming callbacks for the given amount of time in seconds
        (negative value means infinity). Because MicroPython doesn't support
        threads you need to call this method periodically to ensure that
        incoming callbacks are handled. If you don't use callbacks you don't
        need to call this method.

        The recommended dispatch time is 0. This will just dispatch all pending
        callbacks without waiting for further callbacks.
        """
        ...

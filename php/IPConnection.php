<?php

/*
 * Copyright (c) 2012-2017, 2019-2020 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

namespace Tinkerforge;


if (!extension_loaded('bcmath')) {
    throw new \Exception('Required bcmath extension is not available');
}


require_once(__DIR__ . '/DeviceDisplayNames.php');


class Base58
{
    private static $alphabet = '123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ';

    /**
     * Encode string from Base10 to Base58.
     *
     * \param $value Base10 encoded string
     * \returns Base58 encoded string
     */
    public static function encode($value)
    {
        if (bccomp($value, 0) < 0) {
            throw new \InvalidArgumentException('Cannot encode negative value');
        }

        $encoded = '';

        while (bccomp($value, '58') >= 0) {
            $div = bcdiv($value, '58');
            $mod = bcmod($value, '58');
            $encoded = self::$alphabet[intval($mod)] . $encoded;
            $value = $div;
        }

        return self::$alphabet[intval($value)] . $encoded;
    }

    /**
     * Decode string from Base58 to Base10.
     *
     * \param $encoded Base58 encoded string
     * \returns Base10 encoded string
     */
    public static function decode($encoded)
    {
        $length = strlen($encoded);
        $value = '0';
        $base = '1';

        for ($i = $length - 1; $i >= 0; $i--) {
            $index = strpos(self::$alphabet, $encoded[$i]);

            if ($index === FALSE) {
                throw new \InvalidArgumentException('UID "' . $encoded . '" contains invalid character');
            }

            $index = strval($index);
            $value = bcadd($value, bcmul($index, $base));
            $base = bcmul($base, '58');
        }

        return $value;
    }
}


class Base256
{
    /**
     * Encode from Base10 string to Base256 array.
     *
     * \param $value Base10 encoded string
     * \returns array of bytes (little endian)
     */
    public static function encode($value, $length)
    {
        if (bccomp($value, 0) < 0) {
            throw new \InvalidArgumentException('Cannot encode negative value');
        }

        $bytes = array();

        while (bccomp($value, '256') >= 0) {
            $div = bcdiv($value, '256');
            $mod = bcmod($value, '256');
            array_push($bytes, intval($mod));
            $value = $div;
        }

        array_push($bytes, intval($value));

        return array_pad($bytes, $length, 0);
    }

    public static function encodeAndPack($value, $length)
    {
        $bytes = self::encode($value, $length);
        $packed = '';

        foreach ($bytes as $byte) {
            $packed .= pack('C', $byte);
        }

        return $packed;
    }

    public static function encodeAndPackInt64($value)
    {
        if (bccomp($value, 0) < 0) {
            $value = bcadd($value, '18446744073709551616');
        }

        return self::encodeAndPack($value, 8);
    }

    public static function encodeAndPackUInt64($value)
    {
        return self::encodeAndPack($value, 8);
    }

    /**
     * Decode from Base256 array to Base10 string.
     *
     * \param $bytes array of bytes (little endian)
     * \returns Base10 encoded string
     */
    public static function decode($bytes)
    {
        $value = '0';
        $base = '1';

        foreach ($bytes as $byte) {
            $value = bcadd($value, bcmul(strval($byte), $base));
            $base = bcmul($base, '256');
        }

        return $value;
    }
}


class TinkerforgeException extends \Exception
{

}


class TimeoutException extends TinkerforgeException
{

}


class AlreadyConnectedException extends TinkerforgeException
{

}


class NotConnectedException extends TinkerforgeException
{

}


class InvalidParameterException extends TinkerforgeException
{

}


class NotSupportedException extends TinkerforgeException
{

}


class UnknownErrorCodeException extends TinkerforgeException
{

}


class StreamOutOfSyncException extends TinkerforgeException
{

}


class WrongDeviceTypeException extends TinkerforgeException
{

}


class DeviceReplacedException extends TinkerforgeException
{

}


class WrongResponseLengthException extends TinkerforgeException
{

}


abstract class Device
{
    /**
     * @internal
     */
    const DEVICE_IDENTIFIER_CHECK_PENDING = 0;
    const DEVICE_IDENTIFIER_CHECK_MATCH = 1;
    const DEVICE_IDENTIFIER_CHECK_MISMATCH = 2;

    /**
     * @internal
     */
    const RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0;
    const RESPONSE_EXPECTED_ALWAYS_TRUE = 1; // getter
    const RESPONSE_EXPECTED_TRUE = 2; // setter
    const RESPONSE_EXPECTED_FALSE = 3; // setter, default

    /**
     * @internal
     */
    public $replaced = FALSE;

    public $uid = '0'; # Base10
    public $uid_string = ''; # Base58
    public $api_version = array(0, 0, 0);

    public $ipcon = NULL;

    public $device_identifier;
    public $device_display_name;
    public $device_identifier_check = self::DEVICE_IDENTIFIER_CHECK_PENDING;
    public $wrong_device_display_name = '?';

    public $response_expected = array();

    public $expected_response_function_id = 0;
    public $expected_response_sequence_number = 0;
    public $received_response = NULL;

    public $registered_callbacks = array();
    public $registered_callback_user_data = array();
    public $callback_wrappers = array();
    public $high_level_callbacks = array();
    public $pending_callbacks = array();

    /**
     * @internal
     */
    public function __construct($uid, $ipcon, $device_identifier, $device_display_name)
    {
        $this->uid_string = $uid;
        $this->device_identifier = $device_identifier;
        $this->device_display_name = $device_display_name;

        $long_uid = Base58::decode($uid);

        if (bccomp($long_uid, '18446744073709551615' /* 0xFFFFFFFFFFFFFFFF */) > 0) {
            throw new \InvalidArgumentException('UID "' . $uid . '" is to big');
        }

        if (bccomp($long_uid, '4294967295' /* 0xFFFFFFFF */) > 0) {
            // Convert from 64bit to 32bit
            $value1a = (int)bcmod($long_uid, '65536' /* 0x10000 */);
            $value1b = (int)bcmod(bcdiv($long_uid, '65536' /* 0x10000 */), '65536' /* 0x10000 */);
            $value2a = (int)bcmod(bcdiv($long_uid, '4294967296' /* 0x100000000 */), '65536' /* 0x10000 */);
            $value2b = (int)bcmod(bcdiv($long_uid, '281474976710656' /* 0x10000000000 */), '65536' /* 0x10000 */);

            $short_uid1  =  $value1a & 0x0FFF;
            $short_uid1 |= ($value1b & 0x0F00) << 4;

            $short_uid2  =  $value2a & 0x003F;
            $short_uid2 |= ($value2b & 0x000F) << 6;
            $short_uid2 |= ($value2b & 0x3F00) << 2;

            $this->uid = bcadd(bcmul($short_uid2, '65536' /* 0x10000 */), $short_uid1);
        } else {
            $this->uid = $long_uid;
        }

        if (bccomp($this->uid, '0') == 0) {
            throw new \InvalidArgumentException('UID "' . $uid . '" is empty or maps to zero');
        }

        $this->ipcon = $ipcon;

        for ($i = 0; $i < 256; ++$i) {
            $this->response_expected[$i] = self::RESPONSE_EXPECTED_INVALID_FUNCTION_ID;
        }
    }

    /**
     * Returns the API version (major, minor, revision) of the bindings for
     * this device.
     *
     * @return array
     */
    public function getAPIVersion()
    {
        return $this->api_version;
    }

    /**
     * Returns the response expected flag for the function specified by the
     * $function_id parameter. It is *true* if the function is expected to
     * send a response, *false* otherwise.
     *
     * For getter functions this is enabled by default and cannot be disabled,
     * because those functions will always send a response. For callback
     * configuration functions it is enabled by default too, but can be
     * disabled via the setResponseExpected function. For setter functions it
     * is disabled by default and can be enabled.
     *
     * Enabling the response expected flag for a setter function allows to
     * detect timeouts and other error conditions calls of this setter as well.
     * The device will then send a response for this purpose. If this flag is
     * disabled for a setter function then no response is sent and errors are
     * silently ignored, because they cannot be detected.
     *
     * @param int $function_id
     *
     * @return boolean
     */
    public function getResponseExpected($function_id)
    {
        if ($function_id < 0 || $function_id > 255) {
            throw new \InvalidArgumentException("Function ID $function_id out of range");
        }

        $flag = $this->response_expected[$function_id];

        if ($flag === self::RESPONSE_EXPECTED_INVALID_FUNCTION_ID) {
            throw new \InvalidArgumentException("Invalid function ID $function_id");
        }

        if ($flag === self::RESPONSE_EXPECTED_ALWAYS_TRUE ||
            $flag === self::RESPONSE_EXPECTED_TRUE) {
            return TRUE;
        } else {
            return FALSE;
        }
    }

    /**
     * Changes the response expected flag of the function specified by the
     * $function_id parameter. This flag can only be changed for setter
     * (default value: *false*) and callback configuration functions
     * (default value: *true*). For getter functions it is always enabled.
     *
     * Enabling the response expected flag for a setter function allows to
     * detect timeouts and other error conditions calls of this setter as
     * well. The device will then send a response for this purpose. If this
     * flag is disabled for a setter function then no response is sent and
     * errors are silently ignored, because they cannot be detected.
     *
     * @param int $function_id
     * @param boolean $response_expected
     *
     * @return void
     */
    public function setResponseExpected($function_id, $response_expected)
    {
        if ($function_id < 0 || $function_id > 255) {
            throw new \InvalidArgumentException("Function ID $function_id out of range");
        }

        $flag = $this->response_expected[$function_id];

        if ($flag === self::RESPONSE_EXPECTED_INVALID_FUNCTION_ID) {
            throw new \InvalidArgumentException("Invalid function ID $function_id");
        }

        if ($flag === self::RESPONSE_EXPECTED_ALWAYS_TRUE) {
            throw new \InvalidArgumentException("Response Expected flag cannot be changed for function ID $function_id");
        }

        $this->response_expected[$function_id] =
            $response_expected ? self::RESPONSE_EXPECTED_TRUE
                               : self::RESPONSE_EXPECTED_FALSE;
    }

    /**
     * Changes the response expected flag for all setter and callback
     * configuration functions of this device at once.
     *
     * @param boolean $response_expected
     *
     * @return void
     */
    public function setResponseExpectedAll($response_expected)
    {
        $flag = $response_expected ? self::RESPONSE_EXPECTED_TRUE
                                   : self::RESPONSE_EXPECTED_FALSE;

        for ($i = 0; $i < 256; ++$i) {
            if ($this->response_expected[$i] === self::RESPONSE_EXPECTED_TRUE ||
                $this->response_expected[$i] === self::RESPONSE_EXPECTED_FALSE) {
                $this->response_expected[$i] = $flag;
            }
        }
    }

    /**
     * @internal
     */
    public function dispatchPendingCallbacks()
    {
        $pending_callbacks = $this->pending_callbacks;
        $this->pending_callbacks = array();

        foreach ($pending_callbacks as $pending_callback) {
            if ($this->ipcon->socket === FALSE) {
                break;
            }

            try {
                $this->checkValidity();
            } catch (TinkerforgeException $e) {
                continue; // silently ignoring callbacks from mismatching devices
            }

            $this->handleCallback($pending_callback[0], $pending_callback[1]);
        }
    }

    /**
     * @internal
     */
    protected function sendRequest($function_id, $payload, $expected_response_length)
    {
        if ($this->ipcon->socket === FALSE) {
            throw new NotConnectedException('Not connected');
        }

        $header = $this->ipcon->createPacketHeader($this, 8 + strlen($payload), $function_id);
        $request = $header[0] . $payload;
        $sequence_number = $header[1];
        $response_expected = $header[2];

        if ($response_expected) {
            $this->expected_response_function_id = $function_id;
            $this->expected_response_sequence_number = $sequence_number;
            $this->received_response = NULL;
        }

        $this->ipcon->send($request);

        if ($response_expected) {
            $this->ipcon->receive($this->ipcon->timeout, $this, FALSE /* FIXME: this can delay callback up to the current timeout */);

            $this->expected_response_function_id = 0;
            $this->expected_response_sequence_number = 0;

            if ($this->received_response === NULL) {
                throw new TimeoutException("Did not receive response in time for function ID $function_id");
            }

            $response = $this->received_response;
            $this->received_response = NULL;

            $error_code = ($response[0]['error_code_and_future_use'] >> 6) & 0x03;

            if ($error_code === 0) {
                if ($expected_response_length === 0) {
                    // Setter with response-expected enabled
                    $expected_response_length = 8;
                }

                $actual_response_length = 8 + strlen($response[1]);

                if ($actual_response_length !== $expected_response_length) {
                    throw new WrongResponseLengthException("Expected response of $expected_response_length byte for function ID $function_id, got $actual_response_length byte instead");
                }
            } else if ($error_code === 1) {
                throw new InvalidParameterException("Got invalid parameter for function ID $function_id");
            } else if ($error_code === 2) {
                throw new NotSupportedException("Function ID $function_id is not supported");
            } else {
                throw new UnknownErrorCodeException("Function ID $function_id returned an unknown error");
            }

            $payload = $response[1];
        } else {
            $payload = NULL;
        }

        return $payload;
    }

    /**
     * @internal
     */
    protected function createChunkData($data, $chunk_offset, $chunk_length, $chunk_padding)
    {
        $chunk_data = array_slice($data, $chunk_offset, $chunk_length);

        if (count($chunk_data) < $chunk_length) {
            $chunk_data = array_pad($chunk_data, $chunk_length, $chunk_padding);
        }

        return $chunk_data;
    }

    /**
     * @internal
     */
    protected function checkValidity()
    {
        if ($this->replaced) {
            throw new DeviceReplacedException('Device has been replaced');
        }

        if ($this->device_identifier_check === self::DEVICE_IDENTIFIER_CHECK_MATCH) {
            return;
        }

        if ($this->device_identifier_check === self::DEVICE_IDENTIFIER_CHECK_PENDING) {
            $payload = $this->sendRequest(255, '', 33); # getIdentity
            $response = unpack('c8uid/c8connected_uid/c1position/C3hardware_version/C3firmware_version/v1device_identifier', $payload);
            $device_identifier = $response['device_identifier'];

            if ($device_identifier === $this->device_identifier) {
                $this->device_identifier_check = self::DEVICE_IDENTIFIER_CHECK_MATCH;
            } else {
                $this->device_identifier_check = self::DEVICE_IDENTIFIER_CHECK_MISMATCH;
                $this->wrong_device_display_name = getDeviceDisplayName($device_identifier);
            }
        }

        if ($this->device_identifier_check === self::DEVICE_IDENTIFIER_CHECK_MISMATCH) {
            throw new WrongDeviceTypeException('UID ' . $this->uid_string . ' belongs to a ' . $this->wrong_device_display_name .
                                               ' instead of the expected ' . $this->device_display_name);
        }
    }
}


/**
 * @internal
 */
class BrickDaemon extends Device
{
    const FUNCTION_GET_AUTHENTICATION_NONCE = 1;
    const FUNCTION_AUTHENTICATE = 2;

    public function __construct($uid, $ipcon)
    {
        parent::__construct($uid, $ipcon, 0, 'Brick Daemon');

        $this->api_version = array(2, 0, 0);

        $this->response_expected[self::FUNCTION_GET_AUTHENTICATION_NONCE] = self::RESPONSE_EXPECTED_ALWAYS_TRUE;
        $this->response_expected[self::FUNCTION_AUTHENTICATE] = self::RESPONSE_EXPECTED_TRUE;

        $ipcon->addDevice($this);
    }

    public function getAuthenticationNonce()
    {
        $payload = '';

        $data = $this->sendRequest(self::FUNCTION_GET_AUTHENTICATION_NONCE, $payload, 12);

        $payload = unpack('C4nonce', $data);

        return IPConnection::collectUnpackedArray($payload, 'nonce', 4);
    }

    public function authenticate($client_nonce, $digest)
    {
        $payload = '';

        for ($i = 0; $i < 4; $i++) {
            $payload .= pack('C', $client_nonce[$i]);
        }

        for ($i = 0; $i < 20; $i++) {
            $payload .= pack('C', $digest[$i]);
        }

        $this->sendRequest(self::FUNCTION_AUTHENTICATE, $payload, 0);
    }
}


/**
 * @internal
 */
abstract class Socket
{
    const RECEIVE_ERROR = 1;
    const RECEIVE_SHUTDOWN = 2;
    const RECEIVE_TIMEOUT = 3;
    const RECEIVE_DATA = 4;
}


/**
 * @internal
 */
class ExtensionSocket extends Socket
{
    private $handle = FALSE;

    function __construct($address, $port)
    {
        $this->handle = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

        if ($this->handle === FALSE) {
            throw new \Exception('Could not create socket: ' .
                                 socket_strerror(socket_last_error()));
        }

        @socket_set_option($this->handle, SOL_TCP, TCP_NODELAY, 1);

        if (!@socket_connect($this->handle, $address, $port)) {
            $error = socket_strerror(socket_last_error($this->handle));

            socket_close($this->handle);
            $this->handle = FALSE;

            throw new \Exception("Could not connect socket: $error");
        }
    }

    function __destruct()
    {
        if ($this->handle !== FALSE) {
            $this->shutdown();
            $this->close();
        }
    }

    function shutdown()
    {
        @socket_shutdown($this->handle, 2);
    }

    function close()
    {
        @socket_close($this->handle);
        $this->handle = FALSE;
    }

    function send($data, $length)
    {
        return @socket_send($this->handle, $data, $length, 0);
    }

    function receive(&$data, &$length, $timeout)
    {
        $read = array($this->handle);
        $write = NULL;
        $except = array($this->handle);
        $timeout_sec = floor($timeout);
        $timeout_usec = ceil(($timeout - $timeout_sec) * 1000000);
        $changed = @socket_select($read, $write, $except, $timeout_sec, $timeout_usec);

        if ($changed === FALSE) {
            throw new \Exception('Could not receive response: ' .
                                 socket_strerror(socket_last_error($this->handle)));
        }

        if ($changed === 0) {
            return self::RECEIVE_TIMEOUT;
        }

        if (in_array($this->handle, $except)) {
            return self::RECEIVE_ERROR;
        }

        $result = @socket_recv($this->handle, $data, $length, 0);

        if ($result === FALSE || $result === 0) {
            if ($result === FALSE) {
                return self::RECEIVE_ERROR;
            } else {
                return self::RECEIVE_SHUTDOWN;
            }
        }

        $length = $result;

        return self::RECEIVE_DATA;
    }
}


/**
 * @internal
 */
class StreamSocket extends Socket
{
    private $handle = FALSE;

    function __construct($address, $port)
    {
        // FIXME: stream sockets don't support TCP_NODELAY, see https://bugs.php.net/bug.php?id=51879
        $this->handle = stream_socket_client("tcp://$address:$port", $errno, $message);

        if ($this->handle === FALSE) {
            throw new \Exception("Could not connect socket: $message");
        }
    }

    function __destruct()
    {
        if ($this->handle !== FALSE) {
            $this->shutdown();
            $this->close();
        }
    }

    function shutdown()
    {
        stream_socket_shutdown($this->handle, STREAM_SHUT_RDWR);
    }

    function close()
    {
        fclose($this->handle);
        $this->handle = FALSE;
    }

    function send($data, $length)
    {
        return fwrite($this->handle, $data, $length);
    }

    function receive(&$data, &$length, $timeout)
    {
        $read = array($this->handle);
        $write = NULL;
        $except = array($this->handle);
        $timeout_sec = floor($timeout);
        $timeout_usec = ceil(($timeout - $timeout_sec) * 1000000);
        $changed = @stream_select($read, $write, $except, $timeout_sec, $timeout_usec);

        if ($changed === FALSE) {
            throw new \Exception('Could not receive response: ' .
                                 socket_strerror(socket_last_error($this->handle)));
        }

        if ($changed === 0) {
            return self::RECEIVE_TIMEOUT;
        }

        if (in_array($this->handle, $except)) {
            return self::RECEIVE_ERROR;
        }

        $data = fread($this->handle, $length);

        if ($data === FALSE) {
            return self::RECEIVE_ERROR;
        }

        $length = strlen($data);

        if ($length === 0) {
            return self::RECEIVE_SHUTDOWN;
        }

        return self::RECEIVE_DATA;
    }
}


class IPConnection
{
    const DISCONNECT_PROBE_INTERVAL = 5.0;

    const FUNCTION_DISCONNECT_PROBE = 128;
    const FUNCTION_ENUMERATE = 254;

    // IDs for registerCallback
    const CALLBACK_ENUMERATE = 253;
    const CALLBACK_CONNECTED = 0;
    const CALLBACK_DISCONNECTED = 1;

    // enumerationType parameter of CALLBACK_ENUMERATE
    const ENUMERATION_TYPE_AVAILABLE = 0;
    const ENUMERATION_TYPE_CONNECTED = 1;
    const ENUMERATION_TYPE_DISCONNECTED = 2;

    // connectReason parameter of CALLBACK_CONNECTED
    const CONNECT_REASON_REQUEST = 0;

    // disconnectReason parameter of CALLBACK_DISCONNECTED
    const DISCONNECT_REASON_REQUEST = 0;
    const DISCONNECT_REASON_ERROR = 1;
    const DISCONNECT_REASON_SHUTDOWN = 2;

    // returned by getConnectionState
    const CONNECTION_STATE_DISCONNECTED = 0;
    const CONNECTION_STATE_CONNECTED = 1;

    public $timeout = 2.5; // seconds

    private $next_sequence_number = 0;
    private $next_authentication_nonce = 0;

    public $devices = array();

    private $registered_callbacks = array();
    private $registered_callback_user_data = array();
    private $pending_callbacks = array();

    private $host = "";
    private $port = 0;

    public $socket = FALSE;
    private $pending_data = '';

    private $disconnect_probe_request = '';
    private $next_disconnect_probe = 0.0;

    private $brickd = NULL;

    /**
     * Creates an IP Connection object that can be used to enumerate the available
     * devices. It is also required for the constructor of Bricks and Bricklets.
     */
    public function __construct()
    {
        $result = $this->createPacketHeader(NULL, 8, self::FUNCTION_DISCONNECT_PROBE);
        $this->disconnect_probe_request = $result[0];
        $this->next_disconnect_probe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;

        $this->brickd = new BrickDaemon('2', $this);
    }

    function __destruct()
    {
        if ($this->socket !== FALSE) {
            $this->disconnect();
        }
    }

    /**
     * Creates a TCP/IP connection to the given $host and $port. The host
     * and port can point to a Brick Daemon or to a WIFI/Ethernet Extension.
     *
     * Devices can only be controlled when the connection was established
     * successfully.
     *
     * Blocks until the connection is established and throws an exception if
     * there is no Brick Daemon or WIFI/Ethernet Extension listening at the
     * given host and port.
     *
     * @param string $host
     * @param int $port
     *
     * @return void
     */
    public function connect($host, $port)
    {
        if ($this->socket !== FALSE) {
            $hp = $this->host . ':' . $this->port;
            throw new AlreadyConnectedException("Already connected to $hp");
        }

        $this->host = $host;
        $this->port = $port;

        $address = '';

        if (preg_match('/^\d+\.\d+\.\d+\.\d+$/', $host) === 0) {
            $address = gethostbyname($host);

            if ($address === $host) {
                throw new \Exception('Could not resolve hostname');
            }
        } else {
            $address = $host;
        }

        if (extension_loaded('sockets')) {
            $this->socket = new ExtensionSocket($address, $port);
        } else {
            $this->socket = new StreamSocket($address, $port);
        }

        if (array_key_exists(self::CALLBACK_CONNECTED, $this->registered_callbacks)) {
            call_user_func_array($this->registered_callbacks[self::CALLBACK_CONNECTED],
                                 array(self::CONNECT_REASON_REQUEST,
                                       $this->registered_callback_user_data[self::CALLBACK_CONNECTED]));
        }

        $this->next_disconnect_probe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;
    }

    /**
     * Disconnects the TCP/IP connection from the Brick Daemon or the
     * WIFI/Ethernet Extension.
     *
     * @return void
     */
    public function disconnect()
    {
        if ($this->socket === FALSE) {
            throw new NotConnectedException('Not connected');
        }

        $this->socket->shutdown();

        $this->disconnectInternal(self::DISCONNECT_REASON_REQUEST);

        $this->pending_data = '';
    }

    /**
     * Performs an authentication handshake with the connected Brick Daemon or
     * WIFI/Ethernet Extension. If the handshake succeeds the connection switches
     * from non-authenticated to authenticated state and communication can
     * continue as normal. If the handshake fails then the connection gets closed.
     * Authentication can fail if the wrong secret was used or if authentication
     * is not enabled at all on the Brick Daemon or the WIFI/Ethernet Extension.
     *
     * For more information about authentication see
     * https://www.tinkerforge.com/en/doc/Tutorials/Tutorial_Authentication/Tutorial.html
     *
     * @param string $secret
     *
     * @return void
     */
    public function authenticate($secret)
    {
        if (!mb_check_encoding($secret, 'ASCII')) {
            throw new \Exception("Authentication secret contains non-ASCII characters");
        }

        if ($this->next_authentication_nonce === 0) {
            $this->next_authentication_nonce = self::getRandomUInt32();
        }

        $server_nonce = $this->brickd->getAuthenticationNonce();
        $server_nonce_bytes = pack('C4', $server_nonce[0], $server_nonce[1], $server_nonce[2], $server_nonce[3]);

        $client_nonce_number = $this->next_authentication_nonce;
        $this->next_authentication_nonce = bcadd($this->next_authentication_nonce, '1');

        // cannot use pack() here because $client_nonce_number might be a number in a string
        $client_nonce = array((int)bcmod(      $client_nonce_number,              '256'),
                              (int)bcmod(bcdiv($client_nonce_number,      '256'), '256'),
                              (int)bcmod(bcdiv($client_nonce_number,    '65536'), '256'),
                              (int)bcmod(bcdiv($client_nonce_number, '16777216'), '256'));
        $client_nonce_bytes = pack('C4', $client_nonce[0], $client_nonce[1], $client_nonce[2], $client_nonce[3]);

        $digest_bytes = hash_hmac('sha1', $server_nonce_bytes . $client_nonce_bytes, $secret, true);

        if ($digest_bytes === FALSE) {
            throw new \Exception('HMAC-SHA1 not avialable');
        }

        $digest = self::collectUnpackedArray(unpack('C20digest', $digest_bytes), 'digest', 20);

        $this->brickd->authenticate($client_nonce, $digest);
    }

    /**
     * Can return the following states:
     *
     * - CONNECTION_STATE_DISCONNECTED: No connection is established.
     * - CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
     *   the WIFI/Ethernet Extension is established.
     * - CONNECTION_STATE_PENDING: IP Connection is currently trying to
     *   connect.
     *
     * @return int
     */
    public function getConnectionState()
    {
        if ($this->socket !== FALSE) {
            return self::CONNECTION_STATE_CONNECTED;
        } else {
            return self::CONNECTION_STATE_DISCONNECTED;
        }
    }

    /**
     * Sets the timeout in seconds for getters and for setters for which the
     * response expected flag is activated.
     *
     * Default timeout is 2.5.
     *
     * @param float $seconds
     *
     * @return void
     */
    public function setTimeout($seconds)
    {
        if ($seconds < 0) {
            throw new \Exception('Timeout cannot be negative');
        }

        $this->timeout = $seconds;
    }

    /**
     * Returns the timeout as set by setTimeout.
     *
     * @return float
     */
    public function getTimeout()
    {
        return $this->timeout;
    }

    /**
     * Broadcasts an enumerate request. All devices will respond with an
     * enumerate callback.
     *
     * @return void
     */
    public function enumerate()
    {
        $result = $this->createPacketHeader(NULL, 8, self::FUNCTION_ENUMERATE);
        $request = $result[0];

        $this->send($request);
    }

    /**
     * Dispatches incoming callbacks for the given amount of time in seconds
     * (negative value means infinity). Because PHP doesn't support threads
     * you need to call this method periodically to ensure that incoming
     * callbacks are handled. If you don't use callbacks you don't need to
     * call this method.
     *
     * The recommended dispatch time 0. This will just dispatch all pending
     * callbacks without waiting for further callbacks.
     *
     * @param float $seconds
     *
     * @return void
     */
    public function dispatchCallbacks($seconds)
    {
        // Dispatch all pending callbacks
        $this->dispatchPendingCallbacks();

        if ($seconds < 0) {
            while (TRUE) {
                $this->receive($this->timeout, NULL, TRUE);

                // Dispatch all pending callbacks that were received by
                // getters in the meantime
                $this->dispatchPendingCallbacks();
            }
        } else {
            $this->receive($seconds, NULL, TRUE);
        }
    }

    /**
     * Registers the given $function with the given $callback_id. The optional
     * $user_data will be passed as the last parameter to the $function.
     *
     * @param int $callback_id
     * @param callable $function
     * @param mixed $user_data
     *
     * @return void
     */
    public function registerCallback($callback_id, $function, $user_data = NULL)
    {
        if (!is_callable($function)) {
            throw new \Exception('Function is not callable');
        }

        $this->registered_callbacks[$callback_id] = $function;
        $this->registered_callback_user_data[$callback_id] = $user_data;
    }

    /**
     * @internal
     */
    public function addDevice($device)
    {
        if (isset($this->devices[$device->uid])) {
            $this->devices[$device->uid]->replaced = TRUE;
        }

        $this->devices[$device->uid] = $device; // FIXME: use a weakref here
    }

    /**
     * @internal
     */
    public function createPacketHeader($device, $length, $function_id)
    {
        $uid = '0';
        $sequence_number = $this->next_sequence_number + 1;
        $this->next_sequence_number = $sequence_number % 15;
        $response_expected = 0;

        if ($device !== NULL) {
            $uid = $device->uid;

            if ($device->getResponseExpected($function_id)) {
                $response_expected = 1;
            }
        }

        $sequence_number_and_options = ($sequence_number << 4) | ($response_expected << 3);
        $header = Base256::encodeAndPack($uid, 4) . pack('CCCC', $length, $function_id, $sequence_number_and_options, 0);

        return array($header, $sequence_number, $response_expected);
    }

    /**
     * @internal
     */
    public function send($request)
    {
        if ($this->socket->send($request, strlen($request)) === FALSE) {
            $this->disconnectInternal(self::DISCONNECT_REASON_ERROR);

            throw new NotConnectedException('Could not send request: ' .
                                            socket_strerror(socket_last_error($this->socket)));
        }

        $this->next_disconnect_probe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;
    }

    /**
     * @internal
     */
    public function receive($seconds, $device, $direct_callback_dispatch)
    {
        if ($seconds < 0) {
            $seconds = 0;
        }

        $start = microtime(true);
        $end = $start + $seconds;

        do {
            if ($this->socket === FALSE) {
                return;
            }

            $now = microtime(true);

            // FIXME: this works for timeout < DISCONNECT_PROBE_INTERVAL only
            if ($this->next_disconnect_probe < $now ||
                ($this->next_disconnect_probe - $now) > self::DISCONNECT_PROBE_INTERVAL) {
                if ($this->socket->send($this->disconnect_probe_request,
                                        strlen($this->disconnect_probe_request)) === FALSE) {
                    $this->disconnectInternal(self::DISCONNECT_REASON_ERROR);
                    return;
                }

                $now = microtime(true);
                $this->next_disconnect_probe = $now + self::DISCONNECT_PROBE_INTERVAL;
            }

            $timeout = $end - $now;

            if ($timeout < 0) {
                $timeout = 0;
            }

            $data = '';
            $length = 8192;
            $result = $this->socket->receive($data, $length, $timeout);

            if ($result == Socket::RECEIVE_ERROR) {
                $this->disconnectInternal(self::DISCONNECT_REASON_ERROR);
                return;
            } else if ($result == Socket::RECEIVE_SHUTDOWN) {
                $this->disconnectInternal(self::DISCONNECT_REASON_SHUTDOWN);
                return;
            } else if ($result == Socket::RECEIVE_TIMEOUT) {
                // Do nothing
            } else if ($result == Socket::RECEIVE_DATA) {
                $before = microtime(true);

                $this->pending_data .= $data;

                while (TRUE) {
                    if (strlen($this->pending_data) < 8) {
                        // Wait for complete header
                        break;
                    }

                    $tmp = unpack('C', substr($this->pending_data, 4));
                    $length = $tmp[1];

                    if (strlen($this->pending_data) < $length) {
                        // Wait for complete packet
                        break;
                    }

                    $packet = substr($this->pending_data, 0, $length);
                    $this->pending_data = substr($this->pending_data, $length);

                    $this->handleResponse($packet, $direct_callback_dispatch);
                }

                $after = microtime(true);

                if ($after > $before) {
                    $end += $after - $before;
                }

                if ($device !== NULL && $device->received_response !== NULL) {
                    break;
                }
            }

            $now = microtime(true);
        } while ($now >= $start && $now < $end);
    }

    /**
     * @internal
     */
    private function disconnectInternal($disconnect_reason)
    {
        $this->socket->close();
        $this->socket = FALSE;

        if (array_key_exists(self::CALLBACK_DISCONNECTED, $this->registered_callbacks)) {
            call_user_func_array($this->registered_callbacks[self::CALLBACK_DISCONNECTED],
                                 array($disconnect_reason,
                                       $this->registered_callback_user_data[self::CALLBACK_DISCONNECTED]));
        }
    }

    /**
     * @internal
     */
    private function handleResponse($packet, $direct_callback_dispatch)
    {
        $uid = Base256::decode(self::collectUnpackedArray(unpack('C4uid', $packet), 'uid', 4));
        $header = unpack('Clength/Cfunction_id/Csequence_number_and_options/Cerror_code_and_future_use', substr($packet, 4));
        $header['uid'] = $uid;
        $function_id = $header['function_id'];
        $sequence_number = ($header['sequence_number_and_options'] >> 4) & 0x0F;
        $payload = substr($packet, 8);

        $this->next_disconnect_probe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;

        if ($sequence_number === 0 && $function_id === self::CALLBACK_ENUMERATE) {
            if (array_key_exists(self::CALLBACK_ENUMERATE, $this->registered_callbacks)) {
                if ($direct_callback_dispatch) {
                    if ($this->socket === FALSE) {
                        return;
                    }

                    $this->handleEnumerate($header, $payload);
                } else {
                    array_push($this->pending_callbacks, array($header, $payload));
                }
            }

            return;
        }

        if (!array_key_exists($uid, $this->devices)) {
            // Response from an unknown device, ignoring it
            return;
        }

        $device = $this->devices[$uid];

        if ($sequence_number === 0) {
            if (array_key_exists($function_id, $device->registered_callbacks) ||
                array_key_exists(-$function_id, $device->high_level_callbacks)) {
                if ($direct_callback_dispatch) {
                    if ($this->socket === FALSE) {
                        return;
                    }

                    $device->handleCallback($header, $payload);
                } else {
                    array_push($device->pending_callbacks, array($header, $payload));
                }
            }

            return;
        }

        if ($device->expected_response_function_id === $function_id &&
            $device->expected_response_sequence_number === $sequence_number) {
            $device->received_response = array($header, $payload);
            return;
        }

        // Response seems to be OK, but can't be handled
    }

    /**
     * @internal
     */
    private function handleEnumerate($header, $payload)
    {
        if (!array_key_exists(self::CALLBACK_ENUMERATE, $this->registered_callbacks)) {
            return;
        }

        if (8 + strlen($payload) !== 34) {
            return; // Silently ignoring callback with wrong length
        }

        $payload = unpack('c8uid/c8connected_uid/cposition/C3hardware_version/C3firmware_version/vdevice_identifier/Cenumeration_type', $payload);

        $uid = self::implodeUnpackedString($payload, 'uid', 8);
        $connected_uid = self::implodeUnpackedString($payload, 'connected_uid', 8);
        $position = chr($payload['position']);
        $hardware_version = self::collectUnpackedArray($payload, 'hardware_version', 3);
        $firmware_version = self::collectUnpackedArray($payload, 'firmware_version', 3);
        $device_identifier = $payload['device_identifier'];
        $enumeration_type = $payload['enumeration_type'];

        call_user_func_array($this->registered_callbacks[self::CALLBACK_ENUMERATE],
                             array($uid, $connected_uid, $position, $hardware_version,
                                   $firmware_version, $device_identifier, $enumeration_type,
                                   $this->registered_callback_user_data[self::CALLBACK_ENUMERATE]));
    }

    /**
     * @internal
     */
    private function dispatchPendingCallbacks()
    {
        $pending_callbacks = $this->pending_callbacks;
        $this->pending_callbacks = array();

        foreach ($pending_callbacks as $pending_callback) {
            if ($this->socket === FALSE) {
                break;
            }

            if ($pending_callback[0]['function_id'] === self::CALLBACK_ENUMERATE) {
                $this->handleEnumerate($pending_callback[0], $pending_callback[1]);
            }
        }

        foreach ($this->devices as $device) {
            $device->dispatchPendingCallbacks();
        }
    }

    /**
     * @internal
     */
    static public function fixUnpackedInt16($payload, $field)
    {
        $value = $payload[$field];

        // int16 is unpacked as uint16, but PHP stores it in an int32 or int64
        // which makes actually negtive values show up as positive values.
        // detect if this has happend and fix it
        if ($value >= 32768) {
            $value -= 65536;
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function fixUnpackedInt32($payload, $field)
    {
        $value = $payload[$field];

        // int32 is unpacked as uint32, but PHP might store it in an int64
        // which makes actually negtive values show up as positive values.
        // detect if this has happend and fix it
        if (bccomp($value, '2147483648') >= 0) {
            $value = bcsub($value, '4294967296');
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function fixUnpackedUInt32($payload, $field)
    {
        $value = $payload[$field];

        // int32 is unpacked as uint32, but PHP might store it in an int32
        // which makes values bigger than INT32_MAX overflow into negative
        // values. detect if this has happend and fix it
        if (bccomp($value, 0) < 0) {
            $value = bcadd($value, '4294967296');
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function fixUnpackedInt64($payload, $field)
    {
        // int64 is unpacked as 8 uint8 values, collect and decode them
        $value = Base256::decode(self::collectUnpackedArray($payload, $field, 8));

        // the base256 decoder produces and uint64 value, convert back to int64
        if (bccomp($value, '9223372036854775808') >= 0) {
            $value = bcsub($value, '18446744073709551616');
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function fixUnpackedUInt64($payload, $field)
    {
        // uint64 is unpacked as 8 uint8 values, collect and decode them
        return Base256::decode(self::collectUnpackedArray($payload, $field, 8));
    }

    /**
     * @internal
     */
    static public function collectUnpackedInt16Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedInt16($payload, $field . $i));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedInt32Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedInt32($payload, $field . $i));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedUInt32Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedUInt32($payload, $field . $i));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedInt64Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedInt64($payload, $field . chr(ord('A') + $i - 1)));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedUInt64Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedUInt64($payload, $field . chr(ord('A') + $i - 1)));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedBoolArray($payload, $field, $length)
    {
        $_payload = array_fill(0, ceil($length/8), 0);
        $result = array_fill(0, $length, (bool)false);

        if (ceil($length/8) == 1) {
            $_payload[0] = $payload[$field];
        } else {
            for ($i = 1; $i <= ceil($length/8); $i++) {
                $_payload[$i - 1] = $payload[$field . $i];
            }
        }

        for ($i = 0; $i < $length; $i++) {
            $result[$i] = (($_payload[$i / 8] & (1 << ($i % 8))) != 0);
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function implodeUnpackedString($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            $c = $payload[$field . $i];

            if ($c === 0) {
                break;
            }

            array_push($result, chr($c));
        }

        return implode($result);
    }

    /**
     * @internal
     */
    static public function collectUnpackedCharArray($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, chr($payload[$field . $i]));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedArray($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, $payload[$field . $i]);
        }

        return $result;
    }

    /**
     * @internal
     */
    static private function readUInt32NonBlocking($filename)
    {
        $fp = @fopen($filename, 'rb');

        if ($fp === FALSE) {
            return FALSE;
        }

        stream_set_blocking($fp, 0);

        $bytes = @fread($fp, 4);

        @fclose($fp);

        if (strlen($bytes) !== 4) {
            return FALSE;
        }

        $data = unpack('V1number', $bytes);

        return self::fixUnpackedUInt32($data, 'number');
    }

    /**
     * @internal
     */
    static private function getRandomUInt32()
    {
        $r = self::readUInt32NonBlocking('/dev/urandom');

        if ($r !== FALSE) {
            return $r;
        }

        $r = self::readUInt32NonBlocking('/dev/random');

        if ($r !== FALSE) {
            return $r;
        }

        if (function_exists('mcrypt_create_iv')) {
            $bytes = @mcrypt_create_iv(4, MCRYPT_DEV_URANDOM);

            if ($bytes !== FALSE) {
                $data = unpack('V1number', $bytes);

                return self::fixUnpackedUInt32($data, 'number');
            }
        }

        if (function_exists('openssl_random_pseudo_bytes')) {
            $strong = false;
            $bytes = @openssl_random_pseudo_bytes(4, $strong);

            if (!$strong && $bytes !== FALSE) {
                $data = unpack('V1number', $bytes);

                return self::fixUnpackedUInt32($data, 'number');
            }
        }

        $time = gettimeofday();
        $seconds = $time['sec'];
        $microseconds = $time['usec'];

        // (($seconds << 26 | $seconds >> 6) + $microseconds + getmypid()) % (1 << 32)
        return bcmod(bcadd(bcadd(bcadd(bcmul($seconds, '67108864'), bcdiv($seconds, '64')), $microseconds), getmypid()), '4294967296');
    }
}

?>

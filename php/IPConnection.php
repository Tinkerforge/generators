<?php

/*
 * Copyright (c) 2012, Matthias Bolte (matthias@tinkerforge.com)
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

namespace Tinkerforge;


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

        for ($i = $length - 1; $i >= 0; $i--)
        {
            $index = strval(strpos(self::$alphabet, $encoded[$i]));
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


class NotSupportedException extends TinkerforgeException
{

}


abstract class Device
{
    /**
     * @internal
     */
    const RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0;
    const RESPONSE_EXPECTED_ALWAYS_TRUE = 1; // getter
    const RESPONSE_EXPECTED_ALWAYS_FALSE = 2; // callback
    const RESPONSE_EXPECTED_TRUE = 3; // setter
    const RESPONSE_EXPECTED_FALSE = 4; // setter, default

    public $uid = '0'; # Base10
    public $apiVersion = array(0, 0, 0);

    public $ipcon = NULL;

    public $responseExpected = array();

    public $expectedResponseFunctionID = 0;
    public $expectedResponseSequenceNumber = 0;
    public $receivedResponse = NULL;

    public $registeredCallbacks = array();
    public $registeredCallbackUserData = array();
    public $callbackWrappers = array();
    public $pendingCallbacks = array();

    /**
     * Creates the device object with the unique device ID *$uid* and adds
     * it to the IPConnection *$ipcon*.
     *
     * @param string $uid
     * @param IPConnection $ipcon
     */
    public function __construct($uid, $ipcon)
    {
        $longUid = Base58::decode($uid);

        if (bccomp($longUid, '4294967295' /* 0xFFFFFFFF */) > 0) {
            // Convert from 64bit to 32bit
            $value1a = (int)bcmod($longUid, '65536' /* 0x10000 */);
            $value1b = (int)bcmod(bcdiv($longUid, '65536' /* 0x10000 */), '65536' /* 0x10000 */);
            $value2a = (int)bcmod(bcdiv($longUid, '4294967296' /* 0x100000000 */), '65536' /* 0x10000 */);
            $value2b = (int)bcmod(bcdiv($longUid, '281474976710656' /* 0x10000000000 */), '65536' /* 0x10000 */);

            $shortUid1  =  $value1a & 0x0FFF;
            $shortUid1 |= ($value1b & 0x0F00) << 4;

            $shortUid2  =  $value2a & 0x003F;
            $shortUid2 |= ($value2b & 0x000F) << 6;
            $shortUid2 |= ($value2b & 0x3F00) << 2;

            $this->uid = bcadd(bcmul($shortUid2, '65536' /* 0x10000 */), $shortUid1);
        } else {
            $this->uid = $longUid;
        }

        $this->ipcon = $ipcon;

        for ($i = 0; $i < 256; ++$i) {
            $this->responseExpected[$i] = self::RESPONSE_EXPECTED_INVALID_FUNCTION_ID;
        }

        $this->responseExpected[IPConnection::FUNCTION_ENUMERATE] = self::RESPONSE_EXPECTED_ALWAYS_FALSE;
        $this->responseExpected[IPConnection::CALLBACK_ENUMERATE] = self::RESPONSE_EXPECTED_ALWAYS_FALSE;

        $ipcon->devices[$this->uid] = $this; // FIXME: use a weakref here
    }

    /**
     * Returns the API version (major, minor, revision) of the bindings for
     * this device.
     *
     * @return array
     */
    public function getAPIVersion()
    {
        return $this->apiVersion;
    }

    /**
     * Returns the response expected flag for the function specified by the
     * *$functionId* parameter. It is *true* if the function is expected to
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
     * disabled for a setter function then no response is send and errors are
     * silently ignored, because they cannot be detected.
     *
     * @param int $functionId
     *
     * @return boolean
     */
    public function getResponseExpected($functionID)
    {
        if ($functionID < 0 || $functionID > 255) {
            throw new \InvalidArgumentException('Function ID ' . $functionID . ' out of range');
        }

        $flag = $this->responseExpected[$functionID];

        if ($flag == self::RESPONSE_EXPECTED_INVALID_FUNCTION_ID) {
            throw new \InvalidArgumentException('Invalid function ID ' . $functionID);
        }

        if ($flag == self::RESPONSE_EXPECTED_ALWAYS_TRUE ||
            $flag == self::RESPONSE_EXPECTED_TRUE) {
            return TRUE;
        } else {
            return FALSE;
        }
    }

    /**
     * Changes the response expected flag of the function specified by the
     * *$functionId* parameter. This flag can only be changed for setter
     * (default value: *false*) and callback configuration functions
     * (default value: *true*). For getter functions it is always enabled
     * and callbacks it is always disabled.
     *
     * Enabling the response expected flag for a setter function allows to
     * detect timeouts and other error conditions calls of this setter as
     * well. The device will then send a response for this purpose. If this
     * flag is disabled for a setter function then no response is send and
     * errors are silently ignored, because they cannot be detected.
     *
     * @param int $functionId
     * @param boolean $responseExpected
     *
     * @return void
     */
    public function setResponseExpected($functionID, $responseExpected)
    {
        if ($functionID < 0 || $functionID > 255) {
            throw new \InvalidArgumentException('Function ID ' . $functionID . ' out of range');
        }

        $flag = $this->responseExpected[$functionID];

        if ($flag == self::RESPONSE_EXPECTED_INVALID_FUNCTION_ID) {
            throw new \InvalidArgumentException('Invalid function ID ' . $functionID);
        }

        if ($flag == self::RESPONSE_EXPECTED_ALWAYS_TRUE ||
            $flag == self::RESPONSE_EXPECTED_ALWAYS_FALSE) {
            throw new \InvalidArgumentException('Response Expected flag cannot be changed for function ID ' . $functionID);
        }

        $this->responseExpected[$functionID] =
            $responseExpected ? self::RESPONSE_EXPECTED_TRUE
                              : self::RESPONSE_EXPECTED_FALSE;
    }

    /**
     * Changes the response expected flag for all setter and callback
     * configuration functions of this device at once.
     *
     * @param boolean $responseExpected
     *
     * @return void
     */
    public function setResponseExpectedAll($responseExpected)
    {
        $flag = $responseExpected ? self::RESPONSE_EXPECTED_TRUE
                                  : self::RESPONSE_EXPECTED_FALSE;

        for ($i = 0; $i < 256; ++$i) {
            if ($this->responseExpected[$i] == self::RESPONSE_EXPECTED_TRUE ||
                $this->responseExpected[$i] == self::RESPONSE_EXPECTED_FALSE) {
                $this->responseExpected[$i] = $flag;
            }
        }
    }

    /**
     * @internal
     */
    public function dispatchPendingCallbacks()
    {
        $pendingCallbacks = $this->pendingCallbacks;
        $this->pendingCallbacks = array();

        foreach ($pendingCallbacks as $pendingCallback) {
            if ($this->ipcon->socket === FALSE) {
                break;
            }

            $this->handleCallback($pendingCallback[0], $pendingCallback[1]);
        }
    }

    /**
     * @internal
     */
    protected function sendRequest($functionID, $payload)
    {
        if ($this->ipcon->socket === FALSE) {
            throw new NotConnectedException('Not connected');
        }

        $header = $this->ipcon->createPacketHeader($this, 8 + strlen($payload), $functionID);
        $request = $header[0] . $payload;
        $sequenceNumber = $header[1];
        $responseExpected = $header[2];

        if ($responseExpected) {
            $this->expectedResponseFunctionID = $functionID;
            $this->expectedResponseSequenceNumber = $sequenceNumber;
            $this->receivedResponse = NULL;
        }

        $this->ipcon->send($request);

        if ($responseExpected) {
            $this->ipcon->receive($this->ipcon->timeout, $this, FALSE /* FIXME: this can delay callback up to the current timeout */);

            $this->expectedResponseFunctionID = 0;
            $this->expectedResponseSequenceNumber = 0;

            if ($this->receivedResponse == NULL) {
                throw new TimeoutException("Did not receive response in time for function ID $functionID");
            }

            $response = $this->receivedResponse;
            $this->receivedResponse = NULL;

            $errorCode = ($response[0]['errorCodeAndFutureUse'] >> 6) & 0x03;

            if ($errorCode == 0) {
                // no error
            } else if ($errorCode == 1) {
                throw new NotSupportedException("Got invalid parameter for function ID $functionID");
            } else if ($errorCode == 2) {
                throw new NotSupportedException("Function ID $functionID is not supported");
            } else {
                throw new NotSupportedException("Function ID $functionID returned an unknown error");
            }

            $payload = $response[1];
        } else {
            $payload = NULL;
        }

        return $payload;
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

    private $nextSequenceNumber = 0;

    public $devices = array();

    private $registeredCallbacks = array();
    private $registeredCallbackUserData = array();
    private $pendingCallbacks = array();

    private $host = "";
    private $port = 0;

    public $socket = FALSE;
    private $pendingData = '';

    private $disconnectProbeRequest = '';
    private $nextDisconnectProbe = 0.0;

    /**
     * Creates an IP Connection object that can be used to enumerate the available
     * devices. It is also required for the constructor of Bricks and Bricklets.
     */
    public function __construct()
    {
        $result = $this->createPacketHeader(NULL, 8, self::FUNCTION_DISCONNECT_PROBE);
        $this->disconnectProbeRequest = $result[0];
        $this->nextDisconnectProbe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;
    }

    function __destruct()
    {
        if ($this->socket !== FALSE) {
            $this->disconnect();
        }
    }

    /**
     * Creates a TCP/IP connection to the given *$host* and *$port*. The host
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

        if (preg_match('/^\d+\.\d+\.\d+\.\d+$/', $host) == 0) {
            $address = gethostbyname($host);

            if ($address == $host) {
                throw new \Exception('Could not resolve hostname');
            }
        } else {
            $address = $host;
        }

        $this->socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

        if ($this->socket === FALSE) {
            throw new \Exception('Could not create socket: ' .
                                 socket_strerror(socket_last_error()));
        }

        @socket_set_option($this->socket, SOL_TCP, TCP_NODELAY, 1);

        if (!@socket_connect($this->socket, $address, $port)) {
            $error = socket_strerror(socket_last_error($this->socket));

            socket_close($this->socket);
            $this->socket = FALSE;

            throw new \Exception('Could not connect socket: ' . $error);
        }

        if (array_key_exists(self::CALLBACK_CONNECTED, $this->registeredCallbacks)) {
            call_user_func_array($this->registeredCallbacks[self::CALLBACK_CONNECTED],
                                 array(self::CONNECT_REASON_REQUEST,
                                       $this->registeredCallbackUserData[self::CALLBACK_CONNECTED]));
        }

        $this->nextDisconnectProbe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;
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

        @socket_shutdown($this->socket, 2);

        $this->disconnectInternal(self::DISCONNECT_REASON_REQUEST);

        $this->pendingData = '';
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
        if ($timeout < 0) {
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
     * Registers a callback for a given ID.
     *
     * @param int $id
     * @param callable $callback
     * @param mixed $userData
     *
     * @return void
     */
    public function registerCallback($id, $callback, $userData = NULL)
    {
        if (!is_callable($callback)) {
            throw new \Exception('Callback function is not callable');
        }

        $this->registeredCallbacks[$id] = $callback;
        $this->registeredCallbackUserData[$id] = $userData;
    }

    /**
     * @internal
     */
    public function createPacketHeader($device, $length, $functionID)
    {
        $uid = '0';
        $sequenceNumber = $this->nextSequenceNumber + 1;
        $this->nextSequenceNumber = $sequenceNumber % 15;
        $responseExpected = 0;

        if ($device != NULL) {
            $uid = $device->uid;

            if ($device->getResponseExpected($functionID)) {
                $responseExpected = 1;
            }
        }

        $sequenceNumberAndOptions = ($sequenceNumber << 4) | ($responseExpected << 3);
        $header = Base256::encodeAndPack($uid, 4) . pack('CCCC', $length, $functionID, $sequenceNumberAndOptions, 0);

        return array($header, $sequenceNumber, $responseExpected);
    }

    /**
     * @internal
     */
    public function send($request)
    {
        if (@socket_send($this->socket, $request, strlen($request), 0) === FALSE) {
            $this->disconnectInternal(self::DISCONNECT_REASON_ERROR);

            throw new NotConnectedException('Could not send request: ' .
                                            socket_strerror(socket_last_error($this->socket)));
        }

        $this->nextDisconnectProbe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;
    }

    /**
     * @internal
     */
    public function receive($seconds, $device, $directCallbackDispatch)
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
            if ($this->nextDisconnectProbe < $now ||
                ($this->nextDisconnectProbe - $now) > self::DISCONNECT_PROBE_INTERVAL) {
                if (@socket_send($this->socket, $this->disconnectProbeRequest,
                                 strlen($this->disconnectProbeRequest), 0) === FALSE) {
                    $this->disconnectInternal(self::DISCONNECT_REASON_ERROR);
                    return;
                }

                $now = microtime(true);
                $this->nextDisconnectProbe = $now + self::DISCONNECT_PROBE_INTERVAL;
            }

            $read = array($this->socket);
            $write = NULL;
            $except = array($this->socket);
            $timeout = $end - $now;

            if ($timeout < 0) {
                $timeout = 0;
            }

            $timeout_sec = floor($timeout);
            $timeout_usec = ceil(($timeout - $timeout_sec) * 1000000);
            $changed = @socket_select($read, $write, $except, $timeout_sec, $timeout_usec);

            if ($changed === FALSE) {
                throw new \Exception('Could not receive response: ' .
                                     socket_strerror(socket_last_error($this->socket)));
            } else if ($changed > 0) {
                if (in_array($this->socket, $except)) {
                    $this->disconnectInternal(self::DISCONNECT_REASON_ERROR);
                    return;
                }

                $data = '';
                $length = @socket_recv($this->socket, $data, 8192, 0);

                if ($length === FALSE || $length == 0) {
                    if ($length === FALSE) {
                        $disconnectReason = self::DISCONNECT_REASON_ERROR;
                    } else {
                        $disconnectReason = self::DISCONNECT_REASON_SHUTDOWN;
                    }

                    $this->disconnectInternal($disconnectReason);
                    return;
                }

                $before = microtime(true);

                $this->pendingData .= $data;

                while (TRUE) {
                    if (strlen($this->pendingData) < 8) {
                        // Wait for complete header
                        break;
                    }

                    $tmp = unpack('C', substr($this->pendingData, 4));
                    $length = $tmp[1];

                    if (strlen($this->pendingData) < $length) {
                        // Wait for complete packet
                        break;
                    }

                    $packet = substr($this->pendingData, 0, $length);
                    $this->pendingData = substr($this->pendingData, $length);

                    $this->handleResponse($packet, $directCallbackDispatch);
                }

                $after = microtime(true);

                if ($after > $before) {
                    $end += $after - $before;
                }

                if ($device != NULL && $device->receivedResponse != NULL) {
                    break;
                }
            }

            $now = microtime(true);
        } while ($now >= $start && $now < $end);
    }

    /**
     * @internal
     */
    private function disconnectInternal($disconnectReason)
    {
        @socket_close($this->socket);
        $this->socket = FALSE;

        if (array_key_exists(self::CALLBACK_DISCONNECTED, $this->registeredCallbacks)) {
            call_user_func_array($this->registeredCallbacks[self::CALLBACK_DISCONNECTED],
                                 array($disconnectReason,
                                       $this->registeredCallbackUserData[self::CALLBACK_DISCONNECTED]));
        }
    }

    /**
     * @internal
     */
    private function handleResponse($packet, $directCallbackDispatch)
    {
        $uid = Base256::decode(self::collectUnpackedArray(unpack('C4uid', $packet), 'uid', 4));
        $header = unpack('Clength/CfunctionID/CsequenceNumberAndOptions/CerrorCodeAndFutureUse', substr($packet, 4));
        $header['uid'] = $uid;
        $functionID = $header['functionID'];
        $sequenceNumber = ($header['sequenceNumberAndOptions'] >> 4) & 0x0F;
        $payload = substr($packet, 8);

        $this->nextDisconnectProbe = microtime(true) + self::DISCONNECT_PROBE_INTERVAL;

        if ($sequenceNumber == 0 && $functionID == self::CALLBACK_ENUMERATE) {
            if (array_key_exists(self::CALLBACK_ENUMERATE, $this->registeredCallbacks)) {
                if ($directCallbackDispatch) {
                    if ($this->socket === FALSE) {
                        return;
                    }

                    $this->handleEnumerate($header, $payload);
                } else {
                    array_push($this->pendingCallbacks, array($header, $payload));
                }
            }

            return;
        }

        if (!array_key_exists($uid, $this->devices)) {
            // Response from an unknown device, ignoring it
            return;
        }

        $device = $this->devices[$uid];

        if ($sequenceNumber == 0) {
            if (array_key_exists($functionID, $device->registeredCallbacks)) {
                if ($directCallbackDispatch) {
                    if ($this->socket === FALSE) {
                        return;
                    }

                    $device->handleCallback($header, $payload);
                } else {
                    array_push($device->pendingCallbacks, array($header, $payload));
                }
            }

            return;
        }

        if ($device->expectedResponseFunctionID == $functionID &&
            $device->expectedResponseSequenceNumber == $sequenceNumber) {
            $device->receivedResponse = array($header, $payload);
            return;
        }

        // Response seems to be OK, but can't be handled, most likely
        // a callback without registered callback function
    }

    /**
     * @internal
     */
    private function handleEnumerate($header, $payload)
    {
        if (!array_key_exists(self::CALLBACK_ENUMERATE, $this->registeredCallbacks)) {
            return;
        }

        $payload = unpack('c8uid/c8connectedUid/cposition/C3hardwareVersion/C3firmwareVersion/vdeviceIdentifier/CenumerationType', $payload);

        $uid = self::implodeUnpackedString($payload, 'uid', 8);
        $connectedUid = self::implodeUnpackedString($payload, 'connectedUid', 8);
        $position = chr($payload['position']);
        $hardwareVersion = self::collectUnpackedArray($payload, 'hardwareVersion', 3);
        $firmwareVersion = self::collectUnpackedArray($payload, 'firmwareVersion', 3);
        $deviceIdentifier = $payload['deviceIdentifier'];
        $enumerationType = $payload['enumerationType'];

        call_user_func_array($this->registeredCallbacks[self::CALLBACK_ENUMERATE],
                             array($uid, $connectedUid, $position, $hardwareVersion,
                                   $firmwareVersion, $deviceIdentifier, $enumerationType,
                                   $this->registeredCallbackUserData[self::CALLBACK_ENUMERATE]));
    }

    /**
     * @internal
     */
    private function dispatchPendingCallbacks()
    {
        $pendingCallbacks = $this->pendingCallbacks;
        $this->pendingCallbacks = array();

        foreach ($pendingCallbacks as $pendingCallback) {
            if ($this->socket === FALSE) {
                break;
            }

            if ($pendingCallback[0]['functionID'] == self::CALLBACK_ENUMERATE) {
                $this->handleEnumerate($pendingCallback[0], $pendingCallback[1]);
            }
        }

        foreach ($this->devices as $device) {
            $device->dispatchPendingCallbacks();
        }
    }

    /**
     * @internal
     */
    static public function fixUnpackedInt16($value)
    {
        if ($value >= 32768) {
            $value -= 65536;
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function fixUnpackedInt32($value)
    {
        if (bccomp($value, '2147483648') >= 0) {
            $value = bcsub($value, '4294967296');
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function fixUnpackedUInt32($value)
    {
        if (bccomp($value, 0) < 0) {
            $value = bcadd($value, '4294967296');
        }

        return $value;
    }

    /**
     * @internal
     */
    static public function collectUnpackedInt16Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedInt16($payload[$field . $i]));
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
            array_push($result, self::fixUnpackedInt32($payload[$field . $i]));
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
            array_push($result, self::fixUnpackedUInt32($payload[$field . $i]));
        }

        return $result;
    }

    /**
     * @internal
     */
    static public function collectUnpackedBoolArray($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, (bool)$payload[$field . $i]);
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

            if ($c == 0) {
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
}

?>

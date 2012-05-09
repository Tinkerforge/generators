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


class TimeoutException extends \Exception
{

}


abstract class Device
{
    public $uid = '0'; # Base10
    public $stackID = 0;
    public $name = '';

    public $firmwareVersion = array(0, 0, 0);
    public $bindingVersion = array(0, 0, 0);

    public $ipcon = NULL;

    public $expectedResponseFunctionID = 0;
    public $expectedResponsePacketLength = 0;
    public $receivedResponsePayload = NULL;

    public $callbacks = array();
    public $deviceCallbacks = array();

    public function __construct($uid)
    {
        $this->uid = Base58::decode($uid);
    }

    /**
     * Returns the name (including the hardware version), the firmware version
     * and the binding version of the device. The firmware and binding versions
     * are given in arrays of size 3 with the syntax (major, minor, revision).
     *
     * The returned array contains name, firmwareVersion and bindingVersion.
     */
    public function getVersion()
    {
        return array('name' => $this->name,
                     'firmwareVersion' => $this->firmwareVersion,
                     'bindingVersion' => $this->bindingVersion);
    }

    public function registerCallback($id, $callback)
    {
        $this->callbacks[$id] = $callback;
    }

    protected function sendRequestNoResponse($functionID, $payload)
    {
        $header = pack('CCv', $this->stackID, $functionID, 4 + strlen($payload));
        $request = $header . $payload;

        $this->expectedResponseFunctionID = 0;
        $this->expectedResponsePacketLength = 0;
        $this->receivedResponsePayload = NULL;

        $this->ipcon->send($request);
    }

    protected function sendRequestExpectResponse($functionID, $payload,
                                                 $expectedResponsePayloadLength)
    {
        if ($this->ipcon == NULL) {
            throw new \Exception('No added to IPConnection');
        }

        $header = pack('CCv', $this->stackID, $functionID, 4 + strlen($payload));
        $request = $header . $payload;

        $this->expectedResponseFunctionID = $functionID;
        $this->expectedResponsePacketLength = 4 + $expectedResponsePayloadLength;
        $this->receivedResponsePayload = NULL;

        $this->ipcon->send($request);
        $this->ipcon->receive(IPConnection::TIMEOUT_RESPONSE, $this);

        if ($this->receivedResponsePayload == NULL) {
            throw new TimeoutException('Did not receive response in time');
        }

        $payload = $this->receivedResponsePayload;

        $this->expectedResponseFunctionID = 0;
        $this->expectedResponsePacketLength = 0;
        $this->receivedResponsePayload = NULL;

        return $payload;
    }
}


class IPConnection
{
    const TIMEOUT_ADD_DEVICE = 2.5;
    const TIMEOUT_RESPONSE = 2.5;

    const BROADCAST_ADDRESS = 0;
    const FUNCTION_ID_GET_STACK_ID = 255;
    const FUNCTION_ID_ENUMERATE = 254;
    const FUNCTION_ID_ENUMERATE_CALLBACK = 253;

    private $socket = FALSE;
    private $devices = array();
    private $pendingAddDevice = NULL;
    private $enumerateCallback = NULL;

    public function __construct($host, $port)
    {
        $address = '';

        if (preg_match('/^\d+\.\d+\.\d+\.\d+$/', $host) == 0) {
            $address = gethostbyname($host);

            if ($address == $host) {
                throw new \Exception('Unable to connect socket: Unknown host');
            }
        } else {
            $address = $host;
        }

        $this->socket = @socket_create(AF_INET, SOCK_STREAM, SOL_TCP);

        if ($this->socket === FALSE) {
            throw new \Exception('Unable to create socket: ' .
                                 socket_strerror(socket_last_error()));
        }

        if (!@socket_connect($this->socket, $address, $port)) {
            $error = socket_strerror(socket_last_error($this->socket));

            socket_close($this->socket);
            $this->socket = FALSE;

            throw new \Exception('Unable to connect socket: ' . $error);
        }
    }

    function __destruct()
    {
        $this->destroy();
    }

    public function enumerate($callback)
    {
        $this->enumerateCallback = $callback;

        $request = pack('CCv', self::BROADCAST_ADDRESS, self::FUNCTION_ID_ENUMERATE, 4);

        $this->send($request);
    }

    public function addDevice($device)
    {
        $uid = Base256::encodeAndPack($device->uid, 8);
        $request = pack('CCv', self::BROADCAST_ADDRESS, self::FUNCTION_ID_GET_STACK_ID, 12) . $uid;

        $this->pendingAddDevice = $device;

        $this->send($request);
        $this->receive(self::TIMEOUT_ADD_DEVICE, NULL);

        if ($this->pendingAddDevice != NULL) {
            $this->pendingAddDevice = NULL;
            throw new TimeoutException('Unable to add device ' . Base58::encode($device->uid));
        }

        $device->ipcon = $this;
    }

    public function dispatchCallbacks($seconds)
    {
        if ($seconds < 0) {
            while (TRUE) {
                $this->receive(self::TIMEOUT_RESPONSE, NULL);
            }
        } else {
            $this->receive($seconds, NULL);
        }
    }

    public function receive($seconds, $device)
    {
        if ($seconds < 0) {
            $seconds = 0;
        }

        $start = microtime(true);
        $end = $start + $seconds;

        do {
            $read = array($this->socket);
            $write = NULL;
            $except = NULL;
            $timeout = $end - microtime(true);

            if ($timeout < 0) {
                $timeout = 0;
            }

            $timeout_sec = floor($timeout);
            $timeout_usec = ceil(($timeout - $timeout_sec) * 1000000);
            $changed = @socket_select($read, $write, $except, $timeout_sec, $timeout_usec);

            if ($changed === FALSE) {
                throw new \Exception('Unable to receive response: ' .
                                     socket_strerror(socket_last_error($this->socket)));
            } else if ($changed > 0) {
                $data = '';
                $length = @socket_recv($this->socket, $data, 8192, 0);

                if ($length === FALSE) {
                    throw new \Exception('Unable to receive response: ' .
                                         socket_strerror(socket_last_error($this->socket)));
                }

                $isAddingDevice = $this->pendingAddDevice != NULL;

                $before = microtime(true);

                while (strlen($data) > 0) {
                    $handled = $this->handleResponse($data);
                    $data = substr($data, $handled);
                }

                $after = microtime(true);

                if ($after > $before) {
                    $end += $after - $before;
                }

                if (($isAddingDevice && $this->pendingAddDevice == NULL) ||
                    ($device != NULL && $device->expectedResponsePacketLength > 0 &&
                     $device->receivedResponsePayload != NULL)) {
                    break;
                }
            }

            $now = microtime(true);
        } while ($now >= $start && $now < $end);
    }

    public function destroy()
    {
        if ($this->socket === FALSE) {
            return;
        }

        @socket_shutdown($this->socket, 2);
        @socket_close($this->socket);

        $this->socket = FALSE;
    }

    public function send($request)
    {
        if (@socket_send($this->socket, $request, strlen($request), 0) === FALSE) {
            throw new \Exception('Unable to send request: ' .
                                 socket_strerror(socket_last_error($this->socket)));
        }
    }

    private function handleResponse($data)
    {
        $header = unpack('CstackID/CfunctionID/vlength', $data);
        $data = substr($data, 4);

        if ($header['functionID'] == self::FUNCTION_ID_GET_STACK_ID) {
            return $this->handleAddDevice($header, $data);
        } else if ($header['functionID'] == self::FUNCTION_ID_ENUMERATE_CALLBACK) {
            return $this->handleEnumerate($header, $data);
        }

        if (!array_key_exists($header['stackID'], $this->devices)) {
            // Message for an unknown device, ignoring it
            return $header['length'];
        }

        $device = $this->devices[$header['stackID']];

        if ($device->expectedResponseFunctionID == $header['functionID']) {
            if ($device->expectedResponsePacketLength != $header['length']) {
                error_log('Malformed response, discarded: ' .
                          $header['stackID'] . ' ' . $header['functionID']);
                return $header['length'];
            }

            $device->receivedResponsePayload = $data;

            return $header['length'];
        }

        if (array_key_exists($header['functionID'], $device->callbacks)) {
            $device->handleCallback($header, $data);

            return $header['length'];
        }

        // Response seems to be OK, but can't be handled, most likely
        // a callback without registered callback function
        return $header['length'];
    }

    private function handleAddDevice($header, $data)
    {
        if ($this->pendingAddDevice == NULL) {
            return $header['length'];
        }

        $payload = unpack('C8uid/C3firmwareVersion/c40name/CstackID', $data);

        // uid
        $uid = Base256::decode(self::collectUnpackedArray($payload, 'uid', 8));

        if ($this->pendingAddDevice->uid != $uid) {
            return $header['length'];
        }

        // firmware Version
        $this->pendingAddDevice->firmwareVersion =
                self::collectUnpackedArray($payload, 'firmwareVersion', 3);

        // name
        $this->pendingAddDevice->name = self::implodeUnpackedString($payload, 'name', 40);

        // stack ID
        $this->pendingAddDevice->stackID = $payload['stackID'];

        $this->devices[$this->pendingAddDevice->stackID] = $this->pendingAddDevice;
        $this->pendingAddDevice = NULL;

        return $header['length'];
    }

    private function handleEnumerate($header, $data)
    {
        if ($this->enumerateCallback == NULL) {
            return $header['length'];
        }

        $payload = unpack('C8uid/c40name/CstackID/CisNew', $data);

        $uid = Base256::decode(self::collectUnpackedArray($payload, 'uid', 8));
        $name = self::implodeUnpackedString($payload, 'name', 40);
        $stackID = $payload['stackID'];
        $isNew = (bool)$payload['isNew'];

        call_user_func_array($this->enumerateCallback,
                             array(Base58::encode($uid), $name, $stackID, $isNew));

        return $header['length'];
    }

    static public function fixUnpackedInt16($value)
    {
        if ($value >= 32768) {
            $value -= 65536;
        }

        return $value;
    }

    static public function fixUnpackedInt32($value)
    {
        if (bccomp($value, '2147483648') >= 0) {
            $value = bcsub($value, '4294967296');
        }

        return $value;
    }

    static public function fixUnpackedUInt32($value)
    {
        if (bccomp($value, 0) < 0) {
            $value = bcadd($value, '4294967296');
        }

        return $value;
    }

    static public function collectUnpackedInt16Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedInt16($payload[$field . $i]));
        }

        return $result;
    }

    static public function collectUnpackedInt32Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedInt32($payload[$field . $i]));
        }

        return $result;
    }

    static public function collectUnpackedUInt32Array($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, self::fixUnpackedUInt32($payload[$field . $i]));
        }

        return $result;
    }

    static public function collectUnpackedBoolArray($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, (bool)$payload[$field . $i]);
        }

        return $result;
    }

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

    static public function collectUnpackedCharArray($payload, $field, $length)
    {
        $result = array();

        for ($i = 1; $i <= $length; $i++) {
            array_push($result, chr($payload[$field . $i]));
        }

        return $result;
    }

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

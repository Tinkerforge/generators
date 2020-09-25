/*
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2014, 2020 Matthias Bolte <matthias@tinkerforge.com>
Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>

Redistribution and use in source and binary forms of this file,
with or without modification, are permitted. See the Creative
Commons Zero (CC0 1.0) License for more details.
*/

var Device = require('./Device');

IPConnection.FUNCTION_ENUMERATE = 254;
IPConnection.FUNCTION_DISCONNECT_PROBE = 128;
IPConnection.CALLBACK_ENUMERATE = 253;
IPConnection.CALLBACK_CONNECTED = 0;
IPConnection.CALLBACK_DISCONNECTED = 1;
IPConnection.BROADCAST_UID = 0;

// Enumeration type parameter to the enumerate callback
IPConnection.ENUMERATION_TYPE_AVAILABLE = 0;
IPConnection.ENUMERATION_TYPE_CONNECTED = 1;
IPConnection.ENUMERATION_TYPE_DISCONNECTED = 2;

// Connect reason parameter to the connected callback
IPConnection.CONNECT_REASON_REQUEST = 0;
IPConnection.CONNECT_REASON_AUTO_RECONNECT = 1;

// Disconnect reason parameter to the disconnected callback
IPConnection.DISCONNECT_REASON_REQUEST = 0;
IPConnection.DISCONNECT_REASON_ERROR = 1;
IPConnection.DISCONNECT_REASON_SHUTDOWN = 2;

// Returned by getConnectionState()
IPConnection.CONNECTION_STATE_DISCONNECTED = 0;
IPConnection.CONNECTION_STATE_CONNECTED = 1;
IPConnection.CONNECTION_STATE_PENDING = 2; // auto-reconnect in process
IPConnection.DISCONNECT_PROBE_INTERVAL = 5000;
IPConnection.RETRY_CONNECTION_INTERVAL = 2000;

// Error codes
IPConnection.ERROR_ALREADY_CONNECTED = 11;
IPConnection.ERROR_NOT_CONNECTED = 12;
IPConnection.ERROR_CONNECT_FAILED = 13;
IPConnection.ERROR_INVALID_FUNCTION_ID = 21; // keep in sync with Device.ERROR_INVALID_FUNCTION_ID
IPConnection.ERROR_TIMEOUT = 31;
IPConnection.ERROR_INVALID_PARAMETER = 41;
IPConnection.ERROR_FUNCTION_NOT_SUPPORTED = 42;
IPConnection.ERROR_UNKNOWN_ERROR = 43;
IPConnection.ERROR_STREAM_OUT_OF_SYNC = 51;
IPConnection.ERROR_NON_ASCII_CHAR_IN_SECRET = 71;
IPConnection.ERROR_WRONG_DEVICE_TYPE = 81; // keep in sync with Device.ERROR_WRONG_DEVICE_TYPE
IPConnection.ERROR_DEVICE_REPLACED = 82; // keep in sync with Device.ERROR_DEVICE_REPLACED
IPConnection.ERROR_WRONG_RESPONSE_LENGTH = 83;
IPConnection.ERROR_INT64_NOT_SUPPORTED = 91;

IPConnection.TASK_KIND_CONNECT = 0;
IPConnection.TASK_KIND_DISCONNECT = 1;
IPConnection.TASK_KIND_AUTO_RECONNECT = 2;
IPConnection.TASK_KIND_AUTHENTICATE = 3;

// Socket implementation for Node.js and Websocket.
// The API resembles the Node.js API.
function TFSocket(PORT, HOST, ipcon) {
    this.port = PORT;
    this.host = HOST;
    this.socket = null;

    if (process.browser) {
        var webSocketURL = "ws://" + this.host + ":" + this.port + "/";

        if (typeof MozWebSocket != "undefined") {
            this.socket = new MozWebSocket(webSocketURL, "tfp");
        } else {
            this.socket = new WebSocket(webSocketURL, "tfp");
        }

        this.socket.binaryType = 'arraybuffer';
    } else {
        var net = require('net');

        this.socket = new net.Socket();
    }

    this.on = function (str, func) {
        if (process.browser) {
            switch (str) {
            case "connect":
                this.socket.onopen = func;
                break;
            case "data":
                // Websockets in browsers return a MessageEvent. We just
                // expose the data from the event as a Buffer as in Node.js.
                this.socket.onmessage = function (messageEvent) {
                    if (Buffer.from && Buffer.from !== Uint8Array.from) {
                        var data = Buffer.from(new Uint8Array(messageEvent.data));
                    } else {
                        var data = new Buffer(new Uint8Array(messageEvent.data));
                    }
                    func(data);
                };
                break;
            case "error":
                // There is no easy way to get errno for error in browser websockets.
                // We assume error['errno'] === 'ECONNRESET'
                this.socket.onerror = function () {
                    var error = {"errno": "ECONNRESET"};
                    func(error);
                };
                break;
            case "close":
                this.socket.onclose = func;
                break;
            }
        } else {
            this.socket.on(str, func);
        }
    };

    this.connect = function () {
        if (process.browser) {
            // In the browser we already connected by creating a WebSocket object
        } else {
            this.socket.connect(this.port, this.host, null);
        }
    };

    this.setNoDelay = function (value) {
        if (process.browser) {
            // Currently no API available in browsers
            // But Nagle algorithm seems te be turned off in most browsers by default anyway
        } else {
            this.socket.setNoDelay(value);
        }
    };

    this.write = function (data, reset_disconnect_probe) {
        if (process.browser) {
            // Some browers can't send a nodejs Buffer through a websocket,
            // we copy it into an ArrayBuffer
            var arrayBuffer = new Uint8Array(data).buffer;

            this.socket.send(arrayBuffer);

            if (reset_disconnect_probe) {
                ipcon.resetDisconnectProbe();
            }
        } else {
            if (reset_disconnect_probe) {
                this.socket.write(data, ipcon.resetDisconnectProbe);
            } else {
                this.socket.write(data);
            }
        }
    };

    this.end = function () {
        if (process.browser) {
            this.socket.close();
        } else {
            this.socket.end();
        }
    };

    this.destroy = function () {
        if (process.browser) {
            // There is no end/destroy in browser socket, so we close in end
            // and do nothing in destroy
        } else {
            this.socket.destroy();
        }
    };
}

BrickDaemon.FUNCTION_GET_AUTHENTICATION_NONCE = 1;
BrickDaemon.FUNCTION_AUTHENTICATE = 2;

function BrickDaemon(uid, ipcon) {
    Device.call(this, this, uid, ipcon, 0, 'Brick Daemon');
    BrickDaemon.prototype = Object.create(Device);
    this.responseExpected = {};
    this.callbackFormats = {};
    this.APIVersion = [2, 0, 0];
    this.responseExpected[BrickDaemon.FUNCTION_GET_AUTHENTICATION_NONCE] = Device.RESPONSE_EXPECTED_ALWAYS_TRUE;
    this.responseExpected[BrickDaemon.FUNCTION_AUTHENTICATE] = Device.RESPONSE_EXPECTED_TRUE;

    this.getAuthenticationNonce = function(returnCallback, errorCallback) {
        this.ipcon.sendRequest(this, BrickDaemon.FUNCTION_GET_AUTHENTICATION_NONCE, [], '', 12, 'B4', returnCallback, errorCallback, false, false);
    };

    this.authenticate = function(clientNonce, digest, returnCallback, errorCallback) {
        this.ipcon.sendRequest(this, BrickDaemon.FUNCTION_AUTHENTICATE, [clientNonce, digest], 'B4 B20', 0, '', returnCallback, errorCallback, false, false);
    };

    this.ipcon.addDevice(this);
}

// the IPConnection class and constructor
function IPConnection() {
    // Creates an IP Connection object that can be used to enumerate the available
    // devices. It is also required for the constructor of Bricks and Bricklets.
    this.host = undefined;
    this.port = undefined;
    this.timeout = 2500;
    this.autoReconnect = true;
    this.nextSequenceNumber = 0;
    this.nextAuthenticationNonce = 0;
    this.devices = {};
    this.registeredCallbacks = {};
    this.socket = undefined;
    this.disconnectProbeIID = undefined;
    this.taskQueue = [];
    this.isConnected = false;
    this.connectErrorCallback = undefined;
    this.mergeBuffer = Buffer.concat([]); //See https://nodejs.org/en/docs/guides/buffer-constructor-deprecation/#buffer-0

    this.addDevice = function (device) {
        var replacedDevice = this.devices[device.uid];

        if (replacedDevice !== undefined) {
            replacedDevice.replaced = true;
        }

        this.devices[device.uid] = device;
    };

    this.brickd = new BrickDaemon('2', this);

    this.disconnectProbe = function () {
        if (this.socket !== undefined) {
            try {
                this.socket.write(this.createPacketHeader(undefined, 8, IPConnection.FUNCTION_DISCONNECT_PROBE), false);
            }
            catch(e) {
                // Initiating a normal disconnect will ensure autoreconnect decision and connection management
                this.disconnect(undefined);
            }
        }
    };

    this.pushTask = function (handler, kind) {
        this.taskQueue.push({"handler": handler, "kind": kind});

        if (this.taskQueue.length === 1) {
            this.executeTask();
        }
    };

    this.executeTask = function () {
        var task = this.taskQueue[0];

        if (task !== undefined) {
            task.handler();
        }
    };

    this.popTask = function () {
        this.taskQueue.splice(0, 1);
        this.executeTask();
    };

    this.removeNextTask = function () {
        this.taskQueue.splice(1, 1);
    };

    this.getCurrentTaskKind = function () {
        var task = this.taskQueue[0];

        if (task !== undefined) {
            return task.kind;
        }

        return undefined;
    };

    this.getNextTaskKind = function () {
        var task = this.taskQueue[1];

        if (task !== undefined) {
            return task.kind;
        }

        return undefined;
    };

    this.disconnect = function (errorCallback) {
        this.pushTask(this.disconnectInternal.bind(this, errorCallback), IPConnection.TASK_KIND_DISCONNECT);
    };

    this.disconnectInternal = function (errorCallback) {
        var autoReconnectAborted = false;

        if (this.getNextTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            // Remove auto-reconnect task, to break recursion
            this.removeNextTask();
            autoReconnectAborted = true;
        }

        if (!this.isConnected) {
            if (!autoReconnectAborted && errorCallback !== undefined) {
                // Not using `this.` for the error callback function because
                // we want to call what user provided not the saved one
                errorCallback(IPConnection.ERROR_NOT_CONNECTED);
            }

            this.popTask();
            return;
        }

        this.socket.end();
        this.socket.destroy();
        // no popTask() here, will be done in handleConnectionClose()
        return;
    };

    this.connect = function (host, port, errorCallback) {
        this.pushTask(this.connectInternal.bind(this, host, port, errorCallback), IPConnection.TASK_KIND_CONNECT);
    };

    this.connectInternal = function (host, port, errorCallback) {
        if (this.isConnected) {
            if (errorCallback !== undefined) {
                // Not using `this.` for the error callback function because
                // we want to call what user provided not the saved one
                errorCallback(IPConnection.ERROR_ALREADY_CONNECTED);
            }

            this.popTask();
            return;
        }

        // Saving the user provided error callback function for future use
        this.connectErrorCallback = errorCallback;
        clearInterval(this.disconnectProbeIID);
        this.disconnectProbeIID = undefined;
        this.host = host;
        this.port = port;
        this.socket = new TFSocket(this.port, this.host, this);
        this.socket.setNoDelay(true);
        this.socket.on('connect', this.handleConnect.bind(this));
        this.socket.on('data', this.handleIncomingData.bind(this));
        this.socket.on('error', this.handleConnectionError.bind(this));
        this.socket.on('close', this.handleConnectionClose.bind(this));
        this.socket.connect();
    };

    this.handleConnect = function () {
        var connectReason = IPConnection.CONNECT_REASON_REQUEST;

        if (this.getCurrentTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            connectReason = IPConnection.CONNECT_REASON_AUTO_RECONNECT;
        }

        clearInterval(this.disconnectProbeIID);
        this.disconnectProbeIID = undefined;
        this.isConnected = true;

        // Check and call functions if registered for callback connected
        if (this.registeredCallbacks[IPConnection.CALLBACK_CONNECTED] !== undefined) {
            this.registeredCallbacks[IPConnection.CALLBACK_CONNECTED](connectReason);
        }

        this.disconnectProbeIID = setInterval(this.disconnectProbe.bind(this),
                                              IPConnection.DISCONNECT_PROBE_INTERVAL);

        this.popTask();
    };

    this.handleIncomingData = function (data) {
        this.resetDisconnectProbe();

        if (data.length === 0) {
            return;
        }

        this.mergeBuffer = bufferConcat([this.mergeBuffer, data]);

        while (this.mergeBuffer.length > 0) {
            if (this.mergeBuffer.length < 8) {
                return; // wait for complete header
            }

            var length = this.mergeBuffer.readUInt8(4);

            if (this.mergeBuffer.length < length) {
                return; // wait for complete packet
            }

            var newPacket = buffer_wrapper(length);
            this.mergeBuffer.copy(newPacket, 0, 0, length);
            this.handlePacket(newPacket);
            this.mergeBuffer = this.mergeBuffer.slice(length);
        }
    };

    this.handleConnectionError = function (error) {
        if (error.errno === 'ECONNRESET') {
            // Check and call functions if registered for callback disconnected
            if (this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED] !== undefined) {
                this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED](IPConnection.DISCONNECT_REASON_SHUTDOWN);
            }
        }
    };

    this.handleAutoReconnectError = function (error) {
        if (!this.isConnected && this.autoReconnect && error !== IPConnection.ERROR_ALREADY_CONNECTED) {
            // FIXME: add a small sleep here to avoid a tight loop that could consume 100% CPU power
            this.pushTask(this.connectInternal.bind(this, this.host, this.port, this.handleAutoReconnectError), IPConnection.TASK_KIND_AUTO_RECONNECT);
        }
    };

    this.handleConnectionClose = function () {
        if (this.getCurrentTaskKind() === IPConnection.TASK_KIND_DISCONNECT) {
            // This disconnect was requested
            var uid;

            for (uid in this.devices) {
                for (var i=0;i<this.devices[uid].expectedResponses.length;i++) {
                    clearTimeout(this.devices[uid].expectedResponses[i].timeout);

                    if (this.devices[uid].expectedResponses[i].errorCB !== undefined) {
                        this.devices[uid].expectedResponses[i].errorCB(IPConnection.ERROR_TIMEOUT);
                    }
                }

                this.devices[uid].expectedResponses = [];
            }

            this.isConnected = false;
            clearInterval(this.disconnectProbeIID);
            this.disconnectProbeIID = undefined;

            if (this.socket !== undefined) {
                this.socket.end();
                this.socket.destroy();
                this.socket = undefined;
            }

            // Check and call functions if registered for callback disconnected
            if (this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED] !== undefined) {
                this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED](IPConnection.DISCONNECT_REASON_REQUEST);
            }

            this.popTask();
            return;
        }
        // Was connected, disconnected because of error and auto reconnect is enabled
        if (this.isConnected) {
            this.isConnected = false;
            clearInterval(this.disconnectProbeIID);
            this.disconnectProbeIID = undefined;

            if (this.socket !== undefined) {
                this.socket.end();
                this.socket.destroy();
                this.socket = undefined;
            }

            // Check and call functions if registered for callback disconnected
            if (this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED] !== undefined) {
                this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED](IPConnection.DISCONNECT_REASON_ERROR);
            }

            if (this.autoReconnect) {
                this.pushTask(this.connectInternal.bind(this, this.host, this.port, this.handleAutoReconnectError), IPConnection.TASK_KIND_AUTO_RECONNECT);
            }

            return;
        }

        // Were not connected. failed at new connection attempt
        if (this.getCurrentTaskKind() === IPConnection.TASK_KIND_CONNECT || this.getCurrentTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            if (this.connectErrorCallback !== undefined) {
                this.connectErrorCallback(IPConnection.ERROR_CONNECT_FAILED);
            }

            this.popTask();
            return;
        }
    };

    this.resetDisconnectProbe = function() {
        if(this.disconnectProbeIID === undefined) {
            return;
        }

        clearInterval(this.disconnectProbeIID);
        this.disconnectProbeIID = undefined;
        this.disconnectProbeIID = setInterval(this.disconnectProbe.bind(this),
                                              IPConnection.DISCONNECT_PROBE_INTERVAL);
    };

    this.getUIDFromPacket = function (packetUID){
        return packetUID.readUInt32LE(0);
    };

    this.getLengthFromPacket = function (packetLen) {
        return packetLen.readUInt8(4);
    };

    this.getFunctionIDFromPacket = function (packetFID) {
        return packetFID.readUInt8(5);
    };

    this.getSequenceNumberFromPacket = function (packetSeq) {
        return (packetSeq.readUInt8(6) >>> 4) & 0x0F;
    };

    this.getRFromPacket = function (packetR) {
        return (packetR.readUInt8(6) >>> 3) & 0x01;
    };

    this.getEFromPacket = function (packetE) {
        // Getting Error bits(E, 2bits)
        return (packetE.readUInt8(7) >>> 6) & 0x03;
    };

    this.getPayloadFromPacket = function (packetPayload) {
        var payloadReturn = buffer_wrapper(packetPayload.length - 8);
        packetPayload.copy(payloadReturn, 0, 8, packetPayload.length);
        return buffer_wrapper(payloadReturn);
    };

    function mapsToFalse(value) {
        return value === 0 || value === false || value === undefined || value === null || isNaN(value);
    }

    this.pack = function (data, format) {
        var formatArray = format.split(' ');

        if (formatArray.length <= 0) {
            return buffer_wrapper(0);
        }

        var packedBuffer = buffer_wrapper(0);

        for (var i=0; i<formatArray.length; i++){
            if (formatArray[i].split('').length === 1) {
                if (formatArray[i] === 's') {
                    var tmpPackedBuffer = buffer_wrapper(1);
                    tmpPackedBuffer.writeUInt8(data[i].charCodeAt(0), 0);
                    packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                    continue;
                }

                switch (formatArray[i]) {
                    case 'c':
                        var tmpPackedBuffer = buffer_wrapper(1);
                        tmpPackedBuffer.writeUInt8(data[i].charCodeAt(0), 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'b':
                        var tmpPackedBuffer = buffer_wrapper(1);
                        tmpPackedBuffer.writeInt8(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'B':
                        var tmpPackedBuffer = buffer_wrapper(1);
                        tmpPackedBuffer.writeUInt8(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'h':
                        var tmpPackedBuffer = buffer_wrapper(2);
                        tmpPackedBuffer.writeInt16LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'H':
                        var tmpPackedBuffer = buffer_wrapper(2);
                        tmpPackedBuffer.writeUInt16LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'i':
                        var tmpPackedBuffer = buffer_wrapper(4);
                        tmpPackedBuffer.writeInt32LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'I':
                        var tmpPackedBuffer = buffer_wrapper(4);
                        tmpPackedBuffer.writeUInt32LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'q':
                        var tmpPackedBuffer = buffer_wrapper(8);
                        tmpPackedBuffer.writeBigInt64LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'Q':
                        var tmpPackedBuffer = buffer_wrapper(8);
                        tmpPackedBuffer.writeBigUInt64LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'f':
                        var tmpPackedBuffer = buffer_wrapper(4);
                        tmpPackedBuffer.writeFloatLE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'd':
                        var tmpPackedBuffer = buffer_wrapper(8);
                        tmpPackedBuffer.writeDoubleLE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case '?':
                        var tmpPackedBuffer = buffer_wrapper(1);

                        if (mapsToFalse(data[i])) {
                            tmpPackedBuffer.writeUInt8(0x00, 0);
                        } else {
                            tmpPackedBuffer.writeUInt8(0x01, 0);
                        }

                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                }
            }

            if (formatArray[i].split('').length > 1) {
                var singleFormatArray = formatArray[i].split('');

                // Boolean type with cardinality greater than 1
                if (singleFormatArray[0] === '?') {
                    var buffer_value = 0;
                    var count = parseInt(singleFormatArray.slice(1, singleFormatArray.length).join(''));
                    var count_bits = Math.ceil(count / 8);
                    var tmpPackedBuffer = buffer_wrapper(count_bits);

                    for(var _i = 0; _i < count; _i++) {
                        if (mapsToFalse(data[i][_i])) {
                            continue;
                        } else {
                            buffer_value = tmpPackedBuffer.readUInt8(Math.floor(_i / 8));
                            buffer_value |= 1 << (_i % 8);
                            tmpPackedBuffer.writeUInt8(buffer_value, Math.floor(_i / 8));
                        }
                    }

                    packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                    continue;
                }

                for (var j = 0; j < parseInt(formatArray[i].match(/\d/g).join('')); j++) {
                    if (singleFormatArray[0] === 's') {
                        if (!isNaN(data[i].charCodeAt(j))) {
                            var tmpPackedBuffer = buffer_wrapper(1);
                            tmpPackedBuffer.writeUInt8(data[i].charCodeAt(j), 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        } else {
                            var tmpPackedBuffer = buffer_wrapper(1);
                            tmpPackedBuffer.writeUInt8(0x00, 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        }

                        continue;
                    }

                    switch (singleFormatArray[0]) {
                        case 'c':
                            var tmpPackedBuffer = buffer_wrapper(1);
                            tmpPackedBuffer.writeUInt8(data[i][j].charCodeAt(0), 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'b':
                            var tmpPackedBuffer = buffer_wrapper(1);
                            tmpPackedBuffer.writeInt8(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'B':
                            var tmpPackedBuffer = buffer_wrapper(1);
                            tmpPackedBuffer.writeUInt8(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'h':
                            var tmpPackedBuffer = buffer_wrapper(2);
                            tmpPackedBuffer.writeInt16LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'H':
                            var tmpPackedBuffer = buffer_wrapper(2);
                            tmpPackedBuffer.writeUInt16LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'i':
                            var tmpPackedBuffer = buffer_wrapper(4);
                            tmpPackedBuffer.writeInt32LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'I':
                            var tmpPackedBuffer = buffer_wrapper(4);
                            tmpPackedBuffer.writeUInt32LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'q':
                            var tmpPackedBuffer = buffer_wrapper(8);
                            tmpPackedBuffer.writeBigInt64LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'Q':
                            var tmpPackedBuffer = buffer_wrapper(8);
                            tmpPackedBuffer.writeBigUInt64LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'f':
                            var tmpPackedBuffer = buffer_wrapper(4);
                            tmpPackedBuffer.writeFloatLE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'd':
                            var tmpPackedBuffer = buffer_wrapper(8);
                            tmpPackedBuffer.writeDoubleLE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case '?':
                            var tmpPackedBuffer = buffer_wrapper(1);

                            if (mapsToFalse(data[i][j])) {
                                tmpPackedBuffer.writeUInt8(0x00, 0);
                            } else {
                                tmpPackedBuffer.writeUInt8(0x01, 0);
                            }

                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                    }
                }
            }
        }

        return packedBuffer;
    }

    this.unpack = function (unpackPayload, format) {
        var formatArray = format.split(' ');
        var returnArguments = [];
        var returnSubArray = [];
        var constructedString = '';
        var payloadReadOffset = 0;

        if (formatArray.length <= 0) {
            return returnArguments;
        }

        for (var i = 0; i < formatArray.length; i++) {
            if (formatArray[i].split('').length === 1) {
                if (formatArray[i] === 's') {
                    constructedString += String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset));
                    payloadReadOffset++;
                    returnArguments.push(constructedString);
                    constructedString = '';
                    continue;
                }

                switch (formatArray[i]) {
                    case 'c':
                        returnArguments.push(String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset)));
                        payloadReadOffset += 1;
                        continue;
                    case 'b':
                        returnArguments.push(unpackPayload.readInt8(payloadReadOffset));
                        payloadReadOffset += 1;
                        continue;
                    case 'B':
                        returnArguments.push(unpackPayload.readUInt8(payloadReadOffset));
                        payloadReadOffset += 1;
                        continue;
                    case 'h':
                        returnArguments.push(unpackPayload.readInt16LE(payloadReadOffset));
                        payloadReadOffset += 2;
                        continue;
                    case 'H':
                        returnArguments.push(unpackPayload.readUInt16LE(payloadReadOffset));
                        payloadReadOffset += 2;
                        continue;
                    case 'i':
                        returnArguments.push(unpackPayload.readInt32LE(payloadReadOffset));
                        payloadReadOffset += 4;
                        continue;
                    case 'I':
                        returnArguments.push(unpackPayload.readUInt32LE(payloadReadOffset));
                        payloadReadOffset += 4;
                        continue;
                    case 'q':
                        returnArguments.push(unpackPayload.readBigInt64LE(payloadReadOffset));
                        payloadReadOffset += 8;
                        continue;
                    case 'Q':
                        returnArguments.push(unpackPayload.readBigUInt64LE(payloadReadOffset));
                        payloadReadOffset += 8;
                        continue;
                    case 'f':
                        returnArguments.push(unpackPayload.readFloatLE(payloadReadOffset));
                        payloadReadOffset += 4;
                        continue;
                    case 'd':
                        returnArguments.push(unpackPayload.readDoubleLE(payloadReadOffset));
                        payloadReadOffset += 8;
                        continue;
                    case '?':
                        returnArguments.push(unpackPayload.readUInt8(payloadReadOffset) !== 0);
                        payloadReadOffset += 1;
                        continue;
                }
            }

            if (formatArray[i].split('').length > 1) {
                var singleFormatArray = formatArray[i].split('');

                // Boolean type with cardinality greater than 1
                if (singleFormatArray[0] === '?') {
                    var count = parseInt(formatArray[i].match(/\d/g).join(''));
                    var payloadBoolArray = new Array(count);
                    var extractedBoolArray = new Array(count);

                    payloadBoolArray.fill(0x00);
                    extractedBoolArray.fill(false);

                    for (var j = 0; j < Math.ceil(count / 8); j++) {
                        payloadBoolArray[j] = unpackPayload.readUInt8(payloadReadOffset);
                        payloadReadOffset++;
                    }

                    for (var j = 0; j < count; j++) {
                        extractedBoolArray[j] = ((payloadBoolArray[Math.floor(j / 8)] & (1 << (j % 8))) != 0);
                    }

                    returnArguments.push(extractedBoolArray);

                    continue;
                }

                if (singleFormatArray[0] === 's') {
                    constructedString = '';
                    skip = false;

                    for (var j = 0; j < parseInt(formatArray[i].match(/\d/g).join('')); j++) {
                        c = String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset));

                        if (c === '\0' || skip) {
                            skip = true;
                        } else {
                            constructedString += c;
                        }

                        payloadReadOffset++;
                    }

                    skip = false;
                    returnArguments.push(constructedString);
                    constructedString = '';
                    continue;
                }

                returnSubArray = [];

                for (var k = 0; k < parseInt(formatArray[i].match(/\d/g).join('')); k++) {
                    switch (singleFormatArray[0]) {
                        case 'c':
                            returnSubArray.push(String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset)));
                            payloadReadOffset += 1;
                            continue;
                        case 'b':
                            returnSubArray.push(unpackPayload.readInt8(payloadReadOffset));
                            payloadReadOffset += 1;
                            continue;
                        case 'B':
                            returnSubArray.push(unpackPayload.readUInt8(payloadReadOffset));
                            payloadReadOffset += 1;
                            continue;
                        case 'h':
                            returnSubArray.push(unpackPayload.readInt16LE(payloadReadOffset));
                            payloadReadOffset += 2;
                            continue;
                        case 'H':
                            returnSubArray.push(unpackPayload.readUInt16LE(payloadReadOffset));
                            payloadReadOffset += 2;
                            continue;
                        case 'i':
                            returnSubArray.push(unpackPayload.readInt32LE(payloadReadOffset));
                            payloadReadOffset += 4;
                            continue;
                        case 'I':
                            returnSubArray.push(unpackPayload.readUInt32LE(payloadReadOffset));
                            payloadReadOffset += 4;
                            continue;
                        case 'q':
                            returnSubArray.push(unpackPayload.readBigInt64LE(payloadReadOffset));
                            payloadReadOffset += 8;
                            continue;
                        case 'Q':
                            returnSubArray.push(unpackPayload.readBigUInt64LE(payloadReadOffset));
                            payloadReadOffset += 8;
                            continue;
                        case 'f':
                            returnSubArray.push(unpackPayload.readFloatLE(payloadReadOffset));
                            payloadReadOffset += 4;
                            continue;
                        case 'd':
                            returnSubArray.push(unpackPayload.readDoubleLE(payloadReadOffset));
                            payloadReadOffset += 8;
                            continue;
                        case '?':
                            returnSubArray.push(unpackPayload.readUInt8(payloadReadOffset) !== 0);
                            payloadReadOffset += 1;
                            continue;
                    }
                }

                if (returnSubArray.length !== 0) {
                    returnArguments.push(returnSubArray);
                    returnSubArray = [];
                    continue;
                }
            }
        }

        return returnArguments;
    }

    this.sendRequest = function (sendRequestDevice,
                                 sendRequestFID,
                                 sendRequestData,
                                 sendRequestPackFormat,
                                 sendRequestExpectedResponseLength,
                                 sendRequestUnpackFormat,
                                 sendRequestReturnCB,
                                 sendRequestErrorCB,
                                 startStreamResponseTimer,
                                 checkValidity) {
        if (this.getConnectionState() !== IPConnection.CONNECTION_STATE_CONNECTED) {
            if (sendRequestErrorCB !== undefined) {
                sendRequestErrorCB(IPConnection.ERROR_NOT_CONNECTED);
            }

            return;
        }

        // Support for 64 bit integers exists only in node 10.2 or higher
        if ((typeof Buffer.alloc(0).writeBigInt64LE !== "function")
            && ((sendRequestPackFormat.indexOf('q') > -1)
            || (sendRequestPackFormat.indexOf('Q') > -1)
            || (sendRequestUnpackFormat.indexOf('q') > -1)
            || (sendRequestUnpackFormat.indexOf('Q') > -1))) {
            if (sendRequestErrorCB !== undefined) {
                sendRequestErrorCB(IPConnection.ERROR_INT64_NOT_SUPPORTED);
            }

            return;
        }

        if (checkValidity) {
            sendRequestDevice.checkValidity(function () {
                this.sendRequestInternal(sendRequestDevice,
                                         sendRequestFID,
                                         sendRequestData,
                                         sendRequestPackFormat,
                                         sendRequestExpectedResponseLength,
                                         sendRequestUnpackFormat,
                                         sendRequestReturnCB,
                                         sendRequestErrorCB,
                                         startStreamResponseTimer);
            }.bind(this),
            sendRequestErrorCB);
        } else {
            this.sendRequestInternal(sendRequestDevice,
                                     sendRequestFID,
                                     sendRequestData,
                                     sendRequestPackFormat,
                                     sendRequestExpectedResponseLength,
                                     sendRequestUnpackFormat,
                                     sendRequestReturnCB,
                                     sendRequestErrorCB,
                                     startStreamResponseTimer);
        }
    }

    this.sendRequestInternal = function (sendRequestDevice,
                                         sendRequestFID,
                                         sendRequestData,
                                         sendRequestPackFormat,
                                         sendRequestExpectedResponseLength,
                                         sendRequestUnpackFormat,
                                         sendRequestReturnCB,
                                         sendRequestErrorCB,
                                         startStreamResponseTimer) {
        // Packet creation
        var sendRequestPayload = this.pack(sendRequestData, sendRequestPackFormat);
        var sendRequestHeader = this.createPacketHeader(sendRequestDevice,
                                                        8+sendRequestPayload.length,
                                                        sendRequestFID,
                                                        sendRequestErrorCB);

        if (sendRequestHeader === undefined) {
            return;
        }

        var sendRequestPacket = bufferConcat([sendRequestHeader, sendRequestPayload]);
        var sendRequestSEQ = this.getSequenceNumberFromPacket(sendRequestHeader);
        var responseExpected = sendRequestDevice.getResponseExpected(sendRequestFID);

        // Sending the created packet
        if (responseExpected) {
            // Setting the requesting current device's current request
            var sendRequestDeviceOID = sendRequestDevice.getDeviceOID();

            if (!startStreamResponseTimer) {
                sendRequestDevice.expectedResponses.push({
                    DeviceOID:sendRequestDeviceOID,
                    FID:sendRequestFID,
                    SEQ:sendRequestSEQ,
                    unpackFormat:sendRequestUnpackFormat,
                    expectedResponseLength:sendRequestExpectedResponseLength,
                    timeout:setTimeout(this.sendRequestTimeout.bind(this,
                                                                    sendRequestDevice,
                                                                    sendRequestDeviceOID,
                                                                    sendRequestErrorCB),
                                       this.timeout),
                    returnCB:sendRequestReturnCB,
                    errorCB:sendRequestErrorCB
                });
            } else {
                // Setup streaming timer
                if (sendRequestFID in sendRequestDevice.streamStateObjects) {
                    if (sendRequestDevice.streamStateObjects[sendRequestFID]['responseProperties']['timeout'] !== null) {
                        clearTimeout(sendRequestDevice.streamStateObjects[sendRequestFID]['responseProperties']['timeout']);
                        sendRequestDevice.streamStateObjects[sendRequestFID]['responseProperties']['timeout'] = null;
                    }

                    sendRequestDevice.streamStateObjects[sendRequestFID]['responseProperties']['timeout'] =
                        setTimeout(this.sendRequestTimeoutStreamOut.bind(this,
                                                                         sendRequestDevice,
                                                                         sendRequestFID,
                                                                         sendRequestErrorCB),

                                   this.timeout);
                }
            }
        }

        this.socket.write(sendRequestPacket, true);

        if (!responseExpected && sendRequestReturnCB !== undefined) {
            eval('sendRequestReturnCB();');
        }
    };

    this.sendRequestTimeout = function (timeoutDevice, timeoutDeviceOID, timeoutErrorCB) {
        for (var i = 0; i < timeoutDevice.expectedResponses.length; ++i) {
            if (timeoutDevice.expectedResponses[i].DeviceOID === timeoutDeviceOID) {
                clearTimeout(timeoutDevice.expectedResponses[i].timeout);
                timeoutDevice.expectedResponses.splice(i, 1);

                if (timeoutErrorCB !== undefined){
                    timeoutErrorCB(IPConnection.ERROR_TIMEOUT);
                }

                return;
            }
        }
    };

    this.sendRequestTimeoutStreamOut = function (timeoutDevice, timeoutFID, timeoutErrorCB) {
        var streamOutObject = null;

        if (!(timeoutFID in timeoutDevice.streamStateObjects)) {
            return;
        }

        streamOutObject = timeoutDevice.streamStateObjects[timeoutFID];

        if (streamOutObject === null) {
            return;
        }

        // Clear timer
        clearTimeout(streamOutObject['responseProperties']['timeout']);

        // Call error callback (if any)
        if (streamOutObject['responseProperties']['errorCB'] !== undefined) {
            streamOutObject['responseProperties']['errorCB'](IPConnection.ERROR_TIMEOUT);
        }

        // Reset stream state object
        timeoutDevice.resetStreamStateObject(streamOutObject);

        // Call next function from call queue (if any)
        if (streamOutObject['responseProperties']['callQueue'].length > 0) {
            streamOutObject['responseProperties']['callQueue'].shift()(timeoutDevice);
        }
    };

    this.handleResponse = function (packetResponse) {
        var streamStateObject = null;
        var handleResponseDevice = null;
        var handleResponseFID = this.getFunctionIDFromPacket(packetResponse);
        var handleResponseSEQ = this.getSequenceNumberFromPacket(packetResponse);

        handleResponseDevice = this.devices[this.getUIDFromPacket(packetResponse)];

        if (handleResponseDevice === undefined) {
            return;
        }

        // Handle non-streamed response
        if (!(handleResponseFID in handleResponseDevice.streamStateObjects)) {
            for (var i = 0; i < handleResponseDevice.expectedResponses.length; i++) {
                var expectedResponse = handleResponseDevice.expectedResponses[i];

                if (expectedResponse.FID === handleResponseFID &&
                    expectedResponse.SEQ === handleResponseSEQ) {
                    clearTimeout(expectedResponse.timeout);

                    if (this.getEFromPacket(packetResponse) === 1) {
                        if (expectedResponse.errorCB !== undefined) {
                            eval('expectedResponse.errorCB(IPConnection.ERROR_INVALID_PARAMETER);');
                        }

                        handleResponseDevice.expectedResponses.splice(i, 1);
                        return;
                    }

                    if (this.getEFromPacket(packetResponse) === 2) {
                        if (expectedResponse.errorCB !== undefined) {
                            eval('expectedResponse.errorCB(IPConnection.ERROR_FUNCTION_NOT_SUPPORTED);');
                        }

                        handleResponseDevice.expectedResponses.splice(i, 1);
                        return;
                    }

                    if (this.getEFromPacket(packetResponse) !== 0) {
                        if (expectedResponse.errorCB !== undefined) {
                            eval('expectedResponse.errorCB(IPConnection.ERROR_UNKNOWN_ERROR);');
                        }

                        handleResponseDevice.expectedResponses.splice(i, 1);
                        return;
                    }

                    if (expectedResponse.expectedResponseLength === 0) {
                        // setter with response-expected enabled
                        expectedResponse.expectedResponseLength = 8;
                    }

                    if (packetResponse.length != expectedResponse.expectedResponseLength) {
                        if (expectedResponse.errorCB !== undefined) {
                            eval('expectedResponse.errorCB(IPConnection.ERROR_WRONG_RESPONSE_LENGTH);');
                        }

                        handleResponseDevice.expectedResponses.splice(i, 1);
                        return;
                    }

                    if (expectedResponse.returnCB !== undefined) {
                        var retArgs = this.unpack(this.getPayloadFromPacket(packetResponse),
                                                  expectedResponse.unpackFormat);
                        var evalStr = 'expectedResponse.returnCB(';

                        for (var j = 0; j < retArgs.length; j++) {
                            eval('var retSingleArg' + j + ' = retArgs[' + j + '];');

                            evalStr += 'retSingleArg' + j;

                            if (j != retArgs.length - 1) {
                                evalStr += ', ';
                            }
                        }

                        eval(evalStr + ');');
                    }

                    handleResponseDevice.expectedResponses.splice(i, 1);
                    return;
                }
            }
        }
        // Handle streamed response
        else {
            streamStateObject = handleResponseDevice.streamStateObjects[handleResponseFID];

            if (streamStateObject === null) {
                return;
            }

            if (!streamStateObject['responseProperties']['running']) {
                handleResponseDevice.resetStreamStateObject(streamStateObject);
                return;
            }

            if (streamStateObject['responseProperties']['responseHandler'] === null) {
                handleResponseDevice.resetStreamStateObject(streamStateObject);
                return;
            }

            streamStateObject['responseProperties']['responseHandler'](handleResponseDevice,
                                                                       handleResponseFID,
                                                                       packetResponse);
        }
    };

    this.handleCallback = function (packetCallback) {
        var functionID = this.getFunctionIDFromPacket(packetCallback);

        if (functionID === IPConnection.CALLBACK_ENUMERATE) {
            var registeredCallback = this.registeredCallbacks[IPConnection.CALLBACK_ENUMERATE];

            if (registeredCallback !== undefined) {
                if (packetCallback.length != 34) {
                    return; // silently ignoring callback with wrong length
                }

                var args = this.unpack(this.getPayloadFromPacket(packetCallback), 's8 s8 c B3 B3 H B');
                var evalCBString = 'registeredCallback(';

                for (var i = 0; i < args.length; i++) {
                    eval('var cbArg' + i + ' = args[' + i + '];');

                    evalCBString += 'cbArg' + i;

                    if (i != args.length - 1) {
                        evalCBString += ', ';
                    }
                }

                eval(evalCBString + ');');
            }

            return;
        }

        var device = this.devices[this.getUIDFromPacket(packetCallback)];

        if (device === undefined) {
            return;
        }

        if ((device.registeredCallbacks[functionID] === undefined &&
             device.registeredCallbacks[-functionID] === undefined) ||
             device.callbackFormats[functionID] === undefined) {
            return;
        }

        var cbFunction = undefined;
        var cbUnpack = undefined;

        if (device.registeredCallbacks[functionID] !== undefined) {
            cbFunction = device.registeredCallbacks[functionID];
            cbUnpack = device.callbackFormats[functionID];
        } else if (device.registeredCallbacks[-functionID] !== undefined) {
            cbFunction = device.registeredCallbacks[-functionID];
            cbUnpack = device.callbackFormats[functionID];
        }

        if (cbFunction === undefined || cbUnpack === undefined) {
            return;
        }

        if (packetCallback.length != cbUnpack[0]) {
            return; // silently ignoring callback with wrong length
        }

        // llvalues is an array with unpacked values
        var llvalues = this.unpack(this.getPayloadFromPacket(packetCallback), cbUnpack[1]);

        // Process high-level callback
        if (-functionID in device.registeredCallbacks) {
            var length = 0;
            var chunkOffset = 0;
            var chunkData = null;
            var hlcb = device.highLevelCallbacks[-functionID];
            // FIXME: currently assuming that cbUnpack is longer than 1
            var data = null;
            var hasData = false;

            if (hlcb[1]['fixedLength'] !== null) {
                length = hlcb[1]['fixedLength'];
            } else {
                length = llvalues[hlcb[0].indexOf('streamLength')];
            }

            if (!hlcb[1]['singleChunk']) {
                chunkOffset = llvalues[hlcb[0].indexOf('streamChunkOffset')];
            } else {
                chunkOffset = 0;
            }

            chunkData = llvalues[hlcb[0].indexOf('streamChunkData')];

            if (hlcb[2] === null) { // No stream in-progress
                if (chunkOffset === 0) { // Stream starts
                    hlcb[2] = chunkData;

                    if (hlcb[2].length >= length) { // Stream complete
                        hasData = true;
                        data = hlcb[2].splice(0, length);
                    }
                } else {
                    // Ignore tail of current stream, wait for next stream start
                }
            } else { // Stream in-progress
                if (chunkOffset !== hlcb[2].length) { // Stream out-of-sync
                    hasData = true;
                    data = null;
                } else { // Stream in-sync
                    hlcb[2] = hlcb[2].concat(chunkData);

                    if (hlcb[2].length >= length) { // Stream complete
                        hasData = true;
                        data = hlcb[2].splice(0, length);
                    }
                }
            }

            var registeredCallback = device.registeredCallbacks[-functionID];

            if (hasData && registeredCallback !== undefined) {
                var result = [];
                var rolesMappedData = [];
                var evalCBString = 'registeredCallback(';

                for (var i = 0; i < hlcb[0].length; i++) {
                    rolesMappedData.push({'role': hlcb[0][i], 'llvalue': llvalues[i]});
                }

                for (var i = 0; i < rolesMappedData.length; i++) {
                    if (rolesMappedData[i]['role'] === 'streamChunkData') {
                        result.push(data);
                    } else if (rolesMappedData[i]['role'] === null) {
                        result.push(rolesMappedData[i]['llvalue']);
                    }
                }

                for (var i = 0; i < result.length; i++) {
                    eval('var cbArg' + i + ' = result[' + i + '];');

                    evalCBString += 'cbArg' + i;

                    if (i != result.length - 1) {
                        evalCBString += ', ';
                    }
                }

                hlcb[2] = null;

                eval(evalCBString + ');');
            }
        }

        // Process normal or low-level callbacks
        var registeredCallback = device.registeredCallbacks[functionID];

        if (registeredCallback !== undefined) {
            var evalCBString = 'registeredCallback(';

            for (var i = 0; i < llvalues.length; i++) {
                eval('var cbArg' + i + ' = llvalues[' + i + '];');

                evalCBString += 'cbArg' + i;

                if (i != llvalues.length - 1) {
                    evalCBString += ', ';
                }
            }

            eval(evalCBString + ');');
        }
    };

    this.handlePacket = function (packet) {
        if (this.getSequenceNumberFromPacket(packet) === 0) {
            this.handleCallback(packet);
        }

        if (this.getSequenceNumberFromPacket(packet) > 0) {
            this.handleResponse(packet);
        }
    };

    this.getConnectionState = function () {
        if (this.isConnected) {
            return IPConnection.CONNECTION_STATE_CONNECTED;
        }

        if (this.getCurrentTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            return IPConnection.CONNECTION_STATE_PENDING;
        }

        return IPConnection.CONNECTION_STATE_DISCONNECTED;
    };

    this.setAutoReconnect = function (autoReconnect) {
        this.autoReconnect = autoReconnect;
    };

    this.getAutoReconnect = function () {
        return this.autoReconnect;
    };

    this.setTimeout = function (timeout) {
        this.timeout = timeout;
    };

    this.getTimeout = function () {
        return this.timeout;
    };

    this.enumerate = function (errorCallback) {
        if (this.getConnectionState() !== IPConnection.CONNECTION_STATE_CONNECTED) {
            if (errorCallback !== undefined) {
                errorCallback(IPConnection.ERROR_NOT_CONNECTED);
            }

            return;
        }

        this.socket.write(this.createPacketHeader(undefined, 8, IPConnection.FUNCTION_ENUMERATE), true);
    };

    this.getRandomUInt32 = function (returnCallback) {
        if (process.browser) {
            if (typeof window !== 'undefined' && window.crypto && window.crypto.getRandomValues) {
                var r = new Uint32Array(1);
                window.crypto.getRandomValues(r);
                returnCallback(r[0]);
            } else if (typeof window !== 'undefined' && window.msCrypto && window.msCrypto.getRandomValues) {
                var r = new Uint32Array(1);
                window.msCrypto.getRandomValues(r);
                returnCallback(r[0]);
            } else {
                // fallback to non-crypto random numbers
                returnCallback(Math.ceil(Math.random() * 4294967295));
            }
        } else {
            var crypto = require('crypto');

            crypto.randomBytes(4, function(error, buffer) {
                if (error) {
                    crypto.pseudoRandomBytes(4, function(error, buffer) {
                        if (error) {
                            returnCallback(Math.ceil(Math.random() * 4294967295));
                        } else {
                            var data = buffer_wrapper(buffer);
                            returnCallback(data.readUInt32LE(0));
                        }
                    });
                } else {
                    var data = buffer_wrapper(buffer);
                    returnCallback(data.readUInt32LE(0));
                }
            });
        }
    };

    function isASCII(s) {
        for (var i = 0; i < s.length; ++i) {
            if (s.charCodeAt(i) > 0x7f) {
                return false;
            }
        }
        return true;
    }

    this.authenticateInternal = function (secret, returnCallback, errorCallback) {
        if (!isASCII(secret)) {
            errorCallback(IPConnection.ERROR_NON_ASCII_CHAR_IN_SECRET);
        }

        this.brickd.getAuthenticationNonce(function (serverNonce) {
            var clientNonceNumber = this.nextAuthenticationNonce++;
            var clientNonceBytes = this.pack([clientNonceNumber], 'I');
            var clientNonce = this.unpack(clientNonceBytes, 'B4')[0];
            var combinedNonceBytes = this.pack([serverNonce, clientNonce], 'B4 B4');
            var crypto = require('crypto');
            var hmac = crypto.createHmac('sha1', secret);

            hmac.update(combinedNonceBytes);

            var digestBytes = hmac.digest();
            var digest = this.unpack(digestBytes, 'B20')[0];

            this.brickd.authenticate(clientNonce, digest,
                function () {
                    if (returnCallback !== undefined) {
                        returnCallback();
                    }

                    this.popTask();
                }.bind(this),
                function (error) {
                    if (errorCallback !== undefined) {
                        errorCallback(error);
                    }

                    this.popTask();
                }.bind(this)
            );
        }.bind(this), function (error) {
            if (errorCallback !== undefined) {
                errorCallback(error);
            }

            this.popTask();
        }.bind(this));
    };

    this.authenticate = function (secret, returnCallback, errorCallback) {
        // need to do authenticate() as a task because two authenticate() calls
        // are not allowed to overlap, otherwise the correct order of operations
        // in the handshake process cannot be guaranteed
        this.pushTask(function () {
            if (this.nextAuthenticationNonce === 0) {
                this.getRandomUInt32(function (r) {
                    this.nextAuthenticationNonce = r;
                    this.authenticateInternal(secret, returnCallback, errorCallback);
                }.bind(this));
            } else {
                this.authenticateInternal(secret, returnCallback, errorCallback);
            }
        }.bind(this), IPConnection.TASK_KIND_AUTHENTICATE);
    };

    this.on = function (callbackID, function_) {
        this.registeredCallbacks[callbackID] = function_;
    };

    this.getNextSequenceNumber = function () {
        if (this.nextSequenceNumber >= 15) {
            this.nextSequenceNumber = 0;
        }

        return ++this.nextSequenceNumber;
    };

    this.createPacketHeader = function (headerDevice, headerLength, headerFunctionID, headerErrorCB) {
        var UID = IPConnection.BROADCAST_UID;
        var len = headerLength;
        var FID = headerFunctionID;
        var seq = this.getNextSequenceNumber();
        var responseBits = 0;
        var EFutureUse = 0;
        var returnOnError = false;

        if (headerDevice !== undefined) {
            var responseExpected = headerDevice.getResponseExpected(headerFunctionID,
                function (errorCode) {
                    returnOnError = true;

                    if (headerErrorCB !== undefined) {
                        headerErrorCB(errorCode);
                    }
                }
            );

            if (returnOnError) {
                returnOnError = false;
                return;
            }

            UID = headerDevice.uid;

            if (responseExpected) {
                responseBits = 1;
            }
        }

        var seqResponseOOBits = seq << 4;

        if (responseBits) {
            seqResponseOOBits |= (responseBits << 3);
        }

        var returnHeader = buffer_wrapper(8);
        returnHeader.writeUInt32LE(UID, 0);
        returnHeader.writeUInt8(len, 4);
        returnHeader.writeUInt8(FID, 5);
        returnHeader.writeUInt8(seqResponseOOBits, 6);
        returnHeader.writeUInt8(EFutureUse , 7);

        return returnHeader;
    };

    this.createChunkData = function(data, chunkOffset, chunkLength, chunkPadding) {
        var padding = null;
        var chunkData = data.slice(chunkOffset, chunkOffset + chunkLength);

        if (chunkData.length < chunkLength) {
            padding = new Array(chunkLength - chunkData.length);
            padding.fill(chunkPadding);
            chunkData = chunkData.concat(padding);
        }

        return chunkData;
    };

    function bufferConcat(arrayOfBuffers) {
        var newBufferSize = 0;
        var targetStart = 0;

        for (var i = 0; i < arrayOfBuffers.length; i++) {
            newBufferSize += arrayOfBuffers[i].length;
        }

        var returnBufferConcat = buffer_wrapper(newBufferSize);

        for (var j = 0; j < arrayOfBuffers.length; j++) {
            arrayOfBuffers[j].copy(returnBufferConcat, targetStart);
            targetStart += arrayOfBuffers[j].length;
        }

        return returnBufferConcat;
    }

    // new Buffer() is deprecated since nodejs v10.0.0. Use recommended replacements
    // as described here: https://nodejs.org/en/docs/guides/buffer-constructor-deprecation
    // Fallback to buffer constructor to be compatible to v0.10.x.
    function buffer_wrapper(size_or_array, encoding) {
        if (typeof size_or_array === 'number') {
            if (Buffer.alloc) {
                return Buffer.alloc(size_or_array);
            }

            var buf = new Buffer(size_or_array);
            buf.fill(0);
            return buf;
        } else {
            if (Buffer.from && Buffer.from !== Uint8Array.from) {
                return Buffer.from(size_or_array, encoding);
            }

            return new Buffer(size_or_array, encoding);
        }
    }
}

module.exports = IPConnection;

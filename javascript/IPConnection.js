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
IPConnection.CONNECTION_STATE_PENDING = 2; //auto-reconnect in process
IPConnection.DISCONNECT_PROBE_INTERVAL = 5000;
IPConnection.RETRY_CONNECTION_INTERVAL = 2000;
// Error codes
IPConnection.ERROR_ALREADY_CONNECTED = 11;
IPConnection.ERROR_NOT_CONNECTED = 12;
IPConnection.ERROR_AUTO_RECONNECT_IN_PROGRESS = 13;
IPConnection.ERROR_CONNECT_FAILED = 14;
IPConnection.ERROR_INVALID_FUNCTION_ID = 21;
IPConnection.ERROR_TIMEOUT = 31;
IPConnection.ERROR_INVALID_PARAMETER = 41;
IPConnection.ERROR_FUNCTION_NOT_SUPPORTED = 42;
IPConnection.ERROR_UNKNOWN_ERROR = 43;

IPConnection.TASK_KIND_CONNECT = 0;
IPConnection.TASK_KIND_DISCONNECT = 1;
IPConnection.TASK_KIND_AUTO_RECONNECT = 2;

// Socket implementation for Node.js and Websocket. 
// The API resembles the Node.js API.
function TFSocket(PORT, HOST) {
    this.port = PORT;
    this.host = HOST;
    this.socket = null;
    
    if(process.browser) {
        var webSocketURL = "ws://" + this.host + ":" + this.port + "/"
        if (typeof MozWebSocket != "undefined") {
            this.socket = new MozWebSocket(webSocketURL, "tfp");
        }
        else {
            this.socket = new WebSocket(webSocketURL, "tfp");
        }
        this.socket.binaryType = 'arraybuffer';
    }
    else {
        var net = require('net');
        this.socket = new net.Socket();
    }
    this.on = function(str, func) {
        if(process.browser) {
            switch(str) {
                case "connect":
                    this.socket.onopen = func;
                    break;
                case "data":
                    // Websockets in browsers return a MessageEvent. We just
                    // expose the data from the event as a Buffer as in Node.js.
                    this.socket.onmessage = function(messageEvent) {
                        data = new Buffer(new Uint8Array(messageEvent.data))
                        func(data);
                    };
                    break;
                case "error":
                    // There is no easy way to get errno for error in browser websockets.
                    // We assume error['errno'] === 'ECONNRESET'
                    this.socket.onerror = function() {
                        var error = {"errno": "ECONNRESET"};
                        func(error);
                    };
                    break;
                case "close":
                    this.socket.onclose = func;
                    break;
            } 
        }
        else {
            this.socket.on(str, func);
        }
    }
    this.connect = function() {
        if(process.browser) {
            // In the browser we already connected by creating a WebSocket object
        }
        else {
            this.socket.connect(this.port, this.host, null);
        }
    }
    this.setNoDelay = function(value) {
        if(process.browser) {
            // Currently no API available in browsers
			// But Nagle algorithm seems te be turned off in most browsers by default anyway
        }
        else {
            this.socket.setNoDelay(value);
        }
    }
    this.write = function(data) {
        if(process.browser) {
            this.socket.send(data); 
        }
        else {
            this.socket.write(data);
        }
    }
	this.end = function() {
		if(process.browser) {
			this.socket.close();
        }
        else {
            this.socket.end();
        }
	}
	this.destroy = function() {
		if(process.browser) {
			// There is no end/destroy in browser socket, so we close in end
			// and do nothing in destroy
        }
        else {
            this.socket.destroy();
        }
	}
}

// the IPConnection class and constructor
function IPConnection() {
    // Creates an IP Connection object that can be used to enumerate the available
    // devices. It is also required for the constructor of Bricks and Bricklets.
    this.host = undefined;
    this.port = undefined;
    this.timeout = 2500;
    this.autoReconnect = true;
    this.autoReconnectPending = false;
    this.sequenceNumber = 0;
    this.authKey = undefined;
    this.devices = {};
    this.registeredCallbacks = {};
    this.socket = undefined;
    this.disconnectProbeIID = undefined;
    this.taskQueue = [];
    this.isConnected = false;
    this.connectErrorCallback = undefined;
    this.disconnectErrorCallback = undefined;
    this.mergeBuffer = new Buffer(0);
    
    this.disconnectProbe = function() {
        if(this.socket !== undefined) {
            this.socket.write(this.createPacketHeader(undefined, 8, IPConnection.FUNCTION_DISCONNECT_PROBE));
        }
    };
    this.pushTask = function(handler, kind) {
        this.taskQueue.push({"handler":handler, "kind":kind});

        if (this.taskQueue.length === 1) {
            this.executeTask();
        }
    };
    this.executeTask = function() {
        var task = this.taskQueue[0];

        if (task !== undefined) {
            task.handler();
        }
    };
    this.popTask = function() {
        this.taskQueue.splice(0, 1);
        this.executeTask();
    };
    this.removeNextTask = function() {
        this.taskQueue.splice(1, 1);
    };
    this.getCurrentTaskKind = function() {
        var task = this.taskQueue[0];

        if (task !== undefined) {
            return task.kind;
        }

        return undefined;
    };
    this.getNextTaskKind = function() {
        var task = this.taskQueue[1];

        if (task !== undefined) {
            return task.kind;
        }

        return undefined;
    };
    this.disconnect = function(disconnectErrorCallback) {
        this.pushTask(this.disconnectInternal.bind(this, disconnectErrorCallback), IPConnection.TASK_KIND_DISCONNECT);
    };
    this.disconnectInternal = function(disconnectErrorCallback) {
        var autoReconnectAborted = false;

        if (this.getNextTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            // Remove auto-reconnect task, to break recursion
            this.removeNextTask();
            autoReconnectAborted = true;
        }

        if (!this.isConnected) {
            if (!autoReconnectAborted && disconnectErrorCallback !== undefined) {
                disconnectErrorCallback(IPConnection.ERROR_NOT_CONNECTED);
            }

            this.popTask();
            return;
        }

        this.disconnectErrorCallback = disconnectErrorCallback;

        this.socket.end();
        this.socket.destroy();
        return;
    };
    this.connect = function(host, port, connectErrorCallback) {
        this.pushTask(this.connectInternal.bind(this, host, port, connectErrorCallback), IPConnection.TASK_KIND_CONNECT);
    };
    this.connectInternal = function(host, port, connectErrorCallback) {
        if (this.isConnected) {
            if (connectErrorCallback !== undefined) {
                connectErrorCallback(IPConnection.ERROR_ALREADY_CONNECTED);
            }

            this.popTask();
            return;
        }

        clearInterval(this.disconnectProbeIID);

        this.connectErrorCallback = connectErrorCallback;
        this.host = host;
        this.port = port;
        this.socket = new TFSocket(this.port, this.host);
        this.socket.setNoDelay(true);
        this.socket.on('connect', this.handleConnect.bind(this));
        this.socket.on('data', this.handleIncomingData.bind(this));
        this.socket.on('error', this.handleConnectionError.bind(this));
        this.socket.on('close', this.handleConnectionClose.bind(this));
        this.socket.connect();
    };
    this.handleConnect = function() {
        var connectReason = IPConnection.CONNECT_REASON_REQUEST;

        if(this.getCurrentTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            connectReason = IPConnection.CONNECT_REASON_AUTO_RECONNECT;
        }

        clearInterval(this.disconnectProbeIID);
        this.isConnected = true;
        
        // Check and call functions if registered for callback connected
        if(this.registeredCallbacks[IPConnection.CALLBACK_CONNECTED] !== undefined) {
            this.registeredCallbacks[IPConnection.CALLBACK_CONNECTED](connectReason);
        }
        
        this.disconnectProbeIID = setInterval(this.disconnectProbe.bind(this),
                                                   IPConnection.DISCONNECT_PROBE_INTERVAL);

        this.popTask();
    };
    this.handleIncomingData = function(data) {
        if(data.length === 0) {
            return;
        }
        this.mergeBuffer = bufferConcat([this.mergeBuffer, data]);
        if(this.mergeBuffer.length < 8) {
            return;
        }
        if(this.mergeBuffer.length < this.mergeBuffer.readUInt8(4)) {
            return;
        }
        while(this.mergeBuffer.length >= 8) {
            var newPacket = new Buffer(this.mergeBuffer.readUInt8(4));
            this.mergeBuffer.copy(newPacket, 0, 0, this.mergeBuffer.readUInt8(4));
            this.handlePacket(newPacket);
            this.mergeBuffer = this.mergeBuffer.slice(this.mergeBuffer.readUInt8(4));
        }
    };
    this.handleConnectionError = function(error) {
        if(error['errno'] === 'ECONNRESET') {
            // Check and call functions if registered for callback disconnected
            if(this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED] !== undefined) {
                this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED](IPConnection.DISCONNECT_REASON_SHUTDOWN);
            }
        }
    };
    this.handleAutoReconnectError = function(error) {
        if (!this.isConnected && this.autoReconnect && error != IPConnection.ERROR_ALREADY_CONNECTED) {
            this.pushTask(this.connectInternal.bind(this, this.host, this.port, this.handleAutoReconnectError), IPConnection.TASK_KIND_AUTO_RECONNECT);
        }
    }
    this.handleConnectionClose = function() {
        if(this.getCurrentTaskKind() === IPConnection.TASK_KIND_DISCONNECT) {
            // This disconnect was requested
            for(var uid in this.devices) {
                for(var i=0;i<this.devices[uid].expectedResponses.length;i++) {
                    clearTimeout(this.devices[uid].expectedResponses[i].timeout);

                    if (this.devices[uid].expectedResponses[i].errorCB !== undefined) {
                        this.devices[uid].expectedResponses[i].errorCB(IPConnection.ERROR_TIMEOUT);
                    }
                }
                this.devices[uid].expectedResponses = [];
            }
            this.isConnected = false;
            clearInterval(this.disconnectProbeIID);
            if(this.socket !== undefined) {
                this.socket.end();
                this.socket.destroy();
                this.socket = undefined;
            }
            // Check and call functions if registered for callback disconnected
            if(this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED] !== undefined) {
                this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED](IPConnection.DISCONNECT_REASON_REQUEST);
            }
            this.popTask();
            return;
        }
        // Was connected, disconnected because of error and auto reconnect is enabled
        if(this.isConnected) {
            this.isConnected = false;
            clearInterval(this.disconnectProbeIID);
            if(this.socket !== undefined) {
                this.socket.end();
                this.socket.destroy();
                this.socket = undefined;
            }
            // Check and call functions if registered for callback disconnected
            if(this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED] !== undefined) {
                this.registeredCallbacks[IPConnection.CALLBACK_DISCONNECTED](IPConnection.DISCONNECT_REASON_ERROR);
            }
            if (this.autoReconnect) {
                this.pushTask(this.connectInternal.bind(this, this.host, this.port, this.handleAutoReconnectError), IPConnection.TASK_KIND_AUTO_RECONNECT);
            }
            return;
        }
        // Were not connected. failed at new connection attempt
        if(this.getCurrentTaskKind() === IPConnection.TASK_KIND_CONNECT || this.getCurrentTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            if (this.connectErrorCallback !== undefined) {
                this.connectErrorCallback(IPConnection.ERROR_CONNECT_FAILED);
            }
            this.popTask();
            return;
        }
    };
    this.getUIDFromPacket = function(packetUID){
        return packetUID.readUInt32LE(0);
    };
    this.getLengthFromPacket = function(packetLen) {
        return packetLen.readUInt8(4);
        
    };
    this.getFunctionIDFromPacket = function(packetFID) {
        return packetFID.readUInt8(5);
    };
    this.getSequenceNumberFromPacket = function(packetSeq) {
        return (packetSeq.readUInt8(6) >>> 4) & 0x0F;
    };
    this.getRFromPacket = function(packetR) {
        return (packetR.readUInt8(6) >>> 3) & 0x01;
    };
    this.getAFromPacket = function(packetA) {
        return (packetA.readUInt8(6) >>> 2) & 0x01;
    };
    this.getOOFromPacket = function(packetOO) {
        return packetOO.readUInt8(6) & 0x03;
    };
    this.getEFromPacket = function(packetE) {
        // Getting Error bits(E, 2bits)
        return (packetE.readUInt8(7) >>> 6) & 0x03;
    };
    this.getFutureUseFromPacket = function(packetFutureUse) {
        // Getting Future Use(6bits)
        return (packetFutureUse.readUInt8(7) >>> 6) & 0x63;
    };
    this.getPayloadFromPacket = function(packetPayload) {
        var payloadReturn = new Buffer(packetPayload.length - 8);
        packetPayload.copy(payloadReturn, 0, 8, packetPayload.length);
        return new Buffer(payloadReturn);
    };
    function pack(data, format) {
        var formatArray = format.split(' ');
        if(formatArray.length <= 0) {
            return new Buffer(0);
        }
        var packedBuffer = new Buffer(0);
        for(var i=0; i<formatArray.length; i++){
            if(formatArray[i].split('').length === 1) {
                if(formatArray[i] === 's') {
                    var tmpPackedBuffer = new Buffer(1);
                    tmpPackedBuffer.fill(0x00);
                    tmpPackedBuffer.writeUInt8(data[i].charCodeAt(0), 0);
                    packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                    continue;
                }
                switch(formatArray[i]) {
                    case 'c':
                        var tmpPackedBuffer = new Buffer(1);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeUInt8(data[i].charCodeAt(0), 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'b':
                        var tmpPackedBuffer = new Buffer(1);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeInt8(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'B':
                        var tmpPackedBuffer = new Buffer(1);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeUInt8(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'h':
                        var tmpPackedBuffer = new Buffer(2);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeInt16LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'H':
                        var tmpPackedBuffer = new Buffer(2);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeUInt16LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'i':
                        var tmpPackedBuffer = new Buffer(4);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeInt32LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'I':
                        var tmpPackedBuffer = new Buffer(4);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeUInt32LE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'q':
                        var tmpPackedBuffer = new Buffer(8);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeDoubleLE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'Q':
                        var tmpPackedBuffer = new Buffer(8);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeDoubleLE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'f':
                        var tmpPackedBuffer = new Buffer(4);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeFloatLE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                    case 'd':
                        var tmpPackedBuffer = new Buffer(8);
                        tmpPackedBuffer.fill(0x00);
                        tmpPackedBuffer.writeDoubleLE(data[i], 0);
                        packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        continue;
                }
            }
            if(formatArray[i].split('').length > 1) {
                var singleFormatArray = formatArray[i].split('');
                for(var j=0; j<parseInt(formatArray[i].match(/\d/g).join('')); j++) {
                    if(singleFormatArray[0] === 's') {
                        if(!isNaN(data[i].charCodeAt(j))) {
                            var tmpPackedBuffer = new Buffer(1);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeUInt8(data[i].charCodeAt(j), 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        }
                        else {
                            var tmpPackedBuffer = new Buffer(1);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeUInt8(0x00, 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                        }
                        continue;
                    }
                    switch(singleFormatArray[0]) {
                        case 'c':
                            var tmpPackedBuffer = new Buffer(1);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeUInt8(data[i][j].charCodeAt(0), 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'b':
                            var tmpPackedBuffer = new Buffer(1);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeInt8(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'B':
                            var tmpPackedBuffer = new Buffer(1);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeUInt8(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'h':
                            var tmpPackedBuffer = new Buffer(2);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeInt16LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'H':
                            var tmpPackedBuffer = new Buffer(2);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeUInt16LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'i':
                            var tmpPackedBuffer = new Buffer(4);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeInt32LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'I':
                            var tmpPackedBuffer = new Buffer(4);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeUInt32LE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'q':
                            var tmpPackedBuffer = new Buffer(8);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeDoubleLE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'Q':
                            var tmpPackedBuffer = new Buffer(8);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeDoubleLE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'f':
                            var tmpPackedBuffer = new Buffer(4);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeFloatLE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                        case 'd':
                            var tmpPackedBuffer = new Buffer(8);
                            tmpPackedBuffer.fill(0x00);
                            tmpPackedBuffer.writeDoubleLE(data[i][j], 0);
                            packedBuffer = bufferConcat([packedBuffer,tmpPackedBuffer]);
                            continue;
                    }
                }
            }
        }
        return packedBuffer;
    }
    function unpack(unpackPayload, format) {
        var formatArray = format.split(' ');
        var returnArguments = [];
        var returnSubArray = [];
        var constructedString = '';
        var payloadReadOffset = 0;
        if(formatArray.length <= 0) {
            return returnArguments;
        }
        for(var i=0; i<formatArray.length; i++) {
            if(formatArray[i].split('').length === 1) {
                if(formatArray[i] === 's') {
                    constructedString += String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset));
                    payloadReadOffset++;
                    returnArguments.push(constructedString);
                    constructedString = '';
                    continue;
                }
                switch(formatArray[i]) {
                    case 'c':
                        returnArguments.push(String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset)));
                        payloadReadOffset++;
                        continue;
                    case 'b':
                        returnArguments.push(unpackPayload.readInt8(payloadReadOffset));
                        payloadReadOffset++;
                        continue;
                    case 'B':
                        returnArguments.push(unpackPayload.readUInt8(payloadReadOffset));
                        payloadReadOffset++;
                        continue;
                    case 'h':
                        returnArguments.push(unpackPayload.readInt16LE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 2;
                        continue;
                    case 'H':
                        returnArguments.push(unpackPayload.readUInt16LE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 2;
                        continue;
                    case 'i':
                        returnArguments.push(unpackPayload.readInt32LE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 4;
                        continue;
                    case 'I':
                        returnArguments.push(unpackPayload.readUInt32LE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 4;
                        continue;
                    case 'q':
                        returnArguments.push(unpackPayload.readDoubleLE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 8;
                        continue;
                    case 'Q':
                        returnArguments.push(unpackPayload.readDoubleLE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 8;
                        continue;
                    case 'f':
                        returnArguments.push(unpackPayload.readFloatLE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 4;
                        continue;
                    case 'd':
                        returnArguments.push(unpackPayload.readDoubleLE(payloadReadOffset));
                        payloadReadOffset = payloadReadOffset + 8;
                        continue;
                }
            }
            if(formatArray[i].split('').length > 1) {
                var singleFormatArray = formatArray[i].split('');
                if(singleFormatArray[0] === 's') {
                    constructedString = '';
                    for(var j=0; j<parseInt(formatArray[i].match(/\d/g).join('')); j++) {
                        constructedString += String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset));
                        payloadReadOffset++;
                    }
                    returnArguments.push(constructedString);
                    constructedString = '';
                    continue;
                }
                returnSubArray = [];
                for(var k=0; k<parseInt(formatArray[i].match(/\d/g).join('')); k++) {
                    switch(singleFormatArray[0]) {
                        case 'c':
                            returnSubArray.push(String.fromCharCode(unpackPayload.readUInt8(payloadReadOffset)));
                            payloadReadOffset++;
                            continue;
                        case 'b':
                            returnSubArray.push(unpackPayload.readInt8(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'B':
                            returnSubArray.push(unpackPayload.readUInt8(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'h':
                            returnSubArray.push(unpackPayload.readInt16LE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'H':
                            returnSubArray.push(unpackPayload.readIntU16LE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'i':
                            returnSubArray.push(unpackPayload.readInt32LE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'I':
                            returnSubArray.push(unpackPayload.readIntU32LE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'q':
                            returnSubArray.push(unpackPayload.readDoubleLE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'Q':
                            returnSubArray.push(unpackPayload.readDoubleLE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'f':
                            returnSubArray.push(unpackPayload.readFloatLE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                        case 'd':
                            returnSubArray.push(unpackPayload.readDoubleLE(payloadReadOffset));
                            payloadReadOffset++;
                            continue;
                    }
                }
                if(returnSubArray.length !== 0) {
                    returnArguments.push(returnSubArray);
                    returnSubArray = [];
                    continue;
                }
            }
        }
        return returnArguments;
     }
    
    this.sendRequest = function(sendRequestDevice, sendRequestFID, sendRequestData,
                                sendRequestPackFormat, sendRequestUnpackFormat,
                                sendRequestReturnCB, sendRequestErrorCB) {
    	if(this.getConnectionState() !== IPConnection.CONNECTION_STATE_CONNECTED) {
    		if(sendRequestErrorCB !== undefined) {
    			sendRequestErrorCB(IPConnection.ERROR_NOT_CONNECTED);
    		}
    		return;
    	}
        // Packet creation
        var sendRequestPayload = pack(sendRequestData, sendRequestPackFormat);
        var sendRequestHeader = this.createPacketHeader(sendRequestDevice,
                                                        8+sendRequestPayload.length,
                                                        sendRequestFID, sendRequestErrorCB);
        if (sendRequestHeader === undefined) {
            return;
        }
        var sendRequestPacket = bufferConcat([sendRequestHeader, sendRequestPayload]);
        var sendRequestSEQ = this.getSequenceNumberFromPacket(sendRequestHeader);
        // Sending the created packet
        if(sendRequestDevice.getResponseExpected(sendRequestFID)) {
            // Setting the requesting current device's current request            
            var sendRequestDeviceOID = sendRequestDevice.getDeviceOID();
            sendRequestDevice.expectedResponses.push({DeviceOID:sendRequestDeviceOID,
                FID:sendRequestFID,
                SEQ:sendRequestSEQ,
                unpackFormat:sendRequestUnpackFormat,
                timeout:setTimeout(this.sendRequestTimeout.bind
                        (this, sendRequestDevice, sendRequestDeviceOID, sendRequestErrorCB), this.timeout),
                returnCB:sendRequestReturnCB,
                errorCB:sendRequestErrorCB});
        }
        this.socket.write(sendRequestPacket);
    };
    this.sendRequestTimeout = function(timeoutDevice, timeoutDeviceOID, timeoutErrorCB) {
        for(var i=0; i<timeoutDevice.expectedResponses.length; ++i) {
            if(timeoutDevice.expectedResponses[i].DeviceOID === timeoutDeviceOID) {
                clearTimeout(timeoutDevice.expectedResponses[i].timeout);
                timeoutDevice.expectedResponses.splice(i, 1);
                if(timeoutErrorCB !== undefined){
                    timeoutErrorCB(IPConnection.ERROR_TIMEOUT);
                }
                return;
            }
        }
    };
    this.handleResponse = function(packetResponse) {
        var handleResponseDevice = this.devices[this.getUIDFromPacket(packetResponse)];
        var handleResponseFID = this.getFunctionIDFromPacket(packetResponse);
        var handleResponseSEQ = this.getSequenceNumberFromPacket(packetResponse);
        for(var i=0; i < handleResponseDevice.expectedResponses.length; i++) {
            if(this.devices[this.getUIDFromPacket(packetResponse)].expectedResponses[i].returnCB === undefined) {
                clearTimeout(handleResponseDevice.expectedResponses[i].timeout);
                handleResponseDevice.expectedResponses.splice(i, 1);
                return;
            }
            if(this.devices[this.getUIDFromPacket(packetResponse)].expectedResponses[i].unpackFormat === '') {
                clearTimeout(handleResponseDevice.expectedResponses[i].timeout);
                if(handleResponseDevice.expectedResponses[i].returnCB !== undefined) {
                	eval('handleResponseDevice.expectedResponses[i].returnCB();');
                }
                handleResponseDevice.expectedResponses.splice(i, 1);
                return;
            }
            if(handleResponseDevice.expectedResponses[i].FID === handleResponseFID &&
                    handleResponseDevice.expectedResponses[i].SEQ === handleResponseSEQ) {
            	if (this.getEFromPacket(packetResponse) === 1) {
                    clearTimeout(handleResponseDevice.expectedResponses[i].timeout);
            		if(this.devices[this.getUIDFromPacket(packetResponse)].expectedResponses[i].errorCB !== undefined) {
            			eval('handleResponseDevice.expectedResponses[i].errorCB(IPConnection.ERROR_INVALID_PARAMETER);');
            		}
            		handleResponseDevice.expectedResponses.splice(i, 1);
            		return;
            	}
            	if (this.getEFromPacket(packetResponse) === 2) {
                    clearTimeout(handleResponseDevice.expectedResponses[i].timeout);
            		if(this.devices[this.getUIDFromPacket(packetResponse)].expectedResponses[i].errorCB !== undefined) {
            			eval('handleResponseDevice.expectedResponses[i].errorCB(IPConnection.ERROR_FUNCTION_NOT_SUPPORTED);');
            		}
            		handleResponseDevice.expectedResponses.splice(i, 1);
            		return;
            	}
            	if (this.getEFromPacket(packetResponse) !== 0) {
                    clearTimeout(handleResponseDevice.expectedResponses[i].timeout);
            		if(this.devices[this.getUIDFromPacket(packetResponse)].expectedResponses[i].errorCB !== undefined) {
            			eval('handleResponseDevice.expectedResponses[i].errorCB(IPConnection.ERROR_UNKNOWN_ERROR);');
            		}
            		handleResponseDevice.expectedResponses.splice(i, 1);
            		return;
            	}
                clearTimeout(handleResponseDevice.expectedResponses[i].timeout);
                if(handleResponseDevice.expectedResponses[i].returnCB !== undefined) {
                	var retArgs = unpack(this.getPayloadFromPacket(packetResponse),
                			handleResponseDevice.expectedResponses[i].unpackFormat);
                	var evalStr = 'handleResponseDevice.expectedResponses[i].returnCB(';
                	for(var j=0; j<retArgs.length;j++) {
                		eval('var retSingleArg'+j+'=retArgs['+j+'];');
                		if(j != retArgs.length-1) {
                			evalStr += 'retSingleArg'+j+',';
                		}
                		else {
                			evalStr += 'retSingleArg'+j+');';
                		}
                	}
                	eval(evalStr);
                }
                handleResponseDevice.expectedResponses.splice(i, 1);
                return;
            }
        }
    };
    this.handleCallback = function(packetCallback) {
        if(this.getFunctionIDFromPacket(packetCallback) === IPConnection.CALLBACK_ENUMERATE) {
            if(this.registeredCallbacks[IPConnection.CALLBACK_ENUMERATE] !== undefined) {
                var args = unpack(this.getPayloadFromPacket(packetCallback), 's8 s8 c B3 B3 H B');
                var evalCBString = 'this.registeredCallbacks[IPConnection.CALLBACK_ENUMERATE](';
                for(var i=0; i<args.length;i++) {
                    eval('var cbArg'+i+'=args['+i+'];');
                    if(i != args.length-1) {
                        evalCBString += 'cbArg'+i+',';
                    }
                    else {
                        evalCBString += 'cbArg'+i+');';
                    }
                }
                eval(evalCBString);
                return;
            }
        }
        if (this.devices[this.getUIDFromPacket(packetCallback)] === undefined) {
            return;
        }
        if (this.devices[this.getUIDFromPacket(packetCallback)].
            registeredCallbacks[this.getFunctionIDFromPacket(packetCallback)] === undefined ||
            this.devices[this.getUIDFromPacket(packetCallback)].
            callbackFormats[this.getFunctionIDFromPacket(packetCallback)] === undefined) {
            return;
        }
        var cbFunction = this.devices[this.getUIDFromPacket(packetCallback)].
                         registeredCallbacks[this.getFunctionIDFromPacket(packetCallback)];
        var cbUnpackString = this.devices[this.getUIDFromPacket(packetCallback)].
                             callbackFormats[this.getFunctionIDFromPacket(packetCallback)];
        if(cbFunction == undefined) {
            return;
        }
        if(cbUnpackString == undefined) {
            return;
        }
        if(cbUnpackString === '') {
            eval('this.devices[this.getUIDFromPacket(packetCallback)].\
                    registeredCallbacks[this.getFunctionIDFromPacket(packetCallback)]();');
            return;
        }
        var args = unpack(this.getPayloadFromPacket(packetCallback), cbUnpackString);
        var evalCBString = 'this.devices[this.getUIDFromPacket(packetCallback)].\
                            registeredCallbacks[this.getFunctionIDFromPacket(packetCallback)](';
        if(args.length <= 0) {
            eval(evalCBString+');');
            return;
        } 
        for(var i=0; i<args.length;i++) {
            eval('var cbArg'+i+'=args['+i+'];');
            if(i != args.length-1) {
                evalCBString += 'cbArg'+i+',';
            }
            else {
                evalCBString += 'cbArg'+i+');';
            }
        }
        eval(evalCBString);
        return;
    };
    this.handlePacket = function(packet) {
        if(this.getSequenceNumberFromPacket(packet) === 0) {
            this.handleCallback(packet);
        }
        if(this.getSequenceNumberFromPacket(packet) > 0) {
            this.handleResponse(packet);
        }
    };
    this.getConnectionState = function() {
        if(this.isConnected) {
            return IPConnection.CONNECTION_STATE_CONNECTED;
        }
        if(this.getCurrentTaskKind() === IPConnection.TASK_KIND_AUTO_RECONNECT) {
            return IPConnection.CONNECTION_STATE_PENDING;
        }
        return IPConnection.CONNECTION_STATE_DISCONNECTED;
    };
    this.setAutoReconnect = function(autoReconnect) {
        this.autoReconnect = autoReconnect;
    };
    this.getAutoReconnect = function() {
        return this.autoReconnect;
    };
    this.setTimeout = function(timeout) {
        this.timeout = timeout;
    };
    this.getTimeout = function() {
        return this.timeout;
    };
    this.enumerate = function() {
        this.socket.write(this.createPacketHeader(undefined, 8, IPConnection.FUNCTION_ENUMERATE));
    };
    this.on = function(FID, CBFunction) {
        this.registeredCallbacks[FID] = CBFunction;
    };
    this.getNextSequenceNumber = function() {
        if(this.sequenceNumber >= 15) {
            this.sequenceNumber = 0;
        }
        return ++this.sequenceNumber;
    };
    this.createPacketHeader = function(headerDevice, headerLength, headerFunctionID, headerErrorCB) {
        var UID = IPConnection.BROADCAST_UID;
        var len = headerLength;
        var FID = headerFunctionID;
        var seq = this.getNextSequenceNumber();
        var responseBits = 0;
        var authBits = 0;
        var EFutureUse = 0;
        var returnOnError = false;
        if(headerDevice !== undefined) {
            var responseExpected = headerDevice.getResponseExpected(headerFunctionID,
                    function(errorCode){returnOnError = true; if(headerErrorCB !== undefined) {headerErrorCB(errorCode);}});
            if(returnOnError) {
                returnOnError = false;
                
                return;
            }
            UID = headerDevice.uid;
            if(responseExpected) {
                responseBits = 1;
            }
            if(headerDevice.authKey !== undefined) {
                authBits = 1;
            }
        }
        else {
            if(this.authKey != undefined) {
                authBits = 1;
            }
        }
        var seqResponseAuthOOBits = seq << 4;
        if(responseBits) {
            seqResponseAuthOOBits |= (responseBits << 3);
        }
        if(authBits) {
            seqResponseAuthOOBits |= (authBits << 2);
        }
        var returnHeader = new Buffer(8);
        returnHeader.writeUInt32LE(UID, 0);
        returnHeader.writeUInt8(len, 4);
        returnHeader.writeUInt8(FID, 5);
        returnHeader.writeUInt8(seqResponseAuthOOBits, 6);
        returnHeader.writeUInt8(EFutureUse , 7);
        return returnHeader;
    };
    function bufferConcat(arrayOfBuffers) {
        var newBufferSize = 0;
        var targetStart = 0;
        for(var i = 0; i<arrayOfBuffers.length; i++) {
            newBufferSize += arrayOfBuffers[i].length;
        }
        var returnBufferConcat = new Buffer(newBufferSize);
        for(var j=0; j<arrayOfBuffers.length; j++) {
            arrayOfBuffers[j].copy(returnBufferConcat, targetStart);
            targetStart += arrayOfBuffers[j].length;
        }
        return returnBufferConcat;
    }
}

module.exports = IPConnection;

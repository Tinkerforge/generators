/*
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

Redistribution and use in source and binary forms of this file,
with or without modification, are permitted. See the Creative
Commons Zero (CC0 1.0) License for more details.
*/

Device.RESPONSE_EXPECTED_ALWAYS_TRUE = 1; // getter
Device.RESPONSE_EXPECTED_TRUE = 2; // setter
Device.RESPONSE_EXPECTED_FALSE = 3; // setter, default
Device.ERROR_INVALID_FUNCTION_ID = 21;

function base58Decode(str) {
    var alphabet = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";
    var base = alphabet.length;
    var char, char_index, index, num, i, len, ref;
    num = 0;
    ref = str.split(/(?:)/).reverse();
    for (index = i = 0, len = ref.length; i < len; index = ++i) {
        char = ref[index];
        if ((char_index = alphabet.indexOf(char)) === -1) {
            throw new Error('Value passed is not a valid Base58 string.');
        }
        num += char_index * Math.pow(base, index);
    }
    return num;
}

function Device(deviceRegistering, uid, ipcon) {
    if (deviceRegistering !== undefined && uid !== undefined && ipcon !== undefined) {
        this.uid = base58Decode(uid);
        this.responseExpected = {};
        this.callbackFormats = {};
        this.highLevelCallbacks = {};
        this.streamStateObjects = {};
        this.registeredCallbacks = {};
        this.ipcon = ipcon;
        this.deviceOID = 0;
        this.APIVersion = [0, 0, 0];
        this.expectedResponses = []; // Has following structured objects as elements of the array,
                                    /*
                                    {
                                        DeviceOID:,
                                        FID:,
                                        SEQ:,
                                        unpackFormat:,
                                        timeout:,
                                        returnCB:,
                                        errorCB:
                                    }
                                    */
        // Creates the device object with the unique device ID *uid* and adds
        // it to the IPConnection *ipcon*.
        this.ipcon.devices[this.uid] = deviceRegistering;
        this.getDeviceOID = function () {
            return this.deviceOID++;
        };
        this.getAPIVersion = function () {
            return this.APIVersion;
        };
        this.on = function (callbackID, function_) {
            this.registeredCallbacks[callbackID] = function_;
        };
        this.getResponseExpected = function (functionID, errorCallback) {
            if (this.responseExpected[functionID] === undefined) {
                if (errorCallback !== undefined) {
                    errorCallback(Device.ERROR_INVALID_FUNCTION_ID);
                }
                return;
            }
            if (this.responseExpected[functionID] === Device.RESPONSE_EXPECTED_TRUE ||
                this.responseExpected[functionID] === Device.RESPONSE_EXPECTED_ALWAYS_TRUE) {
                return true;
            } else {
                return false;
            }
        };
        this.setResponseExpected = function (functionID, responseBoolean, errorCallback) {
            if (this.responseExpected[functionID] === undefined) {
                if (errorCallback !== undefined) {
                    errorCallback(Device.ERROR_INVALID_FUNCTION_ID);
                }
                return;
            }
            if (this.responseExpected[functionID] === Device.RESPONSE_EXPECTED_TRUE ||
                this.responseExpected[functionID] === Device.RESPONSE_EXPECTED_FALSE) {
                if (responseBoolean) {
                    this.responseExpected[functionID] = Device.RESPONSE_EXPECTED_TRUE;
                } else {
                    this.responseExpected[functionID] = Device.RESPONSE_EXPECTED_FALSE;
                }
                return;
            }
            if (errorCallback !== undefined) {
                errorCallback(Device.ERROR_INVALID_FUNCTION_ID);
            }
        };
        this.setResponseExpectedAll = function (responseBoolean) {
            if (responseBoolean === true || responseBoolean === false) {
                for (var fid in this.responseExpected) {
                    if (this.responseExpected[fid] === Device.RESPONSE_EXPECTED_TRUE ||
                        this.responseExpected[fid] === Device.RESPONSE_EXPECTED_FALSE) {
                        if (responseBoolean) {
                            this.responseExpected[fid] = Device.RESPONSE_EXPECTED_TRUE;
                        }
                        else {
                            this.responseExpected[fid] = Device.RESPONSE_EXPECTED_FALSE;
                        }
                    }
                }
            }
        };

        this.resetStreamStateObject = function (streamStateObject) {
            streamStateObject['responseProperties']['running'] = false;
            streamStateObject['responseProperties']['runningSubcall'] = false;
            streamStateObject['responseProperties']['runningSubcallOOS'] = false;
            streamStateObject['responseProperties']['waitingFirstChunk'] = true;
            if (streamStateObject['responseProperties']['timeout'] !== null) {
              clearTimeout(streamStateObject['responseProperties']['timeout']);
              streamStateObject['responseProperties']['timeout'] = null;
            }
            streamStateObject['responseProperties']['data'].length = 0;
            streamStateObject['responseProperties']['streamInChunkOffset'] = 0;
            streamStateObject['responseProperties']['streamInChunkLength'] = 0;
            streamStateObject['responseProperties']['streamInWritten'] = 0;
            streamStateObject['responseProperties']['streamInLLParams'] = null;
            streamStateObject['responseProperties']['returnCB'] = null;
            streamStateObject['responseProperties']['errorCB'] = null;
        };
    }
}

module.exports = Device;

/*
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>

Redistribution and use in source and binary forms of this file,
with or without modification, are permitted. See the Creative
Commons Zero (CC0 1.0) License for more details.
*/

Device.RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0;
Device.RESPONSE_EXPECTED_ALWAYS_TRUE = 1;// Getter
Device.RESPONSE_EXPECTED_ALWAYS_FALSE = 2;// Callback
Device.RESPONSE_EXPECTED_TRUE = 3;// Setter
Device.RESPONSE_EXPECTED_FALSE = 4;// Setter, default
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
        this.registeredCallbacks = {};
        this.ipcon = ipcon;
        this.deviceOID = 0;
        this.APIVersion = [0, 0, 0];
        this.expectedResponses = [];// Has following structured objects as elements of the array,
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
        this.authKey = undefined;
        //Creates the device object with the unique device ID *uid* and adds
        //it to the IPConnection *ipcon*.
        this.ipcon.devices[this.uid] = deviceRegistering;
        this.getDeviceOID = function () {
            return this.deviceOID++;
        };
        this.getAPIVersion = function () {
            return this.APIVersion;
        };
        this.on = function (id, callback) {
            this.registeredCallbacks[id] = callback;
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
    }
}

module.exports = Device;

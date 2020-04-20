/*
Copyright (C) 2014 Ishraq Ibne Ashraf <ishraq@tinkerforge.com>
Copyright (C) 2020 Matthias Bolte <matthias@tinkerforge.com>

Redistribution and use in source and binary forms of this file,
with or without modification, are permitted. See the Creative
Commons Zero (CC0 1.0) License for more details.
*/

Device.RESPONSE_EXPECTED_ALWAYS_TRUE = 1; // getter
Device.RESPONSE_EXPECTED_TRUE = 2; // setter
Device.RESPONSE_EXPECTED_FALSE = 3; // setter, default

Device.ERROR_INVALID_FUNCTION_ID = 21; // keep in sync with IPConnection.ERROR_INVALID_FUNCTION_ID
Device.ERROR_WRONG_DEVICE_TYPE = 81; // keep in sync with IPConnection.ERROR_WRONG_DEVICE_TYPE
Device.ERROR_DEVICE_REPLACED = 82; // keep in sync with IPConnection.ERROR_DEVICE_REPLACED

Device.DEVICE_IDENTIFIER_CHECK_PENDING = 0;
Device.DEVICE_IDENTIFIER_CHECK_MATCH = 1;
Device.DEVICE_IDENTIFIER_CHECK_MISMATCH = 2;

function base58Decode(str) {
    var alphabet = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";
    var base = alphabet.length;
    var char, char_index, index, num, i, len, ref;

    num = 0;
    ref = str.split(/(?:)/).reverse();

    for (index = i = 0, len = ref.length; i < len; index = ++i) {
        char = ref[index];

        if ((char_index = alphabet.indexOf(char)) === -1) {
            throw new Error('UID "' + str + '" contains invalid character');
        }

        num += char_index * Math.pow(base, index);

        if (!Number.isSafeInteger(num) || num > 0xFFFFFFFF) {
            throw new Error('UID "' + str + '" is too big');
        }
    }

    return num;
}

function Device(that, uid, ipcon, deviceIdentifier, deviceDisplayName) {
    if (uid !== undefined && ipcon !== undefined && deviceIdentifier !== undefined && deviceDisplayName !== undefined) {
        this.replaced = false;
        this.uid = base58Decode(uid);

        if (this.uid === 0) {
            throw new Error('UID "' + uid + '" is empty or maps to zero');
        }

        this.deviceIdentifier = deviceIdentifier;
        this.deviceDisplayName = deviceDisplayName;
        this.deviceIdentifierCheck = Device.DEVICE_IDENTIFIER_CHECK_PENDING;
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
                        } else {
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

        this.checkValidity = function (returnCallback, errorCallback) {
            if (this.replaced) {
                if (errorCallback !== undefined) {
                    errorCallback(Device.ERROR_DEVICE_REPLACED);
                }
            } else if (this.deviceIdentifierCheck === Device.DEVICE_IDENTIFIER_CHECK_MATCH) {
                if (returnCallback !== undefined) {
                    returnCallback();
                }
            } else if (this.deviceIdentifierCheck === Device.DEVICE_IDENTIFIER_CHECK_MISMATCH) {
                if (errorCallback !== undefined) {
                    errorCallback(Device.ERROR_WRONG_DEVICE_TYPE);
                }
            } else { // Device.DEVICE_IDENTIFIER_CHECK_PENDING
                this.ipcon.sendRequest(this, 255, [], '', 33, 's8 s8 c B3 B3 H', // getIdentity
                    function (uid, connectedUid, position, hardwareVersion, firmwareVersion, deviceIdentifier) {
                        if (deviceIdentifier == this.deviceIdentifier) {
                            this.deviceIdentifierCheck = Device.DEVICE_IDENTIFIER_CHECK_MATCH;

                            if (returnCallback !== undefined) {
                                returnCallback();
                            }
                        } else {
                            this.deviceIdentifierCheck = Device.DEVICE_IDENTIFIER_CHECK_MISMATCH;

                            if (errorCallback !== undefined) {
                                errorCallback(Device.ERROR_WRONG_DEVICE_TYPE);
                            }
                        }
                    }.bind(this),
                    errorCallback,
                    false
                );
            }
        }
    }
}

module.exports = Device;

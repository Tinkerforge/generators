Device.RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0;
Device.RESPONSE_EXPECTED_ALWAYS_TRUE = 1; // getter
Device.RESPONSE_EXPECTED_ALWAYS_FALSE = 2; // callback
Device.RESPONSE_EXPECTED_TRUE = 3; // setter
Device.RESPONSE_EXPECTED_FALSE = 4; // setter, default
Device.INVALID_FUNCTION_ID = 21;
Device.INVALID_RESPONSE_EXPECTED = 22;

function Device(deviceRegistering, uid, ipcon) {
	if(deviceRegistering !== undefined &&
			uid !== undefined &&
			ipcon !== undefined) {
		this.uid = base58Decode(uid);
		this.ipcon = ipcon;
		this.deviceOID = 0;
		this.APIVersion = [0, 0, 0];
		this.responseExpected = {};
		this.registeredCallbacks = {};
		this.callbackFormats = {}; //will be overwritten by child class
		this.expectedResponses = [];//has following structured objects as elements of the array,
									//{FID:,
									// SEQ:,
									// unpackFormat:,
									// timeout:,
									// returnCallback:,
									// errorCallback:}
		this.authKey = undefined;
		//Creates the device object with the unique device ID *uid* and adds
		//it to the IPConnection *ipcon*.
		this.ipcon.devices[this.uid] = deviceRegistering; // FIXME: maybe use a weakref here
		this.getDeviceOID = function() {
			return this.deviceOID++;
		};
		this.getAPIVersion = function() {
			return this.APIVersion;
		};
	    this.on = function(id, callback) {
	        this.registeredCallbacks[id] = callback;
	    };
		this.getResponseExpected = function(functionID, errorCallback) {
			if(this.responseExpected[functionID] === undefined) {
				if(errorCallback !== undefined) {
					errorCallback(Device.INVALID_FUNCTION_ID);
					return;
				}
			}
			return this.responseExpected[functionID];
		};
		this.setResponseExpected = function(functionID, expectedResponse, errorCallback) {
			if(this.responseExpected[functionID] === undefined) {
				if(errorCallback !== undefined) {
					errorCallback(Device.INVALID_FUNCTION_ID);
					return;
				}
			}
			if(expectedResponse !== Device.RESPONSE_EXPECTED_TRUE){
				if(expectedResponse !== Device.RESPONSE_EXPECTED_ALWAYS_TRUE){
					if(expectedResponse !== Device.RESPONSE_EXPECTED_FALSE){
						if(expectedResponse !== Device.RESPONSE_EXPECTED_ALWAYS_FALSE) {
							if(errorCallback !== undefined) {
								errorCallback(Device.INVALID_RESPONSE_EXPECTED);
								return;
							}
						}
					}
				}
			}
			if(this.responseExpected[functionID] !== Device.RESPONSE_EXPECTED_ALWAYS_TRUE &&
					this.responseExpected[functionID] !== Device.RESPONSE_EXPECTED_ALWAYS_FALSE) {
				this.responseExpected[functionID] = expectedResponse;
			}
		};
		this.setResponseExpectedAll = function(expectedResponse) {
			if(expectedResponse !== Device.RESPONSE_EXPECTED_TRUE){
				if(expectedResponse !== Device.RESPONSE_EXPECTED_ALWAYS_TRUE){
					if(expectedResponse !== Device.RESPONSE_EXPECTED_FALSE){
						if(expectedResponse !== Device.RESPONSE_EXPECTED_ALWAYS_FALSE) {
							if(errorCallback !== undefined) {
								errorCallback(Device.INVALID_RESPONSE_EXPECTED);
								return;
							}
						}
					}
				}
			}
			for(var fid in this.responseExpected) {
				if(this.responseExpected[fid] !== Device.RESPONSE_EXPECTED_ALWAYS_TRUE &&
						this.responseExpected[fid] !== Device.RESPONSE_EXPECTED_ALWAYS_FALSE) {
					this.responseExpected[fid] = expectedResponse;
				}
			}
		};
		function base58Decode(str) {
			var alphabet = "123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";
			var base = alphabet.length;
			var char;
			var char_index;
			var index;
			var num;
			var _i;
			var _len;
			var _ref;
			num = 0;
			_ref = str.split(/(?:)/).reverse();
			for (index = _i = 0, _len = _ref.length; _i < _len; index = ++_i) {
				char = _ref[index];
				if ((char_index = alphabet.indexOf(char)) === -1) {
					throw new Error('Value passed is not a valid Base58 string.');
				}
				num += char_index * Math.pow(base, index);
			}
			return num;
		}
	}
}

module.exports = Device;

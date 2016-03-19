/*
 * Variable "is_tvpl" is currently only used for Chrome/Safari
 * subworker polyfill code in the file subworkers.js.
 */

var is_tvpl = true;
var _ipcon_cache = {};
var _device_cache = {};
var _running_workers = {};
var _function_tf_call_queue = [];
var _queue_function_tf_call = false;

console.log('*** WORKER MANAGER');

function _error_handler(e) {
    postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
        workerProtocol.TYPE_RES_ERROR,
        'ERROR: ' + String(e) + '\n'));
}

function _do_function_tf_call(data) {
    var ipcon = null;
    var code_eval = '';
    var key_device = [String(data.uid), key_ipcon].join('@');
    var key_ipcon = [String(data.host), String(data.port)].join(':');

    if (data.device_function_input_args === null &&
        data.device_function_output_args !== null) {
        code_eval = 'if (!(key_device in _device_cache)) { var device = new Tinkerforge.' +
            data.device_class_name +
            '(\'' +
            String(data.uid) +
            '\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } \
            _device_cache[key_device].' +
            data.device_function_name +
            '(function(' +
            data.device_function_output_args +
            ') { _running_workers[\'' +
            data.worker_id +
            '\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, \
            workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, ' +
            data.device_function_output_assignment +
            ') ); if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { \
                _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);';
    } else if (data.device_function_input_args !== null &&
        data.device_function_output_args !== null) {
        code_eval = 'if (!(key_device in _device_cache)) { var device = new Tinkerforge.' +
            data.device_class_name +
            '(\'' +
            String(data.uid) +
            '\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } \
            _device_cache[key_device].' +
            data.device_function_name +
            '(\'' +
            data.device_function_input_args +
            ', function(' +
            data.device_function_output_args +
            ') { _running_workers[\'' +
            data.worker_id +
            '\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, \
            workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, ' +
            data.device_function_output_assignment +
            ') ); if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { \
                _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);';
    } else if (data.device_function_input_args === null &&
        data.device_function_output_args === null) {
        code_eval = 'if (!(key_device in _device_cache)) { var device = new Tinkerforge.' +
            data.device_class_name +
            '(\'' +
            String(data.uid) +
            '\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } _device_cache[key_device].' +
            data.device_function_name +
            '(function(e) { _running_workers[\'' +
            data.worker_id +
            '\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, null) ); \
            if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { \
                _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);';
    } else if (data.device_function_input_args !== null &&
        data.device_function_output_args === null) {
        code_eval = 'if (!(key_device in _device_cache)) { var device = new Tinkerforge.' +
            data.device_class_name +
            '(\'' +
            String(data.uid) +
            '\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } _device_cache[key_device].' +
            data.device_function_name +
            '(' +
            data.device_function_input_args +
            ', function(e) { _running_workers[\'' +
            data.worker_id +
            '\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, null) ); \
            if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { \
                _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);';
    }

    if (key_ipcon in _ipcon_cache) {
        ipcon = _ipcon_cache[key_ipcon];
        eval(code_eval);
        return;
    }
    ipcon = new Tinkerforge.IPConnection();
    ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED, function(e) {
        _ipcon_cache[key_ipcon] = ipcon;
        eval(code_eval);
    });
    ipcon.connect(data.host, Number(data.port), _error_handler);
}

function _dispatch_message(message) {
    if (typeof(message) !== 'object') {
        return;
    }

    if (message.type !== null && workerProtocol.isNumber(message.type)) {
        switch (message.type) {
            case workerProtocol.TYPE_REQ_PROGRAM_START:
                if (message.data instanceof Array && message.data.length > 0) {
                    for (var i = 0; i < message.data.length; i++) {
                        var worker_id = message.data[i].split('/')[message.data[i].split('/').length - 1];
                        _running_workers[worker_id] = new Worker(message.data[i]);
                        _running_workers[worker_id].onmessage = onmessage;
                        _running_workers[worker_id].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                            workerProtocol._TYPE_REQ_SUBWORKER_START, { wid: worker_id, dictv: _dict_variables }));
                    }
                    postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                        workerProtocol.TYPE_RES_PROGRAM_START_ACK, null));
                }
                break;
            case workerProtocol.TYPE_REQ_PROGRAM_STOP:
                for (var key in _running_workers) {
                    _running_workers[key].terminate();
                }
                _function_tf_call_queue = []
                for (var key in _ipcon_cache) {
                    _ipcon_cache[key].disconnect();
                }
                postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                    workerProtocol.TYPE_RES_PROGRAM_STOP_ACK, null));
                break;
            case workerProtocol.TYPE_REQ_FUNCTION_EXECUTE:
                var worker_id = message.data.blobFunction.split('/')[message.data.blobFunction.split('/').length - 1];
                _running_workers[worker_id] = new Worker(message.data.blobFunction);
                _running_workers[worker_id].onmessage = onmessage;
                _running_workers[worker_id].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                    workerProtocol._TYPE_REQ_SUBWORKER_START, {
                        wid: worker_id,
                        dictv: _dict_variables,
                        codeButtonEnable: message.data.codeButtonEnable
                    }));
                postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                    workerProtocol.TYPE_RES_FUNCTION_EXECUTE_ACK, null));
                break;
            case workerProtocol._TYPE_RES_SUBWORKER_DONE:
                if (message.data !== null && message.data !== '') {
                    postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                        workerProtocol.TYPE_RES_SUBWORKER_DONE, message.data));
                }
                _running_workers[message.sender].terminate();
                delete _running_workers[message.data];
                break;
            case workerProtocol._TYPE_RES_SET_VARIABLE:
                _dict_variables = message.data;
                for (var key in _running_workers) {
                    _running_workers[key].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                        workerProtocol._TYPE_REQ_SET_VARIABLE, message.data));
                }
                break;
            case workerProtocol._TYPE_RES_FUNCTION_TF_CALL:
                if (_queue_function_tf_call) {
                    _function_tf_call_queue.push(message.data);
                    break;
                }
                _queue_function_tf_call = true;
                _do_function_tf_call(message.data);
                break;
            case workerProtocol._TYPE_RES_MESSAGE_CONSOLE:
                postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                    workerProtocol.TYPE_RES_MESSAGE_CONSOLE, String(message.data)));
                break;
            case workerProtocol._TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD:
                postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                    workerProtocol.TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD, message));
                break;
            case workerProtocol._TYPE_RES_MESSAGE_GUI_PLOT:
                postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER,
                    workerProtocol.TYPE_RES_MESSAGE_GUI_PLOT, message));
                break;
            case workerProtocol._TYPE_RES_ERROR:
                _error_handler(String(message.data));
        }
    }
}

onmessage = function(e) {
    _dispatch_message(e.data);
};
onerror = _error_handler;
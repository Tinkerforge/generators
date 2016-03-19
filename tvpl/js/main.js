// It is a good pattern to keep content and control separate.

/*
 * All the variables and functions that require a JavaScript scope of the page should
 * be declared outside the jQuery document ready callback function. Otherwise the JavaScript
 * variables will have scope limited only to the callback function.
 */

// Constants.

var MSG_SNACKBAR_GUI_EDITOR_DISABLED =
    'GUI editor is disabled as a program is currently running.';
var MSG_OUTPUT_CONSOLE_WAITING_OUTPUT =
    'Program running. Waiting for output...';
var MSG_OUTPUT_CONSOLE_NO_PROGRAM_RUNNING =
    'A running program can print text on this output console.\n\nSTATUS: No program running.';
var INDEX_VIEW_PROGRAM_EDITOR = 1;
var INDEX_VIEW_GUI_EDITOR = 2;
var INDEX_VIEW_EXECUTE_PROGRAM = 3;
var PROGRAM_STATUS_RUNNING = false;
var LIST_IMPORT_SCRIPTS = [
    'Tinkerforge.js',
    'subworkers.js',
    'babelRuntime.js',
    'babelBrowser.js',
    'babelPolyfill.js',
    'workerProtocol.js'
];
var MSG_ERROR_JAVASCRIPT_PREPARE_CODE_FAILED = 'ERROR: The following error occurred while preparing JavaScript code.\n\n\n';

// Variables.

/*
 * Elements of the page.
 * Assigned in the jQuery document ready callback function.
 */
var divBody = null;
var divGUIEditor = null;
var divProgramEditor = null;
var textAreaGUIEditor = null;
var $textAreaGUIEditor = null; // jQuery object.
var divExecuteProgram = null;
var iframeProgramEditor = null;
var divExecuteProgramRenderedGUI = null;
var buttonExecuteProgramRunProgram = null;
var $buttonExecuteProgramRunProgram = null; // jQuery object.
var buttonExecuteProgramStopProgram = null;
var $buttonExecuteProgramStopProgram = null; // jQuery object.
var textareaProgramExecutionConsole = null;
var $textareaProgramExecutionConsole = null; // jQuery object.
var divExecuteProgramRenderedGUIEmpty = null;

var dialogs = {};
var snackbar = null;
var programEditor = null;
var workerManager = null;
var xmlBlocklyToolbox = null;
var codeWorkerManager = null;

/*
var codeWorkerManager = 'var is_tvpl = true;\n' +
    'var _queue_function_tf_call = false;\n' +
    'var _function_tf_call_queue = [];\n' +
    'var _ipcon_cache = {};\n' +
    'var _device_cache = {};\n' +
    'var _running_workers = {};\n' +
    'function _error_handler(e) {\n' +
    '  postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_ERROR, \'ERROR: \' + String(e) + \'\\n\'));\n' +
    '}\n' +
    'function _do_function_tf_call(data) {\n' +
    '  var ipcon = null;\n' +
    '  var key_ipcon = [String(data.host), String(data.port)].join(\':\');\n' +
    '  var key_device = [String(data.uid), key_ipcon].join(\'@\');\n' +
    '  var code_eval = \'\';\n' +
    '  if(data.device_function_input_args === null && data.device_function_output_args !== null) {\n' +
    '    code_eval = \'if (!(key_device in _device_cache)) { var device = new Tinkerforge.\' + data.device_class_name + \'(\\\'\' + String(data.uid) + \'\\\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } _device_cache[key_device].\' + data.device_function_name + \'(function(\' + data.device_function_output_args + \') { _running_workers[\\\'\' + data.worker_id + \'\\\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, \' + data.device_function_output_assignment + \') ); if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);\';\n' +
    '  }\n' +
    '  else if(data.device_function_input_args !== null && data.device_function_output_args !== null) {\n' +
    '    code_eval = \'if (!(key_device in _device_cache)) { var device = new Tinkerforge.\' + data.device_class_name + \'(\\\'\' + String(data.uid) + \'\\\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } _device_cache[key_device].\' + data.device_function_name + \'(\' + data.device_function_input_args + \', function(\' + data.device_function_output_args + \') { _running_workers[\\\'\' + data.worker_id + \'\\\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, \' + data.device_function_output_assignment + \') ); if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);\';\n' +
    '  }\n' +
    '  else if(data.device_function_input_args === null && data.device_function_output_args === null) {\n' +
    '    code_eval = \'if (!(key_device in _device_cache)) { var device = new Tinkerforge.\' + data.device_class_name + \'(\\\'\' + String(data.uid) + \'\\\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } _device_cache[key_device].\' + data.device_function_name + \'(function(e) { _running_workers[\\\'\' + data.worker_id + \'\\\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, null) ); if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);\';\n' +
    '  }\n' +
    '  else if(data.device_function_input_args !== null && data.device_function_output_args === null) {\n' +
    '    code_eval = \'if (!(key_device in _device_cache)) { var device = new Tinkerforge.\' + data.device_class_name + \'(\\\'\' + String(data.uid) + \'\\\', ipcon); device.setResponseExpectedAll(true); _device_cache[key_device] = device; } _device_cache[key_device].\' + data.device_function_name + \'(\' + data.device_function_input_args + \', function(e) { _running_workers[\\\'\' + data.worker_id + \'\\\'].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN, null) ); if(_function_tf_call_queue.length < 1) { _queue_function_tf_call = false; } else { _do_function_tf_call(_function_tf_call_queue.shift()); } }, _error_handler);\';\n' +
    '  }\n' +
    '  if (key_ipcon in _ipcon_cache) {\n' +
    '    ipcon = _ipcon_cache[key_ipcon];\n' +
    '    eval(code_eval);\n' +
    '    return;\n' +
    '  }\n' +
    '  ipcon = new Tinkerforge.IPConnection();\n' +
    '  ipcon.on(Tinkerforge.IPConnection.CALLBACK_CONNECTED, function(e) { _ipcon_cache[key_ipcon] = ipcon; eval(code_eval); });\n' +
    '  ipcon.connect(data.host, Number(data.port), _error_handler);\n' +
    '}\n' +
    'function _dispatch_message(message) {\n' +
    '  if (typeof(message) !== \'object\') {\n' +
    '    return;\n' +
    '  }\n' +
    '\n' +
    '  if (message.type !== null && workerProtocol.isNumber(message.type)) {\n' +
    '    switch(message.type) {\n' +
    '      case workerProtocol.TYPE_REQ_PROGRAM_START:\n' +
    '        if (message.data instanceof Array && message.data.length > 0) {\n' +
    '           for (var i = 0; i < message.data.length; i++) {\n' +
    '             var worker_id = message.data[i].split(\'/\')[message.data[i].split(\'/\').length - 1];\n' +
    '             _running_workers[worker_id] = new Worker(message.data[i]);\n' +
    '             _running_workers[worker_id].onmessage = onmessage;\n' +
    '             _running_workers[worker_id].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_SUBWORKER_START, {wid: worker_id, dictv: _dict_variables}));\n' +
    '           }\n' +
    '          postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_PROGRAM_START_ACK, null));\n' +
    '        }\n' +
    '        break;\n' +
    '      case workerProtocol.TYPE_REQ_PROGRAM_STOP:\n' +
    '        for (var key in _running_workers) {\n' +
    '          _running_workers[key].terminate();\n' +
    '        }\n' +
    '        _function_tf_call_queue = []\n' +
    '        for (var key in _ipcon_cache) {\n' +
    '          _ipcon_cache[key].disconnect();\n' +
    '        }\n' +
    '        postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_PROGRAM_STOP_ACK, null));\n' +
    '        break;\n' +
    '      case workerProtocol.TYPE_REQ_FUNCTION_EXECUTE:\n' +
    '        var worker_id = message.data.blobFunction.split(\'/\')[message.data.blobFunction.split(\'/\').length - 1];\n' +
    '        _running_workers[worker_id] = new Worker(message.data.blobFunction);\n' +
    '        _running_workers[worker_id].onmessage = onmessage;\n' +
    '        _running_workers[worker_id].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_SUBWORKER_START, {wid: worker_id, dictv: _dict_variables, codeButtonEnable: message.data.codeButtonEnable}));\n' +
    '        postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_FUNCTION_EXECUTE_ACK, null));\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_SUBWORKER_DONE:\n' +
    '        if (message.data !== null && message.data !== \'\') {\n' +
    '          postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_SUBWORKER_DONE, message.data));\n' +
    '        }\n' +
    '        _running_workers[message.sender].terminate();\n' +
    '        delete _running_workers[message.data];\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_SET_VARIABLE:\n' +
    '        _dict_variables = message.data;\n' +
    '        for (var key in _running_workers) {\n' +
    '          _running_workers[key].postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol._TYPE_REQ_SET_VARIABLE, message.data));\n' +
    '        }\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_FUNCTION_TF_CALL:\n' +
    '        if(_queue_function_tf_call) {\n' +
    '          _function_tf_call_queue.push(message.data);\n' +
    '          break;\n' +
    '        }\n' +
    '        _queue_function_tf_call = true;\n' +
    '        _do_function_tf_call(message.data);\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_MESSAGE_CONSOLE:\n' +
    '        postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_MESSAGE_CONSOLE, String(message.data)));\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD:\n' +
    '        postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD, message));\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_MESSAGE_GUI_PLOT:\n' +
    '        postMessage(workerProtocol.getMessage(workerProtocol.SENDER_WORKER_MANAGER, workerProtocol.TYPE_RES_MESSAGE_GUI_PLOT, message));\n' +
    '        break;\n' +
    '      case workerProtocol._TYPE_RES_ERROR:\n' +
    '        _error_handler(String(message.data));\n' +
    '    }\n' +
    '  }\n' +
    '}\n' +
    '\n' +
    'onmessage = function(e) {\n' +
    '  _dispatch_message(e.data);\n' +
    '};\n' +
    'onerror = _error_handler;\n';
*/

// Functions.

function eventHandlerResProgramStartAck(e) {
    PROGRAM_STATUS_RUNNING = true;

    $buttonExecuteProgramRunProgram.attr('disabled', true);
    $buttonExecuteProgramStopProgram.removeAttr('disabled');
    $textareaProgramExecutionConsole.addClass('waiting');
    textareaProgramExecutionConsole.value = MSG_OUTPUT_CONSOLE_WAITING_OUTPUT;
    textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;

    /*
    buttonToolbarRunStop.setAttribute('onclick', 'clickedStopProgram()');
    buttonToolbarRunStop.setAttribute('title', MSG_TOOLTIP_BUTTON_RUNSTOP_STOP);
    buttonToolbarRunStopImage.innerHTML = 'stop';
    buttonToolbarRunStop.disabled = false;
    blockEditGUI(true);
    blockRenderGUI(false);

    if (divEditGUI.style.display === 'block') {
        $.growl.warning({ message: MSG_INFO_PROGRAM_RUNNING_GUI_EDITOR_BLOCKED });
    }
    */
}

function eventHandlerMessageWorkerManager(e) {
    console.log('*** eventHandlerMessageWorkerManager()');
    var message = null;

    if (typeof(e.data) !== 'object') {
        return;
    }

    message = e.data;

    if (message.type !== null && workerProtocol.isNumber(message.type)) {
        switch (message.type) {
            case workerProtocol.TYPE_RES_PROGRAM_START_ACK:
                console.log('*** ACK');
                eventHandlerResProgramStartAck();
                break;

            case workerProtocol.TYPE_RES_PROGRAM_STOP_ACK:
                textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;

                if (workerManager) {
                    workerManager.terminate();
                    workerManager = null;
                }

                buttonToolbarRunStop.setAttribute('onclick', 'clickedRunProgram()');
                buttonToolbarRunStop.setAttribute('title', MSG_TOOLTIP_BUTTON_RUNSTOP_RUN);
                buttonToolbarRunStopImage.innerHTML = 'play_arrow';
                buttonToolbarRunStop.disabled = false;
                blockEditGUI(false);
                blockRenderGUI(true);

                if (divRenderGUI.style.display === 'block') {
                    $.growl.warning({
                        message: MSG_INFO_NO_PROGRAM_RUNNING_RENDERED_GUI_BLOCKED
                    });
                }

                break;

            case workerProtocol.TYPE_RES_MESSAGE_CONSOLE:
                console.log('*** MSG CON');
                if (message.data !== null && message.data !== '') {
                    if ($textareaProgramExecutionConsole.hasClass('waiting')) {
                        $textareaProgramExecutionConsole.removeClass('waiting');
                        textareaProgramExecutionConsole.value = message.data;
                        textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;
                        break;
                    }

                    textareaProgramExecutionConsole.value += message.data;
                    textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;
                }
                break;

            case workerProtocol.TYPE_RES_ERROR:
                if (message.data !== null && message.data !== '') {
                    textareaProgramExecutionConsole.value += message.data;
                    textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;
                }
                clickedStopProgram();
                break;

            case workerProtocol.TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD:
                if (message.data.data.widget) {
                    var widgetOutputField = document.getElementById(message.data.data.widget);

                    if (widgetOutputField) {
                        widgetOutputField.value = message.data.data.value;
                    }
                }
                break;

            case workerProtocol.TYPE_RES_MESSAGE_GUI_PLOT:
                if (message.data.data.widget) {
                    if (message.data.data.widget in plotConfigs) {
                        updateWidgetPlot(message.data.data.widget, parseFloat(message.data.data.value));
                    }
                }
                break;

            case workerProtocol.TYPE_RES_SUBWORKER_DONE:
                if (message.data !== null && message.data !== '') {
                    eval(message.data);
                }
        }
    }
}

function prepareImports() {
    var docLocationSplit = [];
    var docLocation = '';
    var workerImportsList = [];

    docLocationSplit = document.location.href.split('/');
    docLocationSplit.pop();
    docLocationSplit.push('js/');
    docLocation = docLocationSplit.join('/');

    for (var i = 0; i < LIST_IMPORT_SCRIPTS.length; i++) {
        workerImportsList.push('importScripts(\'' + docLocation + LIST_IMPORT_SCRIPTS[i] + '\');');
    }
    workerImportsList.push('\n');
    return workerImportsList.join('\n');
}

function prepareJavaScriptCode(code) {
    var returnedCode = [];
    var workerImports = prepareImports();

    try {
        returnedCode = workerImports + babel.transform(code).code;
    } catch (e) {
        return [false, String(e)];
    }

    return [true, String(returnedCode)];
}

function eventHandlerLoadIframeProgramEditor(e) {
    // Assign the program editor.
    programEditor = iframeProgramEditor.contentWindow['programEditor'];

    // Checks view port size and also compatibility.
    checkCompatibility();
}

function closeAllOpenDialogs(e) {
    for (var dialog in dialogs) {
        if (dialogs[dialog].open) dialogs[dialog].close();
    }
}

function checkViewportSize(e) {
    var width = Modernizr.mq('(min-width: 1025px)');
    var height = Modernizr.mq('(min-height: 512px)');

    if (!width || !height) return false;

    return true;
}

// Compatibility checks.
function checkCompatibility(e) {
    // Check view port size.
    if (!checkViewportSize()) {
        closeAllOpenDialogs();
        dialogs.errorScreenSizeSmall.showModal();
        divBody.style.display = 'none';

        return false;
    }

    // Check Blob.
    if (!Modernizr.bloburls || !Modernizr.blobconstructor) {
        closeAllOpenDialogs();
        dialogs.errorNoBlob.showModal();
        divBody.style.display = 'none';

        return false;
    }

    // Check Web Workers.
    if (!Modernizr.webworkers) {
        closeAllOpenDialogs();
        dialogs.errorNoWebWorker.showModal();
        divBody.style.display = 'none';

        return false;
    }

    // Check if Blockly toolbox was loaded.
    if (!Modernizr.blocklytoolboxloaded) {
        if (window.chrome) {
            closeAllOpenDialogs();
            dialogs.errorToolboxLoadFailedChrome.showModal();
        } else {
            closeAllOpenDialogs();
            dialogs.errorToolboxLoadFailed.showModal();
        }

        divBody.style.display = 'none';

        return false;
    }

    // Check if worker manager code was loaded.
    if (!Modernizr.workermanagercodeloaded) {
        closeAllOpenDialogs();
        dialogs.errorToolboxLoadFailedChrome.showModal();

        divBody.style.display = 'none';

        return false;
    }

    // Check if the GUI editor was initialized properly.
    if (!Modernizr.guieditor) {
        closeAllOpenDialogs();
        dialogs.errorGUIEditor.showModal();
        divBody.style.display = 'none';

        return false;
    }

    closeAllOpenDialogs();
    divBody.style.display = 'block';

    return true; // All compatibility tests passed.
}

function viewSwitcher(switchTo) {
    switch (switchTo) {
        case INDEX_VIEW_PROGRAM_EDITOR:
            divGUIEditor.style.display = 'none';
            divProgramEditor.style.display = 'block';
            divExecuteProgram.style.display = 'none';
            break;
        case INDEX_VIEW_GUI_EDITOR:
            divGUIEditor.style.display = 'block';
            divProgramEditor.style.display = 'none';
            divExecuteProgram.style.display = 'none';
            break;
        case INDEX_VIEW_EXECUTE_PROGRAM:
            divGUIEditor.style.display = 'none';
            divProgramEditor.style.display = 'none';
            divExecuteProgram.style.display = 'block';
            break;
    }
}

function eventHandlerClickaProgramEditor(e) {
    viewSwitcher(INDEX_VIEW_PROGRAM_EDITOR);
    return false; // So the link would not follow.
}

function eventHandlerClickaGUIEditor(e) {
    if (PROGRAM_STATUS_RUNNING) {
        snackbar.MaterialSnackbar.showSnackbar({
            message: MSG_SNACKBAR_GUI_EDITOR_DISABLED,
            timeout: 2500
        });
    }
    viewSwitcher(INDEX_VIEW_GUI_EDITOR);
    return false; // So the link would not follow.
}

function eventHandlerClickaExecuteProgram(e) {
    viewSwitcher(INDEX_VIEW_EXECUTE_PROGRAM);
    return false; // So the link would not follow.
}

function eventHandlerClickButtonExecuteProgramStopProgram(e) {
    $buttonExecuteProgramStopProgram.attr('disabled', true);
    $buttonExecuteProgramRunProgram.removeAttr('disabled');
    textareaProgramExecutionConsole.value = MSG_OUTPUT_CONSOLE_NO_PROGRAM_RUNNING;

    /*
    $textareaProgramExecutionConsole.addClass('waiting');
    textareaProgramExecutionConsole.value = 'Program running. Waiting for output...';
    textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;
    */
}

function eventHandlerClickButtonExecuteProgramRunProgram(e) {
    var subworkerBlobsUrlArray = [];
    var dictProgramEditorToCode = {};
    var retPrepareJavaScriptCodeWorkerManager = [];

    dictProgramEditorToCode = Blockly.JavaScript.workspaceToCode(programEditor);

    if (!dictProgramEditorToCode) {
        closeAllOpenDialogs();
        dialogs.errorProgramEditorEmpty.showModal();
        return;
    }

    definitionsGeneratedCode = dictProgramEditorToCode.definitions;

    retPrepareJavaScriptCodeWorkerManager = prepareJavaScriptCode(dictProgramEditorToCode.dictVariablesInit + codeWorkerManager);

    if (!retPrepareJavaScriptCodeWorkerManager[0]) {
        textareaProgramExecutionConsole.value = MSG_ERROR_JAVASCRIPT_PREPARE_CODE_FAILED;
        textareaProgramExecutionConsole.value += retPrepareJavaScriptCodeWorkerManager[1];
        textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;
        return;
    }

    for (var i = 0; i < dictProgramEditorToCode.implementationTopLevelBlocks.length; i++) {
        var retPrepareJavaScriptCode = prepareJavaScriptCode(dictProgramEditorToCode.implementationTopLevelBlocks[i]);

        if (!retPrepareJavaScriptCode[0]) {
            textareaProgramExecutionConsole.value = MSG_ERROR_JAVASCRIPT_PREPARE_CODE_FAILED;
            textareaProgramExecutionConsole.value += retPrepareJavaScriptCode[1];
            textareaProgramExecutionConsole.scrollTop = textareaProgramExecutionConsole.scrollHeight;
            return;
        }
        subworkerBlobsUrlArray.push(window.URL.createObjectURL(new Blob([retPrepareJavaScriptCode[1]])));
    }

    workerManager = new Worker(window.URL.createObjectURL(new Blob([retPrepareJavaScriptCodeWorkerManager[1]])));

    workerManager.onmessage = eventHandlerMessageWorkerManager;

    if (subworkerBlobsUrlArray.length > 0) {
        workerManager.postMessage(workerProtocol.getMessage(workerProtocol.SENDER_GUI,
            workerProtocol.TYPE_REQ_PROGRAM_START,
            subworkerBlobsUrlArray));
        //buttonToolbarRunStop.disabled = true;
        return;
    }
    eventHandlerResProgramStartAck();
}

jQuery(document).ready(function($) {
    /*
     * All JavaScript code that requires that the page has
     * finished loading goes here.
     */

    // Elements of the page.
    divBody = document.getElementById('divBody');
    divGUIEditor = document.getElementById('divGUIEditor');
    divProgramEditor = document.getElementById('divProgramEditor');
    textAreaGUIEditor = document.getElementById('textAreaGUIEditor');
    $textAreaGUIEditor = $(textAreaGUIEditor); // jQuery object.
    divExecuteProgram = document.getElementById('divExecuteProgram');
    iframeProgramEditor = document.getElementById('iframeProgramEditor');
    $iframeProgramEditor = $(iframeProgramEditor); // jQuery object.
    divExecuteProgramRenderedGUI = document.getElementById('divExecuteProgramRenderedGUI');
    buttonExecuteProgramRunProgram = document.getElementById('buttonExecuteProgramRunProgram');
    $buttonExecuteProgramRunProgram = $(buttonExecuteProgramRunProgram); // jQuery object.
    buttonExecuteProgramStopProgram = document.getElementById('buttonExecuteProgramStopProgram');
    $buttonExecuteProgramStopProgram = $(buttonExecuteProgramStopProgram); // jQuery object.
    textareaProgramExecutionConsole = document.getElementById('textareaProgramExecutionConsole');
    $textareaProgramExecutionConsole = $(textareaProgramExecutionConsole); // jQuery object.
    divExecuteProgramRenderedGUIEmpty = document.getElementById('divExecuteProgramRenderedGUIEmpty');

    // Snackbar
    snackbar = document.getElementById('snackbar');

    // Dialogs.
    dialogs.errorNoBlob = document.getElementById('dialogErrorNoBlob');
    dialogs.errorGUIEditor = document.getElementById('dialogErrorGUIEditor');
    dialogs.errorNoWebWorker = document.getElementById('dialogErrorNoWebWorker');
    dialogs.errorScreenSizeSmall = document.getElementById('dialogErrorScreenSizeSmall');
    dialogs.errorToolboxLoadFailed = document.getElementById('dialogErrorToolboxLoadFailed');
    dialogs.errorProgramEditorEmpty = document.getElementById('dialogErrorProgramEditorEmpty');
    dialogs.errorToolboxLoadFailedChrome = document.getElementById('dialogErrorWorkerManagerCodeLoadFailed');

    dialogs.errorProgramEditorEmpty.querySelector('.dialogButtonClose').addEventListener('click', function(e) {
        dialogs.errorProgramEditorEmpty.close();
    });

    // Add custom Modernizr tests.
    Modernizr.addTest('dialogs', function(e) {
        if (!document.querySelector('dialog').showModal) return false;
        return true;
    });

    Modernizr.addTest('blocklytoolboxloaded', function(e) {
        /*
         * If being accessed without a server then Google Chrome must be launched with,
         * "--allow-file-access-from-files" parameter to be able to use TVPL.
         */
        var reqHttp = null;
        var xmlBlocklyToolbox = null;

        try {
            if (window.XMLHttpRequest) {
                reqHttp = new XMLHttpRequest();
            } else {
                reqHttp = new ActiveXObject("Microsoft.XMLHTTP");
            }

            reqHttp.open('GET',
                'xml/toolbox.xml',
                false); // Synchronous.
            reqHttp.send();
            xmlBlocklyToolbox = reqHttp.responseXML;

            return true;
        } catch (e) {
            return false;
        }
    });

    Modernizr.addTest('workermanagercodeloaded', function(e) {
        var reqHttp = null;

        try {
            if (window.XMLHttpRequest) {
                reqHttp = new XMLHttpRequest();
            } else {
                reqHttp = new ActiveXObject("Microsoft.XMLHTTP");
            }

            reqHttp.open('GET',
                'js/workerManagerCode.js',
                false); // Synchronous.
            reqHttp.send();
            codeWorkerManager = reqHttp.responseText;

            return true;
        } catch (e) {
            return false;
        }
    });

    Modernizr.addTest('guieditor', function(e) {
        try {
            /*
             * It is a requirement of the GUI editor that the <textarea> on which it is
             * being initialized be a jQuery object.
             */

            $textAreaGUIEditor.formBuilder();
            return true;
        } catch (e) {
            return false;
        }
    });

    // Use polyfill for dialogs if dialogs aren't available.
    if (!Modernizr.dialogs) {
        for (var dialog in dialogs) {
            // Dialog polyfill registration has to be for each defined dialog.
            dialogPolyfill.registerDialog(dialogs[dialog]);
        }
    }

    /*
     * Register event handlers for the main view switching
     * links (Program Editor, GUI Editor and Execute Program).
     */
    $('#aProgramEditor').click(eventHandlerClickaProgramEditor);
    $('#aGUIEditor').click(eventHandlerClickaGUIEditor);
    $('#aExecuteProgram').click(eventHandlerClickaExecuteProgram);

    // Register windows resize handler.
    window.addEventListener('resize', checkCompatibility, false);

    // Now wait until the program editor has finished loading and only then continue.
    $iframeProgramEditor.load(eventHandlerLoadIframeProgramEditor);
});
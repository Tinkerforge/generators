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
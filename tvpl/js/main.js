// It is a good pattern to keep content and control separate.

/*
 * All the variables and functions that require a JavaScript scope of the page should
 * be declared outside the jQuery document ready callback function. Otherwise the JavaScript
 * variables will have scope limited only to the callback function.
 */

// Constants. Stuff that don't change during runtime.

var FILENAME_GUI_EDITOR = 'tvpl.gui';
var FILENAME_PROGRAM_EDITOR = 'tvpl.prg';
var INDEX_VIEW_PROGRAM_EDITOR = 1;
var INDEX_VIEW_GUI_EDITOR = 2;
var INDEX_VIEW_EXECUTE_PROGRAM = 3;
var LIST_IMPORT_SCRIPTS = [
    'Tinkerforge.js',
    'subworkers.js',
    'babelRuntime.js',
    'babelBrowser.js',
    'babelPolyfill.js',
    'workerProtocol.js'
];
var MONTH_NAMES = ['Jan',
    'Feb',
    'Mar',
    'Apr',
    'May',
    'Jun',
    'Jul',
    'Aug',
    'Sep',
    'Oct',
    'Nov',
    'Dec'
];
var MSG_SNACKBAR_GUI_EDITOR_DISABLED =
    'GUI editor is disabled as a program is currently running.';
var MSG_SNACKBAR_EXECUTE_PROGRAM_RENDERED_GUI_DISABLED =
    'Rendered GUI is disabled no program is currently running.';
var MSG_OUTPUT_CONSOLE_WAITING_OUTPUT =
    'Program running. Waiting for output...';
var MSG_OUTPUT_CONSOLE_NO_PROGRAM_RUNNING =
    'A running program can print text on this output console.\n\nSTATUS: No program running.';
var MSG_ERROR_JAVASCRIPT_PREPARE_CODE_FAILED =
    'ERROR: The following error occurred while preparing JavaScript code.\n\n\n';

// Variables.

/*
 * Elements of the page.
 * Assigned in the jQuery document ready callback function.
 */
var divBody = null;
var divGUIEditor = null;
var $divGUIEditor = null; // jQuery object.
var divProgramEditor = null;
var textAreaGUIEditor = null;
var divExecuteProgram = null;
var $textAreaGUIEditor = null; // jQuery object.
var iframeProgramEditor = null;
var program_status_running = false;
var divExecuteProgramRenderedGUI = null;
var $divExecuteProgramRenderedGUI = null; // jQuery object.
var buttonExecuteProgramRunProgram = null;
var $buttonExecuteProgramRunProgram = null; // jQuery object.
var buttonExecuteProgramStopProgram = null;
var textareaProgramExecutionConsole = null;
var $buttonExecuteProgramStopProgram = null; // jQuery object
var $textareaProgramExecutionConsole = null; // jQuery object.
var divExecuteProgramRenderedGUIEmpty = null;

var dialogs = {};
var snackbar = null;
var plotConfigs = {};
var programEditor = null;
var workerManager = null;
var xmlBlocklyToolbox = null;
var codeWorkerManager = null;

// Functions.

function drawPlotWidget(plotWidget, plotData) {
    var wasVisibility = $divExecuteProgramRenderedGUI.css('display');

    $divExecuteProgramRenderedGUI.css('display', 'block');
    plotWidget.setData(plotData);
    plotWidget.setupGrid();
    plotWidget.draw();
    // Restore visibility.
    $divExecuteProgramRenderedGUI.css('display', wasVisibility);
}

function updatePlotWidget(nameWidgetPlot, value) {
    var plotConfig = plotConfigs[nameWidgetPlot];

    if (!plotConfig.plot) {
        return;
    }

    if (plotConfig.axisY.data.length < plotConfig.dataPoints) {
        // Append new data point.
        var dataLength = plotConfig.axisY.data.length;
        plotConfig.axisY.data.push([dataLength, value]);
    } else if (plotConfig.axisY.data.length == plotConfig.dataPoints) {
        // Shift data set and then append new data point.
        plotConfig.axisY.data.shift();

        for (var i = 0; i < plotConfig.axisY.data.length; i++) {
            plotConfig.axisY.data[i] = [plotConfig.axisY.data[i][0] - 1, plotConfig.axisY.data[i][1]];
        }

        plotConfig.axisY.data.push([plotConfig.dataPoints - 1, value]);
    } else {
        return;
    }

    drawPlotWidget(plotConfig.plot, [plotConfig.axisY]);
}

function updatePlotWidgetConfigs(e) {
    for (var plotCfg in plotConfigs) {
        var found = false;

        for (var i in divExecuteProgramRenderedGUI.childNodes) {
            if (divExecuteProgramRenderedGUI.childNodes[i].tagName !== 'DIV') continue;

            for (var j in divExecuteProgramRenderedGUI.childNodes[i].children) {
                if (divExecuteProgramRenderedGUI.childNodes[i].children[j].id === plotCfg) {
                    found = true;
                    break;
                }
            }

            if (found) break;
        }

        if (!found) {
            // Remove corresponding plot configuration.
            delete plotConfigs[plotCfg];
        }
    }
}

function resetRenderPlotWidgets(e) {
    updatePlotWidgetConfigs();

    for (var plotCfg in plotConfigs) {
        plotConfigs[plotCfg].axisY.data = [
            [0, 0]
        ];
        plotConfigs[plotCfg].plot = $.plot(document.getElementById(plotCfg), [plotConfigs[plotCfg].axisY],
            plotConfigs[plotCfg].options);

        drawPlotWidget(plotConfigs[plotCfg].plot, [plotConfigs[plotCfg].axisY]);
    }
}

function toggleDivGUIEditor(enable) {
    if (enable) {
        $divGUIEditor.addClass('enabled');
        $divGUIEditor.removeClass('disabled');
        return;
    }

    $divGUIEditor.addClass('disabled');
    $divGUIEditor.removeClass('enabled');

    snackbar.MaterialSnackbar.showSnackbar({
        message: MSG_SNACKBAR_GUI_EDITOR_DISABLED,
        timeout: 2500
    });
}

function toggleDivExecuteProgramRenderedGUI(enable) {
    if (enable) {
        $divExecuteProgramRenderedGUI.addClass('enabled');
        $divExecuteProgramRenderedGUI.removeClass('disabled');
        return;
    }

    $divExecuteProgramRenderedGUI.addClass('disabled');
    $divExecuteProgramRenderedGUI.removeClass('enabled');

    if ($divExecuteProgramRenderedGUIEmpty.css('display') === 'none')
        snackbar.MaterialSnackbar.showSnackbar({
            message: MSG_SNACKBAR_EXECUTE_PROGRAM_RENDERED_GUI_DISABLED,
            timeout: 2500
        });
}

function eventHandlerClickGUIButton(id, functionToCall) {
    if (!id || !functionToCall) return;

    var unescapedFunctionToCall = unescape(functionToCall);
    var code = 'onmessage = function (e) {\n' +
        '  _dispatch_message(e.data);\n' +
        '};\n' +
        'onerror = _error_handler;\n' +
        'function *_main() {\n' +
        '    yield* ' + unescapedFunctionToCall + ';\n' +
        '    self.postMessage(workerProtocol.getMessage(_worker_id, workerProtocol._TYPE_RES_SUBWORKER_DONE, _code_button_enable));\n' +
        '}\n' +
        '_iterator_main = _main();\n';

    var codeProgramEditor = Blockly.JavaScript.workspaceToCode(programEditor);

    if (!codeProgramEditor) {
        return;
    }

    var codeRaw = [codeProgramEditor.definitions, code].join('\n');
    var retPrepareJavaScriptCode = prepareJavaScriptCode(codeRaw);

    if (!retPrepareJavaScriptCode[0]) {
        return;
    }

    var blobFunction = window.URL.createObjectURL(new Blob([retPrepareJavaScriptCode[1]]));
    document.getElementById(id).disabled = true;
    workerManager.postMessage(workerProtocol.getMessage(workerProtocol.SENDER_GUI,
        workerProtocol.TYPE_REQ_FUNCTION_EXECUTE, {
            blobFunction: blobFunction,
            codeButtonEnable: 'document.getElementById(\'' + id + '\').disabled = false;'
        }));
}

function eventHandlerChangeTextAreaGUIEditor(e) {
    if ($textAreaGUIEditor.val() === '') {
        $divExecuteProgramRenderedGUI.hide();
        $divExecuteProgramRenderedGUIEmpty.show();
    } else {
        $divExecuteProgramRenderedGUI.show();
        $divExecuteProgramRenderedGUIEmpty.hide();
    }
}

function eventHandlerMessageWorkerManager(e) {
    var message = null;

    if (typeof(e.data) !== 'object') {
        return;
    }

    message = e.data;

    if (message.type !== null && workerProtocol.isNumber(message.type)) {
        switch (message.type) {
            case workerProtocol.TYPE_RES_PROGRAM_START_ACK:
                /*
                 * Update program running status.
                 * Views are enabled/disabled based on the value of this status variable.
                 */
                program_status_running = true;
                // Disable run program button.
                $buttonExecuteProgramRunProgram.attr('disabled', true);
                // Enable stop program button
                $buttonExecuteProgramStopProgram.removeAttr('disabled');
                // Program output console in waiting state.
                $textareaProgramExecutionConsole.addClass('waiting');
                textareaProgramExecutionConsole.value =
                    MSG_OUTPUT_CONSOLE_WAITING_OUTPUT;
                textareaProgramExecutionConsole.scrollTop =
                    textareaProgramExecutionConsole.scrollHeight;

                toggleDivGUIEditor(false);
                toggleDivExecuteProgramRenderedGUI(true);

                break;

            case workerProtocol.TYPE_RES_PROGRAM_STOP_ACK:
                if (workerManager) {
                    workerManager.terminate();
                    workerManager = null;
                }

                program_status_running = false;

                // Update Start/Stop button.
                $buttonExecuteProgramStopProgram.attr('disabled', true);
                $buttonExecuteProgramRunProgram.removeAttr('disabled');

                // Update program output console.
                textareaProgramExecutionConsole.value =
                    MSG_OUTPUT_CONSOLE_NO_PROGRAM_RUNNING;
                textareaProgramExecutionConsole.scrollTop =
                    textareaProgramExecutionConsole.scrollHeight;

                toggleDivGUIEditor(true);
                toggleDivExecuteProgramRenderedGUI(false);

                break;

            case workerProtocol.TYPE_RES_MESSAGE_CONSOLE:
                if (message.data !== null && message.data !== '') {
                    if ($textareaProgramExecutionConsole.hasClass('waiting')) {
                        $textareaProgramExecutionConsole.removeClass('waiting');
                        textareaProgramExecutionConsole.value =
                            message.data;
                        textareaProgramExecutionConsole.scrollTop =
                            textareaProgramExecutionConsole.scrollHeight;

                        break;
                    }

                    textareaProgramExecutionConsole.value += message.data;
                    textareaProgramExecutionConsole.scrollTop =
                        textareaProgramExecutionConsole.scrollHeight;
                }
                break;

            case workerProtocol.TYPE_RES_ERROR:
                if (message.data !== null && message.data !== '') {
                    textareaProgramExecutionConsole.value += message.data;
                    textareaProgramExecutionConsole.scrollTop =
                        textareaProgramExecutionConsole.scrollHeight;
                }
                eventHandlerClickButtonExecuteProgramStopProgram();

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
                        updatePlotWidget(message.data.data.widget,
                            parseFloat(message.data.data.value));
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

function closeAllOpenDialogsWithoutCloseButton(e) {
    for (var dialog in dialogs) {
        if (!dialogs[dialog].querySelector('.dialogButtonClose')) {
            // Try to close only if it is open otherwise an exception is thrown.
            if (dialogs[dialog].open) dialogs[dialog].close();
        }
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
        closeAllOpenDialogsWithoutCloseButton();
        dialogs.errorScreenSizeSmall.showModal();
        divBody.style.display = 'none';

        return false;
    }

    // Check Blob.
    if (!Modernizr.bloburls || !Modernizr.blobconstructor) {
        closeAllOpenDialogsWithoutCloseButton();
        dialogs.errorNoBlob.showModal();
        divBody.style.display = 'none';

        return false;
    }

    // Check Web Workers.
    if (!Modernizr.webworkers) {
        closeAllOpenDialogsWithoutCloseButton();
        dialogs.errorNoWebWorker.showModal();
        divBody.style.display = 'none';

        return false;
    }

    // Check if Blockly toolbox was loaded.
    if (!Modernizr.blocklytoolboxloaded) {
        if (window.chrome) {
            closeAllOpenDialogsWithoutCloseButton();
            dialogs.errorToolboxLoadFailedChrome.showModal();
        } else {
            closeAllOpenDialogsWithoutCloseButton();
            dialogs.errorToolboxLoadFailed.showModal();
        }

        divBody.style.display = 'none';

        return false;
    }

    // Check if worker manager code was loaded.
    if (!Modernizr.workermanagercodeloaded) {
        closeAllOpenDialogsWithoutCloseButton();
        dialogs.errorToolboxLoadFailedChrome.showModal();

        divBody.style.display = 'none';

        return false;
    }

    // Check if the GUI editor was initialized properly.
    if (!Modernizr.guieditor) {
        closeAllOpenDialogsWithoutCloseButton();
        dialogs.errorGUIEditor.showModal();
        divBody.style.display = 'none';

        return false;
    }

    closeAllOpenDialogsWithoutCloseButton();

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

function eventHandlerLoadProjectFile(fileInput) {
    var zip = null;
    var file = null;
    var fileReader = null;
    var guiEditorText = '';
    var xmlProgramEditorText = '';
    var newTextAreaGUIEditor = null;

    if (fileInput.value.substr(-5) !== '.tvpl') {
        dialogs.errorLoadProjectFileInvalid.showModal();
        return;
    }

    try {
        file = fileInput.files[0];
        fileReader = new FileReader();

        fileReader.onload = function(e) {
            zip = new JSZip(fileReader.result);

            if (!zip.file(FILENAME_PROGRAM_EDITOR)) {
                throw 1;
            }

            if (!zip.file(FILENAME_GUI_EDITOR)) {
                throw 1;
            }

            xmlProgramEditorText = zip.file(FILENAME_PROGRAM_EDITOR).asText();
            guiEditorText = zip.file(FILENAME_GUI_EDITOR).asText();

            if (xmlProgramEditorText !== '') {
                programEditor.clear();
                Blockly.Xml.domToWorkspace(programEditor, Blockly.Xml.textToDom(xmlProgramEditorText));

                if (program_status_running)
                    eventHandlerClickButtonExecuteProgramStopProgram();
            }

            if (xmlProgramEditorText !== '') {
                // Remove the textarea which is child of the top level div of the view.
                divGUIEditor.removeChild(document.getElementById('frmb-0-form-wrap'));

                // Recreate the text area
                newTextAreaGUIEditor = document.createElement('textarea');
                newTextAreaGUIEditor.setAttribute('id', 'textAreaGUIEditor');
                divGUIEditor.appendChild(newTextAreaGUIEditor);
                textAreaGUIEditor = newTextAreaGUIEditor;
                $textAreaGUIEditor = $(newTextAreaGUIEditor);

                // Re-initialize form builder
                $textAreaGUIEditor.val(guiEditorText);
                $textAreaGUIEditor.formBuilder();
                $textAreaGUIEditor.formRender({
                    container: $divExecuteProgramRenderedGUI
                });
            }
        }
        fileReader.readAsArrayBuffer(file);
    } catch (e) {
        dialogs.errorLoadProjectReadFailed.showModal();
    }
}

function eventHandlerClickaLoadProject(e) {
    inputLoadProjectFile.click();
    return false; // So the link would not follow.
}

function eventHandlerClickaSaveProject(e) {
    try {
        var xmlProgramEditorText = '';
        var guiEditorText = '';
        var d = new Date();
        var zip = null;
        var zipContent = null;
        var projectFileNameTVPL = MONTH_NAMES[d.getUTCMonth()] +
            d.getUTCDate() +
            '_' +
            d.getUTCHours() +
            '_' +
            d.getUTCMinutes() +
            '_' +
            d.getUTCSeconds() +
            '.tvpl';

        xmlProgramEditorText = Blockly.Xml.domToPrettyText(Blockly.Xml.workspaceToDom(programEditor));

        if (divExecuteProgramRenderedGUI.childNodes.length > 0) {
            guiEditorText = $textAreaGUIEditor.val();
        }

        // Initiate JSZip.
        zip = new JSZip();
        // Create program editor and GUI editor files.
        zip.file(FILENAME_PROGRAM_EDITOR, xmlProgramEditorText);
        zip.file(FILENAME_GUI_EDITOR, guiEditorText);
        // Generate ZIP file.
        zipContent = zip.generate({ type: "blob" });
        // Save the generated ZIP file.
        saveAs(zipContent, projectFileNameTVPL);
    } catch (e) {
        dialogs.errorSaveProjectFailed.showModal();
    }

    return false; // So the link would not follow.
}

function eventHandlerClickaAbout(e) {
    dialogs.informationAbout.showModal();

    return false; // So the link would not follow.
}

function eventHandlerClickaProgramEditor(e) {
    viewSwitcher(INDEX_VIEW_PROGRAM_EDITOR);
    return false; // So the link would not follow.
}

function eventHandlerClickaGUIEditor(e) {
    if (program_status_running) {
        toggleDivGUIEditor(false);
    } else {
        toggleDivGUIEditor(true);
    }

    viewSwitcher(INDEX_VIEW_GUI_EDITOR);
    return false; // So the link would not follow.
}

function eventHandlerClickaExecuteProgram(e) {
    if (program_status_running) {
        toggleDivExecuteProgramRenderedGUI(true);
    } else {
        toggleDivExecuteProgramRenderedGUI(false);
    }

    viewSwitcher(INDEX_VIEW_EXECUTE_PROGRAM);
    return false; // So the link would not follow.
}

function eventHandlerClickButtonExecuteProgramStopProgram(e) {
    /*
     * Just send a request to the worker manager to stop.
     * What should be done after stop is handled in the
     * stop ACK case when the worker manager sends the response.
     */
    if (workerManager !== null) {
        workerManager.postMessage(workerProtocol.getMessage(
            workerProtocol.SENDER_GUI,
            workerProtocol.TYPE_REQ_PROGRAM_STOP,
            null));
    }

}

function eventHandlerClickButtonExecuteProgramRunProgram(e) {
    var subworkerBlobsUrlArray = [];
    var dictProgramEditorToCode = {};
    var retPrepareJavaScriptCodeWorkerManager = [];

    dictProgramEditorToCode = Blockly.JavaScript.workspaceToCode(programEditor);

    if (!dictProgramEditorToCode) {
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
        return;
    }
}

jQuery(document).ready(function($) {
    /*
     * All JavaScript code that requires that the page has
     * finished loading goes here.
     */

    /*
     * Mix of jQuery object and DOM objects is needed because each
     * is better with specific features. Sometimes jQuery causes
     * trouble for example in case of cross frame scripting.
     */

    // Elements of the page.
    divBody = document.getElementById('divBody');
    divGUIEditor = document.getElementById('divGUIEditor');
    $divGUIEditor = $(divGUIEditor); // jQuery object.
    divProgramEditor = document.getElementById('divProgramEditor');
    textAreaGUIEditor = document.getElementById('textAreaGUIEditor');
    $textAreaGUIEditor = $(textAreaGUIEditor); // jQuery object.
    divExecuteProgram = document.getElementById('divExecuteProgram');
    iframeProgramEditor = document.getElementById('iframeProgramEditor');
    $iframeProgramEditor = $(iframeProgramEditor); // jQuery object.
    divExecuteProgramRenderedGUI = document.getElementById('divExecuteProgramRenderedGUI');
    $divExecuteProgramRenderedGUI = $(divExecuteProgramRenderedGUI); // jQuery object.
    buttonExecuteProgramRunProgram = document.getElementById('buttonExecuteProgramRunProgram');
    $buttonExecuteProgramRunProgram = $(buttonExecuteProgramRunProgram); // jQuery object.
    buttonExecuteProgramStopProgram = document.getElementById('buttonExecuteProgramStopProgram');
    $buttonExecuteProgramStopProgram = $(buttonExecuteProgramStopProgram); // jQuery object.
    textareaProgramExecutionConsole = document.getElementById('textareaProgramExecutionConsole');
    $textareaProgramExecutionConsole = $(textareaProgramExecutionConsole); // jQuery object.
    divExecuteProgramRenderedGUIEmpty = document.getElementById('divExecuteProgramRenderedGUIEmpty');
    $divExecuteProgramRenderedGUIEmpty = $(divExecuteProgramRenderedGUIEmpty); // jQuery object.

    // Snackbar
    snackbar = document.getElementById('snackbar');

    // Dialogs.
    dialogs.errorNoBlob = document.getElementById('dialogErrorNoBlob');
    dialogs.errorGUIEditor = document.getElementById('dialogErrorGUIEditor');
    dialogs.informationAbout = document.getElementById('dialogInformationAbout');
    dialogs.errorNoWebWorker = document.getElementById('dialogErrorNoWebWorker');
    dialogs.errorScreenSizeSmall = document.getElementById('dialogErrorScreenSizeSmall');
    dialogs.errorSaveProjectFailed = document.getElementById('dialogErrorSaveProjectFailed');
    dialogs.errorToolboxLoadFailed = document.getElementById('dialogErrorToolboxLoadFailed');
    dialogs.errorProgramEditorEmpty = document.getElementById('dialogErrorProgramEditorEmpty');
    dialogs.errorLoadProjectReadFailed = document.getElementById('dialogErrorLoadProjectReadFailed');
    dialogs.errorLoadProjectFileInvalid = document.getElementById('dialogErrorLoadProjectFileInvalid');
    dialogs.errorToolboxLoadFailedChrome = document.getElementById('dialogErrorWorkerManagerCodeLoadFailed');

    // Dialogs with close button.
    dialogs.informationAbout.querySelector('.dialogButtonClose').addEventListener('click', function(e) {
        dialogs.informationAbout.close();
    });

    dialogs.errorSaveProjectFailed.querySelector('.dialogButtonClose').addEventListener('click', function(e) {
        dialogs.errorSaveProjectFailed.close();
    });

    dialogs.errorLoadProjectReadFailed.querySelector('.dialogButtonClose').addEventListener('click', function(e) {
        dialogs.errorLoadProjectReadFailed.close();
    });

    dialogs.errorLoadProjectFileInvalid.querySelector('.dialogButtonClose').addEventListener('click', function(e) {
        dialogs.errorLoadProjectFileInvalid.close();
    });

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
    $('#aGUIEditor').click(eventHandlerClickaGUIEditor);
    $('#aProgramEditor').click(eventHandlerClickaProgramEditor);
    $('#aExecuteProgram').click(eventHandlerClickaExecuteProgram);

    /*
     * Register event handlers for the drawer button
     * links (Load Project, Save Project and About).
     */
    $('#aAbout').click(eventHandlerClickaAbout);
    $('#aLoadProject').click(eventHandlerClickaLoadProject);
    $('#aSaveProject').click(eventHandlerClickaSaveProject);

    // Register windows resize handler.
    window.addEventListener('resize', checkCompatibility, false);

    // Now wait until the program editor has finished loading and only then continue.
    $iframeProgramEditor.load(eventHandlerLoadIframeProgramEditor);
});

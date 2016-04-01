// It is a good pattern to keep content and control separate.

/*
 * All the variables and functions that require a JavaScript scope of the page should
 * be declared outside the jQuery document ready callback function. Otherwise the JavaScript
 * variables will have scope limited only to the callback function.
 */

var blocklyDiv = null;
var blocklyArea = null;
var programEditor = null;
var xmlBlocklyToolbox = null;

jQuery(document).ready(function($) {
    /*
     * All JavaScript code that requires that the page has
     * finished loading goes here.
     */
    var xmlHttp = null;

    xmlBlocklyToolbox = null;
    blocklyDiv = document.getElementById('blocklyDiv');
    blocklyArea = document.getElementById('blocklyArea');

    /*
     * If being accessed without a server then Google Chrome must
     * be launched with "--allow-file-access-from-files" parameter to be able to use TVPL.
     *
     * We are not verifying toolbox load here because it is being done in main.js.
     * If toolbox loading has problem it will be caught while loading index.html and
     * reported there. In that case the execution would not reach upto loading the
     * program editor.
     */
    if (window.XMLHttpRequest) {
        xmlHttp = new XMLHttpRequest();
    } else {
        xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlHttp.open('GET', 'xml/toolbox.xml', false);
    xmlHttp.send();
    xmlBlocklyToolbox = xmlHttp.responseXML;

    programEditor = Blockly.inject(blocklyDiv, {
        grid: {
            snap: true,
            length: 3,
            Colour: '#ccc',
            spacing: 25
        },
        zoom: {
            wheel: true,
            maxScale: 3,
            minScale: 0.3,
            controls: true,
            startScale: 1.0,
            scaleSpeed: 1.2
        },
        media: 'media/',
        toolbox: xmlBlocklyToolbox.getElementById('toolboxTVPL'),
        trashcan: true
    });

    function onResize(e) {
        // Compute the absolute coordinates and dimensions of blocklyArea.
        var element = blocklyArea;
        var x = 0;
        var y = 0;

        do {
            x += element.offsetLeft;
            y += element.offsetTop;
            element = element.offsetParent;
        }
        while (element);

        // Position blocklyDiv over blocklyArea.
        blocklyDiv.style.left = x + 'px';
        blocklyDiv.style.top = y + 'px';
        blocklyDiv.style.width = blocklyArea.offsetWidth + 'px';
        blocklyDiv.style.height = blocklyArea.offsetHeight + 'px';

        // Must call this so that the workspace bounds actually get redrawn before next click event.
        Blockly.svgResize(programEditor);
    };

    window.addEventListener('resize', onResize, false);
    onResize();
});
importScripts('Tinkerforge.js');

var TVPL_WORKER_CMD_END = '____TVPL:WORKER:CMD:END____';

handlerOnMessage = function(e) {
  try {
    eval(e.data);
  } catch(e) {
      postMessage(String('ERROR: ' + e + '\n'));
      postMessage(TVPL_WORKER_CMD_END);
  }
  postMessage(TVPL_WORKER_CMD_END);
}

self.onmessage = handlerOnMessage;

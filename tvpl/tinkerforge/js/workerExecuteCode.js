importScripts('Tinkerforge.js');

handlerOnMessage = function(e) {
  try {
    eval(e.data);
  } catch(e) {
      postMessage(String('ERROR: ' + e + '\n'));
  }
}

self.onmessage = handlerOnMessage;

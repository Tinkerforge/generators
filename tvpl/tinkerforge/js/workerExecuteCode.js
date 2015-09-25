importScripts('Tinkerforge.js');
importScripts('workerProtocol.js');
importScripts('babelPolyfill.js');
importScripts('babelRuntime.js');
importScripts('babelBrowser.js');

handlerOnMessage = function(e) {
  try {
    babel.run(babel.transform(e.data).code);
  } catch(e) {
      postMessage(workerProtocolSendMessage(WORKER_PROTOCOL_TYPE_MESSAGE,
                                            String('ERROR: ' + e + '\n')));
      postMessage(workerProtocolSendMessage(WORKER_PROTOCOL_TYPE_COMMAND,
                                            WORKER_PROTOCOL_TYPE_DATA_COMMAND_END));
  }
}

self.onmessage = handlerOnMessage;

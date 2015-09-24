importScripts('Tinkerforge.js');
importScripts('workerProtocol.js');

handlerOnMessage = function(e) {
  try {
    eval(e.data);
  } catch(e) {
      postMessage(String('ERROR: ' + e + '\n'));
      postMessage(workerProtocolSendMessage(WORKER_PROTOCOL_TYPE_COMMAND,
                                            WORKER_PROTOCOL_TYPE_DATA_COMMAND_END));
  }
}

self.onmessage = handlerOnMessage;

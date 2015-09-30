function dispatchMessage(message) {
  var messageParsed = JSON.parse(message);

  if (messageParsed.type === null || !workerProtocol.isNumber(messageParsed.type)) {
    postMessage(workerProtocol.getMessage(workerProtocol.TYPE_COMMAND_WORKER_GENERIC_ERROR,
                                          String('ERROR: Malformed protocol message recieved from master.\n')));
  }
  else {
    switch(messageParsed.type) {
      case workerProtocol.TYPE_COMMAND_MASTER_CODE_EXEC_START:
        if (messageParsed.data === null || messageParsed.data === '') {
          postMessage(workerProtocol.getMessage(workerProtocol.TYPE_COMMAND_WORKER_CODE_EXEC_ERROR,
                                                'ERROR: No code provided by master to execute.\n'));
        }
        else {
          babel.run(babel.transform(messageParsed.data).code);
        }
        break;

      case workerProtocol.TYPE_COMMAND_MASTER_CODE_EXEC_STOP:
        self.close();
        break;

      default:
        postMessage(workerProtocol.getMessage(workerProtocol.TYPE_COMMAND_WORKER_GENERIC_ERROR,
                                              'ERROR: Unknown message type received from master.\n'));
    }
  }
}

handlerOnMessage = function(e) {
  dispatchMessage(e.data);
}

handlerOnError = function(e) {
  postMessage(workerProtocol.getMessage(workerProtocol.TYPE_COMMAND_WORKER_CODE_EXEC_ERROR,
                                        String(e.message)));
}

self.onmessage = handlerOnMessage;
self.onerror   = handlerOnError;

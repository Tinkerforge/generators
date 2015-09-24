var workerProtocol = {};
var WORKER_PROTOCOL_TYPE_COMMAND = 1;
var WORKER_PROTOCOL_TYPE_MESSAGE = 2;
var WORKER_PROTOCOL_TYPE_DATA_COMMAND_END = 1;

function workerProtocolSendMessage(type, data) {
  workerProtocol.type = type;
  workerProtocol.data = data;
  return JSON.stringify(workerProtocol);
}

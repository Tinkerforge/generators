var workerProtocol = {};

workerProtocol.TYPE_MESSAGE = 1;
workerProtocol.TYPE_COMMAND_MASTER_CODE_EXEC_START = 2;
workerProtocol.TYPE_COMMAND_MASTER_CODE_EXEC_STOP = 3;
workerProtocol.TYPE_COMMAND_WORKER_GENERIC_ERROR = 4;
workerProtocol.TYPE_COMMAND_WORKER_CODE_EXEC_ERROR = 5;
workerProtocol.TYPE_COMMAND_WORKER_CODE_EXEC_END = 6;

workerProtocol.isNumber = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

workerProtocol.getMessage = function(type, data) {
  var message = {};
  message.type = type;
  message.data = data;
  return JSON.stringify(message);
}

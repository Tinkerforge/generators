var workerProtocol = {};

workerProtocol.TYPE_MESSAGE = 1;
workerProtocol.TYPE_COMMAND_MASTER_STOP = 2;
workerProtocol.TYPE_COMMAND_WORKER_ERROR = 3;

workerProtocol.isNumber = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

workerProtocol.getMessage = function(type, data) {
  var message = {};
  message.type = type;
  message.data = data;
  return JSON.stringify(message);
}

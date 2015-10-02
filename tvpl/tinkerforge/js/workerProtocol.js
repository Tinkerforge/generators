var workerProtocol = {};

/*
 * Requests are master --> worker
 * Responses are master <-- worker
 */
workerProtocol.TYPE_REQUEST_CALL_FUNCTION = 1;
workerProtocol.TYPE_REQUEST_STOP_EXECUTION = 2;
workerProtocol.TYPE_RESPONSE_ERROR = 3;
workerProtocol.TYPE_RESPONSE_CONSOLE_MESSAGE = 4;

workerProtocol.isNumber = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

workerProtocol.getMessage = function(type, data) {
  var message = {};
  message.type = type;
  message.data = data;
  return JSON.stringify(message);
}

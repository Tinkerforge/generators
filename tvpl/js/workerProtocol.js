/*
 *
 * All communication from the UI (user interface)
 * is handled by the worker manager which manages
 * multiple Web Workers as required.
 *
 * Requests are,  UI --> worker manager
 * Responses are, UI <-- worker manager
 *
 * Respons and requests starting with an underscore are
 * only for communicating between the worker manager and
 * sub Web Workers. In this case,
 *
 * Requests are,  worker manager --> workers
 * Responses are, worker manager <-- workers
 *
 * Every request has a corresponding ACK message.
 *
 */

var workerProtocol = {};

workerProtocol.SENDER_GUI = 1;
workerProtocol.SENDER_WORKER_MANAGER = 2;

workerProtocol.TYPE_REQ_PROGRAM_START = 3;
workerProtocol.TYPE_REQ_PROGRAM_STOP  = 4;
workerProtocol.TYPE_REQ_FUNCTION_EXECUTE  = 5;
workerProtocol.TYPE_RES_PROGRAM_START_ACK = 6;
workerProtocol.TYPE_RES_PROGRAM_STOP_ACK = 7;
workerProtocol.TYPE_RES_FUNCTION_EXECUTE_ACK = 8;
workerProtocol.TYPE_RES_SUBWORKER_DONE = 9;
workerProtocol.TYPE_RES_MESSAGE_CONSOLE = 10;
workerProtocol.TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD = 11;
workerProtocol.TYPE_RES_MESSAGE_GUI_PLOT = 12;
workerProtocol.TYPE_RES_ERROR = 13;

workerProtocol._TYPE_REQ_SUBWORKER_START = 14;
workerProtocol._TYPE_REQ_FUNCTION_TF_RETURN = 15;
workerProtocol._TYPE_REQ_SET_VARIABLE = 16;
workerProtocol._TYPE_REQ_YIELD_NEXT = 17;
workerProtocol._TYPE_RES_SUBWORKER_START_ACK = 18;
workerProtocol._TYPE_RES_FUNCTION_TF_RETURN_ACK = 19;
workerProtocol._TYPE_RES_SET_VARIABLE_ACK = 20;
workerProtocol._TYPE_RES_YIELD_NEXT_ACK = 21;
workerProtocol._TYPE_RES_SET_VARIABLE = 22;
workerProtocol._TYPE_RES_FUNCTION_TF_CALL = 23;
workerProtocol._TYPE_RES_SUBWORKER_DONE = 24;
workerProtocol._TYPE_RES_MESSAGE_CONSOLE = 25;
workerProtocol._TYPE_RES_MESSAGE_GUI_OUTPUT_FIELD = 26;
workerProtocol._TYPE_RES_MESSAGE_GUI_PLOT = 27;
workerProtocol._TYPE_RES_ERROR = 28;

workerProtocol.isNumber = function(n) {
  return !isNaN(parseFloat(n)) && isFinite(n);
};

workerProtocol.getMessage = function(sender, type, data) {
  var message = {};
  message.sender = sender;
  message.type = type;
  message.data = data;
  return message;
}

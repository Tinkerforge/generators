function octave_example_authenticate()
    more off;

    global SECRET;

    HOST = "localhost";
    PORT = 4223;
    SECRET = "My Authentication Secret!";

    ipcon = java_new("com.tinkerforge.IPConnection"); % Create IP connection

    % Register Connected Callback
    ipcon.addConnectedCallback(@cb_connected);

    % Register Enumerate Callback
    ipcon.addEnumerateCallback(@cb_enumerate);

    ipcon.connect(HOST, PORT); % Connect to brickd

    input("Press any key to exit...\n", "s");
    ipcon.disconnect();
end

% Authenticate each time the connection got (re-)established
function cb_connected(e)
    ipcon = e.getSource();

    global SECRET;

    if strcmp(e.connectReason.toString(), ipcon.CONNECT_REASON_REQUEST.toString())
        fprintf("Connected by request\n");
    elseif strcmp(e.connectReason.toString(), ipcon.CONNECT_REASON_AUTO_RECONNECT.toString())
        fprintf("Auto-Reconnect\n");
    end

    % Authenticate first...
    try
        ipcon.authenticate(SECRET);
        fprintf("Authentication succeeded\n");
    catch ex
        fprintf("Could not authenticate\n");
        return
    end

    % ...then trigger enumerate
    ipcon.enumerate();
end

% Print incoming enumeration
function cb_enumerate(e)
    fprintf("UID: %s, Enumeration Type: %s\n", e.uid, e.enumerationType.toString());
end

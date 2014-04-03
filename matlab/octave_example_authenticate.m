function octave_example_authenticate
    more off;

    global ipcon;
    global SECRET;

    HOST = "localhost";
    PORT = 4223;
    SECRET = "My Authentication Secret!";

    ipcon = java_new("com.tinkerforge.IPConnection"); % Create IP connection

    % Register Connected Callback
    ipcon.addConnectedListener("cb_connected");

    % Register Enumerate Callback
    ipcon.addEnumerateListener("cb_enumerate");

    ipcon.connect(HOST, PORT); % Connect to brickd

    input("Press any key to exit...\n", "s");
    ipcon.disconnect();
end

% Authenticate each time the connection got (re-)established
function cb_connected(connect_reason)
    global SECRET;
    global ipcon;

    if strcmp(connect_reason.toString(), ipcon.CONNECT_REASON_REQUEST.toString())
        fprintf('Connected by request\n');
    elseif strcmp(connect_reason.toString(), ipcon.CONNECT_REASON_AUTO_RECONNECT.toString())
        fprintf('Auto-Reconnect\n');
    end

    % Authenticate first...
    try
        ipcon.authenticate(SECRET);
        fprintf('Authentication succeeded\n');
    catch e
        fprintf('Could not authenticate\n');
        return
    end

    % ...then trigger enumerate
    ipcon.enumerate();
end

% Print incoming enumeration
function cb_enumerate(uid, connected_uid, position, hardware_version,
                      firmware_version, device_identifier, enumeration_type)
    fprintf("UID: %s, Enumeration Type: %s\n", uid, enumeration_type.toString());
end

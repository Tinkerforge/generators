function octave_example_authenticate()
    more off;

    global SECRET;

    HOST = "localhost";
    PORT = 4223;
    SECRET = "My Authentication Secret!";

    ipcon = javaObject("com.tinkerforge.IPConnection"); % Create IP connection

    % Disable auto reconnect mechanism, in case we have the wrong secret.
    % If the authentication is successful, reenable it.
    ipcon.setAutoReconnect(false)

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

    if java2int(e.connectReason) == java2int(ipcon.CONNECT_REASON_REQUEST)
        fprintf("Connected by request\n");
    elseif java2int(e.connectReason) == java2int(ipcon.CONNECT_REASON_AUTO_RECONNECT)
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

    % ...reenable auto reconnect mechanism, as described above...
    ipcon.setAutoReconnect(true)

    % ...then trigger enumerate
    ipcon.enumerate();
end

% Print incoming enumeration
function cb_enumerate(e)
    fprintf("UID: %s, Enumeration Type: %d\n", e.uid, e.enumerationType);
end

function int = java2int(value)
    if compare_versions(version(), "3.8", "<=")
        int = value.intValue();
    else
        int = value;
    end
end

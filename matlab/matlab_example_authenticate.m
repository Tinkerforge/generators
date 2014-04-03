function matlab_example_authenticate
    import com.tinkerforge.IPConnection;

    global SECRET;
    global ipcon;

    HOST = 'localhost';
    PORT = 4223;
    SECRET = 'My Authentication Secret!';

    ipcon = IPConnection(); % Create IP connection

    % Register Connected Callback
    set(ipcon, 'ConnectedCallback', @(h, e)cb_connected(e.connectReason));

    % Register Enumerate Callback
    set(ipcon, 'EnumerateCallback', @(h, e)cb_enumerate(e.uid, e.connectedUid, e.position, ...
                                                        e.hardwareVersion, e.firmwareVersion, ...
                                                        e.deviceIdentifier, e.enumerationType));

    ipcon.connect(HOST, PORT); % Connect to brickd

    input('Press any key to exit...\n', 's');
    ipcon.disconnect();
end

% Authenticate each time the connection got (re-)established
function cb_connected(connect_reason)
    global SECRET;
    global ipcon;

    if connect_reason == ipcon.CONNECT_REASON_REQUEST
        fprintf('Connected by request\n');
    elseif connect_reason == ipcon.CONNECT_REASON_AUTO_RECONNECT
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
    fprintf('UID: %s, Enumeration Type: %g\n', char(uid), enumeration_type);
end

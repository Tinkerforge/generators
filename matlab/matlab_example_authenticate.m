function matlab_example_authenticate()
    import com.tinkerforge.IPConnection;

    global SECRET;

    HOST = 'localhost';
    PORT = 4223;
    SECRET = 'My Authentication Secret!';

    ipcon = IPConnection(); % Create IP connection

    % Register Connected Callback
    set(ipcon, 'ConnectedCallback', @(h, e) cb_connected(e));

    % Register Enumerate Callback
    set(ipcon, 'EnumerateCallback', @(h, e) cb_enumerate(e));

    ipcon.connect(HOST, PORT); % Connect to brickd

    input('Press any key to exit...\n', 's');
    ipcon.disconnect();
end

% Authenticate each time the connection got (re-)established
function cb_connected(e)
    ipcon = e.getSource();

    global SECRET;

    if e.connectReason == ipcon.CONNECT_REASON_REQUEST
        fprintf('Connected by request\n');
    elseif e.connectReason == ipcon.CONNECT_REASON_AUTO_RECONNECT
        fprintf('Auto-Reconnect\n');
    end

    % Authenticate first...
    try
        ipcon.authenticate(SECRET);
        fprintf('Authentication succeeded\n');
    catch ex
        fprintf('Could not authenticate\n');
        return
    end

    % ...then trigger enumerate
    ipcon.enumerate();
end

% Print incoming enumeration
function cb_enumerate(e)
    fprintf('UID: %s, Enumeration Type: %g\n', char(e.uid), e.enumerationType);
end

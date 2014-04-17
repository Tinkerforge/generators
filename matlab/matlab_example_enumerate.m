function matlab_example_enumerate()
    import com.tinkerforge.IPConnection;

    HOST = 'localhost';
    PORT = 4223;

    ipcon = IPConnection(); % Create IP connection

    ipcon.connect(HOST, PORT); % Connect to brickd

    % Register Enumerate Callback
    set(ipcon, 'EnumerateCallback', @(h, e) cb_enumerate(e));

    % Trigger Enumerate
    ipcon.enumerate();

    input('Press any key to exit...\n', 's');
    ipcon.disconnect();
end

% Print incoming enumeration
function cb_enumerate(e)
    ipcon = e.getSource();

    fprintf('UID: %s\n', char(e.uid));
    fprintf('Enumeration Type: %g\n', e.enumerationType);

    if e.enumerationType == ipcon.ENUMERATION_TYPE_DISCONNECTED
        fprintf('\n');
        return;
    end

    fprintf('Connected UID: %s\n', char(e.connectedUid));
    fprintf('Position: %s\n', e.position);
    fprintf('Hardware Version: ');
    fprintf('%d', rot90(e.hardwareVersion));
    fprintf('\n');
    fprintf('Firmware Version: ');
    fprintf('%d', rot90(e.firmwareVersion));
    fprintf('\n');
    fprintf('Device Identifier: %g\n', e.deviceIdentifier);
    fprintf('\n');
end

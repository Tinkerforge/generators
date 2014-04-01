function matlab_example_enumerate
    import com.tinkerforge.IPConnection;
    
    HOST = 'localhost';
    PORT = 4223;
    
    global ipcon;
    ipcon = IPConnection(); % Create IP connection

    ipcon.connect(HOST, PORT); % Connect to brickd
    % Don't use device before ipcon is connected

    % Register Enumerate Callback
    set(ipcon, 'EnumerateCallback', @(h, e)cb_enumerate(e.uid, e.connectedUid, e.position, ...
                                                e.hardwareVersion, e.firmwareVersion, ...
                                                e.deviceIdentifier, e.enumerationType));

    % Trigger Enumerate
    ipcon.enumerate();
    
    input('\nPress any key to exit...\n', 's');
    ipcon.disconnect();
end

% Print incoming enumeration
function cb_enumerate(uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type)
    global ipcon;
    fprintf('Enumeration Type: %g\n', enumeration_type);

    if enumeration_type == ipcon.ENUMERATION_TYPE_DISCONNECTED
        fprintf('\n');
        return;
    end
    fprintf('UID: %s\n', char(uid));
    fprintf('Connected UID: %s\n', char(connected_uid));
    fprintf('Position: %s\n', position);
    fprintf('Hardware Version: ');
    fprintf('%d', rot90(hardware_version));
    fprintf('\n');
    fprintf('Firmware Version: ');
    fprintf('%d', rot90(firmware_version));
    fprintf('\n');
    fprintf('Device Identifier: %g\n', device_identifier);
    fprintf('\n');
end

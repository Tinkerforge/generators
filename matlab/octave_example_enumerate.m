function octave_example_enumerate
    more off;

    HOST = "localhost";
    PORT = 4223;

    global ipcon;
    ipcon = java_new("com.tinkerforge.IPConnection"); % Create IP connection

    ipcon.connect(HOST, PORT); % Connect to brickd

    % Register Enumerate Callback
    ipcon.addEnumerateListener("cb_enumerate");

    % Trigger Enumerate
    ipcon.enumerate();

    input("Press any key to exit...\n", "s");
    ipcon.disconnect();
end

% Print incoming enumeration
function cb_enumerate(uid, connected_uid, position, hardware_version,
                      firmware_version, device_identifier, enumeration_type)
    global ipcon;

    fprintf("UID: %s\n", uid);
    fprintf("Enumeration Type: %s\n", enumeration_type.toString());

    if strcmp(enumeration_type.toString(), ipcon.ENUMERATION_TYPE_DISCONNECTED.toString())
        fprintf("\n");
        return;
    end

    fprintf("Connected UID: %s\n", connected_uid);
    fprintf("Position: %s\n", position.toString());
    fprintf("Hardware Version: %s.%s.%s\n",hardware_version(1).toString(), ...
            hardware_version(2).toString(), hardware_version(3).toString());
    fprintf("Firmware Version: %s.%s.%s\n",firmware_version(1).toString(), ...
            firmware_version(2).toString(), firmware_version(3).toString());
    fprintf("Device Identifier: %g\n", device_identifier);
    fprintf("\n");
end

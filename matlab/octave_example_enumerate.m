function octave_example_enumerate()
    more off;

    HOST = "localhost";
    PORT = 4223;

    ipcon = java_new("com.tinkerforge.IPConnection"); % Create IP connection

    ipcon.connect(HOST, PORT); % Connect to brickd

    % Register Enumerate Callback
    ipcon.addEnumerateCallback(@cb_enumerate);

    % Trigger Enumerate
    ipcon.enumerate();

    input("Press any key to exit...\n", "s");
    ipcon.disconnect();
end

% Print incoming enumeration
function cb_enumerate(e)
    ipcon = e.getSource();

    fprintf("UID: %s\n", e.uid);
    fprintf("Enumeration Type: %s\n", e.enumerationType.toString());

    if strcmp(e.enumerationType.toString(), ipcon.ENUMERATION_TYPE_DISCONNECTED.toString())
        fprintf("\n");
        return;
    end

    hardwareVersion = e.hardwareVersion;
    firmwareVersion = e.firmwareVersion;

    fprintf("Connected UID: %s\n", e.connectedUid);
    fprintf("Position: %s\n", e.position.toString());
    fprintf("Hardware Version: %s.%s.%s\n", hardwareVersion(1).toString(), ...
                                            hardwareVersion(2).toString(), ...
                                            hardwareVersion(3).toString());
    fprintf("Firmware Version: %s.%s.%s\n", firmwareVersion(1).toString(), ...
                                            firmwareVersion(2).toString(), ...
                                            firmwareVersion(3).toString());
    fprintf("Device Identifier: %g\n", e.deviceIdentifier);
    fprintf("\n");
end

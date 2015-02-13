using Tinkerforge;

class ExampleEnumerate
{
	private static string HOST = "localhost";
	private static int PORT = 4223;

	// Print incoming enumeration
	static void EnumerateCB(IPConnection sender,
	                        string uid, string connectedUid, char position,
	                        short[] hardwareVersion, short[] firmwareVersion,
	                        int deviceIdentifier, short enumerationType)
	{
		System.Console.WriteLine("UID:               " + uid);
		System.Console.WriteLine("Enumeration Type:  " + enumerationType);

		if(enumerationType == IPConnection.ENUMERATION_TYPE_DISCONNECTED)
		{
			System.Console.WriteLine("");
			return;
		}

		System.Console.WriteLine("Connected UID:     " + connectedUid);
		System.Console.WriteLine("Position:          " + position);
		System.Console.WriteLine("Hardware Version:  " + hardwareVersion[0] + "." +
		                                                 hardwareVersion[1] + "." +
		                                                 hardwareVersion[2]);
		System.Console.WriteLine("Firmware Version:  " + firmwareVersion[0] + "." +
		                                                 firmwareVersion[1] + "." +
		                                                 firmwareVersion[2]);
		System.Console.WriteLine("Device Identifier: " + deviceIdentifier);
		System.Console.WriteLine("");
	}

	static void Main()
	{
		// Create connection and connect to brickd
		IPConnection ipcon = new IPConnection();
		ipcon.Connect(HOST, PORT);

		// Register Enumerate Callback
		ipcon.EnumerateCallback += EnumerateCB;

		// Trigger Enumerate
		ipcon.Enumerate();

		System.Console.WriteLine("Press key to exit");
		System.Console.ReadLine();
		ipcon.Disconnect();
	}
}

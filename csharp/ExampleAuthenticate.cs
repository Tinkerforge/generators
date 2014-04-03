using Tinkerforge;

class ExampleAuthenticate
{
	private static string HOST = "localhost";
	private static int PORT = 4223;
	private static string SECRET = "My Authentication Secret!";

	// Authenticate each time the connection got (re-)established
	static void ConnectedCB(IPConnection sender, short connectReason)
	{
		switch(connectReason)
		{
			case IPConnection.CONNECT_REASON_REQUEST:
				System.Console.WriteLine("Connected by request");
				break;

			case IPConnection.CONNECT_REASON_AUTO_RECONNECT:
				System.Console.WriteLine("Auto-Reconnected");
				break;
		}

		// Authenticate first...
		try
		{
			sender.Authenticate(SECRET);
			System.Console.WriteLine("Authentication succeeded");
		}
		catch(TinkerforgeException)
		{
			System.Console.WriteLine("Could not authenticate");
			return;
		}

		// ...then trigger enumerate
		sender.Enumerate();
	}

	// Print incoming enumeration
	static void EnumerateCB(IPConnection sender,
	                        string uid, string connectedUid, char position,
	                        short[] hardwareVersion, short[] firmwareVersion,
	                        int deviceIdentifier, short enumerationType)
	{
		System.Console.WriteLine("UID: " + uid + ", Enumeration Type: " + enumerationType);
	}

	static void Main()
	{
		// Create IP Connection
		IPConnection ipcon = new IPConnection();

		// Register Connected Callback
		ipcon.Connected += ConnectedCB;

		// Register Enumerate Callback
		ipcon.EnumerateCallback += EnumerateCB;

		// Connect to brickd
		ipcon.Connect(HOST, PORT);

		System.Console.WriteLine("Press key to exit");
		System.Console.ReadKey();
		ipcon.Disconnect();
	}
}

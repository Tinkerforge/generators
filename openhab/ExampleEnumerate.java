import com.tinkerforge.IPConnection;

public class ExampleEnumerate {
	private static final String HOST = "localhost";
	private static final int PORT = 4223;

	// Note: To make the example code cleaner we do not handle exceptions. Exceptions you
	//       might normally want to catch are described in the documentation
	public static void main(String args[]) throws Exception {
		// Create connection and connect to brickd
		IPConnection ipcon = new IPConnection();
		ipcon.connect(HOST, PORT);

		// Register enumerate listener and print incoming information
		ipcon.addEnumerateListener(new IPConnection.EnumerateListener() {
			public void enumerate(String uid, String connectedUid, char position,
			                      short[] hardwareVersion, short[] firmwareVersion,
			                      int deviceIdentifier, short enumerationType) {
				System.out.println("UID:               " + uid);
				System.out.println("Enumeration Type:  " + enumerationType);

				if(enumerationType == IPConnection.ENUMERATION_TYPE_DISCONNECTED) {
					System.out.println("");
					return;
				}

				System.out.println("Connected UID:     " + connectedUid);
				System.out.println("Position:          " + position);
				System.out.println("Hardware Version:  " + hardwareVersion[0] + "." +
				                                           hardwareVersion[1] + "." +
				                                           hardwareVersion[2]);
				System.out.println("Firmware Version:  " + firmwareVersion[0] + "." +
				                                           firmwareVersion[1] + "." +
				                                           firmwareVersion[2]);
				System.out.println("Device Identifier: " + deviceIdentifier);
				System.out.println("");
			}
		});

		ipcon.enumerate();

		System.out.println("Press key to exit"); System.in.read();
		ipcon.disconnect();
	}
}

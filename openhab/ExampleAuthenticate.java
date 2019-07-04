import com.tinkerforge.IPConnection;
import com.tinkerforge.TinkerforgeException;
import java.security.SignatureException;

public class ExampleAuthenticate {
	private static final String HOST = "localhost";
	private static final int PORT = 4223;
	private static final String SECRET = "My Authentication Secret!";

	// Note: To make the example code cleaner we do not handle exceptions. Exceptions you
	//       might normally want to catch are described in the documentation
	public static void main(String args[]) throws Exception {
		// Note: Declare ipcon final, so the listener can access it
		final IPConnection ipcon = new IPConnection(); // Create IP Connection

		// Disable auto reconnect mechanism, in case we have the wrong secret.
		// If the authentication is successful, reenable it.
		ipcon.setAutoReconnect(false);

		// Register enumerate listener and print incoming information
		ipcon.addConnectedListener(new IPConnection.ConnectedListener() {
			public void connected(short connectReason) {
				switch(connectReason) {
				case IPConnection.CONNECT_REASON_REQUEST:
					System.out.println("Connected by request");
					break;

				case IPConnection.CONNECT_REASON_AUTO_RECONNECT:
					System.out.println("Auto-Reconnect");
					break;
				}

				// Authenticate first...
				try {
					ipcon.authenticate(SECRET);
					System.out.println("Authentication succeeded");
				} catch(TinkerforgeException e) {
					System.out.println("Could not authenticate: " + e.getMessage());
					return;
				}

				// ...reenable auto reconnect mechanism, as described below...
				ipcon.setAutoReconnect(true);

				// ...then trigger enumerate
				try {
					ipcon.enumerate();
				} catch(TinkerforgeException e) {
				}
			}
		});

		// Register enumerate listener and print incoming information
		ipcon.addEnumerateListener(new IPConnection.EnumerateListener() {
			public void enumerate(String uid, String connectedUid, char position,
			                      short[] hardwareVersion, short[] firmwareVersion,
			                      int deviceIdentifier, short enumerationType) {
				System.out.println("UID: " + uid + ", Enumeration Type: " + enumerationType);
			}
		});

		// Connect to brickd
		ipcon.connect(HOST, PORT);

		System.out.println("Press key to exit"); System.in.read();
		ipcon.disconnect();
	}
}

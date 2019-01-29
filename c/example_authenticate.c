#include <stdio.h>

#include "ip_connection.h"

#define HOST "localhost"
#define PORT 4223
#define SECRET "My Authentication Secret!"

// Authenticate each time the connection got (re-)established
void cb_connected(uint8_t connect_reason, void *user_data) {
	IPConnection *ipcon = (IPConnection *)user_data;

	switch(connect_reason) {
	case IPCON_CONNECT_REASON_REQUEST:        printf("Connected by request\n"); break;
	case IPCON_CONNECT_REASON_AUTO_RECONNECT: printf("Auto-Reconnected\n"); break;
	}

	// Authenticate first...
	if (ipcon_authenticate(ipcon, SECRET) < 0) {
		fprintf(stderr, "Could not authenticate\n");
		return;
	} else {
		printf("Authentication succeeded\n");
	}

	// ...reenable auto reconnect mechanism, as described below...
	ipcon_set_auto_reconnect(ipcon, true);

	// ...then trigger enumerate
	ipcon_enumerate(ipcon);
}

// Print incoming enumeration information
void cb_enumerate(const char *uid, const char *connected_uid,
                  char position, uint8_t hardware_version[3],
                  uint8_t firmware_version[3], uint16_t device_identifier,
                  uint8_t enumeration_type, void *user_data) {
	// avoid unused parameter warnings
	(void)user_data; (void)connected_uid; (void)position;
	(void)hardware_version; (void)firmware_version; (void)device_identifier;

	printf("UID: %s, Enumeration Type: %d\n", uid, enumeration_type);
}

int main(void) {
	// Create IP Connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	// Disable auto reconnect mechanism, in case we have the wrong secret.
	// If the authentication is successful, reenable it.
	ipcon_set_auto_reconnect(&ipcon, false);

	// Register connected callback to "cb_connected"
	ipcon_register_callback(&ipcon,
	                        IPCON_CALLBACK_CONNECTED,
	                        (void *)cb_connected,
	                        &ipcon);

	// Register enumeration callback to "cb_enumerate"
	ipcon_register_callback(&ipcon,
	                        IPCON_CALLBACK_ENUMERATE,
	                        (void *)cb_enumerate,
	                        NULL);

	// Connect to brickd
	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {
		fprintf(stderr, "Could not connect to brickd\n");
		return 1;
	}

	printf("Press key to exit\n");
	getchar();
	ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally
	return 0;
}

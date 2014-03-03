#include <stdio.h>

#include "ip_connection.h"

#define HOST "localhost"
#define PORT 4223

// Print incoming enumeration information
void cb_enumerate(const char *uid, const char *connected_uid,
                  char position, uint8_t hardware_version[3],
                  uint8_t firmware_version[3], uint16_t device_identifier,
                  uint8_t enumeration_type, void *user_data) {
	(void)user_data;

	printf("UID:               %s\n", uid);
	printf("Enumeration Type:  %d\n", enumeration_type);

	if(enumeration_type == IPCON_ENUMERATION_TYPE_DISCONNECTED) {
		printf("\n");
		return;
	}

	printf("Connected UID:     %s\n", connected_uid);
	printf("Position:          %c\n", position);
	printf("Hardware Version:  %d.%d.%d\n", hardware_version[0],
	                                        hardware_version[1],
	                                        hardware_version[2]);
	printf("Firmware Version:  %d.%d.%d\n", firmware_version[0],
	                                        firmware_version[1],
	                                        firmware_version[2]);
	printf("Device Identifier: %d\n", device_identifier);
	printf("\n");
}

int main() {
	// Create IP Connection
	IPConnection ipcon;
	ipcon_create(&ipcon);

	if(ipcon_connect(&ipcon, HOST, PORT) < 0) {
		fprintf(stderr, "Could not connect to brickd\n");
		exit(1);
	}

	// Register enumeration callback to "cb_enumerate"
	ipcon_register_callback(&ipcon,
	                        IPCON_CALLBACK_ENUMERATE,
	                        (void *)cb_enumerate,
	                        NULL);

	// Trigger enumerate
	ipcon_enumerate(&ipcon);

	printf("Press key to exit\n");
	getchar();
	ipcon_destroy(&ipcon); // Calls ipcon_disconnect internally
}

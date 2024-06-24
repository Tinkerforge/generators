// This example is not self-contained.
// It requires usage of the example driver specific to your platform.
// See the HAL documentation.

#include "src/bindings/hal_common.h"
#include "src/bindings/display_names.h"
#include "src/bindings/errors.h"

void check(int rc, const char *msg);
void example_setup(TF_HAL *hal);
void example_loop(TF_HAL *hal);

void example_setup(TF_HAL *hal) {
	for (uint16_t i = 0; ; ++i) {
		char uid[7];
		char port_name;
		uint16_t device_id;

		int rc = tf_hal_get_device_info(hal, i, uid, &port_name, &device_id);

		if (rc == TF_E_DEVICE_NOT_FOUND) {
			break;
		}

		check(rc, "get device info");

		tf_hal_printf("Port %c: %s [%s]\n", port_name, tf_get_device_display_name(device_id), uid);
	}
}

void example_loop(TF_HAL *hal) {
	// Poll for callbacks
	tf_hal_callback_tick(hal, 0);
}

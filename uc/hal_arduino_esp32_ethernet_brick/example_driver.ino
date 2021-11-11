#include "src/hal_arduino_esp32_ethernet_brick/hal_arduino_esp32_ethernet_brick.h"
#include "src/bindings/errors.h"

// Forward declare the example functions.
extern "C" void example_setup(TF_HalContext *hal);
extern "C" void example_loop(TF_HalContext *hal);

// Used to report any error encountered while running the example.
extern "C" void check(int e_code, const char *c) {
    if (e_code == TF_E_OK) {
        return;
    }

    tf_hal_printf("Failed to %s: %s (error code %d)\n", c, tf_hal_strerror(e_code), e_code);
}

TF_HalContext hal;

void setup() {
    Serial.begin(115200);
    delay(3000);
    Serial.println("Hello World!");

    check(tf_hal_create(&hal), "hal create");
    example_setup(&hal);
}

void loop() {
    example_loop(&hal);
}

#include "src/hal_arduino_esp32/hal_arduino_esp32.h"
#include "src/bindings/errors.h"

// Forward declare the example functions.
extern "C" void example_setup(TF_HalContext *hal);
extern "C" void example_loop(TF_HalContext *hal);

// Change this to your port assignment.
// If you use a HAT or one or more Breakout Bricklets
// you have to connect and list all chip select
// signals, to make sure the signals are separated
// correctly.
TF_Port ports[6] = {{
    .chip_select_pin=27,
    .spi=HSPI,
    .port_name='F'
}, {
    .chip_select_pin=26,
    .spi=HSPI,
    .port_name='E'
}, {
    .chip_select_pin=25,
    .spi=HSPI,
    .port_name='D'
}, {
    .chip_select_pin=17,
    .spi=VSPI,
    .port_name='C'
}, {
    .chip_select_pin=33,
    .spi=VSPI,
    .port_name='B'
}, {
    .chip_select_pin=16,
    .spi=VSPI,
    .port_name='A'
}};

// Used to report any error encountered while running the example.
extern "C" void check(int rc, const char *c) {
    if (rc == TF_E_OK) {
        return;
    }
    
    tf_hal_printf("Failed to %s: %s (return code %d)\n", c, tf_strerror(rc), rc);
}

TF_HalContext hal;

void setup() {
    Serial.begin(115200);
    delay(3000);
    Serial.println("Hello World!");
    
    check(tf_hal_arduino_create(&hal, ports, sizeof(ports)/sizeof(ports[0])), "hal create");
    demo_setup(&hal);
}

void loop() {
    demo_loop(&hal);
}

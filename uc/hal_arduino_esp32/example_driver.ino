#include "src/hal_arduino_esp32/hal_arduino_esp32.h"
#include "src/bindings/errors.h"

// Forward declare the example functions.
extern "C" void example_setup(TF_HAL *hal);
extern "C" void example_loop(TF_HAL *hal);

// Change this to your port assignment.
// If you use a HAT or one or more Breakout Bricklets
// you have to connect and list all chip select
// signals, to make sure the signals are separated
// correctly.
TF_Port ports[6] = {
    TF_PORT(16, VSPI, 'A'),
    TF_PORT(33, VSPI, 'B'),
    TF_PORT(17, VSPI, 'C'),

    TF_PORT(25, HSPI, 'D'),
    TF_PORT(26, HSPI, 'E'),
    TF_PORT(27, HSPI, 'F'),
};

// Used to report any error encountered while running the example.
extern "C" void check(int e_code, const char *c) {
    if (e_code == TF_E_OK) {
        return;
    }

    tf_hal_printf("Failed to %s: %s (error code %d)\n", c, tf_hal_strerror(e_code), e_code);
}

TF_HAL hal;

void setup() {
    Serial.begin(115200);
    delay(3000);
    Serial.println("Hello World!");

    check(tf_hal_create(&hal, ports, sizeof(ports) / sizeof(ports[0])), "hal create");
    example_setup(&hal);
}

void loop() {
    example_loop(&hal);
}

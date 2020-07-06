#include "src/hal_arduino_esp32/hal_arduino_esp32.h"

// Forward declare the demo functions here, as the .ino is
// compiled as C++, however the rest of the bindings is plain C.
// This fixes linkage problems.
extern "C" void demo_setup(TF_HalContext *hal);
extern "C" void demo_loop(TF_HalContext *hal);

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

TF_HalContext hal;

void check(int rc, char *msg) {
    if (rc >= 0)
        return;
    Serial.print(millis());
    Serial.print(" Failed to ");
    Serial.print(msg);
    Serial.print( " rc:");
    Serial.println(rc);
    delay(10);
}

void setup() {
  Serial.begin(115200);
  delay(3000);
  Serial.println("Hello World!");

  check(tf_hal_arduino_init(&hal, ports, sizeof(ports)/sizeof(ports[0])), "hal init");
  demo_setup(&hal);
}

void loop() {
  demo_loop(&hal);
}

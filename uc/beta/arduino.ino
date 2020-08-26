#include "src/hal_arduino/hal_arduino.h"

// Forward declare the demo functions here, as the .ino is
// compiled as C++, however the rest of the bindings is plain C.
// This fixes linkage problems.
extern "C" void demo_setup(TF_HalContext *hal);
extern "C" void demo_loop(TF_HalContext *hal);

TF_Port ports[2] = {{
    .chip_select_pin=9,
    .port_name='A'
}, {
    .chip_select_pin=8,
    .port_name='B'
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

  check(tf_hal_create(&hal, ports, sizeof(ports)/sizeof(ports[0])), "hal create");
  demo_setup(&hal);
}

void loop() {
  demo_loop(&hal);
}

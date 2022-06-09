/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "src/bindings/config.h"
#include "src/hal_arduino_esp32_brick/hal_arduino_esp32_brick.h"
#include "src/bindings/errors.h"

// Forward declare the example functions.
extern "C" void example_setup(TF_HAL *hal);
extern "C" void example_loop(TF_HAL *hal);

// Used to report any error encountered while running the example.
extern "C" void check(int e_code, const char *c) {
    if (e_code == TF_E_OK) {
        return;
    }

#if TF_IMPLEMENT_STRERROR != 0
    tf_hal_printf("Failed to %s: %s (error code %d)\n", c, tf_hal_strerror(e_code), e_code);
#else
    tf_hal_printf("Failed to %s: %d\n", c, e_code);
#endif
}

TF_HAL hal;

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

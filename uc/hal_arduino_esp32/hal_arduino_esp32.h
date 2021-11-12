/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_ARDUINO_ESP32_H
#define TF_HAL_ARDUINO_ESP32_H

#include <stdbool.h>
#include <stdint.h>
#include "../bindings/hal_common.h"
#include "../bindings/macros.h"

#include <SPI.h>

#define TF_PORT(chip_select_pin, spi, port_name) {chip_select_pin, spi, port_name, {._to_init = 0}}

typedef struct TF_Port {
    // external
    uint8_t chip_select_pin;
    uint8_t spi;
    char port_name;
    // internal
    TF_PortCommon port_common;
} TF_Port;

struct TF_HalContext {
    SPISettings spi_settings;
    SPIClass hspi;
    SPIClass vspi;
    TF_Port *ports;
    uint8_t port_count;
    TF_HalCommon hal_common;
};

int tf_hal_create(TF_HalContext *hal, TF_Port *ports, uint8_t port_count) TF_ATTRIBUTE_NONNULL_ALL;
int tf_hal_destroy(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL_ALL;

#endif

/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_ARDUINO_H
#define TF_HAL_ARDUINO_H

#include <stdbool.h>
#include <stdint.h>
#include "../bindings/hal_common.h"
#include "../bindings/macros.h"

#include <SPI.h>

typedef struct TF_Port {
    //external
    int chip_select_pin;
    uint8_t spi;
    char port_name;
} TF_Port;

typedef struct TF_HalContext {
    SPISettings spi_settings;
    SPIClass hspi;
    SPIClass vspi;
    TF_Port *ports;
    size_t port_count;
    TF_HalCommon hal_common;
} TF_HalContext;

#define TF_E_INVALID_PIN_CONFIGURATION -100

int tf_hal_arduino_init(struct TF_HalContext *hal, TF_Port *ports, size_t port_count) TF_ATTRIBUTE_NONNULL_ALL;

#endif

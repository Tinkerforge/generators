/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef HAL_ARDUINO_H
#define HAL_ARDUINO_H

#include <stdbool.h>
#include <stdint.h>

#include "../bindings/hal_common.h"

#include <SPI.h>

typedef struct TF_Port {
    //external
    int chip_select_pin;
    char port_name;
} TF_Port;

typedef struct TF_HalContext {
    SPISettings spi_settings;
    TF_Port *ports;
    size_t port_count;
    TF_HalCommon hal_common;
} TF_HalContext;

int tf_hal_arduino_init(struct TF_HalContext *ctx, TF_Port *ports, size_t port_count) TF_ATTRIBUTE_NONNULL_ALL;

#endif

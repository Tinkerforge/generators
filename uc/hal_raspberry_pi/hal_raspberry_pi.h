/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_RASPBERRY_PI_H
#define TF_HAL_RASPBERRY_PI_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

#include "../bindings/hal_common.h"
#include "../bindings/errors.h"
#include "../bindings/macros.h"

typedef struct TF_Port {
    int chip_select_pin;
    char port_name;
} TF_Port;

struct TF_HalContext {
    TF_Port *ports;
    int port_count;

    TF_HalCommon hal_common;
};

#define TF_E_BCM2835_INIT_FAILED -100
#define TF_E_BCM2835_SPI_BEGIN_FAILED -101

int tf_hal_create(struct TF_HalContext *hal, TF_Port *ports, uint8_t port_count) TF_ATTRIBUTE_NONNULL_ALL;

#endif

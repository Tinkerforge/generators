/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_NULL_H
#define TF_HAL_NULL_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

#include "../bindings/hal_common.h"
#include "../bindings/errors.h"
#include "../bindings/macros.h"

#define TF_PORT(port_name) {port_name, {._to_init = 0}}

typedef struct TF_Port {
    // external
    char port_name;

    // internal
    TF_PortCommon port_common;
} TF_Port;

struct TF_HAL {
    TF_Port *ports;
    uint8_t port_count;
    TF_HALCommon hal_common;
};

int tf_hal_create(struct TF_HAL *hal, TF_Port *ports, uint8_t port_count) TF_ATTRIBUTE_NONNULL_ALL;
int tf_hal_destroy(TF_HAL *hal) TF_ATTRIBUTE_NONNULL_ALL;

#endif

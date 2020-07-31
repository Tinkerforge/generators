/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_LINUX_H
#define TF_HAL_LINUX_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

#include "../bindings/hal_common.h"
#include "../bindings/errors.h"
#include "../bindings/macros.h"

typedef struct TF_Port {
    //external
    int chip_select_pin;
    char port_name;

    //internal
    int _cs_pin_fd;
} TF_Port;

struct TF_HalContext {
    TF_Port *ports;
    int port_count;

    int spidev_fd;
    TF_HalCommon hal_common;
};

#define TF_E_EXPORT_GPIO_FAILED -100
#define TF_E_SET_GPIO_DIRECTION_FAILED -101
#define TF_E_OPEN_GPIO_FAILED -102

#define TF_E_OPEN_SPI_DEV_FAILED -103
#define TF_E_SPI_DEV_CONFIG_FAILED -104
#define TF_E_CHIP_SELECT_FAILED -105
#define TF_E_TRANSCEIVE_FAILED -106

int tf_hal_linux_init(struct TF_HalContext *hal, const char *spidev_path, TF_Port *ports, uint8_t port_count) TF_ATTRIBUTE_NONNULL_ALL;

#endif

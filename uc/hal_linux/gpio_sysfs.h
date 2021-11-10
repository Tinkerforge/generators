/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_LINUX_GPIO_SYSFS_H
#define TF_HAL_LINUX_GPIO_SYSFS_H

#include "../bindings/macros.h"

typedef enum TF_GPIOSYSFSValue {
    TF_GPIO_SYSFS_VALUE_LOW = 0,
    TF_GPIO_SYSFS_VALUE_HIGH,
} TF_GPIOSYSFSValue;

typedef struct TF_GPIOSYSFS {
    char name[32];
    int num;
} TF_GPIOSYSFS;

int gpio_sysfs_export(int cs_pin) TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int gpio_sysfs_unexport(int cs_pin) TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int gpio_sysfs_set_direction_out_with_initial_value(char cs_pin_name[32], TF_GPIOSYSFSValue value) TF_ATTRIBUTE_NONNULL_ALL TF_ATTRIBUTE_WARN_UNUSED_RESULT;
int gpio_sysfs_set_output(char cs_pin_name[32], TF_GPIOSYSFSValue value) TF_ATTRIBUTE_NONNULL_ALL TF_ATTRIBUTE_WARN_UNUSED_RESULT;

#endif

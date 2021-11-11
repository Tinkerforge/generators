/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_HAL_RASPBERRY_PI_UTILS_H
#define TF_HAL_RASPBERRY_PI_UTILS_H

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "../bindings/macros.h"

void microsleep(uint32_t duration);
void millisleep(uint32_t duration);
uint64_t microtime(void);
uint64_t millitime(void);
const char *get_errno_name(int error_code);
int robust_close(int fd);

#endif

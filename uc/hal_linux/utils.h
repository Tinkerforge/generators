/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_UTILS_H
#define TF_UTILS_H

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>

#include "../bindings/macros.h"

const char *get_errno_name(int error_code);

int robust_close(int fd);
ssize_t robust_write(int fd, const void *buffer, int length) TF_ATTRIBUTE_NONNULL_ALL TF_ATTRIBUTE_WARN_UNUSED_RESULT;

#endif

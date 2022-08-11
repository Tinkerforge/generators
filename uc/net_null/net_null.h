/*
 * Copyright (C) 2022 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_NET_NULL_H
#define TF_NET_NULL_H

#include <stdbool.h>
#include <stdint.h>
#include <stddef.h>

#include "../bindings/net_common.h"
#include "../bindings/errors.h"

struct TF_NET {
    uint8_t unused;
};


#endif

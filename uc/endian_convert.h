/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_ENDIAN_CONVERT_H
#define TF_ENDIAN_CONVERT_H

#include <stdint.h>

#ifdef __cplusplus
extern "C" {
#endif

/**
 * \internal
 */
int16_t tf_leconvert_int16_to(int16_t native);

/**
 * \internal
 */
uint16_t tf_leconvert_uint16_to(uint16_t native);

/**
 * \internal
 */
int32_t tf_leconvert_int32_to(int32_t native);

/**
 * \internal
 */
uint32_t tf_leconvert_uint32_to(uint32_t native);

/**
 * \internal
 */
int64_t tf_leconvert_int64_to(int64_t native);

/**
 * \internal
 */
uint64_t tf_leconvert_uint64_to(uint64_t native);

/**
 * \internal
 */
float tf_leconvert_float_to(float native);

/**
 * \internal
 */
int16_t tf_leconvert_int16_from(int16_t little);

/**
 * \internal
 */
uint16_t tf_leconvert_uint16_from(uint16_t little);

/**
 * \internal
 */
int32_t tf_leconvert_int32_from(int32_t little);

/**
 * \internal
 */
uint32_t tf_leconvert_uint32_from(uint32_t little);

/**
 * \internal
 */
int64_t tf_leconvert_int64_from(int64_t little);

/**
 * \internal
 */
uint64_t tf_leconvert_uint64_from(uint64_t little);

/**
 * \internal
 */
float tf_leconvert_float_from(float little);

#ifdef __cplusplus
}
#endif

#endif

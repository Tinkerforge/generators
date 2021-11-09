/*
 * brickd
 * Copyright (C) 2012-2014, 2020 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
 *
 * hmac.h: HMAC functions
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, write to the Free Software Foundation, Inc.,
 * 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
 */

#pragma once

#include <stdint.h>

#include "sha1.h"
#ifdef __cplusplus
extern "C" {
#endif
void tf_hmac_sha1(const uint8_t *secret, int secret_length,
               const uint8_t *data, int data_length,
               uint8_t digest[TF_SHA1_DIGEST_LENGTH]);
#ifdef __cplusplus
}
#endif

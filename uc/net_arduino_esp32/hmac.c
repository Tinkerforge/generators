/*
 * brickd
 * Copyright (C) 2012-2014, 2016, 2018, 2020 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2014 Olaf Lüke <olaf@tinkerforge.com>
 *
 * hmac.c: HMAC functions
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

#include "hmac.h"

void tf_hmac_sha1(const uint8_t *secret, int secret_length,
               const uint8_t *data, int data_length,
               uint8_t digest[TF_SHA1_DIGEST_LENGTH]) {
	TF_SHA1 sha1;
	uint8_t secret_digest[TF_SHA1_DIGEST_LENGTH];
	uint8_t inner_digest[TF_SHA1_DIGEST_LENGTH];
	uint8_t ipad[TF_SHA1_BLOCK_LENGTH];
	uint8_t opad[TF_SHA1_BLOCK_LENGTH];
	int i;

	if (secret_length > TF_SHA1_BLOCK_LENGTH) {
		tf_sha1_init(&sha1);
		tf_sha1_update(&sha1, secret, secret_length);
		tf_sha1_final(&sha1, secret_digest);

		secret = secret_digest;
		secret_length = TF_SHA1_DIGEST_LENGTH;
	}

	// inner digest
	for (i = 0; i < secret_length; ++i) {
		ipad[i] = secret[i] ^ 0x36;
	}

	for (i = secret_length; i < TF_SHA1_BLOCK_LENGTH; ++i) {
		ipad[i] = 0x36;
	}

	tf_sha1_init(&sha1);
	tf_sha1_update(&sha1, ipad, TF_SHA1_BLOCK_LENGTH);
	tf_sha1_update(&sha1, data, data_length);
	tf_sha1_final(&sha1, inner_digest);

	// outer digest
	for (i = 0; i < secret_length; ++i) {
		opad[i] = secret[i] ^ 0x5C;
	}

	for (i = secret_length; i < TF_SHA1_BLOCK_LENGTH; ++i) {
		opad[i] = 0x5C;
	}

	tf_sha1_init(&sha1);
	tf_sha1_update(&sha1, opad, TF_SHA1_BLOCK_LENGTH);
	tf_sha1_update(&sha1, inner_digest, TF_SHA1_DIGEST_LENGTH);
	tf_sha1_final(&sha1, digest);
}

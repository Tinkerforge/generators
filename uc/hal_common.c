/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "hal_common.h"

#include <string.h>
#include <stdio.h>

#include "tfp.h"
#include "bricklet_unknown.h"
#include "base58.h"
#include "macros.h"
#include "errors.h"

int tf_hal_common_create(TF_HalContext *hal) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);
    memset(hal_common, 0, sizeof(TF_HalCommon));
    return TF_E_OK;
}

int tf_hal_common_prepare(TF_HalContext *hal, uint8_t port_count, uint32_t port_discovery_timeout_us) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);
    hal_common->timeout = port_discovery_timeout_us;
    hal_common->port_count = port_count;

    TF_Unknown unknown;
    hal_common->used = 1;

    for(int i = 0; i < port_count; ++i) {
        if (hal_common->used >= sizeof(hal_common->uids) / sizeof(hal_common->uids[0]))
            return TF_E_TOO_MANY_DEVICES;
        tf_unknown_create(&unknown, "1", hal, (uint8_t)i, 0);

        int rc = tf_unknown_comcu_enumerate(&unknown);
        if (rc == TF_E_OK) {
            tf_unknown_callback_tick(&unknown, port_discovery_timeout_us);
        }

        tf_unknown_destroy(&unknown);
    }

    if (hal_common->used > sizeof(hal_common->uids) / sizeof(hal_common->uids[0]))
        return TF_E_TOO_MANY_DEVICES;

    hal_common->timeout = 2500000;

    return TF_E_OK;
}

static void enum_handler(TF_HalContext* hal,
                  uint8_t port_id,
                  char uid[8],
                  char connected_uid[8],
                  char position,
                  uint8_t hw_version[3],
                  uint8_t fw_version[3],
                  uint16_t dev_id,
                  uint8_t enumeration_type) {
    (void) connected_uid;
    (void) position;
    (void) hw_version;
    (void) fw_version;
    (void) enumeration_type;
    TF_HalCommon *hal_common = tf_hal_get_common(hal);
    if (hal_common->used >= sizeof(hal_common->uids) / sizeof(hal_common->uids[0]))
        return;

    uint32_t numeric_uid;
    if(tf_base58_decode(uid, &numeric_uid) != TF_E_OK)
        return;

    for(size_t i = 0; i < hal_common->used; ++i)
        if(hal_common->uids[i] == numeric_uid) {
            hal_common->port_ids[i] = port_id;
            hal_common->dids[i] = dev_id;
            if(hal_common->tfps[i] != NULL)
                hal_common->tfps[i]->spitfp.port_id = port_id;
            return;
        }

    tf_hal_log_info("Found device %s of type %d at port %c\n", uid, dev_id, tf_hal_get_port_name(hal, port_id));

    hal_common->port_ids[hal_common->used] = port_id;
    hal_common->uids[hal_common->used] = numeric_uid;
    hal_common->dids[hal_common->used] = dev_id;
    ++hal_common->used;
}

bool tf_hal_enumerate_handler(TF_HalContext *hal, uint8_t port_id, TF_Packetbuffer *payload) {
    int i;
    char uid[8]; tf_packetbuffer_pop_n(payload, (uint8_t*)uid, 8);
    char connected_uid[8]; tf_packetbuffer_pop_n(payload, (uint8_t*)connected_uid, 8);
    char position = tf_packetbuffer_read_char(payload);
    uint8_t hardware_version[3]; for (i = 0; i < 3; ++i) hardware_version[i] = tf_packetbuffer_read_uint8_t(payload);
    uint8_t firmware_version[3]; for (i = 0; i < 3; ++i) firmware_version[i] = tf_packetbuffer_read_uint8_t(payload);
    uint16_t device_identifier = tf_packetbuffer_read_uint16_t(payload);
    uint8_t enumeration_type = tf_packetbuffer_read_uint8_t(payload);

    //No device before us has patched in the position and connected_uid.
    if(connected_uid[0] == 0)
        position = tf_hal_get_port_name(hal, port_id);

    enum_handler(hal, port_id, uid, connected_uid, position, hardware_version, firmware_version, device_identifier, enumeration_type);

    return true;
}

static const char *alphabet = "0123456789abcdef";

static void log_unsigned(uint64_t value, uint8_t base) {
    if(base < 2 || base > 16)
        return;

    char buffer[64] = {0};

    uint64_t len = 0;
    do {
        uint64_t digit = value % base;
        buffer[64 - len - 1] = alphabet[digit];
        ++len;
        value /= base;
    } while(value > 0);

    tf_hal_log_message(buffer + (64 - len), len);

    return;
}

static void log_signed(int64_t value, uint8_t base) {
    if(value < 0) {
        tf_hal_log_message("-", 1);
        value = -value;
    }

    log_unsigned((uint64_t) value, base);

    return;
}

static void write_chunk(const char *fmt, const char *cursor) {
     if(cursor > fmt) {
        // cursor is on the first character that must not be printed
        size_t chunk_len = (size_t)(cursor - fmt) - 1;
        if(chunk_len != 0)
            tf_hal_log_message(fmt, chunk_len);
    }
}

void tf_hal_printf(const char *fmt, ...){
	va_list va;
	va_start(va, fmt);

    char character;
    const char *cursor = fmt;

	while((character = *(cursor++))) {
        if(character == '\n') {
            write_chunk(fmt, cursor);
            fmt = cursor;

            tf_hal_log_newline();
            continue;
        }

		if(character != '%') {
            continue;
        }

        write_chunk(fmt, cursor);
        fmt = cursor;

        // Parse integer prefixes
        int width = 0;

        if (strncmp(cursor, "I8", 2) == 0) {
            width = 1;
            cursor += 2;
        } else if (strncmp(cursor, "I16", 3) == 0) {
            width = 2;
            cursor += 3;
        } else if (strncmp(cursor, "I32", 3) == 0) {
            width = 4;
            cursor += 3;
        } else if (strncmp(cursor, "I64", 3) == 0) {
            width = 8;
            cursor += 3;
        }

        // Parse and handle non-integer placeholders
        character = *(cursor++);

        switch(character) {
            case '\n': {
                write_chunk(fmt, cursor);
                tf_hal_log_newline();
                fmt = cursor;
                continue;
            }
            case '\0': {
                write_chunk(fmt, cursor);
                va_end(va);
                return;
            }

            case 'c' : {
                char c = (char) va_arg(va, int);
                tf_hal_log_message(&c, 1);
                fmt = cursor;
                continue;
            }

            case 's' : {
                const char *str = va_arg(va, char*);
                tf_hal_log_message(str, strlen(str));
                fmt = cursor;
                continue;
            }

            case '%' : {
                tf_hal_log_message("%", 1);
                fmt = cursor;
                continue;
            }
        }

        // Parse integer placeholders
        bool sign = 0;
        uint8_t base = 0;

        switch(character) {
            case 'u': {
                if(width == 0)
                    width = sizeof(unsigned int);
                base = 10;
                sign = false;
                break;
            }

            case 'b': {
                if(width == 0)
                    width = sizeof(unsigned int);
                base = 2;
                sign = false;
                break;
            }

            case 'd': {
                if(width == 0)
                    width = sizeof(int);
                base = 10;
                sign = true;
                break;
            }

            case 'X':
            case 'x': {
                if(width == 0)
                    width = sizeof(unsigned int);
                base = 16;
                sign = false;
                break;
            }
            default:
                tf_hal_log_message("%", 1);
                tf_hal_log_message(&character, 1);
                fmt = cursor;
                continue;
        }

        // Handle integer placeholders with optional prefix.
        uint64_t value = 0;

        // double casts fix implicit conversion signedness change warnings
        switch(width) {
            case 1:
                if (sign) {
                    value = (uint64_t)((int8_t) va_arg(va, int));
                } else {
                    value = (uint8_t) va_arg(va, unsigned int);
                }
                break;
            case 2:
                if (sign) {
                    value = (uint64_t)((int16_t) va_arg(va, int));
                } else {
                    value = (uint16_t) va_arg(va, unsigned int);
                }
                break;
            case 4:
                if (sign) {
                    value = (uint64_t)(va_arg(va, int32_t));
                } else {
                    value = va_arg(va, uint32_t);
                }
                break;
            case 8:
                if (sign) {
                    value = (uint64_t)(va_arg(va, int64_t));
                } else {
                    value = va_arg(va, uint64_t);
                }
                break;
        }

        if (sign) {
            log_signed((int64_t) value, base);
        } else {
            log_unsigned((uint64_t) value, base);
        }

        fmt = cursor;
    }

    write_chunk(fmt, cursor);

    va_end(va);
}

void tf_hal_set_timeout(TF_HalContext *hal, uint32_t timeout_us) {
    tf_hal_get_common(hal)->timeout = timeout_us;
}

uint32_t tf_hal_get_timeout(TF_HalContext *hal) {
    return tf_hal_get_common(hal)->timeout;
}

int tf_hal_get_port_id(TF_HalContext *hal, uint32_t uid, uint8_t *port_id, int *inventory_index) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);

    for(int i = 0; i < (int)hal_common->used; ++i) {
        if(hal_common->uids[i] == uid) {
            *port_id = hal_common->port_ids[i];
            *inventory_index = i;
            return TF_E_OK;
        }
    }

    return TF_E_DEVICE_NOT_FOUND;
}

int tf_hal_get_device_info(TF_HalContext *hal, size_t index, char ret_uid[7], char *ret_port_name, uint16_t *ret_device_id) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);

    // Increment index to skip over the 0th inventory entry
    // (the unknown bricklet used for device discovery).
    ++index;

    if (index >= hal_common->used) {
        return TF_E_DEVICE_NOT_FOUND;
    }
    if (ret_uid != NULL)
        tf_base58_encode(hal_common->uids[index], ret_uid);

    if (ret_port_name != NULL)
        *ret_port_name = tf_hal_get_port_name(hal, hal_common->port_ids[index]);

    if (ret_port_name != NULL)
        *ret_device_id = hal_common->dids[index];
    return TF_E_OK;
}

static TF_TfpContext *next_callback_tick_tfp(TF_HalContext *hal) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);
    TF_TfpContext *tfp = NULL;

    ++hal_common->callback_tick_index;
    if(hal_common->callback_tick_index >= hal_common->used)
        // Skip index 0; used for the unknown bricklet
        hal_common->callback_tick_index = 1;

    for(size_t i = hal_common->callback_tick_index; i < hal_common->callback_tick_index + hal_common->used; ++i) {
        size_t index = i;
        if (index >= hal_common->used) {
            // Skip index 0; used for the unknown bricklet
            index -= hal_common->used - 1;
        }
        tfp = hal_common->tfps[index];
        if(tfp != NULL && tfp->needs_callback_tick) {
            hal_common->callback_tick_index = index;
            return tfp;
        }
    }

    return NULL;
}

int tf_hal_callback_tick(TF_HalContext *hal, uint32_t timeout_us) {
    uint32_t deadline_us = tf_hal_current_time_us(hal) + timeout_us;
    TF_TfpContext *tfp = NULL;

    do {
        tfp = next_callback_tick_tfp(hal);
        if(tfp == NULL)
            return TF_E_OK;

        int result = tf_tfp_callback_tick(tfp, 0);
        if(result != TF_E_OK)
            return result;
    } while(!tf_hal_deadline_elapsed(hal, deadline_us));

    return TF_E_OK;
}

bool tf_hal_deadline_elapsed(TF_HalContext *hal, uint32_t deadline_us) {
    uint32_t now = tf_hal_current_time_us(hal);

    if(now < deadline_us) {
        uint32_t diff = deadline_us - now;
        if (diff < UINT32_MAX / 2)
            return false;
        return true;
    }
    else {
        uint32_t diff = now - deadline_us;
        if(diff > UINT32_MAX / 2)
            return false;
        return true;
    }
}

int tf_hal_get_error_counters(TF_HalContext *hal,
                              char port_name,
                              uint32_t *ret_spitfp_error_count_checksum,
                              uint32_t *ret_spitfp_error_count_frame,
                              uint32_t *ret_tfp_error_count_frame,
                              uint32_t *ret_tfp_error_count_unexpected) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);
    TF_TfpContext *tfp = NULL;

    uint32_t spitfp_error_count_checksum = 0;
    uint32_t spitfp_error_count_frame = 0;
    uint32_t tfp_error_count_frame = 0;
    uint32_t tfp_error_count_unexpected = 0;

    bool port_found = false;

    for(int i = 0; i < (int)hal_common->used; ++i) {
        if(tf_hal_get_port_name(hal, hal_common->port_ids[i]) != port_name)
            continue;

        port_found = true;

        tfp = hal_common->tfps[i];
        if(tfp == NULL)
            continue;

        spitfp_error_count_checksum += tfp->spitfp.error_count_checksum;
        spitfp_error_count_frame += tfp->spitfp.error_count_frame;

        tfp_error_count_frame += tfp->error_count_frame;
        tfp_error_count_unexpected += tfp->error_count_unexpected;
    }

    if(ret_spitfp_error_count_checksum != NULL)
        *ret_spitfp_error_count_checksum = spitfp_error_count_checksum;
    if(ret_spitfp_error_count_frame != NULL)
        *ret_spitfp_error_count_frame = spitfp_error_count_frame;
    if(ret_tfp_error_count_frame != NULL)
        *ret_tfp_error_count_frame = tfp_error_count_frame;
    if(ret_tfp_error_count_unexpected != NULL)
        *ret_tfp_error_count_unexpected = tfp_error_count_unexpected;

    return port_found ? TF_E_OK : TF_E_PORT_NOT_FOUND;
}

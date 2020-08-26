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

const char *alphabet = "0123456789abcdef";

static void log_unsigned(unsigned int value, int base) {
    if(base < 2 || base > 16)
        return;

    char buffer[32] = {0};

    int len = 0;
    do {
        int digit = value % base;
        buffer[32 - len - 1] = alphabet[digit];
        ++len;
        value /= base;
    } while(value > 0);

    tf_hal_log_message(buffer + (32 - len), len);

    return;
}

static void log_signed(int value, int base) {
    if(value < 0) {
        tf_hal_log_message("-", 1);
        value = -value;
    }

    log_unsigned(value, base);

    return;
}

TF_ATTRIBUTE_FMT_PRINTF(1, 2)
void tf_hal_printf(const char *fmt, ...){
    // Very minimalistic printf: no zero-padding, grouping, l-modifier or similar and no float.
    // Newlines (\n) are translated to the platform specific newline character(s).
	va_list va;
	va_start(va, fmt);

    char character;
    const char *cursor = fmt;

	while((character = *(cursor++))) {
        if(character == '\n') {
            if(cursor > fmt) {
                // cursor is on the \n character
                uint32_t chunk_len = cursor - fmt - 1;
                if(chunk_len != 0)
                    tf_hal_log_message(fmt, chunk_len);

                fmt = cursor;
            }
            tf_hal_log_newline();
            continue;
        }

		if(character != '%') {
            continue;
        }

        if(cursor > fmt) {
            // cursor is on the % character
            uint32_t chunk_len = cursor - fmt - 1;
            if(chunk_len != 0)
                tf_hal_log_message(fmt, chunk_len);
        }

        character = *(cursor++);

        switch(character) {
            case '\n': {
                tf_hal_log_newline();
                break;
            }
            case '\0': {
                tf_hal_log_message("%", 1);
                va_end(va);
                return;
            }

            case 'u': {
                uint32_t value = va_arg(va, uint32_t);
                log_unsigned(value, 10);
                break;
            }

            case 'b': {
                uint32_t value = va_arg(va, uint32_t);
                log_unsigned(value, 2);
                break;
            }

            case 'd': {
                int32_t value = va_arg(va, int32_t);
                log_signed(value, 10);
                break;
            }

            case 'X':
            case 'x': {
                uint32_t value = va_arg(va, uint32_t);
                log_unsigned(value, 16);
                break;
            }

            case 'c' : {
                char c = (char)(va_arg(va, int));
                tf_hal_log_message(&c, 1);
                break;
            }

            case 's' : {
                const char *str = va_arg(va, char*);
                tf_hal_log_message(str, strlen(str));
                break;
            }

            case '%' : {
                tf_hal_log_message("%", 1);
                break;
            }

            default:
                tf_hal_log_message("%", 1);
                tf_hal_log_message(&character, 1);
                break;
        }

        fmt = cursor;
    }

    if(cursor > fmt) {
        // cursor is on the null terminator
        uint32_t chunk_len = cursor - fmt - 1;
        if(chunk_len != 0)
            tf_hal_log_message(fmt, chunk_len);
    }

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

bool tf_hal_get_device_info(TF_HalContext *hal, size_t index, char ret_uid[7], char *ret_port_name, uint16_t *ret_device_id) {
    TF_HalCommon *hal_common = tf_hal_get_common(hal);

    // Increment index to skip over the 0th inventory entry
    // (the unknown bricklet used for device discovery).
    ++index;

    if (index >= hal_common->used) {
        return false;
    }

    tf_base58_encode(hal_common->uids[index], ret_uid);
    *ret_port_name = tf_hal_get_port_name(hal, hal_common->port_ids[index]);
    *ret_device_id = hal_common->dids[index];
    return true;
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

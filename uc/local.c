/*
 * Copyright (C) 2021 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "local.h"

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>

#include "endian_convert.h"
#include "packet_buffer.h"
#include "hal_common.h"
#include "errors.h"
#include "base58.h"

static uint8_t tf_local_build_header(TF_Local *local, uint8_t *header_buf, uint8_t length, uint8_t function_id, bool response_expected) {
    TF_TFPHeader header;

    memset(&header, 0, sizeof(TF_TFPHeader));

    uint8_t sequence_number = local->next_sequence_number & 0x0F;

    if (sequence_number == 0) {
        sequence_number = 1;
    }

    local->next_sequence_number = sequence_number + 1;

    header.uid_num = local->uid_num;
    header.length = length;
    header.fid = function_id;
    header.seq_num = sequence_number;
    header.response_expected = response_expected;

    tf_tfp_header_write(&header, header_buf);

    return sequence_number;
}

int tf_local_create(TF_Local *local, const char *uid_str, char position, uint8_t hw_version[3], uint8_t fw_version[3], uint16_t device_id, void *hal) {
    memset(local, 0, sizeof(TF_Local));

    int rc = tf_base58_decode(uid_str, &local->uid_num);

    if (rc != TF_E_OK) {
        return rc;
    }

    memcpy(local->uid_str, uid_str, sizeof(local->uid_str));
    memcpy(local->hw_version, hw_version, sizeof(local->hw_version));
    memcpy(local->fw_version, fw_version, sizeof(local->fw_version));

    local->hal = hal;
    local->device_id = device_id;
    local->position = position;
    local->next_sequence_number = 1;

    return TF_E_OK;
}

void tf_local_prepare_send(TF_Local *local, uint8_t fid, uint8_t payload_size, bool response_expected) {
    // TODO: theoretically, all bytes should be rewritten when sending a new packet, so this is not necessary.
    memset(local->send_buf, 0, TF_LOCAL_MAX_MESSAGE_LENGTH);

    tf_local_build_header(local, local->send_buf, payload_size + TF_LOCAL_MIN_MESSAGE_LENGTH, fid, response_expected);
}

uint8_t *tf_local_get_send_buffer(TF_Local *local) {
    return local->send_buf;
}

uint8_t *tf_local_get_recv_buffer(TF_Local *local) {
    return local->recv_buf;
}

void tf_local_inject_packet(TF_Local *local, TF_TFPHeader *header, uint8_t *packet) {
    memset(local->send_buf, 0, TF_LOCAL_MAX_MESSAGE_LENGTH);
    memcpy(local->send_buf, packet, header->length);
}

int tf_local_transceive_packet(TF_Local *local) {
    TF_TFPHeader header;

    tf_tfp_header_peek_plain(&header, local->send_buf);

    local->tc_handler(local->hal, &header, local->send_buf, local->recv_buf);

    return TF_E_OK;
}

int tf_local_get_error(uint8_t error_code) {
    switch (error_code) {
        case 1:
            return TF_E_INVALID_PARAMETER;

        case 2:
            return TF_E_NOT_SUPPORTED;

        case 3:
            return TF_E_UNKNOWN_ERROR_CODE;

        case 0:
        default:
            return TF_E_OK;
    }
}

bool tf_local_callback_tick(TF_Local *local) {
    TF_TFPHeader header;

    if (local->trigger_enumerate_callback) {
        local->trigger_enumerate_callback = false;

        header.uid_num = local->uid_num;
        header.length = 34;
        header.fid = 253;
        header.seq_num = 0;
        header.response_expected = true;
        header.options = 0;
        header.error_code = 0;
        header.flags = 0;

        tf_tfp_header_write(&header, local->recv_buf);
        memcpy(&local->recv_buf[8], local->uid_str, sizeof(local->uid_str));
        local->recv_buf[8 + 7] = '\0';
        local->recv_buf[8 + 8] = '0';
        local->recv_buf[8 + 9] = '\0';
        local->recv_buf[8 + 16] = local->position;
        local->recv_buf[8 + 17] = local->hw_version[0];
        local->recv_buf[8 + 18] = local->hw_version[1];
        local->recv_buf[8 + 19] = local->hw_version[2];
        local->recv_buf[8 + 20] = local->fw_version[0];
        local->recv_buf[8 + 21] = local->fw_version[1];
        local->recv_buf[8 + 22] = local->fw_version[2];
        memcpy(local->recv_buf + 8 + 23, &local->device_id, 2); // FIXME: tf_leconvert_uint16_to
        local->recv_buf[8 + 25] = 0; // FIXME: IPCON_ENUMERATION_TYPE_AVAILABLE = 0

        return true;
    }

    return local->cb_producer(local->hal, local->recv_buf);
}

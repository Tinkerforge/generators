/*
 * Copyright (C) 2021 Matthias Bolte <matthias@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_LOCAL_H
#define TF_LOCAL_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#include "macros.h"
#include "packet_buffer.h"
#include "tfp_header.h"

#ifdef __cplusplus
extern "C" {
#endif

#define TF_LOCAL_MIN_MESSAGE_LENGTH 8
#define TF_LOCAL_MAX_MESSAGE_LENGTH 80

typedef struct _TF_Local TF_Local;
typedef void (*TF_Local_TransceiveHandler)(TF_Local *local, TF_TFPHeader *header, uint8_t *send_buf, uint8_t *recv_buf);
typedef bool (*TF_Local_CallbackProducer)(TF_Local *local, uint8_t *recv_buf);

typedef struct _TF_Local {
    void *device;
    void *hal;

    TF_Local_TransceiveHandler tc_handler;
    TF_Local_CallbackProducer cb_producer;

    uint32_t uid_num;
    uint8_t next_sequence_number;
    bool trigger_enumerate_callback;

    uint16_t device_id;
    char position;
    char uid_str[7];

    uint8_t hw_version[3];
    uint8_t fw_version[3];

    uint8_t send_buf[TF_LOCAL_MAX_MESSAGE_LENGTH];
    uint8_t recv_buf[TF_LOCAL_MAX_MESSAGE_LENGTH];
} TF_Local;

int tf_local_create(TF_Local *local, const char *uid_str, char position, uint8_t hw_version[3], uint8_t fw_version[3], uint16_t device_id, void *hal) TF_ATTRIBUTE_NONNULL_ALL;
void tf_local_prepare_send(TF_Local *local, uint8_t fid, uint8_t payload_size, bool response_expected) TF_ATTRIBUTE_NONNULL_ALL;
uint8_t *tf_local_get_send_buffer(TF_Local *local) TF_ATTRIBUTE_NONNULL_ALL;
uint8_t *tf_local_get_recv_buffer(TF_Local *local) TF_ATTRIBUTE_NONNULL_ALL;
int tf_local_transceive_packet(TF_Local *local) TF_ATTRIBUTE_NONNULL_ALL;
int tf_local_get_error(uint8_t error_code) TF_ATTRIBUTE_WARN_UNUSED_RESULT;
bool tf_local_callback_tick(TF_Local *local) TF_ATTRIBUTE_NONNULL_ALL;
void tf_local_inject_packet(TF_Local *local, TF_TFPHeader *header, uint8_t *packet) TF_ATTRIBUTE_NONNULL_ALL;

#ifdef __cplusplus
}
#endif

#endif

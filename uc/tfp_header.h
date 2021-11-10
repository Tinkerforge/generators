/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_TFP_HEADER_H
#define TF_TFP_HEADER_H

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>

#include "macros.h"
#include "packetbuffer.h"

#ifdef __cplusplus
extern "C" {
#endif

#define TF_TFP_HEADER_UID_OFFSET 0
#define TF_TFP_HEADER_LENGTH_OFFSET 4
#define TF_TFP_HEADER_FID_OFFSET 5
#define TF_TFP_HEADER_SEQ_NUM_OFFSET 6
#define TF_TFP_HEADER_FLAGS_OFFSET 7
#define TF_TFP_HEADER_LENGTH 8

typedef struct TF_TfpHeader {
    uint32_t uid;
    uint8_t length;
    uint8_t fid;
    uint8_t seq_num;
    bool response_expected;
    uint8_t options;
    uint8_t error_code;
    uint8_t flags;
} TF_TfpHeader;

void tf_read_packet_header(TF_Packetbuffer *buf, TF_TfpHeader *header) TF_ATTRIBUTE_NONNULL_ALL;
void tf_peek_packet_header(TF_Packetbuffer *buf, TF_TfpHeader *header) TF_ATTRIBUTE_NONNULL_ALL;
void tf_peek_packet_header_plain_buf(uint8_t *buf, TF_TfpHeader *header) TF_ATTRIBUTE_NONNULL_ALL;
void tf_write_packet_header(TF_TfpHeader *header, uint8_t buf[8]) TF_ATTRIBUTE_NONNULL_ALL;
void tf_print_packet_header(TF_TfpHeader *header) TF_ATTRIBUTE_NONNULL_ALL;

#ifdef __cplusplus
}
#endif

#endif

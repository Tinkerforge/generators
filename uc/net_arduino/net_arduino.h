/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#ifndef TF_NET_ARDUINO_H
#define TF_NET_ARDUINO_H

#include <stdint.h>
#include <stdbool.h>
#include <stddef.h>

#include <WiFi.h>

#include "../bindings/net_common.h"
#include "../bindings/tfp_header.h"

typedef struct {
    uint32_t id;
    WiFiClient client;
    uint32_t last_recv_ms;
    uint32_t last_send_us;
    uint8_t read_buf[80];
    uint8_t read_buf_used;
    uint8_t send_buf[1400];
    uint32_t send_buf_used;
    uint8_t sends_without_progress;

    bool available_packet_valid;
    TF_TfpHeader available_packet;
} TF_NetClient;

typedef struct TF_Request {
    uint32_t uid;
    uint32_t client_id;
    uint8_t fid;
    uint8_t seq_num;
} TF_Request;

typedef struct TF_NetContext {
    TF_NetClient clients[TF_MAX_CLIENT_COUNT];
    uint8_t clients_used;
    WiFiServer server;

    TF_Request open_requests[TF_MAX_OPEN_REQUEST_COUNT];
    uint8_t open_request_count;
    uint16_t send_buf_timeout_us;
    uint32_t recv_timeout_ms;
} TF_NetContext;

int tf_net_create(TF_NetContext *net, const char* listen_addr, uint16_t port, const char* auth_secret);

#endif

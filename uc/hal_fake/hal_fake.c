/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "hal_fake.h"

int tf_hal_fake_init(struct TF_HalContext *hal, TF_Port *ports, uint8_t port_count) {
    int rc = tf_hal_common_init(hal);
    if (rc != TF_E_OK) {
        return rc;
    }

    hal->ports = ports;
    hal->port_count = port_count;

    return tf_hal_finish_init(hal, port_count, 200000);
}

int tf_hal_destroy(TF_HalContext *hal) {
    (void) hal;

    return TF_E_OK;
}

int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable) {
    (void) hal;
    (void) port_id;
    (void) enable;

    return TF_E_OK;
}

int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, const uint32_t length) {
    (void) hal;
    (void) port_id;
    (void) write_buffer;
    (void) read_buffer;
    (void) length;

    return TF_E_OK;
}

uint32_t tf_hal_current_time_us(TF_HalContext *hal) {
    (void) hal;

    return 0;
}

void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us) {
    (void) hal;
    (void) us;
}

TF_HalCommon *tf_hal_get_common(TF_HalContext *hal) {
    return &hal->hal_common;
}

void tf_hal_log_message(const char *msg, uint32_t len) {
    (void) msg;
    (void) len;
}

void tf_hal_log_newline() {

}

const char *tf_hal_strerror(int rc) {
    (void) rc;
    return "unknown error";
}

char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id) {
    if(port_id > hal->port_count)
        return '?';
    return hal->ports[port_id].port_name;
}


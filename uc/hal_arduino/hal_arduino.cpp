/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "hal_arduino.h"
#include "SPI.h"
#include <Arduino.h>

#include "../bindings/errors.h"

int tf_hal_arduino_init(TF_HalContext *hal, TF_Port *ports, size_t port_count) {
    int rc = tf_hal_common_init(hal);
    if (rc != TF_E_OK) {
        return rc;
    }

    hal->ports = ports;
    hal->port_count = port_count;

    SPI.begin();
    hal->spi_settings = SPISettings(1400000, MSBFIRST, SPI_MODE3);

    for(size_t i = 0; i < port_count; ++i) {
        pinMode(hal->ports[i].chip_select_pin, OUTPUT);
        digitalWrite(hal->ports[i].chip_select_pin, HIGH);
    }

    return tf_hal_finish_init(hal, port_count, 50000);
}

int tf_hal_shutdown(TF_HalContext *hal) {
    SPI.end();
    return TF_E_OK;
}

int tf_hal_chip_select(TF_HalContext *hal, uint8_t device_id, bool enable) {
    if (enable) {
        SPI.beginTransaction(hal->spi_settings);
        digitalWrite(hal->ports[device_id].chip_select_pin, LOW);
    } else {
        digitalWrite(hal->ports[device_id].chip_select_pin, HIGH);
        SPI.endTransaction();
    }
    return TF_E_OK;
}

int tf_hal_transceive(TF_HalContext *hal, uint8_t device_id, const uint8_t *write_buffer, uint8_t *read_buffer, uint32_t length){
    memcpy(read_buffer, write_buffer, length);
    SPI.transfer(read_buffer, length);
    return TF_E_OK;
}

uint32_t tf_hal_current_time_us(TF_HalContext *hal){
    return micros();
}

void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us) {
    while(us > 16000) {
        delay(16);
        us -= 16000;
    }
    delayMicroseconds(us);
}

TF_HalCommon *tf_hal_get_common(TF_HalContext *hal) {
    return &hal->hal_common;
}

void tf_hal_log_message(const char *msg) {
    Serial.println(msg);
}

const char *tf_hal_strerror(int rc) {
    return "unknown error";
}

char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id) {
    if(port_id > hal->port_count)
        return '?';
    return hal->ports[port_id].port_name;
}

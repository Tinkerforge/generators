/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "hal_arduino.h"

#include <Arduino.h>
#include <SPI.h>

#include "../bindings/config.h"
#include "../bindings/errors.h"

int tf_hal_create(TF_HAL *hal, TF_Port *ports, uint8_t port_count) {
    int rc = tf_hal_common_create(hal);

    if (rc != TF_E_OK) {
        return rc;
    }

    hal->ports = ports;
    hal->port_count = port_count;

    SPI.begin();
    hal->spi_settings = SPISettings(1400000, MSBFIRST, SPI_MODE3);

    for (int i = 0; i < port_count; ++i) {
        pinMode(hal->ports[i].chip_select_pin, OUTPUT);
        digitalWrite(hal->ports[i].chip_select_pin, HIGH);
    }

    return tf_hal_common_prepare(hal, port_count, 50000);
}

int tf_hal_destroy(TF_HAL *hal) {
    SPI.end();

    return TF_E_OK;
}

int tf_hal_chip_select(TF_HAL *hal, uint8_t port_id, bool enable) {
    if (enable) {
        SPI.beginTransaction(hal->spi_settings);
        digitalWrite(hal->ports[port_id].chip_select_pin, LOW);
    } else {
        digitalWrite(hal->ports[port_id].chip_select_pin, HIGH);
        SPI.endTransaction();
    }

    return TF_E_OK;
}

int tf_hal_transceive(TF_HAL *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, uint32_t length) {
    memcpy(read_buffer, write_buffer, length);
    SPI.transfer(read_buffer, length);

    return TF_E_OK;
}

uint32_t tf_hal_current_time_us(TF_HAL *hal) {
    return micros();
}

void tf_hal_sleep_us(TF_HAL *hal, uint32_t us) {
    while (us > 16000) {
        delay(16);
        us -= 16000;
    }

    delayMicroseconds(us);
}

TF_HALCommon *tf_hal_get_common(TF_HAL *hal) {
    return &hal->hal_common;
}

void tf_hal_log_message(const char *msg, size_t len) {
    Serial.write((const uint8_t *)msg, len);
}

void tf_hal_log_newline(void) {
    Serial.println("");
}

#if TF_IMPLEMENT_STRERROR != 0
const char *tf_hal_strerror(int e_code) {
    switch (e_code) {
        #include "../bindings/error_cases.h"

        default:
            return "unknown error";
    }
}
#endif

char tf_hal_get_port_name(TF_HAL *hal, uint8_t port_id) {
    return hal->ports[port_id].port_name;
}

TF_PortCommon *tf_hal_get_port_common(TF_HAL *hal, uint8_t port_id) {
    return &hal->ports[port_id].port_common;
}

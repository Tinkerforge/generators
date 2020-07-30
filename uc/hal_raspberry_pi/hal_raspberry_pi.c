/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "hal_raspberry_pi.h"

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <stdbool.h>
#include <unistd.h>
#include <time.h>

#include "bcm2835.h"

#define BRICKLET_STACK_SPI_CONFIG_MODE           SPI_MODE_3
#define BRICKLET_STACK_SPI_CONFIG_LSB_FIRST      0
#define BRICKLET_STACK_SPI_CONFIG_BITS_PER_WORD  8

// On RPi 3 make sure to set "core_freq=250" in /boot/config.txt.
// The SPI clock is scaled with the variable core_freq otherwise
// and the SPI clock is not stable...
#define BRICKLET_STACK_SPI_CONFIG_MAX_SPEED_HZ   1400000

int tf_hal_raspberry_pi_init(struct TF_HalContext *hal, TF_Port *ports, uint8_t port_count) {
    int rc = tf_hal_common_init(hal);
    if (rc != TF_E_OK) {
        return rc;
    }

    if(!bcm2835_init()) {
        return TF_E_BCM2835_INIT_FAILED;
    }

    if(!bcm2835_spi_begin()) {
        return TF_E_BCM2835_SPI_BEGIN_FAILED;
    }

    bcm2835_spi_setBitOrder(BCM2835_SPI_BIT_ORDER_MSBFIRST);
    bcm2835_spi_setDataMode(BCM2835_SPI_MODE3);
    bcm2835_spi_set_speed_hz(BRICKLET_STACK_SPI_CONFIG_MAX_SPEED_HZ);
    bcm2835_spi_chipSelect(BCM2835_SPI_CS_NONE);

    for(int i = 0; i < port_count; ++i) {
        bcm2835_gpio_fsel(ports[i].chip_select_pin, BCM2835_GPIO_FSEL_OUTP);
        bcm2835_gpio_write(ports[i].chip_select_pin, HIGH);
    }

    hal->ports = ports;
    hal->port_count = port_count;

    return tf_hal_finish_init(hal, port_count, 200000);
}

int tf_hal_destroy(TF_HalContext *hal) {
    (void) hal;
    bcm2835_spi_end();
    bcm2835_close();
    return TF_E_OK;
}

int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable) {
    bcm2835_gpio_write(hal->ports[port_id].chip_select_pin, enable ? LOW : HIGH);
    return TF_E_OK;
}

int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, const uint32_t length) {
    (void) hal;
    (void) port_id;
    bcm2835_spi_transfernb((const char*)write_buffer, (char *)read_buffer, length);
    return TF_E_OK;
}

uint32_t tf_hal_current_time_us(TF_HalContext *hal) {
    (void) hal;
    struct timespec t;
    clock_gettime(CLOCK_MONOTONIC, &t);

    return (uint32_t) ((t.tv_sec * 1000000) + t.tv_nsec / 1000);
}

void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us) {
    (void) hal;
    usleep(us);
}

TF_HalCommon *tf_hal_get_common(TF_HalContext *hal) {
    return &hal->hal_common;
}

void tf_hal_log_message(const char *msg) {
    puts(msg);
}

const char *tf_hal_strerror(int rc) {
    switch(rc) {
        case TF_E_BCM2835_INIT_FAILED:
            return "bcm2835_init failed. Are you running as root?";
        case TF_E_BCM2835_SPI_BEGIN_FAILED:
            return "bcm2835_spi_begin failed. Are you running as root?";
        default:
            return "unknown error";
    }
}

char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id) {
    if(port_id > hal->port_count)
        return '?';
    return hal->ports[port_id].port_name;
}


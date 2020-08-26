/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "hal_linux.h"

#include <stdio.h>
#include <errno.h>
#include <string.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <stdbool.h>
#include <sys/eventfd.h>
#include <sys/ioctl.h>
#include <linux/spi/spidev.h>
#include <unistd.h>
#include <time.h>

#include "utils.h"
#include "gpio_sysfs.h"

#define BRICKLET_STACK_SPI_CONFIG_MODE           SPI_MODE_3
#define BRICKLET_STACK_SPI_CONFIG_LSB_FIRST      0
#define BRICKLET_STACK_SPI_CONFIG_BITS_PER_WORD  8

// On RPi 3 make sure to set "core_freq=250" in /boot/config.txt.
// The SPI clock is scaled with the variable core_freq otherwise
// and the SPI clock is not stable...
#define BRICKLET_STACK_SPI_CONFIG_MAX_SPEED_HZ   1400000

static int open_spi_port(TF_Port *port) {
    char buffer[256];

    char cs_pin_name[32];
    snprintf(cs_pin_name, sizeof(cs_pin_name), "gpio%d", port->chip_select_pin);

    if (gpio_sysfs_export(port->chip_select_pin) < 0) {
        return TF_E_EXPORT_GPIO_FAILED;
    }

    if (gpio_sysfs_set_direction_out_with_initial_value(cs_pin_name, GPIO_SYSFS_VALUE_HIGH) < 0) {
        return TF_E_SET_GPIO_DIRECTION_FAILED; // FIXME: unexport gpio cs pin
    }

    snprintf(buffer, sizeof(buffer), "/sys/class/gpio/%s/value", cs_pin_name);
    port->_cs_pin_fd = open(buffer, O_WRONLY);

    if (port->_cs_pin_fd < 0) {
        return TF_E_OPEN_GPIO_FAILED; // FIXME: unexport gpio cs pin
    }
    return TF_E_OK;
}

int tf_hal_linux_create(struct TF_HalContext *hal, const char *spidev_path, TF_Port *ports, uint8_t port_count) {
    int rc = tf_hal_common_create(hal);
    if (rc != TF_E_OK) {
        return rc;
    }

    for(int i = 0; i < port_count; ++i) {
        rc = open_spi_port(&ports[i]);
        if (rc != TF_E_OK) {
            return rc;
        }
    }
    hal->ports = ports;
    hal->port_count = port_count;

    // Use HW chip select if it is done by SPI hardware unit, otherwise set SPI_NO_CS flag.
    const int mode = BRICKLET_STACK_SPI_CONFIG_MODE | SPI_NO_CS;
    const int lsb_first = BRICKLET_STACK_SPI_CONFIG_LSB_FIRST;
    const int bits_per_word = BRICKLET_STACK_SPI_CONFIG_BITS_PER_WORD;
    const int max_speed_hz = BRICKLET_STACK_SPI_CONFIG_MAX_SPEED_HZ;

    hal->spidev_fd = open(spidev_path, O_RDWR);

    if (hal->spidev_fd < 0) {
        printf("Could not open %s: %s (%d)",
                spidev_path, get_errno_name(errno), errno);
        return TF_E_OPEN_SPI_DEV_FAILED; // FIXME: close gpio_fd and unexport gpio cs pin
    }

    if (ioctl(hal->spidev_fd, SPI_IOC_WR_MODE, &mode) < 0) {
        printf("Could not configure SPI mode: %s (%d)",
                get_errno_name(errno), errno);
        return TF_E_SPI_DEV_CONFIG_FAILED; // FIXME: close spidev_fd, close gpio_fd and unexport gpio cs pin
    }

    if (ioctl(hal->spidev_fd, SPI_IOC_WR_MAX_SPEED_HZ, &max_speed_hz) < 0) {
        printf("Could not configure SPI max speed: %s (%d)",
                get_errno_name(errno), errno);
        return TF_E_SPI_DEV_CONFIG_FAILED; // FIXME: close spidev_fd, close gpio_fd and unexport gpio cs pin
    }

    if (ioctl(hal->spidev_fd, SPI_IOC_WR_BITS_PER_WORD, &bits_per_word) < 0) {
        printf("Could not configure SPI bits per word: %s (%d)",
                get_errno_name(errno), errno);
        return TF_E_SPI_DEV_CONFIG_FAILED; // FIXME: close spidev_fd, close gpio_fd and unexport gpio cs pin
    }

    if (ioctl(hal->spidev_fd, SPI_IOC_WR_LSB_FIRST, &lsb_first) < 0) {
        printf("Could not configure SPI lsb first: %s (%d)",
                get_errno_name(errno), errno);
        return TF_E_SPI_DEV_CONFIG_FAILED; // FIXME: close spidev_fd, close gpio_fd and unexport gpio cs pin
    }

    return tf_hal_common_prepare(hal, port_count, 200000);
}

int tf_hal_destroy(TF_HalContext *hal) {
    robust_close(hal->spidev_fd);
    for(int i = 0; i < hal->port_count; ++i) {
	    robust_close(hal->ports[i].chip_select_pin);
    }
    return TF_E_OK;
}

int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable) {
	// Use direct write call instead of gpio_sysfs_set_output on buffered fd to save some CPU time
	ssize_t rc = write(hal->ports[port_id]._cs_pin_fd, enable ? "0" : "1", 1);
    return rc == 1 ? TF_E_OK : TF_E_CHIP_SELECT_FAILED;
}

int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, const uint32_t length) {
    (void) port_id;
    struct spi_ioc_transfer spi_transfer = {
		.tx_buf = (unsigned long)write_buffer,
		.rx_buf = (unsigned long)read_buffer,
		.len = length,
	};

	int rc = ioctl(hal->spidev_fd, SPI_IOC_MESSAGE(1), &spi_transfer);

    return rc >= 0 ? TF_E_OK : TF_E_TRANSCEIVE_FAILED;
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

void tf_hal_log_message(const char *msg, uint32_t len) {
    fwrite(msg, len, 1, stdout);
}

void tf_hal_log_newline() {
    puts("");
}

const char *tf_hal_strerror(int rc) {
    switch(rc) {
        case TF_E_EXPORT_GPIO_FAILED:
            return "failed to export GPIO";
        case TF_E_SET_GPIO_DIRECTION_FAILED:
            return "failed to set GPIO direction";
        case TF_E_OPEN_GPIO_FAILED:
            return "failed to open GPIO";

        case TF_E_OPEN_SPI_DEV_FAILED:
            return "failed to open SPI device";
        case TF_E_SPI_DEV_CONFIG_FAILED:
            return "failed to configure SPI device";
        case TF_E_CHIP_SELECT_FAILED:
            return "failed to write to chip select GPIO";
        case TF_E_TRANSCEIVE_FAILED:
            return "failed to transceive over SPI";
        default:
            return "unknown error";
    }
}

char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id) {
    if(port_id > hal->port_count)
        return '?';
    return hal->ports[port_id].port_name;
}


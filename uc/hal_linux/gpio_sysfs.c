/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include <sys/stat.h>
#include <sys/types.h>
#include <fcntl.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>

#include "gpio_sysfs.h"

#define log_error printf

#include "utils.h"

#define GPIO_SYSFS_DIR "/sys/class/gpio/"
#define GPIO_SYSFS_DIR_MAXLEN 256

#define GPIO_SYSFS_VALUE_NUM 2

static const char * const gpio_sysfs_value[GPIO_SYSFS_VALUE_NUM] = {"0", "1"};
static const char * const gpio_sysfs_direction_initial_value[GPIO_SYSFS_VALUE_NUM] = {"low", "high"};

int gpio_sysfs_export(int cs_pin) {
	int fd;
	char buffer[16];
	int length;
	int rc;

	fd = open(GPIO_SYSFS_DIR "export", O_WRONLY);

	if (fd < 0) {
		log_error("Could not open '%s' for writing: %s (%d)",
		          GPIO_SYSFS_DIR "export", get_errno_name(errno), errno);

		return -1;
	}

	length = snprintf(buffer, sizeof(buffer), "%d", cs_pin);
	rc = robust_write(fd, buffer, length);

	robust_close(fd);

	if (rc < 0) {
		if (errno == EBUSY) {
			return 0; // GPIO was already exported
		}

		log_error("Could not write to '%sexport' to export GPIO %d: %s (%d)",
		          GPIO_SYSFS_DIR, cs_pin, get_errno_name(errno), errno);

		return -1;
	}

	return 0;
}

int gpio_sysfs_unexport(int cs_pin) {
	int fd;
	char buffer[16];
	int length;
	int rc;

	fd = open(GPIO_SYSFS_DIR "unexport", O_WRONLY);

	if (fd < 0) {
		log_error("Could not open '%s' for writing: %s (%d)",
		          GPIO_SYSFS_DIR "unexport", get_errno_name(errno), errno);

		return -1;
	}

	length = snprintf(buffer, sizeof(buffer), "%d", cs_pin);
	rc = robust_write(fd, buffer, length);

	robust_close(fd);

	if (rc < 0) {
		log_error("Could not write to '%sunexport' to unexport GPIO %d: %s (%d)",
		          GPIO_SYSFS_DIR, cs_pin, get_errno_name(errno), errno);

		return -1;
	}

	return 0;
}

int gpio_sysfs_set_direction_out_with_initial_value(char cs_pin_name[32], GPIOSYSFSValue value) {
	int fd;
	char buffer[GPIO_SYSFS_DIR_MAXLEN];
	int rc;

	if(value >= GPIO_SYSFS_VALUE_NUM) {
		log_error("Unknown value: %d", value);
		return -1;
	}

	snprintf(buffer, sizeof(buffer), "%s%s/direction", GPIO_SYSFS_DIR, cs_pin_name);

	fd = open(buffer, O_WRONLY);

	if (fd < 0) {
		log_error("Could not open '%s': %s (%d)", buffer, get_errno_name(errno), errno);
		return -1;
	}

	rc = robust_write(fd, gpio_sysfs_direction_initial_value[value], (int)strlen(gpio_sysfs_direction_initial_value[value]));

	robust_close(fd);

	if (rc < 0) {
		log_error("Could not write to '%s': %s (%d)", buffer, get_errno_name(errno), errno);
		return -1;
	}

	return 0;
}

int gpio_sysfs_set_output(char cs_pin_name[32], GPIOSYSFSValue value) {
	int fd;
	char buffer[GPIO_SYSFS_DIR_MAXLEN];
	int rc;

	if(value >= GPIO_SYSFS_VALUE_NUM) {
		log_error("Unknown value: %d", value);
		return -1;
	}

	snprintf(buffer, sizeof(buffer), "%s%s/value", GPIO_SYSFS_DIR, cs_pin_name);

	fd = open(buffer, O_WRONLY);

	if (fd < 0) {
		log_error("Could not open '%s': %s (%d)", buffer, get_errno_name(errno), errno);
		return -1;
	}

	rc = robust_write(fd, gpio_sysfs_value[value], (int)strlen(gpio_sysfs_value[value]));

	robust_close(fd);

	if (rc < 0) {
		log_error("Could not write to '%s': %s (%d)", buffer, get_errno_name(errno), errno);
		return -1;
	}

	return 0;
}

/* tng-<<<DEVICE_NAME_DASH>>>
 * Copyright (C) <<<YEAR>>> <<<NAME>>> <<<<EMAIL>>>>
 *
 * driver.c: Driver for TBD
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the
 * Free Software Foundation, Inc., 59 Temple Place - Suite 330,
 * Boston, MA 02111-1307, USA.
 */

#include "driver.h"

#include "configs/config_driver.h"
#include "bricklib2/os/coop_task.h"
#include "bricklib2/logging/logging.h"

Driver driver;
CoopTask driver_task;

void driver_task_tick(void) {
	while(true) {
		coop_task_sleep_ms(1);
	}
}

void driver_init(void) {
	memset(&driver, 0, sizeof(Driver));

	coop_task_init(&driver_task, driver_task_tick);
}

void driver_tick(void) {
	coop_task_tick(&driver_task);
}

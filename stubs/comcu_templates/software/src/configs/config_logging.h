/* <<<DEVICE_NAME_DASH>>>-bricklet
 * Copyright (C) <<<YEAR>>> <<<NAME>>> <<<<EMAIL>>>>
 *
 * config_logging.h: Logging configuration for <<<DEVICE_NAME_READABLE>>>
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

#ifndef CONFIG_LOGGING_H
#define CONFIG_LOGGING_H

#define LOGGING_UARTBB
#define LOGGING_LEVEL LOGGING_DEBUG
//#define LOGGING_LEVEL LOGGING_NONE

#define LOGGING_USE_BASENAME
#define LOGGING_HAVE_SYSTEM_TIME
#define LOGGING_TIMESTAMP_FORMAT "%u "
#define LOGGING_SYSTEM_TIME_HEADER "bricklib2/hal/system_timer/system_timer.h"
#define LOGGING_SYSTEM_TIME_FUNCTION system_timer_get_ms

#endif

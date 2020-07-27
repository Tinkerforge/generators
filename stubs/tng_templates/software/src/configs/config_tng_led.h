/* <<<DEVICE_NAME_DASH>>>
 * Copyright (C) <<<YEAR>>> <<<NAME>>> <<<<EMAIL>>>>
 *
 * config_led.h: LED driver configuration for <<<DEVICE_NAME_READABLE>>>
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

#ifndef CONFIG_LED_H
#define CONFIG_LED_H

#include "configs/config.h"

#define TNG_LED_STATUS_R_PIN        GPIO_PIN_8
#define TNG_LED_STATUS_R_PORT       GPIOA
#define TNG_LED_STATUS_R_TIM_ALT    GPIO_AF2_TIM1
#define TNG_LED_STATUS_R_TIM_CH     TIM_CHANNEL_1
#define TNG_LED_STATUS_G_PIN        GPIO_PIN_9
#define TNG_LED_STATUS_G_PORT       GPIOA
#define TNG_LED_STATUS_G_TIM_ALT    GPIO_AF2_TIM1
#define TNG_LED_STATUS_G_TIM_CH     TIM_CHANNEL_2
#define TNG_LED_STATUS_B_PIN        GPIO_PIN_10
#define TNG_LED_STATUS_B_PORT       GPIOA
#define TNG_LED_STATUS_B_TIM_ALT    GPIO_AF2_TIM1
#define TNG_LED_STATUS_B_TIM_CH     TIM_CHANNEL_3

#endif

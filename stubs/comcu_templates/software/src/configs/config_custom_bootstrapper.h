/* <<<DEVICE_NAME_DASH>>>-bricklet
 * Copyright (C) <<<YEAR>>> <<<NAME>>> <<<<EMAIL>>>>
 *
 * config_custom_bootstrapper.h: XMC bootstrapper configurations for
 *                               <<<DEVICE_NAME_READABLE>>>
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

#ifndef CONFIG_CUSTOM_BOOTSTRAPPER_H
#define CONFIG_CUSTOM_BOOTSTRAPPER_H

// TODO: CHECK ALL DEFINES!!!

#define BOOTSTRAPPER_STATUS_LED_PIN P2_1
#define BOOTSTRAPPER_USIC_CHANNEL   USIC0_CH0
#define BOOTSTRAPPER_PAGE_SIZE      256
#define BOOTSTRAPPER_FLASH_START    0x10001000

#define BOOTSTRAPPER_USIC           XMC_UART0_CH0
#define BOOTSTRAPPER_RX_PIN         P0_14
#define BOOTSTRAPPER_RX_INPUT       XMC_USIC_CH_INPUT_DX0
#define BOOTSTRAPPER_RX_SOURCE      0b000 // DX0A

#define BOOTSTRAPPER_TX_PIN         P0_15
#define BOOTSTRAPPER_TX_PIN_AF      (XMC_GPIO_MODE_OUTPUT_PUSH_PULL_ALT6 | P0_15_AF_U0C0_DOUT0)

#define BOOTSTRAPPER_BMI_WITH_CAN   0

#endif

/*
 * Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

// HAL for stm32f0 projects that are based on cubef0 SDK

#ifndef TF_HAL_STM32F0_H
#define TF_HAL_STM32F0_H

#include <stdbool.h>
#include <stdint.h>

#include "stm32f0xx_hal.h"
#include "bindings/hal_common.h"

#define TF_HAL_STM32F0_MAX_PORT_COUNT 8

typedef struct {
	GPIO_InitTypeDef pin;
	GPIO_TypeDef *port;
} TF_STMGPIO;

typedef struct TF_Port {
	//external
	TF_STMGPIO clk;
	TF_STMGPIO mosi;
	TF_STMGPIO miso;
	TF_STMGPIO *cs;
	uint8_t cs_count;

	SPI_TypeDef *spi_instance;

	IRQn_Type irq_tx;
	IRQn_Type irq_rx;

	DMA_Channel_TypeDef *dma_channel_rx;
	DMA_Channel_TypeDef *dma_channel_tx;

	//internal
	SPI_HandleTypeDef spi;
	DMA_HandleTypeDef hdma_tx;
	DMA_HandleTypeDef hdma_rx;
} TF_Port;

struct TF_HalContext {
	TF_Port *ports;
	uint8_t spi_port_count;

	TF_HalCommon hal_common;
};

#define TF_E_CHIP_SELECT_FAILED -100
#define TF_E_TRANSCEIVE_FAILED -101

int tf_hal_create(struct TF_HalContext *hal, TF_Port *ports, uint8_t spi_port_count) TF_ATTRIBUTE_NONNULL_ALL;
int tf_hal_destroy(TF_HalContext *hal) TF_ATTRIBUTE_NONNULL_ALL;

#endif

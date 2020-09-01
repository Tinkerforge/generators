/*
 * Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

// HAL for stm32f0 projects that are based on cubef0 SDK

#include "hal_stm32f0.h"

#include "bricklib2/hal/system_timer/system_timer.h"
#include "bricklib2/hal/uartbb/uartbb.h"
#include "bricklib2/os/coop_task.h"

#include "bindings/errors.h"
#include "bindings/config.h"

#include "configs/config.h"

#define TF_HAL_USE_COOP_TASK    // Comment out to not use coop task
#define TF_HAL_SPI_TIMEOUT 1000 // in ms

// Filled in tf_hal_create, to be used by IRQs
static SPI_HandleTypeDef *tf_hal_irq2_3_spi = NULL;
static SPI_HandleTypeDef *tf_hal_irq4_5_spi = NULL;

void HAL_SPI_TxRxCpltCallback(SPI_HandleTypeDef *spi) {
	// Nothing
}

void HAL_SPI_ErrorCallback(SPI_HandleTypeDef *spi) {
	// TODO: Maybe log error?
}

void DMA1_Channel2_3_IRQHandler(void) {
	if(tf_hal_irq2_3_spi != NULL) {
		HAL_DMA_IRQHandler(tf_hal_irq2_3_spi->hdmarx);
		HAL_DMA_IRQHandler(tf_hal_irq2_3_spi->hdmatx);
	}
}

void DMA1_Channel4_5_IRQHandler(void) {
	if(tf_hal_irq4_5_spi != NULL) {
		HAL_DMA_IRQHandler(tf_hal_irq4_5_spi->hdmarx);
		HAL_DMA_IRQHandler(tf_hal_irq4_5_spi->hdmatx);
	}
}

int tf_hal_create(struct TF_HalContext *hal, TF_Port *ports, uint8_t spi_port_count) {
	int rc = tf_hal_common_create(hal);
	if (rc != TF_E_OK) {
		return rc;
	}

	hal->ports = ports;
	hal->spi_port_count = spi_port_count;

	__HAL_RCC_GPIOA_CLK_ENABLE();
	__HAL_RCC_GPIOB_CLK_ENABLE();

	__HAL_RCC_DMA1_CLK_ENABLE();

	uint8_t count = 0;
	for(uint8_t i = 0; i < spi_port_count; i++) {
		if(hal->ports[i].spi_instance == SPI1) {
			if(tf_hal_irq2_3_spi == NULL) {
				tf_hal_irq2_3_spi = &hal->ports[i].spi;
			}
			__HAL_RCC_SPI1_CLK_ENABLE();
		} else {
			if(tf_hal_irq4_5_spi == NULL) {
				tf_hal_irq4_5_spi = &hal->ports[i].spi;
			}
			__HAL_RCC_SPI2_CLK_ENABLE();
		}

		HAL_GPIO_Init(hal->ports[i].clk.port,  &hal->ports[i].clk.pin);
		HAL_GPIO_Init(hal->ports[i].miso.port, &hal->ports[i].miso.pin);
		HAL_GPIO_Init(hal->ports[i].mosi.port, &hal->ports[i].mosi.pin);

		for(uint8_t j = 0; j < hal->ports[j].cs_count; j++) {
			HAL_GPIO_Init(hal->ports[i].cs[j].port, &hal->ports[i].cs[j].pin);
			hal->_port[count]    = &hal->ports[i];
			hal->_cs_gpio[count] = &hal->ports[i].cs[j];
			count++;
		}

		hal->ports[i].hdma_tx.Instance                 = hal->ports[i].dma_channel_tx;
		hal->ports[i].hdma_tx.Init.Direction           = DMA_MEMORY_TO_PERIPH;
		hal->ports[i].hdma_tx.Init.PeriphInc           = DMA_PINC_DISABLE;
		hal->ports[i].hdma_tx.Init.MemInc              = DMA_MINC_ENABLE;
		hal->ports[i].hdma_tx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
		hal->ports[i].hdma_tx.Init.MemDataAlignment    = DMA_MDATAALIGN_BYTE;
		hal->ports[i].hdma_tx.Init.Mode                = DMA_NORMAL;
		hal->ports[i].hdma_tx.Init.Priority            = DMA_PRIORITY_LOW;
		HAL_DMA_Init(&hal->ports[i].hdma_tx);
		__HAL_LINKDMA(&hal->ports[i].spi, hdmatx, hal->ports[i].hdma_tx);

		hal->ports[i].hdma_rx.Instance                 = hal->ports[i].dma_channel_rx;
		hal->ports[i].hdma_rx.Init.Direction           = DMA_PERIPH_TO_MEMORY;
		hal->ports[i].hdma_rx.Init.PeriphInc           = DMA_PINC_DISABLE;
		hal->ports[i].hdma_rx.Init.MemInc              = DMA_MINC_ENABLE;
		hal->ports[i].hdma_rx.Init.PeriphDataAlignment = DMA_PDATAALIGN_BYTE;
		hal->ports[i].hdma_rx.Init.MemDataAlignment    = DMA_MDATAALIGN_BYTE;
		hal->ports[i].hdma_rx.Init.Mode                = DMA_NORMAL;
		hal->ports[i].hdma_rx.Init.Priority            = DMA_PRIORITY_HIGH;
		HAL_DMA_Init(&hal->ports[i].hdma_rx);
		__HAL_LINKDMA(&hal->ports[i].spi, hdmarx, hal->ports[i].hdma_rx);

		HAL_NVIC_SetPriority(hal->ports[i].irq_tx, 1, 1);
		HAL_NVIC_EnableIRQ(hal->ports[i].irq_tx);

		HAL_NVIC_SetPriority(hal->ports[i].irq_rx, 1, 0);
		HAL_NVIC_EnableIRQ(hal->ports[i].irq_rx);

		if(hal->ports[i].spi_instance == SPI1) {
			__HAL_RCC_SPI1_FORCE_RESET();
			__HAL_RCC_SPI1_RELEASE_RESET();
		} else {
			__HAL_RCC_SPI2_FORCE_RESET();
			__HAL_RCC_SPI2_RELEASE_RESET();
		}

		hal->ports[i].spi.Instance               = hal->ports[i].spi_instance;
		hal->ports[i].spi.Init.BaudRatePrescaler = SPI_BAUDRATEPRESCALER_64;
		hal->ports[i].spi.Init.Direction         = SPI_DIRECTION_2LINES;
		hal->ports[i].spi.Init.CLKPhase          = SPI_PHASE_1EDGE;
		hal->ports[i].spi.Init.CLKPolarity       = SPI_POLARITY_LOW;
		hal->ports[i].spi.Init.CRCCalculation    = SPI_CRCCALCULATION_DISABLE;
		hal->ports[i].spi.Init.CRCPolynomial     = 7;
		hal->ports[i].spi.Init.DataSize          = SPI_DATASIZE_8BIT;
		hal->ports[i].spi.Init.FirstBit          = SPI_FIRSTBIT_MSB;
		hal->ports[i].spi.Init.NSS               = SPI_NSS_SOFT;
		hal->ports[i].spi.Init.NSSPMode          = SPI_NSS_PULSE_DISABLE;
		hal->ports[i].spi.Init.TIMode            = SPI_TIMODE_DISABLE;
		hal->ports[i].spi.Init.Mode              = SPI_MODE_MASTER;
		HAL_SPI_Init(&hal->ports[i].spi);
	}

	hal->_port_count = count;

	return tf_hal_common_prepare(hal, hal->_port_count, 200000);
}

int tf_hal_destroy(TF_HalContext *hal) {
	return TF_E_OK;
}

int tf_hal_chip_select(TF_HalContext *hal, uint8_t port_id, bool enable) {
	if(port_id > TF_HAL_STM32F0_MAX_PORT_COUNT) {
		return TF_E_CHIP_SELECT_FAILED;
	}

	TF_STMGPIO *cs = hal->_cs_gpio[port_id];
	if(cs == NULL) {
		return TF_E_CHIP_SELECT_FAILED;
	}

	HAL_GPIO_WritePin(cs->port, cs->pin.Pin, enable ? GPIO_PIN_RESET : GPIO_PIN_SET);

	return TF_E_OK;
}

int tf_hal_transceive(TF_HalContext *hal, uint8_t port_id, const uint8_t *write_buffer, uint8_t *read_buffer, const uint32_t length) {
	if(port_id > TF_HAL_STM32F0_MAX_PORT_COUNT) {
		return TF_E_CHIP_SELECT_FAILED;
	}

	TF_Port *port = hal->_port[port_id];
	if(port == NULL) {
		return TF_E_TRANSCEIVE_FAILED;
	}

	if((length == 0) || (write_buffer == NULL) || (read_buffer == NULL)) {
		return TF_E_OK;
	}

	HAL_StatusTypeDef status = HAL_SPI_TransmitReceive_DMA(&port->spi, (uint8_t *)write_buffer, read_buffer, length);
	HAL_SPI_StateTypeDef spi_state;

	uint32_t deadline = tf_hal_current_time_us(hal) + TF_HAL_SPI_TIMEOUT*1000;
	while((spi_state = HAL_SPI_GetState(&port->spi)) != HAL_SPI_STATE_READY) {
#ifdef TF_HAL_USE_COOP_TASK
		// Don't yield if we only transceive one byte.
		// We don't want to wait unnecessary long for that.
		if(length > 1) {
			tf_hal_get_common(hal)->locked = true;
			coop_task_yield(); // bricklib2-specific, change me for other platforms
			tf_hal_get_common(hal)->locked = false;
		}
#endif

		// Timeout if SPI state doesn't change to ready within 1s.
		// TODO: Maybe also explicitly check for ERROR and ABORT states here?
		if(tf_hal_deadline_elapsed(hal, deadline)) {
			return TF_E_TRANSCEIVE_TIMEOUT;
		}
	}

	return status == HAL_OK ? TF_E_OK : TF_E_TRANSCEIVE_FAILED;
}

uint32_t tf_hal_current_time_us(TF_HalContext *hal) {
	// bricklib2-specific, change me for other platforms
	return system_timer_get_us();
}

void tf_hal_sleep_us(TF_HalContext *hal, uint32_t us) {
#ifdef TF_HAL_USE_COOP_TASK
	const uint32_t deadline = tf_hal_current_time_us(hal) + us;
	while(!tf_hal_deadline_elapsed(hal, deadline)) {
		coop_task_yield(); // bricklib2-specific, change me for other platforms
	}
#else
	system_timer_sleep_us(us); // bricklib2-specific, change me for other platforms
#endif
}

TF_HalCommon *tf_hal_get_common(TF_HalContext *hal) {
	return &hal->hal_common;
}

void tf_hal_log_message(const char *msg, size_t len) {
    // bricklib2-specific, change me for other platforms
    for(size_t i = 0; i < len; ++i) {
        uartbb_tx(msg[i]);
    }
}

void tf_hal_log_newline() {
    // bricklib2-specific, change me for other platforms
    uartbb_tx('\n');
    uartbb_tx('\r');
}

#ifdef TF_IMPLEMENT_STRERROR
const char *tf_hal_strerror(int e_code) {
    switch(e_code) {
        #include "../bindings/error_cases.h"
        case TF_E_CHIP_SELECT_FAILED:
            return "failed to write to chip select GPIO";
        case TF_E_TRANSCEIVE_FAILED:
            return "failed to transceive over SPI";
        case TF_E_TRANSCEIVE_TIMEOUT:
            return "timeout during transceive over SPI";
        default:
            return "unknown error";
    }
}
#endif

char tf_hal_get_port_name(TF_HalContext *hal, uint8_t port_id) {
	if(port_id > hal->_port_count)
		return '?';

	return 'a' + port_id;
}


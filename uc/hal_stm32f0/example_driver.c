/*
 * Copyright (C) 2020 Olaf Lüke <olaf@tinkerforge.com>
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "src/bindings/config.h"
#include "src/hal_stm32f0/hal_stm32f0.h"
#include "src/bindings/errors.h"

#define BRICKLET_SPI0_CS0_PIN        GPIO_PIN_2
#define BRICKLET_SPI0_CS0_PORT       GPIOA
#define BRICKLET_SPI0_CS1_PIN        GPIO_PIN_3
#define BRICKLET_SPI0_CS1_PORT       GPIOA
#define BRICKLET_SPI0_CLK_PIN        GPIO_PIN_5
#define BRICKLET_SPI0_CLK_PORT       GPIOA
#define BRICKLET_SPI0_CLK_AF         GPIO_AF0_SPI1
#define BRICKLET_SPI0_MISO_PIN       GPIO_PIN_6
#define BRICKLET_SPI0_MISO_PORT      GPIOA
#define BRICKLET_SPI0_MISO_AF        GPIO_AF0_SPI1
#define BRICKLET_SPI0_MOSI_PIN       GPIO_PIN_7
#define BRICKLET_SPI0_MOSI_PORT      GPIOA
#define BRICKLET_SPI0_MOSI_AF        GPIO_AF0_SPI1
#define BRICKLET_SPI0_INSTANCE       SPI1

#define BRICKLET_SPI1_CS0_PIN        GPIO_PIN_10
#define BRICKLET_SPI1_CS0_PORT       GPIOB
#define BRICKLET_SPI1_CS1_PIN        GPIO_PIN_11
#define BRICKLET_SPI1_CS1_PORT       GPIOB
#define BRICKLET_SPI1_CLK_PIN        GPIO_PIN_13
#define BRICKLET_SPI1_CLK_PORT       GPIOB
#define BRICKLET_SPI1_CLK_AF         GPIO_AF0_SPI2
#define BRICKLET_SPI1_MISO_PIN       GPIO_PIN_14
#define BRICKLET_SPI1_MISO_PORT      GPIOB
#define BRICKLET_SPI1_MISO_AF        GPIO_AF0_SPI2
#define BRICKLET_SPI1_MOSI_PIN       GPIO_PIN_15
#define BRICKLET_SPI1_MOSI_PORT      GPIOB
#define BRICKLET_SPI1_MOSI_AF        GPIO_AF0_SPI2
#define BRICKLET_SPI1_INSTANCE       SPI2

TF_STMGPIO bricklet_cs[2][2] = {
	{
		{
			.pin = {
				.Pin       = BRICKLET_SPI0_CS0_PIN,
				.Mode      = GPIO_MODE_OUTPUT_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
			},
			.port = BRICKLET_SPI0_CS0_PORT
		}, {
			.pin = {
				.Pin       = BRICKLET_SPI0_CS1_PIN,
				.Mode      = GPIO_MODE_OUTPUT_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
			},
			.port = BRICKLET_SPI0_CS1_PORT
		}
	}, {
		{
			.pin = {
				.Pin       = BRICKLET_SPI1_CS0_PIN,
				.Mode      = GPIO_MODE_OUTPUT_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
			},
			.port = BRICKLET_SPI1_CS0_PORT
		}, {
			.pin = {
				.Pin       = BRICKLET_SPI1_CS1_PIN,
				.Mode      = GPIO_MODE_OUTPUT_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
			},
			.port = BRICKLET_SPI1_CS1_PORT
		}
	}
};

TF_Port bricklet_ports[2] = {
	{
		.cs = bricklet_cs[0],
		.cs_count = 2,
		.spi_instance = BRICKLET_SPI0_INSTANCE,
		.irq_tx = DMA1_Channel2_3_IRQn,
		.irq_rx = DMA1_Channel2_3_IRQn,
		.dma_channel_rx = DMA1_Channel2,
		.dma_channel_tx = DMA1_Channel3,
		.clk = {
			.pin = {
				.Pin       = BRICKLET_SPI0_CLK_PIN,
				.Mode      = GPIO_MODE_AF_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
				.Alternate = BRICKLET_SPI0_CLK_AF
			},
			.port = BRICKLET_SPI0_CLK_PORT
		},
		.miso = {
			.pin = {
				.Pin       = BRICKLET_SPI0_MISO_PIN,
				.Mode      = GPIO_MODE_AF_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
				.Alternate = BRICKLET_SPI0_MISO_AF
			},
			.port = BRICKLET_SPI0_MISO_PORT
		},
		.mosi = {
			.pin = {
				.Pin       = BRICKLET_SPI0_MOSI_PIN,
				.Mode      = GPIO_MODE_AF_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
				.Alternate = BRICKLET_SPI0_MOSI_AF
			},
			.port = BRICKLET_SPI0_MOSI_PORT
		}
	}, {
		.cs = bricklet_cs[1],
		.cs_count = 2,
		.spi_instance = BRICKLET_SPI1_INSTANCE,
		.irq_tx = DMA1_Channel4_5_IRQn,
		.irq_rx = DMA1_Channel4_5_IRQn,
		.dma_channel_rx = DMA1_Channel4,
		.dma_channel_tx = DMA1_Channel5,
		.clk = {
			.pin = {
				.Pin       = BRICKLET_SPI1_CLK_PIN,
				.Mode      = GPIO_MODE_AF_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
				.Alternate = BRICKLET_SPI1_CLK_AF
			},
			.port = BRICKLET_SPI1_CLK_PORT
		},
		.miso = {
			.pin = {
				.Pin       = BRICKLET_SPI1_MISO_PIN,
				.Mode      = GPIO_MODE_AF_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
				.Alternate = BRICKLET_SPI1_MISO_AF
			},
			.port = BRICKLET_SPI1_MISO_PORT
		},
		.mosi = {
			.pin = {
				.Pin       = BRICKLET_SPI1_MOSI_PIN,
				.Mode      = GPIO_MODE_AF_PP,
				.Pull      = GPIO_NOPULL,
				.Speed     = GPIO_SPEED_FREQ_HIGH,
				.Alternate = BRICKLET_SPI1_MOSI_AF
			},
			.port = BRICKLET_SPI1_MOSI_PORT
		}
	}
};

// Used to report any error encountered while running the example.
void check(int e_code, const char *c) {
	if (e_code == TF_E_OK) {
		return;
	}

#if TF_IMPLEMENT_STRERROR != 0
	tf_hal_printf("Failed to %s: %s (error code %d)\n", c, tf_hal_strerror(e_code), e_code);
#else
	tf_hal_printf("Failed to %s: %d\n", c, e_code);
#endif
}

TF_HAL hal;

int bricklet_main(void) {
	tf_hal_printf("Hello World!\n");
	check(tf_hal_create(&bricklet.hal, bricklet_ports, 2), "hal create");
	example_setup(&hal);

	while (true) {
		example_loop(&hal);
	}

	return 0;
}

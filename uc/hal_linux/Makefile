.SILENT:

# Compile with your cross compiler prefix. For example:
# make CROSS_COMPILE=arm-linux-gnueabihf-
# for Raspberry Pi

# Executable name
TARGET := uc_example

CC = $(CROSS_COMPILE)gcc

CFLAGS += -std=gnu99 -Wall -Wextra -I..
LDFLAGS += -pthread
LIBS += -lrt -ldl

WITH_DEBUG ?= yes

ifeq ($(WITH_DEBUG),yes)
	CFLAGS += -g -ggdb
endif

# These files are always required when using the bindings
SOURCES_BINDINGS := bindings/base58.c \
					bindings/bricklet_unknown.c \
					bindings/endian_convert.c \
					bindings/hal_common.c \
					bindings/packetbuffer.c \
					bindings/pearson_hash.c \
					bindings/spitfp.c \
					bindings/tfp.c \

# HAL specific files
SOURCES_HAL_LINUX := hal_linux/hal_linux.c \
					hal_linux/gpio_sysfs.c \
					hal_linux/utils.c \

# TODO: List your used devices here
SOURCES_DEVICES :=

# TODO: Add your example file below
SOURCES := example_driver.c \

SOURCES += $(SOURCES_BINDINGS)
SOURCES += $(SOURCES_HAL_LINUX)
SOURCES += $(SOURCES_DEVICES)

OBJECTS := ${SOURCES:.c=.o}
DEPENDS := ${SOURCES:.c=.p}

$(TARGET): $(OBJECTS)
	$(CC) -o $(TARGET) $(LDFLAGS) $(OBJECTS) $(LIBS)

%.o: %.c Makefile
	@echo CC $@
ifneq ($(PLATFORM),Windows)
	$(E)$(CC) -M $(CFLAGS) -o $*.d $<; cp $*.d $*.p; sed -e 's/#.*//' -e 's/^[^:]*: *//' -e 's/ *\\$$//' -e '/^$$/ d' -e 's/$$/ :/' < $*.d >> $*.p; rm -f $*.d
endif
	$(E)$(CC) $(CFLAGS) -c -o $@ $<

# FIXME: make dependency handling work for MinGW
# http://make.paulandlesley.org/autodep.html
ifneq ($(PLATFORM),Windows)
-include $(DEPENDS)
endif

.PHONY: all clean

clean: Makefile
	$(E)$(RM) $(OBJECTS) $(TARGET) $(DEPENDS)

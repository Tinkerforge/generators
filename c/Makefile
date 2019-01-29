#
# Minimal Makefile to create a basic Tinkerforge shared/static library for Linux
#

ifneq ($(findstring $(MAKEFLAGS),s),s)
ifndef V
	E := @
endif
endif

ifndef prefix
	prefix := /usr/local
endif

ifndef incdir
	incdir := $(prefix)/include/tinkerforge
endif

ifndef libdir
	libdir := $(prefix)/lib
endif

ifeq ($(OS),Windows_NT)
	CC := gcc
else
	CC ?= gcc
endif

AR ?= ar
RM := rm -f --
INSTALL := install

CFLAGS += -O2 -Wall -Wextra

ifneq ($(OS),Windows_NT)
	CFLAGS += -fPIC
endif

HEADERS := $(wildcard *.h)
SOURCES := $(wildcard *.c)
OBJECTS := ${SOURCES:.c=.o}

.PHONY: all clean install

ifeq ($(OS),Windows_NT)
all: tinkerforge.dll Makefile
else
all: libtinkerforge.so libtinkerforge.a Makefile
endif

%.o: %.c Makefile
	@echo CC $@
	$(E)$(CC) $(CFLAGS) -c -o $@ $<

libtinkerforge.so: $(OBJECTS) Makefile
	@echo LD $@
	$(E)$(CC) -shared -o $@ *.o

libtinkerforge.a: $(OBJECTS) Makefile
	@echo AR $@
	$(E)$(AR) rcs $@ *.o

tinkerforge.dll: $(OBJECTS) Makefile
	@echo LD $@
	$(E)$(CC) -shared -o $@ *.o *.def -lws2_32 -ladvapi32

clean: Makefile
	$(E)$(RM) $(OBJECTS) libtinkerforge.so libtinkerforge.a tinkerforge.dll

install: $(HEADERS) libtinkerforge.so Makefile
	@echo "MD $(incdir)"
	$(E)$(INSTALL) -d -m 755 $(incdir)

	@echo "CP $(HEADERS)"
	$(E)$(INSTALL) -m 644 $(HEADERS) $(incdir)

	@echo "MD $(libdir)"
	$(E)$(INSTALL) -d -m 755 $(libdir)

	@echo "CP libtinkerforge.so"
	$(E)$(INSTALL) -m 644 libtinkerforge.so $(libdir)

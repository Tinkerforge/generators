#
# Minimal Makefile to create a basic Tinkerforge shared/static library
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

CC ?= gcc
AR ?= ar
RM := rm -f --
INSTALL := install

CFLAGS += -O2 -fPIC -Wall -Wextra

HEADERS := $(wildcard *.h)
SOURCES := $(wildcard *.c)
OBJECTS := ${SOURCES:.c=.o}

.PHONY: all clean install

all: libtinkerforge.so libtinkerforge.a Makefile

%.o: %.c Makefile
	@echo CC $@
	$(E)$(CC) $(CFLAGS) -c -o $@ $<

libtinkerforge.so: $(OBJECTS) Makefile
	@echo LD $@
	$(E)$(CC) -shared -o $@ *.o

libtinkerforge.a: $(OBJECTS) Makefile
	@echo AR $@
	$(E)$(AR) rcs $@ *.o

clean: Makefile
	$(E)$(RM) $(OBJECTS) libtinkerforge.so libtinkerforge.a

install: $(HEADERS) libtinkerforge.so Makefile
	@echo "MD $(incdir)"
	$(E)$(INSTALL) -d -m 755 $(incdir)

	@echo "CP $(HEADERS)"
	$(E)$(INSTALL) -m 644 $(HEADERS) $(incdir)

	@echo "MD $(libdir)"
	$(E)$(INSTALL) -d -m 755 $(libdir)

	@echo "CP libtinkerforge.so"
	$(E)$(INSTALL) -m 644 libtinkerforge.so $(libdir)

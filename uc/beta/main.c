#include <stdio.h>

#include "hal_linux/hal_linux.h"

#include "demo/demo.h"

static void check(int rc, const char *c) {
    if (rc < 0) {
        printf("Failed to %s: %s (return code %d)\n", c, tf_strerror(rc), rc);
    }
}

TF_HalContext hal;

int main(int argc, char **argv) {
    printf("Hello World!\n");

    // HAT Brick
    TF_Port ports[9] = {{
        .chip_select_pin=23,
        .port_name = 'A'
    }, {
        .chip_select_pin=22,
        .port_name = 'B'
    }, {
        .chip_select_pin=25,
        .port_name = 'C'
    }, {
        .chip_select_pin=26,
        .port_name = 'D'
    }, {
        .chip_select_pin=27,
        .port_name = 'E'
    }, {
        .chip_select_pin=24,
        .port_name = 'F'
    }, {
        .chip_select_pin=7,
        .port_name = 'G'
    }, {
        .chip_select_pin=6,
        .port_name = 'H'
    }, {
        .chip_select_pin=5,
        .port_name = 'I'
    }};
    // HAT Zero Brick
    /*TF_Port ports[5] = {{
        .chip_select_pin=27,
        .port_name = 'A'
    }, {
        .chip_select_pin=23,
        .port_name = 'B'
    }, {
        .chip_select_pin=24,
        .port_name = 'C'
    }, {
        .chip_select_pin=22,
        .port_name = 'D'
    }, {
        .chip_select_pin=25,
        .port_name = 'E'
    }};*/

    check(tf_hal_create(&hal, "/dev/spidev0.0", ports, sizeof(ports)/sizeof(ports[0])), "hal create");

    demo_setup(&hal);

    while(true)
        demo_loop(&hal);

    return 0;
}

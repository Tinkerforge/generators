#include <stdio.h>

#include "hal_linux/hal_linux.h"
#include "bindings/errors.h"

// Forward declare the example functions.
void example_setup(TF_HalContext *hal);
void example_loop(TF_HalContext *hal);

void check(int e_code, const char *c);

// Change this to your port assignment.
// If you use a HAT or one or more Breakout Bricklets
// you have to connect and list all chip select
// signals, to make sure the signals are separated
// correctly.

// HAT Brick
static TF_Port ports[9] = {
    TF_PORT(23, 'A'),
    TF_PORT(22, 'B'),
    TF_PORT(25, 'C'),
    TF_PORT(26, 'D'),
    TF_PORT(27, 'E'),
    TF_PORT(24, 'F'),
    TF_PORT(7, 'G'),
    TF_PORT(6, 'H'),
    TF_PORT(5, 'I')
};

// HAT Zero Brick
/*static TF_Port ports[5] = {
    TF_PORT(27, 'A'),
    TF_PORT(23, 'B'),
    TF_PORT(24, 'C'),
    TF_PORT(22, 'D'),
    TF_PORT(25, 'I')
};*/

// Used to report any error encountered while running the example.
void check(int e_code, const char *c) {
    if(e_code == TF_E_OK) {
        return;
    }

    tf_hal_printf("Failed to %s: %s (error code %d)\n", c, tf_hal_strerror(e_code), e_code);
}

static TF_HalContext hal;

int main(void) {
    printf("Hello World!\n");
    check(tf_hal_create(&hal, "/dev/spidev0.0", ports, sizeof(ports)/sizeof(ports[0])), "hal create");
    example_setup(&hal);

    while(true) {
        example_loop(&hal);
    }
}

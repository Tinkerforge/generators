#include <stdio.h>

#include "hal_fake.h"

static TF_Port ports[1] = {
    TF_PORT(1, 'A')
};

void example_setup(TF_HalContext *hal);
void example_loop(TF_HalContext *hal);

void check(int e_code, const char *c);

void check(int e_code, const char *c) {
    if (e_code < 0) {
        tf_hal_printf("Failed to %s: %s (error code %d)\n", c, tf_hal_strerror(e_code), e_code);
    }
}

static TF_HalContext hal;

int main() {
    check(tf_hal_create(&hal, ports, sizeof(ports)/sizeof(ports[0])), "hal create");

    example_setup(&hal);

    while(true)
        example_loop(&hal);
}

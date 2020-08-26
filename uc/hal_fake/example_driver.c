#include <stdio.h>

#include "hal_fake.h"

void example_setup(TF_HalContext *hal);
void example_loop(TF_HalContext *hal);

void check(int rc, const char *c) {
    if (rc < 0) {
        tf_hal_printf("Failed to %s: %s (return code %d)\n", c, tf_strerror(rc), rc);
    }
}

TF_HalContext hal;

int main() {
    TF_Port ports[1] = {{
        .chip_select_pin=1,
        .port_name = 'A'
    }};

    check(tf_hal_create(&hal, ports, sizeof(ports)/sizeof(ports[0])), "hal create");

    example_setup(&hal);

    while(true)
        example_loop(&hal);

    return 0;
}

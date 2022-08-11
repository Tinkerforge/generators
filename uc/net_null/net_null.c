/*
 * Copyright (C) 2022 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "net_null.h"

int tf_net_tick(TF_Net *net) {
    (void) net;
    return TF_E_OK;
}
bool tf_net_get_available_tfp_header(TF_Net *net, TF_TFPHeader *header, int *packet_id) {
    (void) net;
    (void) header;
    (void) packet_id;
    return false;
}
int tf_net_get_packet(TF_Net *net, uint8_t packet_id, uint8_t *buf) {
    (void) net;
    (void) packet_id;
    (void) buf;
    return TF_E_OK;
}
int tf_net_drop_packet(TF_Net *net, uint8_t packet_id) {
    (void) net;
    (void) packet_id;
    return TF_E_OK;
}
void tf_net_send_packet(TF_Net *net, TF_TFPHeader *header, uint8_t *buf) {
    (void) net;
    (void) header;
    (void) buf;
}

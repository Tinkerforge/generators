/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "errors.h"

#include "hal_common.h"

const char *tf_strerror(int rc) {
    switch(rc) {
        case TF_E_OK:
            return "no error";
        case TF_E_TIMEOUT:
            return "timeout";
        case TF_E_INVALID_PARAMETER:
            return "device reported invalid parameter";
        case TF_E_NOT_SUPPORTED:
            return "device reported not supported";
        case TF_E_UNKNOWN_ERROR_CODE:
            return "device reported unknown error code";
        case TF_E_STREAM_OUT_OF_SYNC:
            return "stream out of sync, please retry";

        case TF_E_INVALID_CHAR_IN_UID:
            return "invalid char in UID, see base58.c for valid chars";
        case TF_E_UID_TOO_LONG:
            return "UID too long, see base58.c for maximum size";
        case TF_E_UID_OVERFLOW:
            return "UID overflow: encoded value was bigger than UINT64_MAX";

        case TF_E_TOO_MANY_DEVICES:
            return "too many devices found: increase INVENTORY_SIZE in config.h";
        case TF_E_DEVICE_NOT_FOUND:
            return "no device with the given UID is reachable";
        case TF_E_WRONG_DEVICE_TYPE:
            return "the device with the given UID is of unexpected device type";
        case TF_E_CALLBACK_EXEC:
            return "calling device functions from a callback handler is not allowed";
        case TF_E_PORT_NOT_FOUND:
            return "no port with the given port name was found";
        default:
            return tf_hal_strerror(rc);
    }
}

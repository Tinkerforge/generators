/*
 * Copyright (C) 2020 Erik Fleckstein <erik@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted. See the Creative
 * Commons Zero (CC0 1.0) License for more details.
 */

#include "tfp.h"

#include <stdint.h>
#include <stddef.h>
#include <stdbool.h>
#include <string.h>

#include "endian_convert.h"
#include "packetbuffer.h"
#include "hal_common.h"
#include "errors.h"

// Time in µs to sleep if there is no data available
#define TF_TFP_SLEEP_TIME_US 250

static uint32_t packet_header_get_uid(uint8_t *header) {
    uint32_t uid;
    memcpy(&uid, header + TFP_HEADER_UID_OFFSET, sizeof(uid));
    return tf_leconvert_uint32_from(uid);
}

static void packet_header_set_uid(uint8_t *header, uint32_t uid) {
    uid = tf_leconvert_uint32_to(uid);
    memcpy(header + TFP_HEADER_UID_OFFSET, &uid, sizeof(uid));
}

static uint8_t packet_header_get_length(uint8_t *header) {
    return header[TFP_HEADER_LENGTH_OFFSET];
}

static void packet_header_set_length(uint8_t *header, uint8_t length) {
    header[TFP_HEADER_LENGTH_OFFSET] = length;
}

static uint8_t packet_header_get_function_id(uint8_t *header) {
    return header[TFP_HEADER_FID_OFFSET];
}

static void packet_header_set_function_id(uint8_t *header, uint8_t function_id) {
    header[TFP_HEADER_FID_OFFSET] = function_id;
}


static uint8_t packet_header_get_sequence_number(uint8_t *header) {
	return (header[TFP_HEADER_SEQ_NUM_OFFSET] >> 4) & 0x0F;
}

static void packet_header_set_sequence_number(uint8_t *header, uint8_t sequence_number) {
	header[TFP_HEADER_SEQ_NUM_OFFSET] &= ~0xF0;
	header[TFP_HEADER_SEQ_NUM_OFFSET] |= (sequence_number << 4) & 0xF0;
}


static uint8_t packet_header_get_error_code(uint8_t *header) {
	return header[TFP_HEADER_FLAGS_OFFSET] >> 6;
}

static void packet_header_set_response_expected(uint8_t *header, bool response_expected) {
	if (response_expected) {
		header[TFP_HEADER_SEQ_NUM_OFFSET] |= 0x01 << 3;
	} else {
		header[TFP_HEADER_SEQ_NUM_OFFSET] &= ~(0x01 << 3);
	}
}

static uint8_t tf_tfp_build_header(TF_TfpContext *tfp, uint8_t *header, uint8_t length, uint8_t function_id, bool response_expected) {
	uint8_t sequence_number;

	sequence_number = tfp->next_sequence_number & 0x0F;
    if (sequence_number == 0) {
        sequence_number = 1;
    }
    tfp->next_sequence_number = sequence_number + 1;

	memset(header, 0, TFP_HEADER_LENGTH);

    packet_header_set_uid(header, tfp->uid);
    packet_header_set_length(header, length);
    packet_header_set_function_id(header, function_id);
	packet_header_set_sequence_number(header, sequence_number);

    packet_header_set_response_expected(header, response_expected);
    return sequence_number;
}

static bool tf_tfp_dispatch_callback(TF_TfpContext *tfp, uint32_t uid, uint8_t fid, uint8_t seq_num, TF_Packetbuffer *payload) {
    TF_HalCommon *common = tf_hal_get_common(tfp->spitfp.hal);

    if(fid == 253) {
        bool result = tf_hal_enumerate_handler(tfp->spitfp.hal, tfp->spitfp.port_id, payload);
        if(result)
            tf_tfp_packet_processed(tfp);
        return result;
    }

    TF_TfpContext *other_tfp = NULL;
    for(uint8_t i = 0; i < common->used; ++i) {
        if(common->uids[i] == uid) {
            other_tfp = common->tfps[i];
            break;
        }
    }

    // Received callback for not initialized device.
    if (other_tfp == NULL)
        return false;

    // This callback packet was already seen
    if (other_tfp->last_seen_spitfp_seq_num == seq_num) {
        return false;
    }
    else {
        other_tfp->last_seen_spitfp_seq_num = seq_num;
    }

    // Using the TfpContext* as a pointer to the specific device is safe
    // because the TfpContext is the first struct member i.e. has the same address.
    return other_tfp->cb_handler(other_tfp, fid, payload);
}

static bool tf_tfp_filter_received_packet(TF_TfpContext *tfp, bool remove_interesting, uint8_t spitfp_seq_num, uint8_t *error_code) {
    uint8_t used = tf_packetbuffer_get_used(&tfp->spitfp.recv_buf);
    if(used < 8) {
        tf_hal_log_debug("Too short!");
        tf_packetbuffer_remove(&tfp->spitfp.recv_buf, used);
        //tf_tfp_packet_processed(tfp);
        return false;
    }

    uint8_t header[8];
    tf_packetbuffer_pop_n(&tfp->spitfp.recv_buf, header, 8);

    uint32_t header_uid = packet_header_get_uid(header);
	uint8_t header_length = packet_header_get_length(header);
	uint8_t header_fid = packet_header_get_function_id(header);
	uint8_t header_seq_num = packet_header_get_sequence_number(header);

    // Compare with <= as behind the tfp packet there has to be the SPITFP checksum
    if(used <= header_length) {
        tf_hal_log_debug("Too short! used (%d) < header_length (%d)", used, header_length);
        tf_packetbuffer_remove(&tfp->spitfp.recv_buf, used);
        //tf_tfp_packet_processed(tfp);
        return false;
    }

    bool packet_uninteresting = (tfp->waiting_for_fid == 0) // we could do this before parsing the header, but in this order it's possible to remove the unwanted packet from the buffer.
        || (tfp->uid != 0 && header_uid != tfp->uid)
        || (header_fid != tfp->waiting_for_fid)
        || (header_length != tfp->waiting_for_length)
        || (header_seq_num != tfp->waiting_for_sequence_number);

    if (packet_uninteresting) {
        if(!tf_tfp_dispatch_callback(tfp, header_uid, header_fid, spitfp_seq_num, &tfp->spitfp.recv_buf)) {
            tf_hal_log_debug("Remove unexpected");

            if (tfp->waiting_for_fid == 0) {
                tf_hal_log_debug("tfp->waiting_for_fid == 0");
            }
            if (tfp->uid != 0 && header_uid != tfp->uid) {
                tf_hal_log_debug("tfp->uid != 0 && header_uid (%d) != tfp->uid (%d)", header_uid, tfp->uid);
            }
            if (header_fid != tfp->waiting_for_fid) {
                tf_hal_log_debug("header_fid (%d) != tfp->waiting_for_fid (%d)", header_fid, tfp->waiting_for_fid);
            }
            if (header_length != tfp->waiting_for_length) {
                tf_hal_log_debug("header_length (%d) != tfp->waiting_for_length (%d)", header_length, tfp->waiting_for_length);
            }
            if (header_seq_num != tfp->waiting_for_sequence_number) {
                tf_hal_log_debug("header_seq_num (%d) != tfp->waiting_for_sequence_number (%d)", header_seq_num, tfp->waiting_for_sequence_number);
            }
            tf_packetbuffer_remove(&tfp->spitfp.recv_buf, header_length);
            tf_tfp_packet_processed(tfp);
        }
        return false;
    }

    tfp->last_seen_spitfp_seq_num = spitfp_seq_num;

    if(remove_interesting) {
        tf_hal_log_debug("Remove unexpected 2");
        tf_packetbuffer_remove(&tfp->spitfp.recv_buf, header_length);
        tf_tfp_packet_processed(tfp);
        return false;
    }

    *error_code = packet_header_get_error_code(header);
    return true;
}

void tf_tfp_packet_processed(TF_TfpContext *tfp) {
    tf_spitfp_packet_processed(&tfp->spitfp);
}

int tf_tfp_init(TF_TfpContext *tfp, uint32_t uid, uint16_t dev_id, TF_HalContext *hal, uint8_t port_id, int inventory_index, CallbackHandler cb_handler) {
    memset(tfp, 0, sizeof(TF_TfpContext));
    int rc = tf_spitfp_init(&tfp->spitfp, hal, port_id);
    if (rc != TF_E_OK)
        return rc;

    tfp->next_sequence_number = 1;
    tfp->last_seen_spitfp_seq_num = 0;
    tfp->uid = uid;
    tfp->cb_handler = cb_handler;
    TF_HalCommon *common = tf_hal_get_common(hal);

    if(dev_id != 0 && common->dids[inventory_index] != dev_id) {
        return TF_E_WRONG_DEVICE_TYPE;
    }

    common->tfps[inventory_index] = tfp;

    return TF_E_OK;
}

int tf_tfp_destroy(TF_TfpContext *tfp) {
    TF_HalCommon *common = tf_hal_get_common(tfp->spitfp.hal);

    uint8_t port_id;
    int inventory_index;
    int rc = tf_hal_get_port_id(tfp->spitfp.hal, tfp->uid, &port_id, &inventory_index);
    if (rc < 0) {
        return rc;
    }

    if(common->tfps[inventory_index] != tfp)
        return TF_E_DEVICE_NOT_FOUND;

    common->tfps[inventory_index] = NULL;

    return tf_spitfp_destroy(&tfp->spitfp);
}

void tf_tfp_prepare_send(TF_TfpContext *tfp, uint8_t fid, uint8_t payload_size, uint8_t response_size, bool response_expected) {
    //TODO: theoretically, all bytes should be rewritten when sending a new packet, so this is not necessary.
    uint8_t *buf = tf_spitfp_get_payload_buffer(&tfp->spitfp);
    memset(buf, 0, TF_TFP_MESSAGE_MAX_LENGTH);

    uint8_t tf_tfp_seq_num = tf_tfp_build_header(tfp, buf, payload_size + TF_TFP_MESSAGE_MIN_LENGTH, fid, response_expected);

    if (response_expected) {
        tfp->waiting_for_fid = fid;
        tfp->waiting_for_length = response_size + TF_TFP_MESSAGE_MIN_LENGTH;
        tfp->waiting_for_sequence_number = tf_tfp_seq_num;
    } else {
        tfp->waiting_for_fid = 0;
        tfp->waiting_for_length = 0;
        tfp->waiting_for_sequence_number = 0;
    }
}

uint8_t *tf_tfp_get_payload_buffer(TF_TfpContext *tfp) {
    return tf_spitfp_get_payload_buffer(&tfp->spitfp) + TF_TFP_MESSAGE_MIN_LENGTH;
}

static int tf_tfp_transmit_getter(TF_TfpContext *tfp, uint32_t deadline_us, uint8_t *error_code) {
    tf_spitfp_build_packet(&tfp->spitfp, false);

    int result = TF_TICK_AGAIN;

    bool packet_received = false;

    uint32_t last_send = tf_hal_current_time_us(tfp->spitfp.hal);


    while(tf_hal_current_time_us(tfp->spitfp.hal) < deadline_us && !packet_received) {
        if (result & TF_TICK_TIMEOUT && tf_hal_current_time_us(tfp->spitfp.hal) - last_send >= 5000) {
            last_send = tf_hal_current_time_us(tfp->spitfp.hal);
            tf_spitfp_build_packet(&tfp->spitfp, true);
        }

        result = tf_spitfp_tick(&tfp->spitfp, deadline_us);
        if(result < 0)
            return result;

        if (result & TF_TICK_PACKET_RECEIVED) {
            if (tf_tfp_filter_received_packet(tfp, false, tfp->spitfp.last_sequence_number_seen, error_code)) {
                tfp->waiting_for_fid = 0;
                tfp->waiting_for_length = 0;
                tfp->waiting_for_sequence_number = 0;
                packet_received = true;
            }
        }
        if (result & TF_TICK_SLEEP) {
            tf_hal_sleep_us(tfp->spitfp.hal, TF_TFP_SLEEP_TIME_US);
        }
    }

    return (packet_received ? TF_TICK_PACKET_RECEIVED : TF_TICK_TIMEOUT) | (result & TF_TICK_AGAIN);
}

static int tf_tfp_transmit_setter(TF_TfpContext *tfp, uint32_t deadline_us) {
    tf_spitfp_build_packet(&tfp->spitfp, false);

    int result = TF_TICK_AGAIN;
    bool packet_sent = false;

    while(tf_hal_current_time_us(tfp->spitfp.hal) < deadline_us && !packet_sent) {
        if (result & TF_TICK_TIMEOUT)
            tf_spitfp_build_packet(&tfp->spitfp, true);

        result = tf_spitfp_tick(&tfp->spitfp, deadline_us);
        if(result < 0)
            return result;

        if (result & TF_TICK_PACKET_RECEIVED) {
            uint8_t error_code;
            tf_tfp_filter_received_packet(tfp, true, tfp->spitfp.last_sequence_number_seen, &error_code);
        }

        if (result & TF_TICK_PACKET_SENT) {
            packet_sent = true;
        }

        if (result & TF_TICK_SLEEP) {
            tf_hal_sleep_us(tfp->spitfp.hal, TF_TFP_SLEEP_TIME_US);
        }
    }

    return (packet_sent ? TF_TICK_PACKET_SENT : TF_TICK_TIMEOUT) | (result & TF_TICK_AGAIN);
}


int tf_tfp_transmit_packet(TF_TfpContext *tfp, bool response_expected, uint32_t deadline_us, uint8_t *error_code) {
    return response_expected ? tf_tfp_transmit_getter(tfp, deadline_us, error_code) : tf_tfp_transmit_setter(tfp, deadline_us);
}

int tf_tfp_finish_send(TF_TfpContext *tfp, int previous_result, uint32_t deadline_us) {
    int result = previous_result;

    while(tf_hal_current_time_us(tfp->spitfp.hal) < deadline_us && (result & TF_TICK_AGAIN)) {
        result = tf_spitfp_tick(&tfp->spitfp, deadline_us);
        if(result < 0)
            return result;
    }

    // Prevent sending the packet again for example in the callback_tick
    tfp->spitfp.send_buf[0] = 0;

    return (result & TF_TICK_AGAIN) ? -1 : 0;
}

int tf_tfp_get_error(uint8_t error_code) {
    switch(error_code) {
        case 1:
            return TF_E_INVALID_PARAMETER;
        case 2:
            return TF_E_NOT_SUPPORTED;
        case 3:
            return TF_E_UNKNOWN_ERROR_CODE;
        case 0:
        default:
            return TF_E_OK;
    }
}

int tf_tfp_callback_tick(TF_TfpContext *tfp, uint32_t deadline_us) {
    int result = TF_TICK_AGAIN;
    // Allow the state machine to run a bit over the deadline:
    // Timeout is returned when the state machine goes back into the idle state.
    // In the worst case, we just ticking the idling state machine into RECEIVE
    // when the deadline is triggered, then we receive a packet, create an ACK and transmit
    // it. Transmitting the ACK only clocks out three bytes, so no other packet should be
    // able to be received there. In other words this is not an infinite loop.
    while(tf_hal_current_time_us(tfp->spitfp.hal) < deadline_us || !(result & TF_TICK_TIMEOUT)) {
        result = tf_spitfp_tick(&tfp->spitfp, deadline_us);
        if(result < 0)
            return result;
        if (result & TF_TICK_PACKET_RECEIVED) {
            //handle possible callback packet
            uint8_t error_code;
            tf_tfp_filter_received_packet(tfp, false, tfp->spitfp.last_sequence_number_seen, &error_code);
        }
        if (result & TF_TICK_SLEEP) {
            tf_hal_sleep_us(tfp->spitfp.hal, TF_TFP_SLEEP_TIME_US);
        }
    }
    return 0;
}

#include "net_arduino.h"

#include "Arduino.h"

#include <WiFi.h>

#include "string.h"

#include "../bindings/macros.h"
#include "../bindings/hal_common.h"

void remove_open_request(TF_NetContext *net, size_t idx) {
    memmove(net->open_requests + idx, net->open_requests + idx + 1, sizeof(TF_Request) * (net->open_request_count - idx - 1));
    --net->open_request_count;
}

void add_open_request(TF_NetContext *net, uint32_t client_id, TF_TfpHeader *header) {
    if(net->open_request_count == sizeof(net->open_requests) / sizeof(net->open_requests[0])) {
        // The open_request array is full. Drop the oldest request.
        // Note that this does not mean, that a later response to the dropped request will be
        // dropped too: As only the mapping to where the request came from is missing, the response
        // will be broadcasted to all connected clients.
        remove_open_request(net, 0);
    }

    net->open_requests[net->open_request_count].client_id = client_id;
    net->open_requests[net->open_request_count].uid = header->uid;
    net->open_requests[net->open_request_count].fid = header->fid;
    net->open_requests[net->open_request_count].seq_num = header->seq_num;

    ++net->open_request_count;
}

uint32_t tf_net_current_time_us(TF_NetContext *net) {
    return micros();
}

uint32_t tf_net_current_time_ms(TF_NetContext *net) {
    return millis();
}

void remove_client(TF_NetContext *net, uint32_t client_idx) {
    TF_NetClient *client = &net->clients[client_idx];

    for(int i = 0; i < net->open_request_count; ++i) {
        if(net->open_requests[i].client_id == client->id) {
            remove_open_request(net, i);
            --i;
        }
    }

    client->client.stop();

    memmove(net->clients + client_idx, net->clients + (client_idx + 1), sizeof(TF_NetClient) * (net->clients_used - client_idx - 1));
    --net->clients_used;
    net->clients[net->clients_used].id = 0;
    net->clients[net->clients_used].read_buf_used = 0;
    net->clients[net->clients_used].send_buf_used = 0;
    // TODO clear read_buf?;

    tf_hal_log_info("disconnect; clients used: %d\n", net->clients_used);
}

int read_packets(TF_NetContext *net) {
    for(size_t i = 0; i < net->clients_used; ++i) {
        TF_NetClient *client = &net->clients[i];
        uint8_t *buf = client->read_buf;
        uint8_t to_write = sizeof(client->read_buf) / sizeof(client->read_buf[0]) - client->read_buf_used;

        if(to_write == 0) {
            continue;
        }

        //ssize_t written = recv(client->fd, buf + client->read_buf_used, to_write, 0);
        size_t available = client->client.available();

        to_write = MIN(to_write, available);
        ssize_t written = client->client.read(buf + client->read_buf_used, to_write);

        if(written == 0) {
            remove_client(net, i);
            --i;

            continue;
        }

        if(written < 0) {
            if(errno != EAGAIN && errno != EWOULDBLOCK) {
                remove_client(net, i);
                --i;
            }

            continue;
        }

        client->read_buf_used += written;
        client->last_recv_ms = tf_net_current_time_ms(net);
    }
    return 0;
}

int send_from_buf(TF_NetContext *net, int client_idx) {
    TF_NetClient *client = &net->clients[client_idx];
    size_t written = client->client.write(client->send_buf, client->send_buf_used);

    client->last_send_us = tf_net_current_time_us(net);

    size_t send_buf_size = sizeof(client->send_buf) / sizeof(client->send_buf[0]);

    memmove(client->send_buf, client->send_buf + written, send_buf_size - written * sizeof(client->send_buf[0]));
    client->send_buf_used -= written;

    return written;
}

bool deadline_elapsed(uint32_t now, uint32_t deadline_us) {
    return ((uint32_t)(now - deadline_us)) < (UINT32_MAX / 2);
}

int add_to_send_buf(TF_NetContext *net, int client_idx, uint8_t *buf, uint8_t len) {
    TF_NetClient *client = &net->clients[client_idx];
    size_t send_buf_size = sizeof(client->send_buf) / sizeof(client->send_buf[0]);
    uint32_t deadline_us = tf_net_current_time_us(net) + 10000;

    while(len > send_buf_size - client->send_buf_used) {
        if(deadline_elapsed(tf_net_current_time_us(net), deadline_us)) {
            ++client->sends_without_progress;

            if(client->sends_without_progress < 10) {
                return 0;
            }

            return -1;
        }

        int err = send_from_buf(net, client_idx);

        if(err < 0) {
            return err;
        }
    }

    client->sends_without_progress = 0;

    memcpy(client->send_buf + client->send_buf_used, buf, len);
    client->send_buf_used += len;

    return len;
}

void flush_send_buffers(TF_NetContext *net) {
    for(size_t i = 0; i < net->clients_used; ++i) {
        TF_NetClient *client = &net->clients[i];

        if(client->send_buf_used == 0) {
            continue;
        }

        if(deadline_elapsed(tf_net_current_time_us(net), client->last_send_us + net->send_buf_timeout_us) || client->send_buf_used > 1300) {
            if(send_from_buf(net, i) < 0) {
                remove_client(net, i);
                --i;
            }
        }
    }
}

int accept_connections(TF_NetContext *net) {
    TF_NetClient *clients = net->clients;
    size_t max_clients = sizeof(net->clients)/sizeof(net->clients[0]);
    static uint32_t client_id = 0;
    WiFiClient client = net->server.available();

    if(!client) {
        return 0;
    }

    if(!client.connected()) {
        return 0;
    }

    client.setNoDelay(true);

    size_t insert_idx = net->clients_used;
    clients[insert_idx].client = client;
    clients[insert_idx].id = ++client_id;
    clients[insert_idx].last_recv_ms = tf_net_current_time_ms(net);
    clients[insert_idx].last_send_us = tf_net_current_time_us(net);

    memset(clients[insert_idx].read_buf, 0, sizeof(clients[insert_idx].read_buf) / sizeof(clients[insert_idx].read_buf[0]));
    clients[insert_idx].read_buf_used = 0;

    memset(clients[insert_idx].send_buf, 0, sizeof(clients[insert_idx].send_buf) / sizeof(clients[insert_idx].send_buf[0]));
    clients[insert_idx].send_buf_used = 0;
    ++net->clients_used;

    printf("clients used: %d\n", net->clients_used);

    /*if(net->clients_used == max_clients) {
        // We already have the maximum amount of clients, don't accept more.
        close(net->server_fd);
        net->server_fd = -1;
    }*/

    return 0;
}

void remove_dead_clients(TF_NetContext *net) {
    for(size_t i = 0; i < net->clients_used; ++i) {
        if(deadline_elapsed(tf_net_current_time_ms(net), net->clients[i].last_recv_ms + net->recv_timeout_ms)) {
            remove_client(net, i);
        }
    }
}

bool is_valid_header(TF_TfpHeader *header) {
    if(header->length < TF_TFP_MIN_MESSAGE_LENGTH) {
        return false;
    }

    if(header->length > TF_TFP_MAX_MESSAGE_LENGTH) {
        return false;
    }

    if(header->fid == 0) {
        return false;
    }

    return true;
}

void reassemble_packets(TF_NetContext *net) {
    for(int i = 0; i < net->clients_used; ++i) {
        TF_NetClient *client = &net->clients[i];

        if(client->available_packet_valid) {
            continue;
        }

        uint8_t used = client->read_buf_used;
        if (used < 8)
            continue;

        uint8_t *buf = client->read_buf;
        TF_TfpHeader header;
        tf_peek_packet_header_plain_buf(buf, &header);

        if(!is_valid_header(&header)) {
            tf_hal_log_info("invalid request, closing connection\n");
            tf_print_packet_header(&header);

            for(int i = 0; i < 80; ++i){
                printf("%02x ", buf[i]);
            }

            printf("\n");
            remove_client(net, i);

            continue;
        }

        if (used < header.length)
            continue;

        client->available_packet = header;
        client->available_packet_valid = true;
    }
}

int tf_net_create(TF_NetContext *net, const char* listen_addr, uint16_t port, const char* auth_secret) {
    (void)listen_addr;
    (void)port;
    (void)auth_secret;

    // TODO: if we memset here, the wifi server is borked
    //memset(net, 0, sizeof(TF_NetContext));
    net->server.begin(4223);
    net->server.setNoDelay(true);

    net->send_buf_timeout_us = 20000;
    net->recv_timeout_ms = 60000;

    return 0;
}

int tf_net_tick(TF_NetContext *net) {
    flush_send_buffers(net);
    read_packets(net);
    reassemble_packets(net);
    accept_connections(net);

    // TODO: reenable this when we have a useful heartbeat
    //remove_dead_clients(net);

    return 0;
}

bool tf_net_get_available_packet_header(TF_NetContext *net, TF_TfpHeader *header, int *packet_id) {
    for(int i = (*packet_id) + 1; i < net->clients_used; ++i) {
        TF_NetClient *client = &net->clients[i];
        if(!client->available_packet_valid)
            continue;
        *header = client->available_packet;
        *packet_id = i;

        return true;
    }

    return false;
}

int tf_net_get_packet(TF_NetContext *net, uint8_t packet_id, uint8_t *buf) {
    TF_NetClient *client = &net->clients[packet_id];
    if(!client->available_packet_valid)
        return -1;

    memcpy(buf, client->read_buf, client->available_packet.length);

    // If we output a packet that is a request, keep track over the request to be able to unicast the response.
    if(client->available_packet.uid != 0 && client->available_packet.response_expected) {
        add_open_request(net, client->id, &client->available_packet);
    }

    return 0;
}

int tf_net_drop_packet(TF_NetContext *net, uint8_t packet_id) {
    TF_NetClient *client = &net->clients[packet_id];
    if(!client->available_packet_valid)
        return -1;

    memmove(client->read_buf, client->read_buf + client->available_packet.length, client->read_buf_used - client->available_packet.length);
    client->read_buf_used -= client->available_packet.length;
    client->available_packet_valid = false;

    return 0;
}

void broadcast(TF_NetContext *net, TF_TfpHeader *header, uint8_t *buf) {
     for(size_t i = 0; i < net->clients_used; ++i) {
        if(add_to_send_buf(net, i, buf, header->length) < 0) {
            remove_client(net, i);
            --i;

            continue;
        }
    }
}

void unicast(TF_NetContext *net, TF_TfpHeader *header, uint8_t *buf, size_t client_idx) {
    if(add_to_send_buf(net, client_idx, buf, header->length) < 0) {
        remove_client(net, client_idx);
        return;
    }

    // TODO: if send_from_buf can't send anything here we will send again in 20 ms. maybe set last_send to a lower value to force more sends.
    if(send_from_buf(net, client_idx) < 0) {
        remove_client(net, client_idx);
        return;
    }
}

void tf_net_send_packet(TF_NetContext *net, TF_TfpHeader *header, uint8_t *buf) {
    if(header->seq_num == 0) {
        broadcast(net, header, buf);
    } else {
        TF_Request *request = NULL;
        size_t request_idx = 0;

        for(; request_idx < net->open_request_count; ++request_idx) {
            TF_Request *req = &net->open_requests[request_idx];

            if(req->fid == header->fid && req->seq_num == header->seq_num && req->uid == header->uid) {
                request = req;
                break;
            }
        }

        if(request == NULL) {
            // We don't know where the request came from anymore.
            broadcast(net, header, buf);
            return;
        }

        uint32_t client_id = request->client_id;
        remove_open_request(net, request_idx);

        TF_NetClient *client = NULL;
        size_t client_idx = 0;

        for(; client_idx < net->clients_used; ++client_idx) {
            if(net->clients[client_idx].id == client_id) {
                client = &net->clients[client_idx];
                break;
            }
        }

        if(client == NULL) {
            // The client for this response is gone. Drop the response.
            return;
        }

        unicast(net, header, buf, client_idx);
    }
}

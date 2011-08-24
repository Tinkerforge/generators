/*******************************************************************
 * Copyright (c) 2011, Olaf Lüke (olaf@tinkerforge.com)            *
 *                                                                 *
 * Redistribution and use in source and binary forms of this file, *
 * with or without modification, are permitted.                    *
 *******************************************************************/

#include "ip_connection.h"

#include <stdbool.h>
#include <stdio.h>

#include <time.h>

#ifdef _WIN32
	#include <windows.h>
	#include <winsock2.h>
#else
	#include <pthread.h>
	#include <semaphore.h>
	#include <sys/types.h>
	#include <sys/socket.h> // connect
	#include <sys/select.h>
	#include <netinet/in.h> // struct sockaddr_in
	#include <netdb.h> // gethostbyname
#endif

#include <unistd.h> 

#define MAX_BASE58_STR_SIZE 13
const char BASE58_STR[] = \
	"123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

#ifdef _WIN32
void ipcon_recv_loop(void *param) {
#else
void* ipcon_recv_loop(void *param) {
#endif
	IPConnection *ipcon = (IPConnection*)param;
	unsigned char buffer[RECV_BUFFER_SIZE] = { 0 };
	int position = 0;

	while(ipcon->recv_loop_flag) {
#ifdef _WIN32
		int length = recv(ipcon->s, buffer, RECV_BUFFER_SIZE, 0);
#else
		int length = read(ipcon->fd, buffer, RECV_BUFFER_SIZE);
#endif
		if(length == 0) {
			if(ipcon->recv_loop_flag) {
				printf("Socket disconnected by Server, destroying ipcon\n");
				ipcon_destroy(ipcon);
			}
#ifdef _WIN32
			return;
#else
			return NULL;
#endif
		}
		int handled = 0;
		do {
			handled += ipcon_handle_message(ipcon, buffer + handled);
		} while(handled < length);
	}
}

void ipcon_destroy(IPConnection *ipcon) {
	ipcon->recv_loop_flag = false;

#ifdef _WIN32
	shutdown(ipcon->s, 2);
	closesocket(ipcon->s);
#else
	shutdown(ipcon->fd, 2);
	close(ipcon->fd);
#endif
}

void ipcon_join_thread(IPConnection *ipcon) {
#ifdef _WIN32
	WaitForSingleObject(ipcon->handle_recv_loop, INFINITE);
#else
	pthread_join(ipcon->thread_recv_loop, NULL);
#endif
}

void ipcon_enumerate(IPConnection *ipcon, enumerate_callback_func_t cb) {
	ipcon->enumerate_callback = cb;

	Enumerate e = {
		BROADCAST_ADDRESS,
		TYPE_ENUMERATE,
		sizeof(Enumerate)
	};

#ifdef _WIN32
	send(ipcon->s, (const char*)&e, sizeof(Enumerate), 0);
#else
	write(ipcon->fd, &e, sizeof(Enumerate));
#endif
}

int ipcon_handle_enumerate(IPConnection *ipcon, const unsigned char *buffer) {
	int length = ipcon_get_length_from_data(buffer);

	if(ipcon->enumerate_callback == NULL) {
		return length;
	}

	EnumerateReturn *er = (EnumerateReturn *)buffer;
	char str_uid[MAX_BASE58_STR_SIZE];
	ipcon_base58encode(er->device_uid, str_uid);

	ipcon->enumerate_callback(str_uid, 
	                          er->device_name, 
	                          er->device_stack_id,
							  er->is_new);

	return length;
}

int ipcon_handle_message(IPConnection *ipcon, const unsigned char *buffer) {
	unsigned char type = ipcon_get_type_from_data(buffer);
	if(type == TYPE_GET_STACK_ID) {
		return ipcon_add_device_handler(ipcon, buffer);
	} else if(type == TYPE_ENUMERATE_CALLBACK) {
		return ipcon_handle_enumerate(ipcon, buffer);
	}

	unsigned char stack_id = ipcon_get_stack_id_from_data(buffer);
	int length = ipcon_get_length_from_data(buffer);
	if(ipcon->devices[stack_id] == NULL) {
		fprintf(stderr, "Message with unknown Stack ID, discarded %d %d\n", stack_id, type);
		return length;
	}

	Device *device =  ipcon->devices[stack_id];
	DeviceAnswer *answer = &device->answer;

	if(answer->type == type) {
		if(answer->length != 0 && answer->length != length) {
			fprintf(stderr, 
			        "Received malformed message, discarded: %d\n", 
			        stack_id);
			return length;
		}

		memcpy(answer->buffer, buffer, length);
		answer->length = length;

#ifdef _WIN32
		ReleaseSemaphore(device->sem_answer,1,NULL);
#else
		sem_post(&device->sem_answer);
#endif
		return length;
	}

	if(device->callbacks[type] != NULL) {
		return device->device_callbacks[type](device, buffer);
	}

	// Message seems to be OK, but can't be handled, most likely
	// a signal without registered callback
	return length;
}

void ipcon_device_write(Device *device, const char *buffer, const int length) {
	// Wait for next write until answer is there. This makes the
	// IMU API thread safe.
	// It is in theory possible to allow concurrent writes from different 
	// threads, we would have to use lists of buffers for that.
	// Perhaps someone will implement that in the future.
#ifdef _WIN32
	send(device->ipcon->s, buffer, length, 0);
#else
	write(device->ipcon->fd, buffer, length);
#endif
}

void ipcon_device_create(Device *device, const char *uid) {
	int i;
	for(i = 0; i < MAX_NUM_CALLBACKS; i++) {
		device->callbacks[i] = NULL;
		device->device_callbacks[i] = NULL;
	}

	device->uid = ipcon_base58decode(uid);
	device->ipcon = NULL;

#ifdef _WIN32
	device->sem_write = CreateSemaphore(NULL,1,1,NULL);
	// Default state for answer semaphore is locked
	device->sem_answer = CreateSemaphore(NULL,0,1,NULL);
#else
	sem_init(&device->sem_write, 0, 1);
	sem_init(&device->sem_answer, 0, 1);

	// Default state for answer semaphore is locked
	sem_wait(&device->sem_answer);
#endif
}

int ipcon_answer_sem_wait_timeout(Device *device) {
#ifdef _WIN32
	return WaitForSingleObject(device->sem_answer, TIMEOUT_ANSWER);
#else
	struct timespec time;
	clock_gettime(CLOCK_REALTIME, &time);
	time.tv_sec += TIMEOUT_ANSWER/1000;
	return sem_timedwait(&device->sem_answer, &time);
#endif

}

int ipcon_create(IPConnection *ipcon, const char* host, const int port) {
	int i;
	for(i = 0; i < MAX_NUM_DEVICES; i++) {
		ipcon->devices[i] = NULL;
	}
	ipcon->add_device = NULL;
	ipcon->enumerate_callback = NULL;
	ipcon->recv_loop_flag = true;

#ifdef _WIN32

	WSADATA wsaData;
	
	// Initialize Winsock
	if(WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		return E_NO_STREAM_SOCKET;
	}

	ipcon->s = INVALID_SOCKET;
	ipcon->s = socket(AF_INET, SOCK_STREAM, 0);
	if(ipcon->s < 0) {
		return E_NO_STREAM_SOCKET;
	}

#else
	ipcon->fd = socket(AF_INET, SOCK_STREAM, 0);
	if(ipcon->fd < 0) {
		return E_NO_STREAM_SOCKET;
	}
#endif

	struct hostent *he = gethostbyname(host);
	if(he == NULL) { 
		return E_HOSTNAME_INVALID;
	}

	memset(&ipcon->server, 0, sizeof(struct sockaddr_in));
	memcpy(&ipcon->server.sin_addr, he->h_addr_list[0], he->h_length);
	ipcon->server.sin_family = AF_INET;
	ipcon->server.sin_port = htons(port);
#ifdef _WIN32
	if(connect(ipcon->s, 
	           (struct sockaddr *)&ipcon->server, 
	           sizeof(ipcon->server)) < 0 ) {
		return E_NO_CONNECT;
	}
#else
	if(connect(ipcon->fd, 
	           (struct sockaddr *)&ipcon->server, 
	           sizeof(ipcon->server)) < 0 ) {
		return E_NO_CONNECT;
	}
#endif

#ifdef _WIN32
	double thread_recv_loop_id;
	ipcon->handle_recv_loop = CreateThread(
		NULL,
		0,
		(LPTHREAD_START_ROUTINE)ipcon_recv_loop,
		(void*)ipcon,
		0,
		(LPDWORD)&thread_recv_loop_id
	);
#else
	if(pthread_create(&ipcon->thread_recv_loop, 
					  NULL, 
					  ipcon_recv_loop, 
					  (void*)ipcon) < 0) {
		return E_NO_THREAD;
	}
#endif
	return E_OK;
}

int ipcon_add_device_handler(IPConnection *ipcon, 
                             const unsigned char *buffer) {
	const GetStackIDReturn *gsidr = (const GetStackIDReturn*)buffer;
	if(ipcon->add_device != NULL && 
	   ipcon->add_device->uid == gsidr->device_uid) {
		ipcon->add_device->stack_id = gsidr->device_stack_id;
		ipcon->devices[gsidr->device_stack_id] = ipcon->add_device;
#ifdef _WIN32
		ReleaseSemaphore(ipcon->add_device->sem_answer,1,NULL);
#else
		sem_post(&ipcon->add_device->sem_answer);
#endif

		ipcon->add_device = NULL;
	}

	return sizeof(GetStackIDReturn);
}

int ipcon_add_device(IPConnection *ipcon, Device *device) {
	device->ipcon = ipcon;

	GetStackID gsid = {
		BROADCAST_ADDRESS,
		TYPE_GET_STACK_ID,
		sizeof(GetStackID),
		device->uid
	};

#ifdef _WIN32
	send(ipcon->s, (const char*) &gsid, sizeof(GetStackID), 0);
#else
	write(ipcon->fd, &gsid, sizeof(GetStackID));
#endif
	ipcon->add_device = device;
	// Block until there is an answer, timeout after TIMEOUT_ADD_DEVICE ms
	if(ipcon_answer_sem_wait_timeout(device) != 0) {
		return E_TIMEOUT;
	}
}

unsigned short ipcon_get_length_from_data(const unsigned char *data) {
	return *((unsigned short*)(data + 2));
}

unsigned char ipcon_get_stack_id_from_data(const unsigned char *data) {
	return data[0];
}

unsigned char ipcon_get_type_from_data(const unsigned char *data) {
	return data[1];
}

int ipcon_sem_wait_write(Device *device) {
#ifdef _WIN32
	return WaitForSingleObject(device->sem_write, INFINITE);
#else
	return sem_wait(&device->sem_write);
#endif
}

int ipcon_sem_post_write(Device *device) {
#ifdef _WIN32
	return ReleaseSemaphore(device->sem_write,1,NULL);
#else
	return sem_post(&device->sem_write);
#endif
}

void ipcon_base58encode(uint64_t value, char *str) {
	char reverse_str[MAX_BASE58_STR_SIZE] = {0};
	int i = 0;
	while(value >= 58) {
		uint64_t mod = value % 58;
		reverse_str[i] = BASE58_STR[mod];
		value = value/58;
		i++;
	}

	reverse_str[i] = BASE58_STR[value];
	int j = 0;
	i = 0;
	while(reverse_str[MAX_BASE58_STR_SIZE-1 - i] == '\0') {
		i++;
	}
	for(j = 0; j < MAX_BASE58_STR_SIZE; j++) {
		if(MAX_BASE58_STR_SIZE - i >= 0) {
			str[j] = reverse_str[MAX_BASE58_STR_SIZE-1 - i];
		} else {
			str[j] = '\0';
		}
		i++;
	}
}

uint64_t ipcon_base58decode(const char *str) {
	uint64_t value = 0;
	uint64_t column_multiplier = 1;

	int i;
	for(i = 0; i < MAX_BASE58_STR_SIZE; i++) {
		if(str[i] == '\0') {
			break;
		}
	}
	i -= 1;

	for(; i >= 0; i--) {
		if(str[i] == '\0') {
			continue;
		}

		int column;
		for(column = 0; column < 58; column++) {
			if(BASE58_STR[column] == str[i]) {
				break;
			}
		}
		
		value += column * column_multiplier;
		column_multiplier *= 58;
	}

	return value;
}


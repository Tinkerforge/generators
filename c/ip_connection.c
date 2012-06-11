/*
 * Copyright (C) 2012 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

#include "ip_connection.h"

#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>

#ifndef _WIN32
	#include <unistd.h>
	#include <sys/types.h>
	#include <sys/time.h> // gettimeofday
	#include <sys/socket.h> // connect
	#include <sys/select.h>
	#include <netdb.h> // gethostbyname
#endif

#define MAX_BASE58_STR_SIZE 13
const char BASE58_STR[] = \
	"123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

#ifdef _WIN32

void ipcon_mutex_lock(CRITICAL_SECTION *mutex) {
	EnterCriticalSection(mutex);
}

void ipcon_mutex_unlock(CRITICAL_SECTION *mutex) {
	LeaveCriticalSection(mutex);
}

static bool ipcon_semaphore_request(HANDLE semaphore) {
	return WaitForSingleObject(semaphore, INFINITE) == WAIT_OBJECT_0;
}

static void ipcon_semaphore_release(HANDLE semaphore) {
	ReleaseSemaphore(semaphore, 1, NULL);
}

#define THREAD_RETURN_TYPE void
#define THREAD_RETURN return

#else

void ipcon_mutex_lock(pthread_mutex_t *mutex) {
	pthread_mutex_lock(mutex);
}

void ipcon_mutex_unlock(pthread_mutex_t *mutex) {
	pthread_mutex_unlock(mutex);
}

static bool ipcon_semaphore_request(sem_t *semaphore) {
	return sem_wait(semaphore) == 0;
}

static void ipcon_semaphore_release(sem_t *semaphore) {
	sem_post(semaphore);
}

#define THREAD_RETURN_TYPE void *
#define THREAD_RETURN return NULL

#endif

THREAD_RETURN_TYPE ipcon_recv_loop(void *param) {
	IPConnection *ipcon = (IPConnection*)param;
	unsigned char buffer[RECV_BUFFER_SIZE] = { 0 };

	while(ipcon->recv_loop_flag) {
#ifdef _WIN32
		int length = recv(ipcon->s, (char*)buffer, RECV_BUFFER_SIZE, 0);
		if(length == SOCKET_ERROR) {
			if (WSAGetLastError() == WSAEINTR) {
				continue;
			}

			fprintf(stderr, "A socket error occurred, destroying ipcon\n");
			ipcon_destroy(ipcon);
			THREAD_RETURN;
		}
#else
		int length = read(ipcon->fd, buffer, RECV_BUFFER_SIZE);
		if(length < 0) {
			if (errno == EINTR) {
				continue;
			}

			fprintf(stderr, "A socket error occurred, destroying ipcon\n");
			ipcon_destroy(ipcon);
			THREAD_RETURN;
		}
#endif

		if(length == 0) {
			if(ipcon->recv_loop_flag) {
				fprintf(stderr, "Socket disconnected by Server, destroying ipcon\n");
				ipcon_destroy(ipcon);
			}
			THREAD_RETURN;
		}
		int handled = 0;
		do {
			handled += ipcon_handle_message(ipcon, buffer + handled);
		} while(handled < length);
	}
	THREAD_RETURN;
}

THREAD_RETURN_TYPE ipcon_callback_loop(void *param) {
	IPConnection *ipcon = (IPConnection*)param;

	while(ipcon->recv_loop_flag) {
		if (!ipcon_semaphore_request(ipcon->callback_queue_semaphore)) {
			continue;
		}

		if (!ipcon->recv_loop_flag) {
			break;
		}

		if (ipcon->callback_queue_head == NULL) {
			continue;
		}

		ipcon_mutex_lock(&ipcon->callback_queue_mutex);

		CallbackQueueNode *node = ipcon->callback_queue_head;
		ipcon->callback_queue_head = node->next;
		node->next = NULL;

		if (ipcon->callback_queue_tail == node) {
			ipcon->callback_queue_head = NULL;
			ipcon->callback_queue_tail = NULL;
		}

		ipcon_mutex_unlock(&ipcon->callback_queue_mutex);

		uint8_t function_id = ipcon_get_function_id_from_data(node->buffer);
		if (function_id == FUNCTION_ENUMERATE_CALLBACK) {
			EnumerateReturn *er = (EnumerateReturn *)node->buffer;
			char str_uid[MAX_BASE58_STR_SIZE];
			ipcon_base58encode(er->device_uid, str_uid);

			if (ipcon->enumerate_callback != NULL) {
				ipcon->enumerate_callback(str_uid,
				                          er->device_name,
				                          er->device_stack_id,
				                          er->is_new);
			}
		} else {
			uint8_t stack_id = ipcon_get_stack_id_from_data(node->buffer);
			Device *device = ipcon->devices[stack_id];

			device->device_callbacks[function_id](device, node->buffer);
		}

		free(node);
	}
	THREAD_RETURN;
}

void ipcon_destroy(IPConnection *ipcon) {
	ipcon->recv_loop_flag = false;

	ipcon_semaphore_release(ipcon->callback_queue_semaphore);

#ifdef _WIN32
	shutdown(ipcon->s, 2);
	closesocket(ipcon->s);
#else
	shutdown(ipcon->fd, 2);
	close(ipcon->fd);
#endif

	ipcon_mutex_lock(&ipcon->callback_queue_mutex);

	CallbackQueueNode *node = ipcon->callback_queue_head;

	while (node != NULL) {
		CallbackQueueNode *next = node->next;

		free(node);
		node = next;
	}

	ipcon->callback_queue_head = NULL;
	ipcon->callback_queue_tail = NULL;

	ipcon_mutex_unlock(&ipcon->callback_queue_mutex);
}

void ipcon_join_thread(IPConnection *ipcon) {
#ifdef _WIN32
	WaitForSingleObject(ipcon->handle_recv_loop, INFINITE);
	WaitForSingleObject(ipcon->handle_callback_loop, INFINITE);
#else
	pthread_join(ipcon->thread_recv_loop, NULL);
	pthread_join(ipcon->thread_callback_loop, NULL);
#endif
}

void ipcon_enumerate(IPConnection *ipcon, enumerate_callback_func_t cb) {
	ipcon->enumerate_callback = cb;

	Enumerate e = {
		BROADCAST_ADDRESS,
		FUNCTION_ENUMERATE,
		sizeof(Enumerate)
	};

#ifdef _WIN32
	send(ipcon->s, (const char*)&e, sizeof(Enumerate), 0);
#else
	write(ipcon->fd, &e, sizeof(Enumerate));
#endif
}

static void ipcon_callback_queue_enqueue(IPConnection *ipcon, const unsigned char *buffer) {
	uint16_t length = ipcon_get_length_from_data(buffer);
	CallbackQueueNode *node = (CallbackQueueNode *)malloc(offsetof(CallbackQueueNode, buffer) + length);

	node->next = NULL;
	memcpy(node->buffer, buffer, length);

	ipcon_mutex_lock(&ipcon->callback_queue_mutex);

	if (ipcon->callback_queue_tail == NULL) {
		ipcon->callback_queue_head = node;
		ipcon->callback_queue_tail = node;
	} else {
		ipcon->callback_queue_tail->next = node;
		ipcon->callback_queue_tail = node;
	}

	ipcon_mutex_unlock(&ipcon->callback_queue_mutex);
	ipcon_semaphore_release(ipcon->callback_queue_semaphore);
}

int ipcon_handle_enumerate(IPConnection *ipcon, const unsigned char *buffer) {
	uint16_t length = ipcon_get_length_from_data(buffer);

	if(ipcon->enumerate_callback == NULL) {
		return length;
	}

	ipcon_callback_queue_enqueue(ipcon, buffer);

	return length;
}

int ipcon_handle_message(IPConnection *ipcon, const unsigned char *buffer) {
	uint8_t function_id = ipcon_get_function_id_from_data(buffer);
	if(function_id == FUNCTION_GET_STACK_ID) {
		return ipcon_add_device_handler(ipcon, buffer);
	} else if(function_id == FUNCTION_ENUMERATE_CALLBACK) {
		return ipcon_handle_enumerate(ipcon, buffer);
	}

	uint8_t stack_id = ipcon_get_stack_id_from_data(buffer);
	uint16_t length = ipcon_get_length_from_data(buffer);
	if(ipcon->devices[stack_id] == NULL) {
		// Message for an unknown device, ignoring it
		return length;
	}

	Device *device = ipcon->devices[stack_id];
	DeviceAnswer *answer = &device->answer;

	if(answer->function_id == function_id) {
		if(answer->length != length) {
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
		pthread_mutex_lock(&device->sem_answer);
		device->sem_answer_flag = true;
		pthread_cond_signal(&device->cond);
		pthread_mutex_unlock(&device->sem_answer);
#endif
		return length;
	}

	if(device->callbacks[function_id] != NULL) {
		ipcon_callback_queue_enqueue(ipcon, buffer);

		return length;
	}

	// Message seems to be OK, but can't be handled, most likely
	// a callback without registered function
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
	device->answer.function_id = 0;
	device->answer.length = 0;

#ifdef _WIN32
	InitializeCriticalSection(&device->write_mutex);
	// Default state for answer semaphore is locked
	device->sem_answer = CreateSemaphore(NULL,0,1,NULL);
#else
	pthread_mutex_init(&device->write_mutex, NULL);
	pthread_mutex_init(&device->sem_answer, NULL);
	pthread_cond_init(&device->cond, NULL);

	device->sem_answer_flag = false;
#endif
}

int ipcon_answer_sem_wait_timeout(Device *device) {
#ifdef _WIN32
	return WaitForSingleObject(device->sem_answer, TIMEOUT_ANSWER);
#else
	struct timespec ts;
	struct timeval tp;
	gettimeofday(&tp, NULL);
	ts.tv_sec  = tp.tv_sec + TIMEOUT_ANSWER / 1000;
	ts.tv_nsec = (tp.tv_usec + (TIMEOUT_ANSWER % 1000) * 1000) * 1000;
	while (ts.tv_nsec >= 1000000000) {
		ts.tv_sec  += 1;
		ts.tv_nsec -= 1000000000;
	}
	pthread_mutex_lock(&device->sem_answer);

	int ret = 0;
	while(!device->sem_answer_flag) {
		ret = pthread_cond_timedwait(&device->cond,
		                             &device->sem_answer,
		                             &ts);
		if(ret != 0) {
			break;
		}
	}
	device->sem_answer_flag = false;
	pthread_mutex_unlock(&device->sem_answer);

	return ret;
#endif
}

int ipcon_create(IPConnection *ipcon, const char *host, const int port) {
	int i;
	for(i = 0; i < MAX_NUM_DEVICES; i++) {
		ipcon->devices[i] = NULL;
	}
	ipcon->add_device = NULL;
	ipcon->enumerate_callback = NULL;
	ipcon->recv_loop_flag = true;
	ipcon->callback_queue_head = NULL;
	ipcon->callback_queue_tail = NULL;

#ifdef _WIN32
	WSADATA wsaData;

	// Initialize Winsock
	if(WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
		return E_NO_STREAM_SOCKET;
	}

	ipcon->s = socket(AF_INET, SOCK_STREAM, 0);
	if(ipcon->s == INVALID_SOCKET) {
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
	           sizeof(ipcon->server)) == SOCKET_ERROR) {
		return E_NO_CONNECT;
	}
#else
	if(connect(ipcon->fd,
	           (struct sockaddr *)&ipcon->server,
	           sizeof(ipcon->server)) < 0) {
		return E_NO_CONNECT;
	}
#endif

#ifdef _WIN32
	InitializeCriticalSection(&ipcon->callback_queue_mutex);
	ipcon->callback_queue_semaphore = CreateSemaphore(NULL, 0, INT32_MAX, NULL);
#elif defined __APPLE__
	pthread_mutex_init(&ipcon->callback_queue_mutex, NULL);

	// Mac OS does not support unnamed semaphores, so we fake them.
	// Unlink first to ensure that there is no existing semaphore with that name.
	// Then open the semaphore to create a new one. Finally unlink it again to
	// avoid leaking the name. The semaphore will just work fine without a name.
	#define SEMAPHORE_NAME "tinkerforge-ipcon-internal"
	sem_unlink(SEMAPHORE_NAME);
	ipcon->callback_queue_semaphore = sem_open(SEMAPHORE_NAME, O_CREAT | O_EXCL, S_IRUSR | S_IWUSR | S_IXUSR, 0);
	sem_unlink(SEMAPHORE_NAME);
#else
	pthread_mutex_init(&ipcon->callback_queue_mutex, NULL);
	ipcon->callback_queue_semaphore = &ipcon->callback_queue_semaphore_object;
	sem_init(ipcon->callback_queue_semaphore, 0, 0);
#endif

#ifdef _WIN32
	DWORD thread_recv_loop_id;
	ipcon->handle_recv_loop = CreateThread(NULL,
	                                       0,
	                                       (LPTHREAD_START_ROUTINE)ipcon_recv_loop,
	                                       (void*)ipcon,
	                                       0,
	                                       (LPDWORD)&thread_recv_loop_id);
	if(ipcon->handle_recv_loop == NULL) {
		return E_NO_THREAD;
	}
	DWORD thread_callback_loop_id;
	ipcon->handle_callback_loop = CreateThread(NULL,
	                                           0,
	                                           (LPTHREAD_START_ROUTINE)ipcon_callback_loop,
	                                           (void*)ipcon,
	                                           0,
	                                           (LPDWORD)&thread_callback_loop_id);
	if(ipcon->handle_callback_loop == NULL) {
		return E_NO_THREAD;
	}
#else
	if(pthread_create(&ipcon->thread_recv_loop,
	                  NULL,
	                  ipcon_recv_loop,
	                  (void*)ipcon) < 0) {
		return E_NO_THREAD;
	}
	if(pthread_create(&ipcon->thread_callback_loop,
	                  NULL,
	                  ipcon_callback_loop,
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
		const char *p = gsidr->device_name;
		const char *e = gsidr->device_name + MAX_LENGTH_NAME;

		// Search for a possible NUL-terminator
		while (p < e && *p != '\0') {
			++p;
		}

		// Go back to the previous char if there is any
		if (p >= gsidr->device_name) {
			--p;
		}

		// Go back to the last space if there is any
		while (p >= gsidr->device_name && *p != ' ') {
			--p;
		}

		// Match with expected name
		int length = p - gsidr->device_name;
		int expected_length = strlen(ipcon->add_device->expected_name);
		if (length != expected_length) {
			return sizeof(GetStackIDReturn);
		}

		int i;
		for (i = 0; i < length; i++) {
			if (gsidr->device_name[i] != ipcon->add_device->expected_name[i]) {
				if ((gsidr->device_name[i] == ' ' && ipcon->add_device->expected_name[i] == '-') ||
				    (gsidr->device_name[i] == '-' && ipcon->add_device->expected_name[i] == ' ')) {
					// Treat ' ' and '-' as equal for backward compatibility
					continue;
				} else {
					return sizeof(GetStackIDReturn);
				}
			}
		}

		ipcon->add_device->stack_id = gsidr->device_stack_id;
		strncpy(ipcon->add_device->name, gsidr->device_name, MAX_LENGTH_NAME);
		ipcon->add_device->firmware_version[0] = gsidr->device_firmware_version[0];
		ipcon->add_device->firmware_version[1] = gsidr->device_firmware_version[1];
		ipcon->add_device->firmware_version[2] = gsidr->device_firmware_version[2];
		ipcon->devices[gsidr->device_stack_id] = ipcon->add_device;

#ifdef _WIN32
		ReleaseSemaphore(ipcon->add_device->sem_answer,1,NULL);
#else
		pthread_mutex_lock(&ipcon->add_device->sem_answer);
		ipcon->add_device->sem_answer_flag = true;
		pthread_cond_signal(&ipcon->add_device->cond);
		pthread_mutex_unlock(&ipcon->add_device->sem_answer);
#endif

		ipcon->add_device = NULL;
	}

	return sizeof(GetStackIDReturn);
}

int ipcon_add_device(IPConnection *ipcon, Device *device) {
	device->ipcon = ipcon;

	GetStackID gsid = {
		BROADCAST_ADDRESS,
		FUNCTION_GET_STACK_ID,
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

	return E_OK;
}

uint8_t ipcon_get_stack_id_from_data(const unsigned char *data) {
	return data[0];
}

uint8_t ipcon_get_function_id_from_data(const unsigned char *data) {
	return data[1];
}

uint16_t ipcon_get_length_from_data(const unsigned char *data) {
	return *((uint16_t*)(data + 2));
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

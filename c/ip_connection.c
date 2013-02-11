/*
 * Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

#ifndef _WIN32
	#define _BSD_SOURCE // for usleep from unistd.h
#endif

#include <errno.h>
#include <stddef.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#ifdef _WIN32
	#include <winsock2.h>
#else
	#include <unistd.h>
	#include <sys/types.h>
	#include <sys/time.h> // gettimeofday
	#include <sys/socket.h> // connect
	#include <sys/select.h>
	#include <netinet/tcp.h> // TCP_NO_DELAY
	#include <netdb.h> // gethostbyname
	#include <netinet/in.h> // struct sockaddr_in
#endif

#define IPCON_EXPOSE_INTERNALS

#include "ip_connection.h"

#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(push)
	#pragma pack(1)
	#define ATTRIBUTE_PACKED
#elif defined __GNUC__
	#define ATTRIBUTE_PACKED __attribute__((packed))
#else
	#error unknown compiler, do not know how to enable struct packing
#endif

typedef struct {
	PacketHeader header;
} ATTRIBUTE_PACKED Enumerate;

typedef struct {
	PacketHeader header;
	char uid[8];
	char connected_uid[8];
	char position;
	uint8_t hardware_version[3];
	uint8_t firmware_version[3];
	uint16_t device_identifier;
	uint8_t enumeration_type;
} ATTRIBUTE_PACKED EnumerateCallback;

#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(pop)
#endif
#undef ATTRIBUTE_PACKED

/*****************************************************************************
 *
 *                                 BASE58
 *
 *****************************************************************************/

#define BASE58_MAX_STR_SIZE 13

static const char BASE58_ALPHABET[] = \
	"123456789abcdefghijkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ";

#if 0
static void base58_encode(uint64_t value, char *str) {
	uint32_t mod;
	char reverse_str[BASE58_MAX_STR_SIZE] = {'\0'};
	int i = 0;
	int k = 0;

	while (value >= 58) {
		mod = value % 58;
		reverse_str[i] = BASE58_ALPHABET[mod];
		value = value / 58;
		++i;
	}

	reverse_str[i] = BASE58_ALPHABET[value];

	for (k = 0; k <= i; k++) {
		str[k] = reverse_str[i - k];
	}

	for (; k < BASE58_MAX_STR_SIZE; k++) {
		str[k] = '\0';
	}
}
#endif

static uint64_t base58_decode(const char *str) {
	int i;
	int k;
	uint64_t value = 0;
	uint64_t base = 1;

	for (i = 0; i < BASE58_MAX_STR_SIZE; i++) {
		if (str[i] == '\0') {
			break;
		}
	}

	--i;

	for (; i >= 0; i--) {
		if (str[i] == '\0') {
			continue;
		}

		for (k = 0; k < 58; k++) {
			if (BASE58_ALPHABET[k] == str[i]) {
				break;
			}
		}

		value += k * base;
		base *= 58;
	}

	return value;
}

/*****************************************************************************
 *
 *                                 Socket
 *
 *****************************************************************************/

struct _Socket {
#ifdef _WIN32
	SOCKET handle;
#else
	int handle;
#endif
};

#ifdef _WIN32

static int socket_create(Socket *socket_, int domain, int type, int protocol) {
	BOOL flag = 1;

	socket_->handle = socket(domain, type, protocol);

	if (socket_->handle == INVALID_SOCKET) {
		return -1;
	}

	if (setsockopt(socket_->handle, IPPROTO_TCP, TCP_NODELAY,
	               (const char *)&flag, sizeof(flag)) == SOCKET_ERROR) {
		closesocket(socket_->handle);

		return -1;
	}

	return 0;
}

static void socket_destroy(Socket *socket) {
	closesocket(socket->handle);
}

static int socket_connect(Socket *socket, struct sockaddr_in *address, int length) {
	return connect(socket->handle, (struct sockaddr *)address, length) == SOCKET_ERROR ? -1 : 0;
}

static void socket_shutdown(Socket *socket) {
	shutdown(socket->handle, SD_BOTH);
}

static int socket_receive(Socket *socket, void *buffer, int length) {
	length = recv(socket->handle, (char *)buffer, length, 0);

	if (length == SOCKET_ERROR) {
		length = -1;

		if (WSAGetLastError() == WSAEINTR) {
			errno = EINTR;
		} else {
			errno = EFAULT;
		}
	}

	return length;
}

static int socket_send(Socket *socket, void *buffer, int length) {
	length = send(socket->handle, (const char *)buffer, length, 0);

	if (length == SOCKET_ERROR) {
		length = -1;
	}

	return length;
}

#else

static int socket_create(Socket *socket_, int domain, int type, int protocol) {
	int flag = 1;

	socket_->handle = socket(domain, type, protocol);

	if (socket_->handle < 0) {
		return -1;
	}

	if (setsockopt(socket_->handle, IPPROTO_TCP, TCP_NODELAY, (void *)&flag,
	               sizeof(flag)) < 0) {
		close(socket_->handle);

		return -1;
	}

	return 0;
}

static void socket_destroy(Socket *socket) {
	close(socket->handle);
}

static int socket_connect(Socket *socket, struct sockaddr_in *address, int length) {
	return connect(socket->handle, (struct sockaddr *)address, length);
}

static void socket_shutdown(Socket *socket) {
	shutdown(socket->handle, SHUT_RDWR);
}

static int socket_receive(Socket *socket, void *buffer, int length) {
	return recv(socket->handle, buffer, length, 0);
}

static int socket_send(Socket *socket, void *buffer, int length) {
	return send(socket->handle, buffer, length, 0);
}

#endif

/*****************************************************************************
 *
 *                                 Mutex
 *
 *****************************************************************************/

#ifdef _WIN32

static void mutex_create(Mutex *mutex) {
	InitializeCriticalSection(&mutex->handle);
}

static void mutex_destroy(Mutex *mutex) {
	DeleteCriticalSection(&mutex->handle);
}

void mutex_lock(Mutex *mutex) {
	EnterCriticalSection(&mutex->handle);
}

void mutex_unlock(Mutex *mutex) {
	LeaveCriticalSection(&mutex->handle);
}

#else

static void mutex_create(Mutex *mutex) {
	pthread_mutex_init(&mutex->handle, NULL);
}

static void mutex_destroy(Mutex *mutex) {
	pthread_mutex_destroy(&mutex->handle);
}

void mutex_lock(Mutex *mutex) {
	pthread_mutex_lock(&mutex->handle);
}

void mutex_unlock(Mutex *mutex) {
	pthread_mutex_unlock(&mutex->handle);
}
#endif

/*****************************************************************************
 *
 *                                 Event
 *
 *****************************************************************************/

#ifdef _WIN32

static void event_create(Event *event) {
	event->handle = CreateEvent(NULL, TRUE, FALSE, NULL);
}

static void event_destroy(Event *event) {
	CloseHandle(event->handle);
}

static void event_set(Event *event) {
	SetEvent(event->handle);
}

static void event_reset(Event *event) {
	ResetEvent(event->handle);
}

static int event_wait(Event *event, uint32_t timeout) { // in msec
	return WaitForSingleObject(event->handle, timeout) == WAIT_OBJECT_0 ? 0 : -1;
}

#else

static void event_create(Event *event) {
	pthread_mutex_init(&event->mutex, NULL);
	pthread_cond_init(&event->condition, NULL);

	event->flag = false;
}

static void event_destroy(Event *event) {
	pthread_mutex_destroy(&event->mutex);
	pthread_cond_destroy(&event->condition);
}

static void event_set(Event *event) {
	pthread_mutex_lock(&event->mutex);

	event->flag = true;

	pthread_cond_signal(&event->condition);
	pthread_mutex_unlock(&event->mutex);
}

static void event_reset(Event *event) {
	pthread_mutex_lock(&event->mutex);

	event->flag = false;

	pthread_mutex_unlock(&event->mutex);
}

static int event_wait(Event *event, uint32_t timeout) { // in msec
	struct timeval tp;
	struct timespec ts;
	int ret = 0;

	gettimeofday(&tp, NULL);

	ts.tv_sec = tp.tv_sec + timeout / 1000;
	ts.tv_nsec = (tp.tv_usec + (timeout % 1000) * 1000) * 1000;

	while (ts.tv_nsec >= 1000000000L) {
		ts.tv_sec += 1;
		ts.tv_nsec -= 1000000000L;
	}

	pthread_mutex_lock(&event->mutex);

	while (!event->flag) {
		ret = pthread_cond_timedwait(&event->condition, &event->mutex, &ts);

		if (ret != 0) {
			ret = -1;
			break;
		}
	}

	pthread_mutex_unlock(&event->mutex);

	return ret;
}

#endif

/*****************************************************************************
 *
 *                                 Semaphore
 *
 *****************************************************************************/

#ifdef _WIN32

static int semaphore_create(Semaphore *semaphore) {
	semaphore->handle = CreateSemaphore(NULL, 0, INT32_MAX, NULL);

	return semaphore->handle == NULL ? -1 : 0;
}

static void semaphore_destroy(Semaphore *semaphore) {
	CloseHandle(semaphore->handle);
}

static int semaphore_acquire(Semaphore *semaphore) {
	return WaitForSingleObject(semaphore->handle, INFINITE) != WAIT_OBJECT_0 ? -1 : 0;
}

static void semaphore_release(Semaphore *semaphore) {
	ReleaseSemaphore(semaphore->handle, 1, NULL);
}

#else

static int semaphore_create(Semaphore *semaphore) {
#ifdef __APPLE__
	// Mac OS X does not support unnamed semaphores, so we fake them. Unlink
	// first to ensure that there is no existing semaphore with that name.
	// Then open the semaphore to create a new one. Finally unlink it again to
	// avoid leaking the name. The semaphore will work fine without a name.
	char name[100];

	snprintf(name, sizeof(name), "tf-ipcon-%p", semaphore);

	sem_unlink(name);
	semaphore->pointer = sem_open(name, O_CREAT | O_EXCL, S_IRWXU, 0);
	sem_unlink(name);

	if (semaphore->pointer == SEM_FAILED) {
		return -1;
	}
#else
	semaphore->pointer = &semaphore->object;

	if (sem_init(semaphore->pointer, 0, 0) < 0) {
		return -1;
	}
#endif

	return 0;
}

static void semaphore_destroy(Semaphore *semaphore) {
#ifdef __APPLE__
	sem_close(semaphore->pointer);
#else
	sem_destroy(semaphore->pointer);
#endif
}

static int semaphore_acquire(Semaphore *semaphore) {
	return sem_wait(semaphore->pointer) < 0 ? -1 : 0;
}

static void semaphore_release(Semaphore *semaphore) {
	sem_post(semaphore->pointer);
}

#endif

/*****************************************************************************
 *
 *                                 Thread
 *
 *****************************************************************************/

#ifdef _WIN32

static DWORD WINAPI thread_wrapper(void *opaque) {
	Thread *thread = (Thread *)opaque;

	thread->function(thread->opaque);

	return 0;
}

static int thread_create(Thread *thread, ThreadFunction function, void *opaque) {
	thread->function = function;
	thread->opaque = opaque;

	thread->handle = CreateThread(NULL, 0, thread_wrapper, thread, 0, &thread->id);

	return thread->handle == NULL ? -1 : 0;
}

static void thread_destroy(Thread *thread) {
	CloseHandle(thread->handle);
}

static bool thread_is_current(Thread *thread) {
	return thread->id == GetCurrentThreadId();
}

static void thread_join(Thread *thread) {
	WaitForSingleObject(thread->handle, INFINITE);
}

static void thread_sleep(int msec) {
	Sleep(msec);
}

#else

static void *thread_wrapper(void *opaque) {
	Thread *thread = (Thread *)opaque;

	thread->function(thread->opaque);

	return NULL;
}

static int thread_create(Thread *thread, ThreadFunction function, void *opaque) {
	thread->function = function;
	thread->opaque = opaque;

	return pthread_create(&thread->handle, NULL, thread_wrapper, thread);
}

static void thread_destroy(Thread *thread) {
	(void)thread;
}

static bool thread_is_current(Thread *thread) {
	return pthread_equal(thread->handle, pthread_self()) ? true : false;
}

static void thread_join(Thread *thread) {
	pthread_join(thread->handle, NULL);
}

static void thread_sleep(int msec) {
	usleep(msec * 1000);
}

#endif

/*****************************************************************************
 *
 *                                 Table
 *
 *****************************************************************************/

static void table_create(Table *table) {
	mutex_create(&table->mutex);

	table->used = 0;
	table->allocated = 16;
	table->keys = (uint32_t *)malloc(sizeof(uint32_t) * table->allocated);
	table->values = (void **)malloc(sizeof(void *) * table->allocated);
}

static void table_destroy(Table *table) {
	free(table->keys);
	free(table->values);

	mutex_destroy(&table->mutex);
}

static void table_insert(Table *table, uint32_t key, void *value) {
	int i;

	mutex_lock(&table->mutex);

	for (i = 0; i < table->used; ++i) {
		if (table->keys[i] == key) {
			table->values[i] = value;

			mutex_unlock(&table->mutex);

			return;
		}
	}

	if (table->allocated <= table->used) {
		table->allocated += 16;
		table->keys = (uint32_t *)realloc(table->keys, sizeof(uint32_t) * table->allocated);
		table->values = (void **)realloc(table->values, sizeof(void *) * table->allocated);
	}

	table->keys[table->used] = key;
	table->values[table->used] = value;

	++table->used;

	mutex_unlock(&table->mutex);
}

static void table_remove(Table *table, uint32_t key) {
	int i;
	int tail;

	mutex_lock(&table->mutex);

	for (i = 0; i < table->used; ++i) {
		if (table->keys[i] == key) {
			tail = table->used - i - 1;

			if (tail > 0) {
				memmove(table->keys + i, table->keys + i + 1, sizeof(uint32_t) * tail);
				memmove(table->values + i, table->values + i + 1, sizeof(void *) * tail);
			}

			--table->used;

			break;
		}
	}

	mutex_unlock(&table->mutex);
}

static void *table_get(Table *table, uint32_t key) {
	int i;
	void *value = NULL;

	mutex_lock(&table->mutex);

	for (i = 0; i < table->used; ++i) {
		if (table->keys[i] == key) {
			value = table->values[i];

			break;
		}
	}

	mutex_unlock(&table->mutex);

	return value;
}

/*****************************************************************************
 *
 *                                 Queue
 *
 *****************************************************************************/

enum {
	QUEUE_KIND_EXIT = 0,
	QUEUE_KIND_META,
	QUEUE_KIND_PACKET
};

typedef struct {
	uint8_t id;
	uint8_t parameter;
} Meta;

static void queue_create(Queue *queue) {
	queue->head = NULL;
	queue->tail = NULL;

	mutex_create(&queue->mutex);
	semaphore_create(&queue->semaphore);
}

static void queue_destroy(Queue *queue) {
	QueueItem *item = queue->head;
	QueueItem *next;

	while (item != NULL) {
		next = item->next;

		free(item->data);
		free(item);

		item = next;
	}

	mutex_destroy(&queue->mutex);
	semaphore_destroy(&queue->semaphore);
}

static void queue_put(Queue *queue, int kind, void *data, int length) {
	QueueItem *item = (QueueItem *)malloc(sizeof(QueueItem));

	item->next = NULL;
	item->kind = kind;
	item->data = NULL;
	item->length = length;

	if (data != NULL) {
		item->data = malloc(length);
		memcpy(item->data, data, length);
	}

	mutex_lock(&queue->mutex);

	if (queue->tail == NULL) {
		queue->head = item;
		queue->tail = item;
	} else {
		queue->tail->next = item;
		queue->tail = item;
	}

	mutex_unlock(&queue->mutex);
	semaphore_release(&queue->semaphore);
}

static int queue_get(Queue *queue, int *kind, void **data, int *length) {
	QueueItem *item;

	if (semaphore_acquire(&queue->semaphore) < 0) {
		return -1;
	}

	mutex_lock(&queue->mutex);

	if (queue->head == NULL) {
		mutex_unlock(&queue->mutex);

		return -1;
	}

	item = queue->head;
	queue->head = item->next;
	item->next = NULL;

	if (queue->tail == item) {
		queue->head = NULL;
		queue->tail = NULL;
	}

	mutex_unlock(&queue->mutex);

	*kind = item->kind;
	*data = item->data;
	*length = item->length;

	free(item);

	return 0;
}

/*****************************************************************************
 *
 *                                 Device
 *
 *****************************************************************************/

enum {
	IPCON_FUNCTION_ENUMERATE = 254
};

static int ipcon_send_request(IPConnection *ipcon, Packet *request);

void device_create(Device *device, const char *uid_str, IPConnection *ipcon,
                   uint8_t api_version_major, uint8_t api_version_minor,
                   uint8_t api_version_release) {
	uint64_t uid;
	uint32_t value1;
	uint32_t value2;
	int i;

	uid = base58_decode(uid_str);

	if (uid > 0xFFFFFFFF) {
		// convert from 64bit to 32bit
		value1 = uid & 0xFFFFFFFF;
		value2 = (uid >> 32) & 0xFFFFFFFF;

		uid  = (value1 & 0x00000FFF);
		uid |= (value1 & 0x0F000000) >> 12;
		uid |= (value2 & 0x0000003F) << 16;
		uid |= (value2 & 0x000F0000) << 6;
		uid |= (value2 & 0x3F000000) << 2;
	}

	device->uid = uid & 0xFFFFFFFF;

	device->ipcon = ipcon;

	device->api_version[0] = api_version_major;
	device->api_version[1] = api_version_minor;
	device->api_version[2] = api_version_release;

	// request
	mutex_create(&device->request_mutex);

	// response
	device->expected_response_function_id = 0;
	device->expected_response_sequence_number = 0;

	memset(&device->response_packet, 0, sizeof(Packet));

	event_create(&device->response_event);

	for (i = 0; i < DEVICE_NUM_FUNCTION_IDS; i++) {
		device->response_expected[i] = DEVICE_RESPONSE_EXPECTED_INVALID_FUNCTION_ID;
	}

	device->response_expected[IPCON_FUNCTION_ENUMERATE] = DEVICE_RESPONSE_EXPECTED_FALSE;
	device->response_expected[IPCON_CALLBACK_ENUMERATE] = DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE;

	// callbacks
	for (i = 0; i < DEVICE_NUM_FUNCTION_IDS; i++) {
		device->registered_callbacks[i] = NULL;
		device->registered_callback_user_data[i] = NULL;
		device->callback_wrappers[i] = NULL;
	}

	// add to IPConnection
	table_insert(&ipcon->devices, device->uid, device);
}

void device_destroy(Device *device) {
	table_remove(&device->ipcon->devices, device->uid);

	event_destroy(&device->response_event);

	mutex_destroy(&device->request_mutex);
}

int device_get_response_expected(Device *device, uint8_t function_id,
                                 bool *ret_response_expected) {
	if (device->response_expected[function_id] == DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE ||
	    device->response_expected[function_id] == DEVICE_RESPONSE_EXPECTED_TRUE) {
		*ret_response_expected = true;
	} else if (device->response_expected[function_id] == DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE ||
	           device->response_expected[function_id] == DEVICE_RESPONSE_EXPECTED_FALSE) {
		*ret_response_expected = false;
	} else {
		return E_INVALID_PARAMETER;
	}

	return E_OK;
}

int device_set_response_expected(Device *device, uint8_t function_id, bool response_expected) {
	if (device->response_expected[function_id] != DEVICE_RESPONSE_EXPECTED_TRUE &&
	    device->response_expected[function_id] != DEVICE_RESPONSE_EXPECTED_FALSE) {
		return E_INVALID_PARAMETER;
	}

	device->response_expected[function_id] = response_expected ? DEVICE_RESPONSE_EXPECTED_TRUE
	                                                           : DEVICE_RESPONSE_EXPECTED_FALSE;

	return E_OK;
}

int device_set_response_expected_all(Device *device, bool response_expected) {
	int flag = response_expected ? DEVICE_RESPONSE_EXPECTED_TRUE : DEVICE_RESPONSE_EXPECTED_FALSE;
	int i;

	for (i = 0; i < DEVICE_NUM_FUNCTION_IDS; ++i) {
		if (device->response_expected[i] == DEVICE_RESPONSE_EXPECTED_TRUE ||
		    device->response_expected[i] == DEVICE_RESPONSE_EXPECTED_FALSE) {
			device->response_expected[i] = flag;
		}
	}

	return E_OK;
}

void device_register_callback(Device *device, uint8_t id, void *callback,
                              void *user_data) {
	device->registered_callbacks[id] = callback;
	device->registered_callback_user_data[id] = user_data;
}

int device_get_api_version(Device *device, uint8_t ret_api_version[3]) {
	ret_api_version[0] = device->api_version[0];
	ret_api_version[1] = device->api_version[1];
	ret_api_version[2] = device->api_version[2];

	return E_OK;
}

int device_send_request(Device *device, Packet *request, Packet *response) {
	int ret = E_OK;

	if (request->header.response_expected) {
		mutex_lock(&device->request_mutex);

		event_reset(&device->response_event);

		device->expected_response_function_id = request->header.function_id;
		device->expected_response_sequence_number = request->header.sequence_number;
	}

	ret = ipcon_send_request(device->ipcon, request);

	if (ret != E_OK) {
		if (request->header.response_expected) {
			mutex_unlock(&device->request_mutex);
		}

		return ret;
	}

	if (request->header.response_expected) {
		if (event_wait(&device->response_event, device->ipcon->timeout) < 0) {
			ret = E_TIMEOUT;
		}

		device->expected_response_function_id = 0;
		device->expected_response_sequence_number = 0;

		event_reset(&device->response_event);

		if (ret == E_OK) {
			if (device->response_packet.header.error_code == 0) {
				// no error
				if (response != NULL) {
					memcpy(response, &device->response_packet,
					       device->response_packet.header.length);
				}
			} else if (device->response_packet.header.error_code == 1) {
				ret = E_INVALID_PARAMETER;
			} else if (device->response_packet.header.error_code == 2) {
				ret = E_NOT_SUPPORTED;
			} else {
				ret = E_UNKNOWN_ERROR_CODE;
			}
		}

		mutex_unlock(&device->request_mutex);
	}

	return ret;
}

/*****************************************************************************
 *
 *                                 IPConnection
 *
 *****************************************************************************/

typedef struct {
	IPConnection *ipcon;
	Queue *queue;
	Thread *thread;
} CallbackContext;

typedef int (*CallbackWrapperFunction)(Device *device, Packet *packet);

static int ipcon_connect_unlocked(IPConnection *ipcon, bool is_auto_reconnect);

static void ipcon_dispatch_meta(IPConnection *ipcon, Meta *meta) {
	ConnectedCallbackFunction connected_callback_function;
	DisconnectedCallbackFunction disconnected_callback_function;
	void *user_data;
	bool retry;

	if (meta->id == IPCON_CALLBACK_CONNECTED) {
		if (ipcon->registered_callbacks[IPCON_CALLBACK_CONNECTED] != NULL) {
			connected_callback_function = (ConnectedCallbackFunction)ipcon->registered_callbacks[IPCON_CALLBACK_CONNECTED];
			user_data = ipcon->registered_callback_user_data[IPCON_CALLBACK_CONNECTED];

			connected_callback_function(meta->parameter, user_data);
		}
	} else if (meta->id == IPCON_CALLBACK_DISCONNECTED) {
		// need to do this here, the receive loop is not allowed to
		// hold the socket mutex because this could cause a deadlock
		// with a concurrent call to the (dis-)connect function
		mutex_lock(&ipcon->socket_mutex);

		if (ipcon->socket != NULL) {
			socket_destroy(ipcon->socket);
			free(ipcon->socket);
			ipcon->socket = NULL;
		}

		mutex_unlock(&ipcon->socket_mutex);

		// FIXME: wait a moment here, otherwise the next connect
		// attempt will succeed, even if there is no open server
		// socket. the first receive will then fail directly
		thread_sleep(100);

		if (ipcon->registered_callbacks[IPCON_CALLBACK_DISCONNECTED] != NULL) {
			disconnected_callback_function = (DisconnectedCallbackFunction)ipcon->registered_callbacks[IPCON_CALLBACK_DISCONNECTED];
			user_data = ipcon->registered_callback_user_data[IPCON_CALLBACK_DISCONNECTED];

			disconnected_callback_function(meta->parameter, user_data);
		}

		if (meta->parameter != IPCON_DISCONNECT_REASON_REQUEST &&
			ipcon->auto_reconnect && ipcon->auto_reconnect_allowed) {
			ipcon->auto_reconnect_pending = true;
			retry = true;

			// block here until reconnect. this is okay, there is no
			// callback to deliver when there is no connection
			while (retry) {
				retry = false;

				mutex_lock(&ipcon->socket_mutex);

				if (ipcon->auto_reconnect_allowed && ipcon->socket == NULL) {
					if (ipcon_connect_unlocked(ipcon, true) < 0) {
						retry = true;
					}
				} else {
					ipcon->auto_reconnect_pending = false;
				}

				mutex_unlock(&ipcon->socket_mutex);

				if (retry) {
					// wait a moment to give another thread a chance to
					// interrupt the auto-reconnect
					thread_sleep(100);
				}
			}
		}
	}
}

static void ipcon_dispatch_packet(IPConnection *ipcon, Packet *packet) {
	EnumerateCallbackFunction enumerate_callback_function;
	void *user_data;
	EnumerateCallback *enumerate_callback;
	Device *device;
	CallbackWrapperFunction callback_wrapper_function;

	if (packet->header.function_id == IPCON_CALLBACK_ENUMERATE) {
		if (ipcon->registered_callbacks[IPCON_CALLBACK_ENUMERATE] != NULL) {
			enumerate_callback_function = (EnumerateCallbackFunction)ipcon->registered_callbacks[IPCON_CALLBACK_ENUMERATE];
			user_data = ipcon->registered_callback_user_data[IPCON_CALLBACK_ENUMERATE];
			enumerate_callback = (EnumerateCallback *)packet;

			enumerate_callback_function(enumerate_callback->uid,
			                            enumerate_callback->connected_uid,
			                            enumerate_callback->position,
			                            enumerate_callback->hardware_version,
			                            enumerate_callback->firmware_version,
			                            leconvert_uint16_from(enumerate_callback->device_identifier),
			                            enumerate_callback->enumeration_type,
			                            user_data);
		}
	} else {
		device = (Device *)table_get(&ipcon->devices, packet->header.uid);

		if (device == NULL) {
			return;
		}

		callback_wrapper_function = (CallbackWrapperFunction)device->callback_wrappers[packet->header.function_id];

		if (callback_wrapper_function == NULL) {
			return;
		}

		callback_wrapper_function(device, packet);
	}
}

static void ipcon_callback_loop(void *opaque) {
	CallbackContext *context = (CallbackContext *)opaque;
	int kind;
	void *data;
	int length;

	while (1) {
		if (queue_get(context->queue, &kind, &data, &length) < 0) {
			// FIXME: what to do here? try again? exit?
			break;
		}

		if (kind == QUEUE_KIND_EXIT) {
			break;
		} else if (kind == QUEUE_KIND_META) {
			ipcon_dispatch_meta(context->ipcon, (Meta *)data);
		} else if (kind == QUEUE_KIND_PACKET) {
			// don't dispatch callbacks when the receive thread isn't running
			if (context->ipcon->receive_flag) {
				ipcon_dispatch_packet(context->ipcon, (Packet *)data);
			}
		}

		free(data);
	}

	// cleanup
	queue_destroy(context->queue);
	free(context->queue);

	thread_destroy(context->thread);
	free(context->thread);

	free(context);
}

static void ipcon_handle_response(IPConnection *ipcon, Packet *response) {
	Device *device;

	response->header.uid = leconvert_uint32_from(response->header.uid);

	if (response->header.sequence_number == 0 &&
	    response->header.function_id == IPCON_CALLBACK_ENUMERATE) {
		if (ipcon->registered_callbacks[IPCON_CALLBACK_ENUMERATE] != NULL) {
			queue_put(ipcon->callback_queue, QUEUE_KIND_PACKET, response,
			          response->header.length);
		}

		return;
	}

	device = (Device *)table_get(&ipcon->devices, response->header.uid);

	if (device == NULL) {
		// ignoring response for an unknown device
		return;
	}

	if (response->header.sequence_number == 0) {
		if (device->registered_callbacks[response->header.function_id] != NULL) {
			queue_put(ipcon->callback_queue, QUEUE_KIND_PACKET, response,
			          response->header.length);
		}

		return;
	}

	if (device->expected_response_function_id == response->header.function_id &&
	    device->expected_response_sequence_number == response->header.sequence_number) {
		memcpy(&device->response_packet, response, response->header.length);
		event_set(&device->response_event);
		return;
	}

	// response seems to be OK, but can't be handled, most likely
	// a callback without registered function
}

static void ipcon_receive_loop(void *opaque) {
	IPConnection *ipcon = (IPConnection *)opaque;
	uint8_t pending_data[sizeof(Packet) * 10] = { 0 };
	int pending_length = 0;
	int length;
	Meta meta;

	while (ipcon->receive_flag) {
		length = socket_receive(ipcon->socket, pending_data + pending_length,
		                        sizeof(pending_data) - pending_length);

		if (!ipcon->receive_flag) {
			return;
		}

		if (length <= 0) {
			if (length < 0 && errno == EINTR) {
				continue;
			}

			ipcon->auto_reconnect_allowed = true;
			ipcon->receive_flag = false;

			meta.id = IPCON_CALLBACK_DISCONNECTED;
			meta.parameter = length == 0 ? IPCON_DISCONNECT_REASON_SHUTDOWN
			                             : IPCON_DISCONNECT_REASON_ERROR;

			queue_put(ipcon->callback_queue, QUEUE_KIND_META, &meta, sizeof(meta));
			return;
		}

		pending_length += length;

		while (1) {
			if (pending_length < 8) {
				// wait for complete header
				break;
			}

			length = ((PacketHeader *)pending_data)->length;

			if (pending_length < length) {
				// wait for complete packet
				break;
			}

			ipcon_handle_response(ipcon, (Packet *)pending_data);

			memmove(pending_data, pending_data + length, pending_length - length);
			pending_length -= length;
		}
	}
}

// NOTE: assumes that socket_mutex is locked
static int ipcon_connect_unlocked(IPConnection *ipcon, bool is_auto_reconnect) {
	CallbackContext *context;
	struct hostent *entity;
	struct sockaddr_in address;
	uint8_t connect_reason;
	Meta meta;

	// create callback queue and thread
	if (ipcon->callback_thread == NULL) {
		ipcon->callback_queue = (Queue *)malloc(sizeof(Queue));
		ipcon->callback_thread = (Thread *)malloc(sizeof(Thread));

		queue_create(ipcon->callback_queue);

		context = (CallbackContext *)malloc(sizeof(CallbackContext));

		context->ipcon = ipcon;
		context->queue = ipcon->callback_queue;
		context->thread = ipcon->callback_thread;

		if (thread_create(ipcon->callback_thread, ipcon_callback_loop, context) < 0) {
			free(context);

			queue_destroy(ipcon->callback_queue);
			free(ipcon->callback_queue);
			ipcon->callback_queue = NULL;

			free(ipcon->callback_thread);
			ipcon->callback_thread = NULL;

			return E_NO_THREAD;
		}
	}

	// create and connect socket
	entity = gethostbyname(ipcon->host);

	if (entity == NULL) {
		return E_HOSTNAME_INVALID;
	}

	memset(&address, 0, sizeof(struct sockaddr_in));
	memcpy(&address.sin_addr, entity->h_addr_list[0], entity->h_length);

	address.sin_family = AF_INET;
	address.sin_port = htons(ipcon->port);

	ipcon->socket = (Socket *)malloc(sizeof(Socket));

	if (socket_create(ipcon->socket, AF_INET, SOCK_STREAM, 0) < 0) {
		free(ipcon->socket);
		ipcon->socket = NULL;

		return E_NO_STREAM_SOCKET;
	}

	if (socket_connect(ipcon->socket, &address, sizeof(address)) < 0) {
		socket_destroy(ipcon->socket);

		free(ipcon->socket);
		ipcon->socket = NULL;

		return E_NO_CONNECT;
	}

	// create receive thread
	ipcon->receive_flag = true;
	ipcon->receive_thread = (Thread *)malloc(sizeof(Thread));

	if (thread_create(ipcon->receive_thread, ipcon_receive_loop, ipcon) < 0) {
		ipcon->receive_flag = false;

		free(ipcon->receive_thread);
		ipcon->receive_thread = NULL;

		socket_destroy(ipcon->socket);

		free(ipcon->socket);
		ipcon->socket = NULL;

		if (!is_auto_reconnect) {
			queue_put(ipcon->callback_queue, QUEUE_KIND_EXIT, NULL, 0);

			if (!thread_is_current(ipcon->callback_thread)) {
				thread_join(ipcon->callback_thread);
			}

			queue_destroy(ipcon->callback_queue);
			free(ipcon->callback_queue);
			ipcon->callback_queue = NULL;

			thread_destroy(ipcon->callback_thread);
			free(ipcon->callback_thread);
			ipcon->callback_thread = NULL;
		}

		return E_NO_THREAD;
	}

	ipcon->auto_reconnect_allowed = false;
	ipcon->auto_reconnect_pending = false;

	// trigger connected callback
	if (is_auto_reconnect) {
		connect_reason = IPCON_CONNECT_REASON_AUTO_RECONNECT;
	} else {
		connect_reason = IPCON_CONNECT_REASON_REQUEST;
	}

	meta.id = IPCON_CALLBACK_CONNECTED;
	meta.parameter = connect_reason;

	queue_put(ipcon->callback_queue, QUEUE_KIND_META, &meta, sizeof(meta));

	return E_OK;
}

static int ipcon_send_request(IPConnection *ipcon, Packet *request) {
	mutex_lock(&ipcon->socket_mutex);

	if (ipcon->socket == NULL) {
		mutex_unlock(&ipcon->socket_mutex);

		return E_NOT_CONNECTED;
	}

	socket_send(ipcon->socket, request, request->header.length);

	mutex_unlock(&ipcon->socket_mutex);

	return E_OK;
}

void ipcon_create(IPConnection *ipcon) {
	int i;

#ifdef _WIN32
	ipcon->wsa_startup_done = false;
#endif

	ipcon->host = NULL;
	ipcon->port = 0;

	ipcon->timeout = 2500;

	ipcon->auto_reconnect = true;
	ipcon->auto_reconnect_allowed = false;
	ipcon->auto_reconnect_pending = false;

	mutex_create(&ipcon->sequence_number_mutex);
	ipcon->next_sequence_number = 0;

	table_create(&ipcon->devices);

	for (i = 0; i < IPCON_NUM_CALLBACK_IDS; ++i) {
		ipcon->registered_callbacks[i] = NULL;
		ipcon->registered_callback_user_data[i] = NULL;
	}

	mutex_create(&ipcon->socket_mutex);
	ipcon->socket = NULL;

	ipcon->receive_flag = false;
	ipcon->receive_thread = NULL;

	ipcon->callback_queue = NULL;
	ipcon->callback_thread = NULL;

	semaphore_create(&ipcon->wait);
}

void ipcon_destroy(IPConnection *ipcon) {
	ipcon_disconnect(ipcon); // FIXME: disable disconnected callback before?

	mutex_destroy(&ipcon->sequence_number_mutex);

	table_destroy(&ipcon->devices);

	mutex_destroy(&ipcon->socket_mutex);

	semaphore_destroy(&ipcon->wait);

	free(ipcon->host);
}

int ipcon_connect(IPConnection *ipcon, const char *host, uint16_t port) {
	int ret;
#ifdef _WIN32
	WSADATA wsa_data;
#endif

	mutex_lock(&ipcon->socket_mutex);

#ifdef _WIN32
	if (!ipcon->wsa_startup_done) {
		if (WSAStartup(MAKEWORD(2, 2), &wsa_data) != 0) {
			mutex_unlock(&ipcon->socket_mutex);

			return E_NO_STREAM_SOCKET;
		}

		ipcon->wsa_startup_done = true;
	}
#endif

	if (ipcon->socket != NULL) {
		mutex_unlock(&ipcon->socket_mutex);

		return E_ALREADY_CONNECTED;
	}

	free(ipcon->host);

	ipcon->host = strdup(host);
	ipcon->port = port;

	ret = ipcon_connect_unlocked(ipcon, false);

	mutex_unlock(&ipcon->socket_mutex);

	return ret;
}

int ipcon_disconnect(IPConnection *ipcon) {
	Queue *callback_queue;
	Thread *callback_thread;
	Meta meta;

	mutex_lock(&ipcon->socket_mutex);

	ipcon->auto_reconnect_allowed = false;

	if (ipcon->auto_reconnect_pending) {
		// abort pending auto-reconnect
		ipcon->auto_reconnect_pending = false;
	} else {
		if (ipcon->socket == NULL) {
			mutex_unlock(&ipcon->socket_mutex);

			return E_NOT_CONNECTED;
		}

		// destroy receive thread
		ipcon->receive_flag = false;

		socket_shutdown(ipcon->socket);

		if (!thread_is_current(ipcon->receive_thread)) {
			thread_join(ipcon->receive_thread);
		}

		thread_destroy(ipcon->receive_thread);
		free(ipcon->receive_thread);
		ipcon->receive_thread = NULL;

		// destroy socket
		socket_destroy(ipcon->socket);
		free(ipcon->socket);
		ipcon->socket = NULL;
	}

	// destroy callback thread
	callback_queue = ipcon->callback_queue;
	callback_thread = ipcon->callback_thread;

	ipcon->callback_queue = NULL;
	ipcon->callback_thread = NULL;

	mutex_unlock(&ipcon->socket_mutex);

	// do this outside of socket_mutex to allow calling (dis-)connect from
	// the callbacks while blocking on the join call here
	meta.id = IPCON_CALLBACK_DISCONNECTED;
	meta.parameter = IPCON_DISCONNECT_REASON_REQUEST;

	queue_put(callback_queue, QUEUE_KIND_META, &meta, sizeof(meta));
	queue_put(callback_queue, QUEUE_KIND_EXIT, NULL, 0);

	if (!thread_is_current(callback_thread)) {
		thread_join(callback_thread);
	}

	// NOTE: no further cleanup of the callback queue and thread here, the
	// callback thread is doing this when it exits

	return E_OK;
}

int ipcon_get_connection_state(IPConnection *ipcon) {
	if (ipcon->socket != NULL) {
		return IPCON_CONNECTION_STATE_CONNECTED;
	} else if (ipcon->auto_reconnect_pending) {
		return IPCON_CONNECTION_STATE_PENDING;
	} else {
		return IPCON_CONNECTION_STATE_DISCONNECTED;
	}
}

void ipcon_set_auto_reconnect(IPConnection *ipcon, bool auto_reconnect) {
	ipcon->auto_reconnect = auto_reconnect;

	if (!ipcon->auto_reconnect) {
		// abort potentially pending auto reconnect
		ipcon->auto_reconnect_allowed = false;
	}
}

bool ipcon_get_auto_reconnect(IPConnection *ipcon) {
	return ipcon->auto_reconnect;
}

void ipcon_set_timeout(IPConnection *ipcon, uint32_t timeout) { // in msec
	ipcon->timeout = timeout;
}

uint32_t ipcon_get_timeout(IPConnection *ipcon) { // in msec
	return ipcon->timeout;
}

int ipcon_enumerate(IPConnection *ipcon) {
	Enumerate enumerate;
	int ret;

	ret = packet_header_create(&enumerate.header, sizeof(Enumerate),
	                           IPCON_FUNCTION_ENUMERATE, ipcon, NULL);

	if (ret < 0) {
		return ret;
	}

	return ipcon_send_request(ipcon, (Packet *)&enumerate);
}

void ipcon_wait(IPConnection *ipcon) {
	semaphore_acquire(&ipcon->wait);
}

void ipcon_unwait(IPConnection *ipcon) {
	semaphore_release(&ipcon->wait);
}

void ipcon_register_callback(IPConnection *ipcon, uint8_t id, void *callback,
                             void *user_data) {
	ipcon->registered_callbacks[id] = callback;
	ipcon->registered_callback_user_data[id] = user_data;
}

int packet_header_create(PacketHeader *header, uint8_t length,
                         uint8_t function_id, IPConnection *ipcon,
                         Device *device) {
	int sequence_number;
	bool response_expected = false;
	int ret = E_OK;

	mutex_lock(&ipcon->sequence_number_mutex);

	sequence_number = ipcon->next_sequence_number + 1;
	ipcon->next_sequence_number = sequence_number % 15;

	mutex_unlock(&ipcon->sequence_number_mutex);

	memset(header, 0, sizeof(PacketHeader));

	if (device != NULL) {
		header->uid = leconvert_uint32_to(device->uid);
	}

	header->length = length;
	header->function_id = function_id;
	header->sequence_number = sequence_number;

	if (device != NULL) {
		ret = device_get_response_expected(device, function_id, &response_expected);
		header->response_expected = response_expected ? 1 : 0;
	}

	return ret;
}

// undefine potential defines from /usr/include/endian.h
#undef LITTLE_ENDIAN
#undef BIG_ENDIAN

#define LITTLE_ENDIAN 0x03020100ul
#define BIG_ENDIAN    0x00010203ul

static const union {
	uint8_t bytes[4];
	uint32_t value;
} native_endian = {
	{ 0, 1, 2, 3 }
};

static void *leconvert_swap16(void *data) {
	uint8_t *s = (uint8_t *)data;
	uint8_t d[2];

	d[0] = s[1];
	d[1] = s[0];

	s[0] = d[0];
	s[1] = d[1];

	return data;
}

static void *leconvert_swap32(void *data) {
	uint8_t *s = (uint8_t *)data;
	uint8_t d[4];

	d[0] = s[3];
	d[1] = s[2];
	d[2] = s[1];
	d[3] = s[0];

	s[0] = d[0];
	s[1] = d[1];
	s[2] = d[2];
	s[3] = d[3];

	return data;
}

static void *leconvert_swap64(void *data) {
	uint8_t *s = (uint8_t *)data;
	uint8_t d[8];

	d[0] = s[7];
	d[1] = s[6];
	d[2] = s[5];
	d[3] = s[4];
	d[4] = s[3];
	d[5] = s[2];
	d[6] = s[1];
	d[7] = s[0];

	s[0] = d[0];
	s[1] = d[1];
	s[2] = d[2];
	s[3] = d[3];
	s[4] = d[4];
	s[5] = d[5];
	s[6] = d[6];
	s[7] = d[7];

	return data;
}

int16_t leconvert_int16_to(int16_t native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(int16_t *)leconvert_swap16(&native);
	}
}

uint16_t leconvert_uint16_to(uint16_t native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(uint16_t *)leconvert_swap16(&native);
	}
}

int32_t leconvert_int32_to(int32_t native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(int32_t *)leconvert_swap32(&native);
	}
}

uint32_t leconvert_uint32_to(uint32_t native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(uint32_t *)leconvert_swap32(&native);
	}
}

int64_t leconvert_int64_to(int64_t native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(int64_t *)leconvert_swap64(&native);
	}
}

uint64_t leconvert_uint64_to(uint64_t native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(uint64_t *)leconvert_swap64(&native);
	}
}

float leconvert_float_to(float native) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return native;
	} else {
		return *(float *)leconvert_swap32(&native);
	}
}

int16_t leconvert_int16_from(int16_t little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(int16_t *)leconvert_swap32(&little);
	}
}

uint16_t leconvert_uint16_from(uint16_t little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(uint16_t *)leconvert_swap32(&little);
	}
}

int32_t leconvert_int32_from(int32_t little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(int32_t *)leconvert_swap32(&little);
	}
}

uint32_t leconvert_uint32_from(uint32_t little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(uint32_t *)leconvert_swap32(&little);
	}
}

int64_t leconvert_int64_from(int64_t little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(int64_t *)leconvert_swap64(&little);
	}
}

uint64_t leconvert_uint64_from(uint64_t little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(uint64_t *)leconvert_swap64(&little);
	}
}

float leconvert_float_from(float little) {
	if (native_endian.value == LITTLE_ENDIAN) {
		return little;
	} else {
		return *(float *)leconvert_swap32(&little);
	}
}

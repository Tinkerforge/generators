/*
 * Copyright (C) 2012-2013 Matthias Bolte <matthias@tinkerforge.com>
 * Copyright (C) 2011 Olaf Lüke <olaf@tinkerforge.com>
 *
 * Redistribution and use in source and binary forms of this file,
 * with or without modification, are permitted.
 */

#ifndef IP_CONNECTION_H
#define IP_CONNECTION_H

/**
 * \defgroup IPConnection IP Connection
 */

#ifndef __STDC_LIMIT_MACROS
	#define __STDC_LIMIT_MACROS
#endif
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

#if !defined __cplusplus && defined __GNUC__
	#include <stdbool.h>
#endif

#ifdef _WIN32
	#ifndef WIN32_LEAN_AND_MEAN
		#define WIN32_LEAN_AND_MEAN
	#endif
	#include <windows.h>
#else
	#include <pthread.h>
	#include <semaphore.h>
#endif

enum {
	E_OK = 0,
	E_TIMEOUT = -1,
	E_NO_STREAM_SOCKET = -2,
	E_HOSTNAME_INVALID = -3,
	E_NO_CONNECT = -4,
	E_NO_THREAD = -5,
	E_NOT_ADDED = -6, // unused since v2.0
	E_ALREADY_CONNECTED = -7,
	E_NOT_CONNECTED = -8,
	E_INVALID_PARAMETER = -9, // error response from device
	E_NOT_SUPPORTED = -10, // error response from device
	E_UNKNOWN_ERROR_CODE = -11 // error response from device
};

typedef struct _Socket Socket;

typedef struct {
#ifdef _WIN32
	CRITICAL_SECTION handle;
#else
	pthread_mutex_t handle;
#endif
} Mutex;

#ifdef IPCON_EXPOSE_INTERNALS

void mutex_lock(Mutex *mutex);

void mutex_unlock(Mutex *mutex);

#endif

typedef struct {
#ifdef _WIN32
	HANDLE handle;
#else
	pthread_cond_t condition;
	pthread_mutex_t mutex;
	bool flag;
#endif
} Event;

typedef struct {
#ifdef _WIN32
	HANDLE handle;
#else
	sem_t object;
	sem_t *pointer;
#endif
} Semaphore;

typedef void (*ThreadFunction)(void *opaque);

typedef struct {
#ifdef _WIN32
	HANDLE handle;
	DWORD id;
#else
	pthread_t handle;
#endif
	ThreadFunction function;
	void *opaque;
} Thread;

typedef struct {
	Mutex mutex;
	int used;
	int allocated;
	uint32_t *keys;
	void **values;
} Table;

typedef struct QueueItem_ {
	struct QueueItem_ *next;
	int kind;
	void *data;
	int length;
} QueueItem;

typedef struct {
	Mutex mutex;
	Semaphore semaphore;
	QueueItem *head;
	QueueItem *tail;
} Queue;

#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(push)
	#pragma pack(1)
	#define ATTRIBUTE_PACKED
#elif defined __GNUC__
	#define ATTRIBUTE_PACKED __attribute__((packed))
#else
	#error unknown compiler, do not know how to enable struct packing
#endif

/**
 * \internal
 */
typedef struct {
	uint32_t uid;
	uint8_t length;
	uint8_t function_id;
	uint8_t other_options : 2,
	        authentication : 1,
	        response_expected : 1,
	        sequence_number : 4;
	uint8_t future_use : 6,
	        error_code : 2;
} ATTRIBUTE_PACKED PacketHeader;

/**
 * \internal
 */
typedef struct {
	PacketHeader header;
	uint8_t payload[64];
	uint8_t optional_data[8];
} ATTRIBUTE_PACKED Packet;

#if defined _MSC_VER || defined __BORLANDC__
	#pragma pack(pop)
#endif
#undef ATTRIBUTE_PACKED

typedef struct IPConnection_ IPConnection;
typedef struct Device_ Device;

typedef void (*EnumerateCallbackFunction)(const char *uid,
                                          const char *connected_uid,
                                          char position,
                                          uint8_t hardware_version[3],
                                          uint8_t firmware_version[3],
                                          uint16_t device_identifier,
                                          uint8_t enumeration_type,
                                          void *user_data);
typedef void (*ConnectedCallbackFunction)(uint8_t connect_reason,
                                          void *user_data);
typedef void (*DisconnectedCallbackFunction)(uint8_t disconnect_reason,
                                             void *user_data);

#define DEVICE_NUM_FUNCTION_IDS 256

/**
 * \internal
 */
struct Device_ {
	uint32_t uid;

	IPConnection *ipcon;

	uint8_t api_version[3];

	Mutex request_mutex;

	uint8_t expected_response_function_id;
	uint8_t expected_response_sequence_number;
	Packet response_packet;
	Event response_event;
	int response_expected[DEVICE_NUM_FUNCTION_IDS];

	void *registered_callbacks[DEVICE_NUM_FUNCTION_IDS];
	void *registered_callback_user_data[DEVICE_NUM_FUNCTION_IDS];
	void *callback_wrappers[DEVICE_NUM_FUNCTION_IDS];
};

#ifdef IPCON_EXPOSE_INTERNALS

/**
 * \internal
 */
enum {
	DEVICE_RESPONSE_EXPECTED_INVALID_FUNCTION_ID = 0,
	DEVICE_RESPONSE_EXPECTED_ALWAYS_TRUE, // getter
	DEVICE_RESPONSE_EXPECTED_ALWAYS_FALSE, // callback
	DEVICE_RESPONSE_EXPECTED_TRUE, // setter
	DEVICE_RESPONSE_EXPECTED_FALSE // setter, default
};

/**
 * \internal
 */
void device_create(Device *device, const char *uid, IPConnection *ipcon,
                   uint8_t api_version_major, uint8_t api_version_minor,
                   uint8_t api_version_release);

/**
 * \internal
 */
void device_destroy(Device *device);

/**
 * \internal
 */
int device_get_response_expected(Device *device, uint8_t function_id,
                                 bool *ret_response_expected);

/**
 * \internal
 */
int device_set_response_expected(Device *device, uint8_t function_id,
                                 bool response_expected);

/**
 * \internal
 */
int device_set_response_expected_all(Device *device, bool response_expected);

/**
 * \internal
 */
void device_register_callback(Device *device, uint8_t id, void *callback,
                              void *user_data);

/**
 * \internal
 */
int device_get_api_version(Device *device, uint8_t ret_api_version[3]);

/**
 * \internal
 */
int device_send_request(Device *device, Packet *request);

#endif

/**
 * \ingroup IPConnection
 *
 * Possible IDs for ipcon_register_callback.
 */
enum {
	IPCON_CALLBACK_ENUMERATE = 253,
	IPCON_CALLBACK_CONNECTED = 0,
	IPCON_CALLBACK_DISCONNECTED = 1
};

/**
 * \ingroup IPConnection
 *
 * Possible values for enumeration_type parameter of EnumerateCallback.
 */
enum {
	IPCON_ENUMERATION_TYPE_AVAILABLE = 0,
	IPCON_ENUMERATION_TYPE_CONNECTED = 1,
	IPCON_ENUMERATION_TYPE_DISCONNECTED = 2
};

/**
 * \ingroup IPConnection
 *
 * Possible values for connect_reason parameter of ConnectedCallback.
 */
enum {
	IPCON_CONNECT_REASON_REQUEST = 0,
	IPCON_CONNECT_REASON_AUTO_RECONNECT = 1
};

/**
 * \ingroup IPConnection
 *
 * Possible values for disconnect_reason parameter of DisconnectedCallback.
 */
enum {
	IPCON_DISCONNECT_REASON_REQUEST = 0,
	IPCON_DISCONNECT_REASON_ERROR = 1,
	IPCON_DISCONNECT_REASON_SHUTDOWN = 2
};

/**
 * \ingroup IPConnection
 *
 * Possible return values of ipcon_get_connection_state.
 */
enum {
	IPCON_CONNECTION_STATE_DISCONNECTED = 0,
	IPCON_CONNECTION_STATE_CONNECTED = 1,
	IPCON_CONNECTION_STATE_PENDING = 2 // auto-reconnect in progress
};

#define IPCON_NUM_CALLBACK_IDS 256

/**
 * \internal
 */
struct IPConnection_ {
#ifdef _WIN32
	bool wsa_startup_done;
#endif

	char *host;
	uint16_t port;

	uint32_t timeout; // in msec

	bool auto_reconnect;
	bool auto_reconnect_allowed;
	bool auto_reconnect_pending;

	Mutex sequence_number_mutex;
	int next_sequence_number;

	Table devices;

	void *registered_callbacks[IPCON_NUM_CALLBACK_IDS];
	void *registered_callback_user_data[IPCON_NUM_CALLBACK_IDS];

	Mutex socket_mutex;
	Socket *socket;

	bool receive_flag;
	Thread *receive_thread;

	Queue *callback_queue;
	Thread *callback_thread;

	Semaphore wait;
};

/**
 * \ingroup IPConnection
 *
 * Creates an IP Connection object that can be used to enumerate the available
 * devices. It is also required for the constructor of Bricks and Bricklets.
 */
void ipcon_create(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Destroys the IP Connection object. Calls ipcon_disconnect internally.
 * The connection to the Brick Daemon gets closed and the threads of the
 * IP Connection are terminated.
 */
void ipcon_destroy(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Creates a TCP/IP connection to the given \c host and c\ port. The host and
 * port can point to a Brick Daemon or to a WIFI/Ethernet Extension.
 *
 * Devices can only be controlled when the connection was established
 * successfully.
 *
 * Blocks until the connection is established and returns an error code if
 * there is no Brick Daemon or WIFI/Ethernet Extension listening at the given
 * host and port.
 */
int ipcon_connect(IPConnection *ipcon, const char *host, uint16_t port);

/**
 * \ingroup IPConnection
 *
 * Disconnects the TCP/IP connection from the Brick Daemon or the WIFI/Ethernet
 * Extension.
 */
int ipcon_disconnect(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Can return the following states:
 *
 * - IPCON_CONNECTION_STATE_DISCONNECTED: No connection is established.
 * - IPCON_CONNECTION_STATE_CONNECTED: A connection to the Brick Daemon or
 *   the WIFI/Ethernet Extension is established.
 * - IPCON_CONNECTION_STATE_PENDING: IP Connection is currently trying to
 *   connect.
 */
int ipcon_get_connection_state(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Enables or disables auto-reconnect. If auto-reconnect is enabled,
 * the IP Connection will try to reconnect to the previously given
 * host and port, if the connection is lost.
 *
 * Default value is *true*.
 */
void ipcon_set_auto_reconnect(IPConnection *ipcon, bool auto_reconnect);

/**
 * \ingroup IPConnection
 *
 * Returns *true* if auto-reconnect is enabled, *false* otherwise.
 */
bool ipcon_get_auto_reconnect(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Sets the timeout in milliseconds for getters and for setters for which the
 * response expected flag is activated.
 *
 * Default timeout is 2500.
 */
void ipcon_set_timeout(IPConnection *ipcon, uint32_t timeout);

/**
 * \ingroup IPConnection
 *
 * Returns the timeout as set by ipcon_set_timeout.
 */
uint32_t ipcon_get_timeout(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Broadcasts an enumerate request. All devices will respond with an enumerate
 * callback.
 */
int ipcon_enumerate(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Stops the current thread until ipcon_unwait is called.
 *
 * This is useful if you rely solely on callbacks for events, if you want
 * to wait for a specific callback or if the IP Connection was created in
 * a thread.
 *
 * ipcon_wait and ipcon_unwait act in the same way as "acquire" and "release"
 * of a semaphore.
 */
void ipcon_wait(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Unwaits the thread previously stopped by ipcon_wait.
 *
 * ipcon_wait and ipcon_unwait act in the same way as "acquire" and "release"
 * of a semaphore.
 */
void ipcon_unwait(IPConnection *ipcon);

/**
 * \ingroup IPConnection
 *
 * Registers a callback for a given ID.
 */
void ipcon_register_callback(IPConnection *ipcon, uint8_t id,
                             void *callback, void *user_data);

#ifdef IPCON_EXPOSE_INTERNALS

/**
 * \internal
 */
int packet_header_create(PacketHeader *header, uint8_t length,
                         uint8_t function_id, IPConnection *ipcon,
                         Device *device);

/**
 * \internal
 */
int16_t leconvert_int16_to(int16_t native);

/**
 * \internal
 */
uint16_t leconvert_uint16_to(uint16_t native);

/**
 * \internal
 */
int32_t leconvert_int32_to(int32_t native);

/**
 * \internal
 */
uint32_t leconvert_uint32_to(uint32_t native);

/**
 * \internal
 */
int64_t leconvert_int64_to(int64_t native);

/**
 * \internal
 */
uint64_t leconvert_uint64_to(uint64_t native);

/**
 * \internal
 */
float leconvert_float_to(float native);

/**
 * \internal
 */
int16_t leconvert_int16_from(int16_t little);

/**
 * \internal
 */
uint16_t leconvert_uint16_from(uint16_t little);

/**
 * \internal
 */
int32_t leconvert_int32_from(int32_t little);

/**
 * \internal
 */
uint32_t leconvert_uint32_from(uint32_t little);

/**
 * \internal
 */
int64_t leconvert_int64_from(int64_t little);

/**
 * \internal
 */
uint64_t leconvert_uint64_from(uint64_t little);

/**
 * \internal
 */
float leconvert_float_from(float little);

#endif

#endif

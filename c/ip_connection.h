#ifndef IP_CONNECTION
#define IP_CONNECTION

#ifndef _GNU_SOURCE
#define _GNU_SOURCE // for CLOCK_REALTIME
#endif
#ifndef __USE_BSD
#define __USE_BSD // for sleep 
#endif

#include <stdint.h>
#include <stdbool.h>
#include <string.h>
#include <stdlib.h>


#ifdef _WIN32
	#include <windows.h>
	#include <winsock2.h>
#else
	#include <netinet/in.h> // struct sockaddr_in
	#include <pthread.h>
	#include <semaphore.h>
#endif

#define E_OK 0
#define E_TIMEOUT -1
#define E_NO_STREAM_SOCKET -2
#define E_HOSTNAME_INVALID -3
#define E_NO_CONNECT -4
#define E_NO_THREAD -5
#define E_NOT_ADDED -6

#define TIMEOUT_ADD_DEVICE 2500
#define TIMEOUT_ANSWER 2500

#define MAX_NUM_DEVICES 256
#define MAX_NUM_CALLBACKS 256
#define MAX_PACKET_SIZE 4096
#define RECV_BUFFER_SIZE 8192

#define BROADCAST_ADDRESS 0
#define TYPE_GET_STACK_ID 255
#define TYPE_ENUMERATE 254
#define TYPE_ENUMERATE_CALLBACK 253
#define TYPE_STACK_ENUMERATE 252
#define TYPE_ADC_CALIBRATE 251
#define TYPE_GET_ADC_CALIBRATION 250

#define TYPE_READ_BRICKLET_UID 249
#define TYPE_WRITE_BRICKLET_UID 248
#define TYPE_READ_BRICKLET_PLUGIN 247
#define TYPE_WRITE_BRICKLET_PLUGIN 246
#define TYPE_READ_BRICKLET_NAME 245
#define TYPE_WRITE_BRICKLET_NAME 244

struct IPConnection_;
struct Device_;

typedef void (*enumerate_callback_func_t)(char*, char*, uint8_t, bool);
typedef int (*device_callback_func_t)(struct Device_*, const unsigned char*);

typedef struct {
	unsigned char type;
	int length;
	char buffer[MAX_PACKET_SIZE];
} DeviceAnswer;

typedef struct Device_{
	unsigned char stack_id;
	unsigned long long uid;
#ifdef _WIN32
	HANDLE  sem_write;
	HANDLE  sem_answer;
#else
	sem_t sem_write;
	sem_t sem_answer;
#endif
	DeviceAnswer answer;
	void *callbacks[MAX_NUM_CALLBACKS];
	device_callback_func_t device_callbacks[MAX_NUM_CALLBACKS];
	struct IPConnection_ *ipcon;
} Device;


typedef struct IPConnection_{
#ifdef _WIN32
	SOCKET s;
	HANDLE handle_recv_loop;
#else
	int fd;
	pthread_t thread_recv_loop;
#endif
	bool recv_loop_flag;
	struct sockaddr_in server;
	Device* devices[MAX_NUM_DEVICES];
	Device *add_device;
	enumerate_callback_func_t enumerate_callback;
} IPConnection;

typedef struct {
	uint8_t stack_id;
	uint8_t type;
	uint16_t length;
	uint64_t uid;
} __attribute__((__packed__)) GetStackID;

typedef struct {
	uint8_t stack_id;
	uint8_t type;
	uint16_t length;
	uint64_t device_uid;
	uint8_t device_stack_id;
} __attribute__((__packed__)) GetStackIDReturn;

typedef struct {
	uint8_t stack_id;
	uint8_t type;
	uint16_t length;
} __attribute__((__packed__)) Enumerate;

typedef struct {
	unsigned short length;
	unsigned char stack_id;
	unsigned char type;
	uint64_t device_uid;
	char device_name[40];
	uint8_t device_stack_id;
	bool is_new;
} __attribute__((__packed__)) EnumerateReturn;

int ipcon_create(IPConnection *ipcon, const char* host, const int port);
void ipcon_enumerate(IPConnection *ipcon, enumerate_callback_func_t cb);
int ipcon_add_device(IPConnection *ipcon, Device *device);
void ipcon_join_thread(IPConnection *ipcon);
void ipcon_destroy(IPConnection *ipcon);

void ipcon_base58encode(uint64_t value, char *str);
uint64_t ipcon_base58decode(const char *str);

#ifdef _WIN32
void ipcon_recv_loop(void *param);
#else
void* ipcon_recv_loop(void *param);
#endif
int ipcon_handle_enumerate(IPConnection *ipcon, const unsigned char *buffer);
int ipcon_handle_message(IPConnection *ipcon, const unsigned char *buffer);
void ipcon_device_write(Device *device, const char *buffer, const int length);
void ipcon_device_create(Device *device, const char *uid);
int ipcon_add_device_handler(IPConnection *ipcon, 
                             const unsigned char *buffer);
int ipcon_answer_sem_wait_timeout(Device *device);

unsigned short ipcon_get_length_from_data(const unsigned char *data);
unsigned char ipcon_get_stack_id_from_data(const unsigned char *data);
unsigned char ipcon_get_type_from_data(const unsigned char *data);

int ipcon_sem_wait_write(Device *device);
int ipcon_sem_post_write(Device *device);
#endif

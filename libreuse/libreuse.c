#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <stdbool.h>

static int (*orig_socket)(int domain, int type, int protocol) = NULL;
static int (*orig_setsockopt)(int sockfd, int level, int optname, const void *optval, socklen_t optlen) = NULL;

static bool initialized = false;

#define LIBC "/lib/x86_64-linux-gnu/libc.so.6"

// Just some basic setup
static void init() {
	if (initialized) {
		return;
	}

	// open libc
	void *my_libc = dlopen(LIBC, RTLD_LAZY);
	if (!my_libc) {
		char *err = dlerror();
		fprintf(stderr, "dlopen: %s\n", err);
		exit(-1);
	}

	// get handles to socket and setsockopt functions
	orig_socket = (int (*)(int domain, int type, int protocol)) dlsym(my_libc, "socket");
	orig_setsockopt = (int (*)(int sockfd, int level, int optname,
				const void *optval, socklen_t optlen)) dlsym(my_libc, "setsockopt");

	// so we don't do init twice
	initialized = true;
}

// hooking the socket call
int socket(int domain, int type, int protocol) {
	// init our libc
	init();

	// forward request to original socket implementation
	int fd = orig_socket(domain, type, protocol);

	// set SO_REUSEADDR on the socket
	orig_setsockopt(fd, SOL_SOCKET, SO_REUSEADDR, &(int){ 1 }, sizeof(int));

	// return the fd
	return fd;
}


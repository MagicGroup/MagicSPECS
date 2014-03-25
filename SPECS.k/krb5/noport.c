#define _GNU_SOURCE
#include <sys/socket.h>
#include <dlfcn.h>
#include <errno.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>

static int
port_is_okay(unsigned short port)
{
	char *p, *q;
	long l;

	p = getenv("NOPORT");
	while ((p != NULL) && (*p != '\0')) {
		l = strtol(p, &q, 10);
		if ((q == NULL) || (q == p)) {
			break;
		}
		if ((*q == '\0') || (*q == ',')) {
			if (port == l) {
				errno = ECONNREFUSED;
				return -1;
			}
		}
		p = q;
		p += strspn(p, ",");
	}
	return 0;
}

int
connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen)
{
	unsigned short port;
	static int (*next_connect)(int, const struct sockaddr *, socklen_t);

	if (next_connect == NULL) {
		next_connect = dlsym(RTLD_NEXT, "connect");
		if (next_connect == NULL) {
			errno = ENOSYS;
			return -1;
		}
	}

	if (getenv("NOPORT") == NULL) {
		return next_connect(sockfd, addr, addrlen);
	}

	switch (addr->sa_family) {
	case AF_INET:
		port = ntohs(((struct sockaddr_in *)addr)->sin_port);
		if (port_is_okay(port) != 0) {
			return -1;
		}
		break;
	case AF_INET6:
		port = ntohs(((struct sockaddr_in6 *)addr)->sin6_port);
		if (port_is_okay(port) != 0) {
			return -1;
		}
		break;
	default:
		break;
	}
	return next_connect(sockfd, addr, addrlen);
}

ssize_t
sendto(int sockfd, const void *buf, size_t len, int flags,
       const struct sockaddr *dest_addr, socklen_t addrlen)
{
	unsigned short port;
	static int (*next_sendto)(int, const void *, size_t, int,
				  const struct sockaddr *, socklen_t);

	if (next_sendto == NULL) {
		next_sendto = dlsym(RTLD_NEXT, "sendto");
		if (next_sendto == NULL) {
			errno = ENOSYS;
			return -1;
		}
	}

	if (getenv("NOPORT") == NULL) {
		return next_sendto(sockfd, buf, len, flags, dest_addr, addrlen);
	}

	if (dest_addr != NULL) {
		switch (dest_addr->sa_family) {
		case AF_INET:
			port = ((struct sockaddr_in *)dest_addr)->sin_port;
			port = ntohs(port);
			if (port_is_okay(port) != 0) {
				return -1;
			}
			break;
		case AF_INET6:
			port = ((struct sockaddr_in6 *)dest_addr)->sin6_port;
			port = ntohs(port);
			if (port_is_okay(port) != 0) {
				return -1;
			}
			break;
		default:
			break;
		}
	}
	return next_sendto(sockfd, buf, len, flags, dest_addr, addrlen);
}

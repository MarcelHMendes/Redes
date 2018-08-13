#include <stdlib.h>
#include <stdio.h>
#include <string.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>

#define BUFSZ 1024

void logexit(const char *str)
{
	perror(str);
	exit(EXIT_FAILURE);
}

void show(const struct sockaddr *addr)
{
	int version;	
	char str[INET6_ADDRSTRLEN+1];
	str[INET6_ADDRSTRLEN] = '\0';
	short port;

	if(addr->sa_family == AF_INET) {
		version = 4;
		struct sockaddr_in *addr4 = (struct sockaddr_in *)addr;
		if(!inet_ntop(addr4->sin_family, &(addr4->sin_addr),
				str, INET6_ADDRSTRLEN)) {
			logexit("ntop");
		}
		port = ntohs(addr4->sin_port);
	} else {
		version = 6;
		struct sockaddr_in6 *addr6 = (struct sockaddr_in6 *)addr;
		if(!inet_ntop(addr6->sin6_family, &(addr6->sin6_addr),
				str, INET6_ADDRSTRLEN))
		{
			logexit("ntop");
		}
		port = ntohs(addr6->sin6_port);
	}
	printf("IPv%d %s %hd\n", version, str, port);
}


int main(void)
{
	struct addrinfo hints;
	memset(&hints, 0, sizeof(struct addrinfo));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;
	struct addrinfo *info;
	if(getaddrinfo("www.dcc.ufmg.br", "http", &hints, &info)) {
		logexit("addrinfo");
	}

	struct addrinfo *curr = info;

	while(curr) {
		show(info->ai_addr);
		curr = curr->ai_next;
	}
	freeaddrinfo(info);

	exit(EXIT_SUCCESS);
}


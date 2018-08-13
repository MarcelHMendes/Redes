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


int main(void)
{
	struct in_addr addr;
	if(inet_pton(AF_INET, "150.164.0.135", &addr) < 1)
		logexit("pton");

	struct sockaddr_in dst;
	dst.sin_family = AF_INET;
	dst.sin_port = htons(80);
	dst.sin_addr = addr;

	int s = socket(AF_INET, SOCK_STREAM, 0);
	if(s == -1) logexit("socket");

	if(connect(s, (struct sockaddr *)&dst, sizeof(dst)))
		logexit("connect");

	char req[] = "GET /dcc/index.html HTTP/1.1\n"
			"Host: www.dcc.ufmg.br\n\n";

	ssize_t count;
	count = send(s, req, strlen(req), 0);
	if(count != strlen(req)) logexit("send");

	char buf[BUFSZ];
	count = recv(s, buf, BUFSZ, 0);
	
	printf("received %d bytes\n", (int)count);
	puts(buf);

	exit(EXIT_SUCCESS);
}


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
	int s;

	struct in_addr inaddr;
	inet_pton(AF_INET, "127.0.0.1",
			&inaddr);

	struct sockaddr_in addr;
	struct sockaddr *addrptr = (struct sockaddr *)&addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(5152);
	addr.sin_addr = inaddr;

	s = socket(AF_INET, SOCK_STREAM, 0);
	if(s == -1) logexit("socket");

	if(connect(s, addrptr, sizeof(struct sockaddr_in)))
		logexit("connect");

	char linha[512];
	printf("mensagem> ");
	fgets(linha, 511, stdin);
	ssize_t count;
	count = send(s, linha, strlen(linha)+1, 0);
	if(count != strlen(linha)+1)
		logexit("send");

	char buf[512];
	memset(buf, 0, 512);
	unsigned total = 0;
	while(1) {
		count = recv(s, buf+total, 512, 0);
		if(count == 0) break;
		total += count;
	}

	printf("received %d bytes\n", (int)total);
	puts(buf);

	exit(EXIT_SUCCESS);
}


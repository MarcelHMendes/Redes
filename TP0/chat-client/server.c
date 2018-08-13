#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <string.h>
#include <pthread.h>

#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>

void logexit(const char *str)
{
	perror(str);
	exit(EXIT_FAILURE);
}


int main(void)
{
	int s;
	s = socket(AF_INET, SOCK_STREAM, 0);
	if(s == -1) logexit("socket");

	struct in_addr inaddr;
	inet_pton(AF_INET, "127.0.0.1", &inaddr);

	struct sockaddr_in addr;
	struct sockaddr *addrptr = (struct sockaddr *)&addr;
	addr.sin_family = AF_INET;
	addr.sin_port = htons(5152);
	addr.sin_addr = inaddr;

	if(bind(s, addrptr, sizeof(struct sockaddr_in)))
		logexit("bind");

	if(listen(s, 10)) logexit("listen");
	printf("esperando conexao\n");

	while(1) {
		struct sockaddr_in raddr;
		struct sockaddr *raddrptr =
			(struct sockaddr *)&raddr;
		socklen_t rlen = sizeof(struct sockaddr_in);

		int r = accept(s, raddrptr, &rlen);
		if(r == -1) logexit("accept");

		char buf[512];
		char ipcliente[512];
		inet_ntop(AF_INET, &(raddr.sin_addr),
				ipcliente, 512);

		printf("conexao de %s %d\n", ipcliente,
				(int)ntohs(raddr.sin_port));

		size_t c = recv(r, buf, 512, 0);
		printf("recebemos %d bytes\n", (int)c);
		puts(buf);

		sprintf(buf, "seu IP eh %s %d\n", ipcliente,
				(int)ntohs(raddr.sin_port));
		//printf("enviando %s\n", buf);

		//send(r, buf, strlen(buf)+1, 0);
		//printf("enviou\n");

		close(r);
	}

	exit(EXIT_SUCCESS);
}






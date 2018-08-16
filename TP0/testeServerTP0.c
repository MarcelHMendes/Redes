//Codigo servidor
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>


#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#define TAM_MAX 512
#define TAM_MIN 4

char *decifra(char *mensagem,int chave){ //Cifra de Cesar
	char *cifra = (char *) malloc(TAM_MAX*sizeof(char));

	int i;

	for(i = 0;i < strlen(mensagem);i++){
		cifra[i] = mensagem[i] - chave;
	}
	cifra[strlen(mensagem)] = '\0';

	return cifra;
}

void *connection_handler(void *);

int main(int argc, char *argv[]){
	int sock,i,i2,a;
	int port = atoi(argv[1]);
	 

	sock = socket(AF_INET,SOCK_STREAM,0);

	struct sockaddr_in server_addr;
	struct in_addr inaddr;
	
	i = inet_pton(AF_INET,"127.0.0.1",&inaddr);
	if(i == -1){
		perror("inet_pton");
		exit(1);
	}


	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port);
	server_addr.sin_addr = inaddr;

	if(bind(sock,(struct sockaddr *) &server_addr,sizeof(struct sockaddr_in)) < 0){
		perror("bind");
		exit(1);
	}
	int l = listen(sock, 10);
	if(l == -1){
		perror("listen");
		exit(1);
	}

	
	struct sockaddr_in cliente_addr;
	socklen_t cliente_len = sizeof(struct sockaddr_in);
	pthread_t thread_id;


	while(a = accept(sock, (struct sockaddr *) &cliente_addr, &cliente_len)){
		if(a == -1){
			perror("accept");
			exit(1);
		}

		if(pthread_create(&thread_id,NULL , connection_handler, (void *) &a) < 0){
			perror("pthread_create");
			exit(1);
		}

		

		//close(a);
	}


	exit(0);
}

void *connection_handler(void *socket_desc){

	int sock = *(int*)socket_desc;
	char *msgDecript = (char *) malloc(TAM_MAX * sizeof(char));
	char buf[512];
	uint32_t tamMsg;
	uint32_t chave;

	size_t c = recv(sock,&tamMsg , sizeof(int), MSG_WAITALL);
	size_t c2 = recv(sock,buf,ntohl(tamMsg),MSG_WAITALL);
	size_t c3 = recv(sock,&chave,sizeof(int),MSG_WAITALL);	

	msgDecript = decifra(buf, (int)ntohl(chave));

	if(send(sock, msgDecript, strlen(msgDecript), 0) < 0){
		perror("send");
		exit(1);
	}

	close(sock);
}
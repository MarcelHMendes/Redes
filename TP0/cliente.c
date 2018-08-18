//Código do cliente
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netdb.h>
#define TAM_MAX 512
#define TAM_MIN 4

char *cifra(char *mensagem,int chave){ //Cifra de Cesar
	char *cifra = (char *) malloc(TAM_MAX*sizeof(char));

	int i;

	for(i = 0;i < strlen(mensagem);i++){
		cifra[i] = mensagem[i] + chave;
	}
	cifra[strlen(mensagem)] = '\0';

	return cifra;
}
	
int main(int argc, char *argv[]){
	int sock,i;
	ssize_t rBytes;
	char mensagem[TAM_MAX];
	char *menEncript = (char *) malloc(TAM_MAX*sizeof(char));
	int x,port;
	char *ip = (char *) malloc(32*sizeof(char));

	ip = argv[1];
	port = atoi(argv[2]);
	x = atoi(argv[4]);
	strcpy(mensagem,argv[3]);	//Mensagem original

	//printf("%s\n",mensagem);

	struct sockaddr_in server_addr;

	sock = socket(AF_INET,SOCK_STREAM,0);

	if(sock == -1){
		perror("socket");
		exit(1);
	}	

	struct in_addr inaddr;//
	i = inet_pton(AF_INET,ip,&inaddr); //IP passado por parametro no momento da execução
	if(i == -1){
		perror("inet_pton");
		exit(1);
	}
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(port); //passado como parametro no momento da execução 
	server_addr.sin_addr = inaddr;

	bzero(&(server_addr.sin_zero),8);

	if(connect(sock,(struct sockaddr *) &server_addr, sizeof(struct sockaddr)) < 0){	//Conexão com servidor
		perror("connect");
		exit(1);
	}

	menEncript = cifra(mensagem,x);	//Cifrando mensagem
	
	uint32_t tamMsg;	//Tamanho da mensagem, será enviado ao servidor
	uint32_t chave;		//Chave a ser usada, será enviada ao servidor
	char *buf = (char *) malloc(TAM_MAX * sizeof(char)); //buffer para receber a msg
	ssize_t c;
	

	memset(buf, 0, 512);

	//sprintf(tamMsg ,"%d" , strlen(menEncript)); 	
	//strcpy(chave,argv[4]);

	tamMsg = htonl(strlen(menEncript));
	chave = htonl(x);


	if(send(sock, &tamMsg, sizeof(int),0) < 0){	//Enviando tamanho da msg
		perror("send");
		exit(1);
	}

	if(send(sock, menEncript, strlen(menEncript),0) < 0){	//Enviando msg
		perror("send");
		exit(1);
	}

	if(send(sock, &chave, sizeof(int),0) < 0){	//Enviando chave
		perror("send");
		exit(1);
	}

	/////////////////////////////////// TESTE

	struct timeval tv;
	tv.tv_sec = 15;
	tv.tv_usec = 0;
	if(setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (const char*)&tv, sizeof(tv))){
		perror("setsockopt- rcvtimeo");
    	exit(1);
	}

	c = recv(sock, buf,strlen(mensagem),MSG_WAITALL);
	if(c < 0){
		perror("recv");
		exit(1);
	}


	printf("%s\n",buf);
	
	//NAO ESQUECER DE PASSAR OS ARGUENTOS, VAI DAR SEGFAULT!!!!!

	exit(0);
	
}	

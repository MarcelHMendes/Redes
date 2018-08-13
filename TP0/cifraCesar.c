#include <stdio.h>
#include <stdlib.h>
#include <string.h>


char *cifra(char *mensagem){
	char *cifra = (char *) malloc(512*sizeof(char));

	int chave = 13;

	int i;

	for(i = 0;i < strlen(mensagem);i++){
		cifra[i] = mensagem[i] + 13;
	}
	cifra[strlen(mensagem)] = '\0';

	return cifra;
}



int main(){
	char msg[512] = "ola mundo";
 	char *cipher = (char *) malloc(512*sizeof(char));
 	char teste[512];

 	cipher = cifra(msg);
 	printf("%s\n", cipher);

	int i;

	for(i = 0;i  < strlen(cipher);i++){
		teste[i]  = cipher[i] - 13;
	}
	teste[strlen(cipher)]  = '\0';

	printf("%s\n", teste);

	exit(0);
}
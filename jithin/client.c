#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h> 

void error(const char *msg)
{
    perror(msg);
    exit(0);
}

int main(int argc, char *argv[])
{
    int sockfd, portno, n;
    struct sockaddr_in serv_addr;
    struct hostent *server;
    char buffer[256];

    int msg_id = 0;

    sockfd = socket(PF_INET, SOCK_DGRAM, IPPROTO_UDP);
    if (sockfd < 0) {
        error("ERROR opening socket");
    }   

    bzero((char *) &serv_addr, sizeof(serv_addr));
    serv_addr.sin_family = AF_INET;
    serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
    serv_addr.sin_port = htons(54321);

    if (bind(sockfd, (struct sockaddr* ) &serv_addr, sizeof(serv_addr)) < 0) {
        error("bind");
        return -1; 
    }    

    while(1) {
        bzero(buffer, 256);
        int received = recvfrom(sockfd, buffer, 256, 0, NULL, NULL);
        if (received < 0) {
            error("recvfrom");
            return -1; 
        }

        printf("[%d] message received: %s\n", msg_id++, buffer);
    }   

    close(sockfd);
    return 0;
}


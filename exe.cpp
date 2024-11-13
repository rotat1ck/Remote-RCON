#include <iostream>
#include <winsock2.h>

#pragma comment(lib, "ws2_32.lib")

int main() {
    WSADATA wsaData;
    const char* server_ip = "77.37.246.6";
    const int server_port = 7777;

    // Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        std::cerr << "WSAStartup failed" << std::endl;
        return 1;
    }

    // Create a socket
    SOCKET sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        std::cerr << "Could not create socket" << std::endl;
        WSACleanup();
        return 1;
    }

    struct sockaddr_in server_address;
    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(server_port);
    server_address.sin_addr.s_addr = inet_addr(server_ip);

    // Connect to the server
    if (connect(sock, (struct sockaddr*)&server_address, sizeof(server_address)) == SOCKET_ERROR) {
        std::cerr << "Connection failed" << std::endl;
        closesocket(sock);
        WSACleanup();
        return 1;
    }

    // Send a message
    const char* message = "3b981e15105be428cbec298e0c619f234819750c38d7e7aea124480cf4d0b9d5";
    send(sock, message, strlen(message), 0);

    // Receive a response
    char buffer[1024] = {0};
    int bytes_received = recv(sock, buffer, sizeof(buffer) - 1, 0);
    if (bytes_received > 0) {
        buffer[bytes_received] = '\0';
        std::cout << "Received from server: " << buffer << std::endl;
    }

    // Close the socket
    closesocket(sock);
    WSACleanup();
    system("pause");
    return 0;
}
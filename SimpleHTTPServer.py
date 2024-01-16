# server.py

import socket

def start_server():
    # Set the host and port
    host = '127.0.0.1'  # Use '0.0.0.0' to listen on all available interfaces
    port = 8080

    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind((host, port))

    # Listen for incoming connections
    server_socket.listen(1)
    print(f"Server listening on http://{host}:{port}/")

    while True:
        # Wait for a connection
        client_socket, client_address = server_socket.accept()

        # Receive the data sent by the client
        request_data = client_socket.recv(1024).decode('utf-8')

        # Parse the received data to get the requested file path
        requested_file = request_data.split()[1][1:]

        # If no specific file is requested, default to 'index.html'
        if requested_file == '':
            requested_file = 'index.html'

        try:
            # Open and read the requested file
            with open(requested_file, 'r') as file:
                response_data = file.read()
            status_line = 'HTTP/1.1 200 OK\r\n'
        except FileNotFoundError:
            # If the file is not found, return a 404 Not Found response
            response_data = '404 Not Found'
            status_line = 'HTTP/1.1 404 Not Found\r\n'

        # Construct the HTTP response
        response = status_line + '\r\n' + response_data

        # Send the response back to the client
        client_socket.sendall(response.encode('utf-8'))

        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    start_server()

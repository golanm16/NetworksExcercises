# Ex 4.4 - HTTP Server Shell
# Author: Barak Gonen
# Purpose: Provide a basis for Ex. 4.4
# Note: The code is written in a simple way, without classes, log files or other utilities, for educational purpose
# Usage: Fill the missing functions and constants

# TO DO: import modules
import os
import socket
import animation

# TO DO: set constants

IP = '0.0.0.0'
PORT = 80
SOCKET_TIMEOUT = 0.2
DEFAULT_URL = 'index.html'
FIXED_RESPONSE = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: 5\r\n\r\nHello"


def get_content_length_header(size):
    return fr'Content-Length: {str(size)}\r\n'


HEADERS = {
    'http_ok': 'HTTP/1.1 200 OK\r\n',
    'html': 'Content-Type: text/html; charset=UTF-8\r\n',
    'jpeg': 'Content-Type: image/jpeg; charset=UTF-8\r\n',
    'js': 'Content-Type: text/javascript; charset=UTF-8\r\n',
    'css': 'Content-Type: text/css; charset=UTF-8\r\n',
    'len': get_content_length_header,
    'header_end': '\r\n'

           }



def get_file_data(filename):
    """ Get data from file """
    return open(filename).read(os.path.getsize(filename))


def handle_client_request(resource, client_socket):
    """ Check the required resource, generate proper HTTP response and send to client"""
    # TO DO : add code that given a resource (URL and parameters) generates the proper response
    # return

    if resource == '':
        url = DEFAULT_URL
    else:
        url = resource

    # # TO DO: check if URL had been redirected, not available or other error code. For example:
    # if url in REDIRECTION_DICTIONARY:
    #     # TO DO: send 302 redirection response
    filename, filetype = os.path.splitext(url)
    print(url)
    if os.path.isfile(url):

        # TO DO: extract requested file tupe from URL (html, jpg etc)
        http_header = HEADERS['http_ok']
        if filetype == '.html':
            http_header += HEADERS['html']
        elif filetype == '.jpg':
            http_header += HEADERS['jpeg']
        elif filetype == '.js':
            http_header += HEADERS['js']
        elif filetype == '.css':
            http_header += HEADERS['css']
        # TO DO: handle all other headers
        http_header += HEADERS['len'](os.path.getsize(url))
        # TO DO: read the data from the file
        data = get_file_data(url)
        http_header += HEADERS['header_end']
        http_response = http_header + data
        print(http_header)
        client_socket.send(http_response.encode())


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # TO DO: write function
    # split the request to [GET, URL, HTTP_Ver\r\n]
    request = str(request)
    request_arr = request.split()
    if request_arr[0] == 'GET' and request_arr[2] == 'HTTP/1.1':
        return True, request_arr[1][1:]

    return False, request_arr[1]


def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        # TODO: insert code that receives client request
        client_request = client_socket.recv(1024).decode()
        # ...
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            print('Error: Not a valid HTTP request')
            break
    # client_socket.send(FIXED_RESPONSE.encode())
    print('Closing connection')
    client_socket.close()


def main():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((IP, PORT))
    server_socket.listen()
    print(f"Listening for connections on port {PORT}")

    while True:
        wait_animation = animation.Wait('spinner', text="waiting for a client to connect ... ", speed=0.25)
        wait_animation.start()
        client_socket, client_address = server_socket.accept()
        wait_animation.stop()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


if __name__ == "__main__":
    # Call the main handler function
    main()

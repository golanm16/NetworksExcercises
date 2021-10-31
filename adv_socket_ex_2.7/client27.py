#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
# import pathlib
import socket
import protocol


IP = "127.0.0.1"
# The path + filename where the copy of the screenshot at the client should be saved
# SAVED_PHOTO_LOCATION = pathlib.Path().resolve()
SAVED_PHOTO_LOCATION = r"D:\Coding\networks\NetworksExercises\adv_socket_ex_2.7" + r"\client_screenshot.jpg"


def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    response = protocol.get_msg(my_socket)
    # (10) treat SEND_PHOTO
    if cmd == 'SEND_PHOTO':
        photo_file = open(SAVED_PHOTO_LOCATION, 'wb')
        photo_chunk = my_socket.recv(protocol.PHOTO_CHUNK)
        while photo_chunk:
            photo_file.write(photo_chunk)
            photo_chunk = my_socket.recv(protocol.PHOTO_CHUNK)
        photo_file.close()
    return response


def main():
    # open socket with the server
    my_socket = socket.socket()
    my_socket.connect((IP, protocol.PORT))
    # (2)

    # print instructions
    print('Welcome to remote computer application. Available commands are:\n')
    print('TAKE_SCREENSHOT\nSEND_PHOTO\nDIR\nDELETE\nCOPY\nEXECUTE\nEXIT')

    # loop until user requested to exit
    while True:
        cmd = input("Please enter command:\n")
        if protocol.check_cmd(cmd):
            packet = protocol.create_msg(cmd)
            my_socket.send(packet)
            response = handle_server_response(my_socket, cmd)
            if cmd == 'EXIT':
                break
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()

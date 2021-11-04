#   Ex. 2.7 template - client side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
# import pathlib
import socket

import animation

import protocol


IP = "127.0.0.1"
# The path + filename where the copy of the screenshot at the client should be saved
# SAVED_PHOTO_LOCATION = pathlib.Path().resolve()
SAVED_PHOTO_LOCATION = r"D:\Coding\networks\NetworksExercises\adv_socket_ex_2.7" + r"\client_screenshot.jpg"


@animation.wait('spinner', text="waiting for server response ... ", speed=0.25)
def handle_server_response(my_socket, cmd):
    """
    Receive the response from the server and handle it, according to the request
    For example, DIR should result in printing the contents to the screen,
    Note- special attention should be given to SEND_PHOTO as it requires and extra receive
    """
    # (8) treat all responses except SEND_PHOTO
    valid_rsp, response = protocol.get_msg(my_socket)
    # (10) treat SEND_PHOTO
    if cmd == 'SEND_PHOTO' and valid_rsp and response.isdecimal():
        photo_file = open(SAVED_PHOTO_LOCATION, 'wb')
        photo_size = int(response)
        while photo_size > 0:
            photo_chunk = my_socket.recv(protocol.PHOTO_CHUNK_SIZE)
            photo_file.write(photo_chunk)
            photo_size -= protocol.PHOTO_CHUNK_SIZE
        """
        photo_chunk = my_socket.recv(protocol.PHOTO_CHUNK_SIZE)
        while photo_chunk:
            photo_file.write(photo_chunk)
            photo_chunk = my_socket.recv(protocol.PHOTO_CHUNK_SIZE)
        """
        photo_file.close()
    return valid_rsp, response


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
            print("command sent to server.")
            if cmd == 'EXIT':
                break
            valid_rsp, response = handle_server_response(my_socket, cmd)
            if valid_rsp:
                print(f"the server responded: {response}")
            else:
                print("server returned an invalid response")
        else:
            print("Not a valid command, or missing parameters\n")

    my_socket.close()


if __name__ == '__main__':
    main()

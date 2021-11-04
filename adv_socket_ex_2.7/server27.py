#   Ex. 2.7 template - server side
#   Author: Barak Gonen, 2017
#   Modified for Python 3, 2020
import glob
import shutil
import socket
import subprocess

import animation
import pyautogui

import protocol
import os.path

IP = "0.0.0.0"
# The path + filename where the screenshot at the server should be saved

# can use auto path getting for easy time
# PHOTO_PATH = str(pathlib.Path().resolve()) + r"server_screenshot.jpg"
PHOTO_PATH = r"D:\Coding\networks\NetworksExercises\adv_socket_ex_2.7" + r"\server_screenshot.jpg"


def __dir_response(param):
    is_successful = True
    try:
        notes = glob.glob(str(param[0]) + r"\*")
    except Exception as e:
        notes = str(e)
        is_successful = False
    return is_successful, notes


def __delete_response(param):
    is_successful = True
    notes = 'success!'
    try:
        os.remove(param[0])
    except Exception as e:
        notes = str(e)
        is_successful = False
    return is_successful, notes


def __copy_response(params):
    is_successful = True
    notes = 'success!'
    try:
        shutil.copy(params[0], params[1])
    except Exception as e:
        notes = str(e)
        is_successful = False
    return is_successful, notes


def __execute_response(param):
    is_successful = True
    notes = 'success!'
    try:
        subprocess.call(param)
    except Exception as e:
        notes = str(e)
        is_successful = False
    return is_successful, notes


def __take_screenshot_response(param):
    is_successful = True
    notes = 'success!'
    try:
        image = pyautogui.screenshot(PHOTO_PATH)
        image.save(PHOTO_PATH)
    except Exception as e:
        notes = str(e)
        print(f"there was an exception:\n{notes}")
        is_successful = False
    return is_successful, notes


def __send_photo_response(param):
    return os.path.isfile(PHOTO_PATH), str(os.path.getsize(PHOTO_PATH))


def __exit_response(param):
    return True, "exiting ..."


@animation.wait('spinner', text=f"sending image to client by chunks of {protocol.PHOTO_CHUNK_SIZE} ... ", speed=0.25)
def send_photo(client_socket: socket):
    """
    sends the server screenshot to the client's socket
    :param client_socket: the socket to send the photo to
    :return: nothing
    """
    # open the photo file
    photo_file = open(PHOTO_PATH, 'rb')

    # get a piece of the image
    photo_chunk = photo_file.read(protocol.PHOTO_CHUNK_SIZE)
    while photo_chunk:
        # send the piece of the image
        client_socket.send(photo_chunk)
        photo_chunk = photo_file.read(protocol.PHOTO_CHUNK_SIZE)
    photo_file.close()


# list the known commands, how many parameters they can get, and what function handles them
# map: {'COMMAND': (NUMBER_OF_PARAMETERS, FUNCTION_TO_HANDLE_COMMAND),...}
COMMANDS_RESPONSES = {'DIR': __dir_response, 'DELETE': __delete_response, 'COPY': __copy_response,
                      'EXECUTE': __execute_response, 'TAKE_SCREENSHOT': __take_screenshot_response,
                      'EXIT': __exit_response, 'SEND_PHOTO': __send_photo_response}


def check_client_request(cmd_data):
    """
    Break cmd to command and parameters
    Check if the command and params are good.

    For example, the filename to be copied actually exists

    Returns:
        valid: True/False
        command: The requested cmd (ex. "DIR")
        params: List of the cmd params (ex. ["c:\\cyber"])
    """
    # Use protocol.check_cmd first
    # protocol.check_cmd check that the command is one of the known commands,
    # and that they sent the correct number of parameters.
    protocol_check = protocol.check_cmd(cmd_data)
    is_request_valid = False
    cmd_with_params = cmd_data.split()
    # the first entry in the data is the command
    cmd = cmd_with_params[0]
    # the rest of the data is the command params
    params = cmd_with_params[1:]
    # Then make sure the params are valid
    # TODO: need to add else for every if and describe the error
    if protocol_check:
        """
        command             #parameters     type
        DIR:                1               Directory
        DELETE:             1               File/Directory
        COPY:               2               File/Directory, File/Directory
        EXECUTE:            1               File(.exe)
        TAKE_SCREENSHOT:    0
        EXIT:               0
        """
        if cmd in ('EXIT', 'TAKE_SCREENSHOT'):
            # commands with no parameters, the protocol check is enough
            is_request_valid = True
        elif cmd == 'SEND_PHOTO':
            if os.path.isfile(PHOTO_PATH):
                is_request_valid = True
        elif cmd == 'DIR':
            if os.path.isdir(params[0]):
                is_request_valid = True
        elif cmd == 'DELETE':
            if os.path.isdir(params[0]) or os.path.isfile(params[0]):
                is_request_valid = True
        elif cmd == 'EXECUTE':
            if os.path.isfile(params[0]) and params[0].endswith('.exe'):
                is_request_valid = True
        elif cmd == 'COPY':
            if os.path.isfile(params[0]) and not os.path.exists(params[1]):
                # the extension of the parameter is the last item in the array after splitting by '.'
                extension_from = params[0].split('.')[-1]
                extension_to = params[1].split('.')[-1]
                if extension_from == extension_to:
                    is_request_valid = True
    # (6)
    return is_request_valid, cmd, params


def handle_client_request(command, params):
    """Create the response to the client, given the command is legal and params are OK

    For example, return the list of filenames in a directory
    Note: in case of SEND_PHOTO, only the length of the file will be sent

    Returns:
        is_successful: if the requested were successful
        response: the requested data

    """

    # (7)
    is_successful, notes = COMMANDS_RESPONSES[command](params)
    return is_successful, notes


def main():
    # open socket with client
    server_socket = socket.socket()
    server_socket.bind((IP, protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    wait_animation = animation.Wait('spinner', text="waiting for a client to connect ... ", speed=0.25)
    wait_animation.start()
    (client_socket, client_address) = server_socket.accept()
    wait_animation.stop()
    print("Client connected")
    # (1)

    # handle requests until user asks to exit
    while True:
        # Check if protocol is OK, e.g. length field OK
        valid_protocol, cmd = protocol.get_msg(client_socket)
        print("message received from client.")

        if valid_protocol:
            print("client returned a valid response.\nchecking if: '" + cmd + "' is a valid command...")
            # Check if params are good, e.g. correct number of params, file name exists
            valid_cmd, command, params = check_client_request(cmd)
            if valid_cmd:
                print("command is valid, creating response...")
                # (6)

                # prepare a response using "handle_client_request"
                is_command_successful, response = handle_client_request(command, params)
                # add length field using "create_msg"
                msg = protocol.create_msg(str(response))
                # send to client
                client_socket.send(msg)

                if command == 'SEND_PHOTO':
                    if is_command_successful:
                        # Send the data itself to the client
                        send_photo(client_socket)
                    else:
                        response = "something went wrong with sending the photo. this should not happen"
                        print(response)
                    # (9)
                if command == 'EXIT':
                    break
            else:
                # prepare proper error to client
                is_command_successful = False
                response = 'Bad command or parameters'
                print(response)
                # send to client

        else:
            # prepare proper error to client
            is_command_successful = False
            response = 'Packet not according to protocol'
            print(response)
            # send to client

            # Attempt to clean garbage from socket
            # client_socket.recv(1024)
        if not is_command_successful:
            client_socket.send(protocol.create_msg(response))

    # close sockets
    print("Closing connection")


if __name__ == '__main__':
    main()

"""EX 2.6 protocol implementation
   Author:
   Date:
"""
import datetime

LENGTH_FIELD_SIZE = 2
PORT = 8820
COMMANDS = ('RAND', 'WHORU', 'TIME', 'EXIT')

import socket


def __rand_response():
    import random
    return random.randint(1, 10)


def __whoru_response():
    return "my name is slim shady"


def __time_response():
    return str(datetime.datetime.now())


def __exit_response():
    return "terminating connection..."


COMMAND_RESPONSE = {'RAND': __rand_response, 'WHORU': __whoru_response, 'TIME': __time_response, 'EXIT': __exit_response}


def check_cmd(data):
    """Check if the command is defined in the protocol (e.g RAND, NAME, TIME, EXIT)"""
    return data in COMMANDS


def create_msg(data):
    """Create a valid protocol message, with length field"""
    msg_length = str(len(data)).zfill(LENGTH_FIELD_SIZE)
    msg = msg_length + data
    return msg.encode()


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    msg_length = str(my_socket.recieve(LENGTH_FIELD_SIZE).decode())
    if msg_length.isdecimal():
        return True, str(my_socket.recieve(msg_length).decode())
    else:
        return False, "Error: length field did not contain only numbers"


def create_server_rsp(cmd):
    """Based on the command, create a proper response"""
    if check_cmd(cmd):
        return COMMAND_RESPONSE[cmd]()
    return "Server response"

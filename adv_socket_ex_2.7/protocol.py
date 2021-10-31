#   Ex. 2.7 template - protocol
import socket

LENGTH_FIELD_SIZE = 4
PORT = 8820
"""
command             #parameters
DIR:                1
DELETE:             1
COPY:               2
EXECUTE:            1
TAKE_SCREENSHOT:    0
EXIT:               0
can i do it with dict?
like: {'DIR':1}
"""

# list the known commands, how many parameters they can get
# map: {'COMMAND': NUMBER_OF_PARAMETERS,...}
COMMANDS_PARAM_NUM = {'DIR': 1, 'DELETE': 1, 'COPY': 2, 'EXECUTE': 1, 'TAKE_SCREENSHOT': 0, 'EXIT': 0, 'SEND_PHOTO': 0}


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE "c:\\work\\file.txt" is good, but DELETE alone is not
    """
    # data = [command, param1, param2, ...]-> data[0] =command
    # if data is empty can't execute a command
    if len(data) == 0:
        return False
    # the first entry in the data is the command
    cmd = data[0]
    # the rest of the data is the command params
    params = data[1:]
    # get the needed parameter number for the current command from te commands dictionary
    needed_parameters_number = COMMANDS_PARAM_NUM[cmd]
    # if the command is in commands list AND the number of parameters is the number needed by the command,
    # we can continue handling the command
    if cmd in COMMANDS_PARAM_NUM.keys() and len(params) == needed_parameters_number:
        return True
    # (3)
    return False


def create_msg(msg_data):
    """
    Create a valid protocol message, with length field
    """

    # (4)
    msg_length = str(len(msg_data)).zfill(LENGTH_FIELD_SIZE)
    msg = msg_length + msg_data
    return msg.encode()


def get_msg(my_socket: socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    # (5)
    msg_length = my_socket.recv(LENGTH_FIELD_SIZE).decode()
    if msg_length.isdecimal():
        msg_length = int(msg_length)
        return True, str(my_socket.recv(msg_length).decode())
    else:
        # attempt to empty the socket
        # my_socket.recv(1024)
        return False, "Error: length field did not contain only numbers"


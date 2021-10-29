#   Ex. 2.7 template - protocol


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
like: {'DIR':(1,handle_dir_cmd)}
"""


def __dir_response(param):
    return "dir"


def __delete_response(param):
    return "dir"


def __copy_response(param):
    return "dir"


def __execute_response(param):
    return "dir"


def __take_screenshot_response(param):
    return "dir"


def __exit_response(param):
    return "dir"


COMMANDS = {'DIR': (1, __dir_response), 'DELETE': (1, __delete_response), 'COPY': (2, __copy_response),
            'EXECUTE': (1, __execute_response), 'TAKE_SCREENSHOT': (0, __take_screenshot_response),
            'EXIT': (0, __exit_response)}


def check_cmd(data):
    """
    Check if the command is defined in the protocol, including all parameters
    For example, DELETE "c:\work\file.txt" is good, but DELETE alone is not
    """
    # data = [command, param1, param2, ...]-> data[0] =command
    # if
    if len(data) == 0:
        return False
    if data[0] in COMMANDS:
        pass
    # (3)
    return True


def create_msg(data):
    """
    Create a valid protocol message, with length field
    """

    # (4)
    return "0002OK".encode()


def get_msg(my_socket):
    """
    Extract message from protocol, without the length field
    If length field does not include a number, returns False, "Error"
    """

    # (5)
    return True, "OK"

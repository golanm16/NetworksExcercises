"""EX 2.6 client implementation
   Author:
   Date:
"""

import socket
import protocol


def main():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(("127.0.0.1", protocol.PORT))

    while True:
        user_cmd = input("Enter command\n")
        # Check if user entered a valid command as defined in protocol
        # valid_cmd = protocol.check_cmd(user_cmd)

        if True:
            # If the command is valid:
            # 1. Add length field ("RAND" -> "04RAND")
            cmd = protocol.create_msg(user_cmd)

            # 2. Send it to the server
            my_socket.send(user_cmd.encode())

            # 3. If command is EXIT, break from while loop
            if user_cmd == 'EXIT':
                print("exiting program")
                break

            # 4. Get server's response
            valid_rsp, response = protocol.get_msg(my_socket)

            # 5. If server's response is valid, print it
            if valid_rsp:
                print("the server responded: " + response)
            else:
                print("server returned an invalid response\n")
        else:
            print("Not a valid command")

    print("Closing\n")
    # Close socket


if __name__ == "__main__":
    main()

"""EX 2.6 server implementation
   Author:
   Date:
"""

import socket
import protocol
import animation


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", protocol.PORT))
    server_socket.listen()
    print("Server is up and running")
    wait_animation = animation.Wait('spinner', text="waiting for a client to connect ", speed=0.25)
    wait_animation.start()
    (client_socket, client_address) = server_socket.accept()
    wait_animation.stop()
    print("Client connected")

    while True:
        # Get message from socket and check if it is according to protocol
        valid_msg, cmd = protocol.get_msg(client_socket)
        print("message received from client. checking validity...")
        if valid_msg:
            # 1. Print received message
            print("client returned a valid response.\nchecking if: " + cmd + "is a valid command...")
            # 2. Check if the command is valid
            # 3. If valid command - create response
            if protocol.check_cmd(cmd):
                print("command is valid, creating response...")
                response = protocol.create_server_rsp(cmd)
            else:
                response = "Wrong command"
                print(response)
        else:
            response = "Wrong protocol"
            print(response)
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage
        # Handle EXIT command, no need to respond to the client
        if cmd == 'EXIT':
            break
        # Send response to the client
        print("sending response: " + response + " to client")
        client_socket.send(protocol.create_msg(response))
    print("Closing\n")
    # Close sockets
    server_socket.close()


if __name__ == "__main__":
    main()

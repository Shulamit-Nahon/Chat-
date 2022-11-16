import socket
import select
import protocol

MAX_MSG_LENGTH = 1024
SERVER_PORT = 5555
SERVER_IP = '0.0.0.0'
clients_names = {}


def create_server_rsp(socket_, msg):
    cmd = msg.split()
    if cmd[0] == "NAME":
        if cmd[1] in clients_names.keys():
            return socket_, "Client name already exist"
        else:
            clients_names[cmd[1]] = socket_
            return socket_, "Hello " + cmd[1]
    if cmd[0] == "GET_NAMES":
        return socket_, ','.join(list(clients_names.keys()))
    if cmd[0] == "MSG":
        if cmd[1] in clients_names.keys():
            key_send = list(clients_names.keys())[list(clients_names.values()).index(socket_)]
            message = " sent " + " ".join(msg.split()[2:])
            socket_message = clients_names[cmd[1]]
            return socket_message, key_send + message
        else:
            return socket_, "The client does not exist"
    if cmd[0] == "EXIT":
        return socket_, ""
    else:
        return socket_, "Command not found"


def check_cmd(msg):
    cmd = msg.split()
    if cmd[0] in ["NAME", "GET_NAMES", "MSG", "EXIT"]:
        return True, cmd[0]
    return False, ""


def print_client_sockets(client_sockets):
    for c in client_sockets:
        print("\t", c.getpeername())


def main():
    print("Setting up server...")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))
    server_socket.listen()
    print("Listening for clients...")
    client_sockets = []
    messages_to_send = []

    while True:
        rlist, wlist, xlist = select.select([server_socket] + client_sockets, client_sockets, [])
        for current_socket in rlist:
            if current_socket is server_socket:
                connection, client_address = current_socket.accept()
                print("New client joined!", client_address)
                client_sockets.append(connection)
            else:
                valid_msg, cmd = protocol.get_msg(current_socket)
                if valid_msg:
                    if cmd == "":
                        print("Connection closed", )
                        client_sockets.remove(current_socket)
                        current_socket.close()
                        print_client_sockets(client_sockets)
                        del clients_names[current_socket] # added yesterday tired
                        # break
                    else:
                        # 2. Check if the command is valid, use "check_cmd" function
                        if check_cmd(cmd):
                            print(cmd)
                            # 3. If valid command - create response
                            socket_, response = create_server_rsp(current_socket, cmd)
                            reply = protocol.create_msg(response)
                            messages_to_send.append((socket_, reply))
                else:
                    response = "Wrong protocol"
                    messages_to_send.append((socket_, response))
                    current_socket.recv(1024)  # Attempt to empty the socket from possible garbage

                # Send response to the client
                # reply = protocol.create_msg(response)

                # current_socket.send(reply.encode())

            for message in messages_to_send:
                current_socket, data = message
                if current_socket in wlist:
                    current_socket.send(data.encode())
                    messages_to_send.remove(message)


if __name__ == '__main__':
    main()

'''
 valid_msg, cmd = protocol.get_msg(client_socket)
        if valid_msg:
            # 1. Print received message
            print("Received message")
            # 2. Check if the command is valid, use "check_cmd" function
            if check_cmd(cmd):
                # 3. If valid command - create response
                response = create_server_rsp(cmd)
            else:
                response = "Wrong server response"
        else:
            response = "Wrong protocol"
            client_socket.recv(1024)  # Attempt to empty the socket from possible garbage

        # Send response to the client
        reply = protocol.create_msg(response)
        client_socket.send(reply.encode())

        # If EXIT command, break from loop
        if response == "EXIT":
            break
'''
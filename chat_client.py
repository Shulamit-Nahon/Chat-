import msvcrt
import select
import socket
import protocol
MAX_MSG_LENGTH = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
print("Pls enter commands")
user_input = ""
while user_input != "EXIT":

    rlist, wlist, xlist = select.select([my_socket], [my_socket], [], 0.1)
    for current_socket in rlist:
        if current_socket is my_socket:
            valid, response = protocol.get_msg(current_socket)
            if valid:
                print("Server sent:", response)
            else:
                print("Response not valid")
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode()
            print(char , end="", flush=True)
            user_input += char
            if char == "\r":
                message = protocol.create_msg(user_input)
                my_socket.send(message.encode())
                valid, response = protocol.get_msg(my_socket)
                if response=="":
                    break
                if valid:
                    print("\nServer sent:", response)
                    user_input = ""
                    print("Pls enter commands")
my_socket.close()

'''
client from class
msg = input("Pls enter message\n")
while msg != "EXIT":
    my_socket.send(msg.encode())
    data = my_socket.recv(1024).decode()
    print("Server replied:", data)
    msg = input("Pls enter message\n")
    
---------------------------------------- 
client with protocol
import socket
import protocol

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
user_input = input("Pls enter commands\n")
while user_input != "EXIT":

    # 1. Add length field ("HELLO" -> "04HELLO")
    message = protocol.create_msg(user_input)
    # 2. Send it to the server
    my_socket.send(message.encode())
    # 3. Get server's response
    valid, response = protocol.get_msg(my_socket)
    # 4. If server's response is valid, print it
    if valid:
        print("Server replied:", response)
    else:
        print("Response not valid")
    # 5. If command is EXIT, break from while loop
    user_input = input("Pls enter commands\n")
    
    
    
    np exit 
    -------------------
    import msvcrt
import select
import socket
import protocol
MAX_MSG_LENGTH = 1024

my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.connect(("127.0.0.1", 5555))
print("Pls enter commands")
user_input = ""
while user_input != "EXIT":

    rlist, wlist, xlist = select.select([my_socket], [my_socket], [], 0.1)
    for current_socket in rlist:
        if current_socket is my_socket:
            valid, response = protocol.get_msg(current_socket)
            if valid:
                print("Server sent:", response)
            else:
                print("Response not valid")
    while True:
        if msvcrt.kbhit():
            char = msvcrt.getch().decode()
            print(char , end="", flush=True)
            user_input += char
            if char == "\r":
                message = protocol.create_msg(user_input)
                my_socket.send(message.encode())
                valid, response = protocol.get_msg(my_socket)
                if valid:
                    print("\nServer sent:", response)
                    user_input = ""
                    print("Pls enter commands")
my_socket.close()


---- yocheved

'''
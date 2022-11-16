"""EX 2.6 protocol implementation
   Author: Shulamit Nahon - 323782854
   Date: 04.11.22
   Possible client commands:
   NUMBER - server should reply with a random number, 0-99
   HELLO - server should reply with the server's name, anything you want
   TIME - server should reply with time and date
   EXIT - server should send acknowledge and quit
"""

LENGTH_FIELD_SIZE = 2
PORT = 8820


def create_msg(data):
    """Create a valid protocol message, with length field"""
    if data == "":
        return data
    return str(len(data)).zfill(LENGTH_FIELD_SIZE) + data


def get_msg(my_socket):
    """Extract message from protocol, without the length field
       If length field does not include a number, returns False, "Error" """
    length = str(my_socket.recv(LENGTH_FIELD_SIZE).decode())
    if length.isdigit():
        message = my_socket.recv(int(length)).decode()
        return True, message
    return False, "ERROR"

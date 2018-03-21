def check_message(path):
    with open(path, 'rb') as reader:
        data = reader.read()
    key = 0xE8
    byte_data = [ord(c) for c in data]
    bytes_to_xor = min(byte_data[0], len(byte_data)-2)
    offset = 2
    for i in range(len(byte_data)-2):
    	if i == 0:
    		xor_res = byte_data[i+offset] ^ key
    	else:
    		xor_res ^= byte_data[i+offset]
    return xor_res == byte_data[1]


def main(argv):
    if len(argv) != 2:
        print('USAGE: python {} <msg-file>'.format(argv[0]))
        return -1
    path = argv[1]
    if check_message(path):
        print('valid message')
        return 0
    else:
        print('invalid message')
        return 1


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

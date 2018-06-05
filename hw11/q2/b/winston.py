import socket
from Crypto.Cipher import AES

MESSAGE = "I love you"

def send_message(ip, port):
    # TODO: Reimplement me! (question 2b)
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        cipher = init_aes_chiper() # init chiper object
        message_padd = pad_message(MESSAGE) # add padding to message before encryption
        cipher_message = cipher.encrypt(message_padd) # encrpyt
        connection.send(cipher_message)
    finally:
        connection.close()

def init_aes_chiper(key="462D4A614E645267556B587032733575", mode=AES.MODE_CBC, IV="38856934446DD6E8"):
	'''
    function to init an AES chiper object with a defualt key mode and IV
    '''
	return AES.new(key, mode, IV)

def pad_message(message):
	'''
	add padding using the pkcs7 shceme
	we will always add a padding using this scheme (1 to 16 bytes of padding)
	'''
	padd_len = 16 - (len(message) % 16)
	message_padd = message + chr(padd_len) * padd_len # added the padding length ascii value char as many times as needed
	return message_padd

def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()

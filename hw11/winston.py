import socket
from Crypto.Cipher import AES

MESSAGE = "I love you"

def send_message(ip, port):
    # TODO: Reimplement me! (question 2b)
    connection = socket.socket()
    try:
        connection.connect((ip, port))
        cipher = init_aes_chiper()
        message_padd = pad_message(MESSAGE)
        cipher_message = cipher.encrypt(message_padd)
        connection.send(cipher_message)
    finally:
        connection.close()

def init_aes_chiper(key="462D4A614E645267556B587032733575", mode=AES.MODE_CBC, IV="38856934446DD6E8"):
	return AES.new(key, mode, IV)

def pad_message(message):
	padd_len = 16 - (len(message) % 16)
	message_padd = message + chr(padd_len) * padd_len
	return message_padd

def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()

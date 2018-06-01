import socket
from Crypto.Cipher import AES

def receive_message(port):
    # TODO: Reimplement me! (question 2b)
    listener = socket.socket()
    try:
        listener.bind(('', port))
        listener.listen(1)
        connection, address = listener.accept()
        try:
            cipher_message = connection.recv(1024)
            cipher = init_aes_chiper()
            plain_message_padd = cipher.decrypt(cipher_message)
            plain_message = unpad_message(plain_message_padd)
            print cipher_message, plain_message
            return plain_message
        finally:
            connection.close()
    finally:
        listener.close()

def init_aes_chiper(key="462D4A614E645267556B587032733575", mode=AES.MODE_CBC, IV="38856934446DD6E8"):
    return AES.new(key, mode, IV)

def unpad_message(padd_message):
    padd_len = ord(padd_message[-1])
    message = padd_message[:-padd_len]
    return message

def main():
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()

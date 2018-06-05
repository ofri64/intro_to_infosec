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
            cipher_message = connection.recv(1024) # receive message
            cipher = init_aes_chiper() # init the AES chiper object
            plain_message_padd = cipher.decrypt(cipher_message) # decrpyt with secret key
            plain_message = unpad_message(plain_message_padd) # remove padding
            return plain_message
        finally:
            connection.close()
    finally:
        listener.close()

def init_aes_chiper(key="462D4A614E645267556B587032733575", mode=AES.MODE_CBC, IV="38856934446DD6E8"):
    '''
    function to init an AES chiper object with a defualt key mode and IV
    '''
    return AES.new(key, mode, IV)

def unpad_message(padd_message):
    '''
    remove padding (after decryption)
    using the pkcs7 scheme we will always have padding
    '''
    padd_len = ord(padd_message[-1]) # padding length is the decimal value of the last char
    message = padd_message[:-padd_len] # slice the message to remove padding
    return message

def main():
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()

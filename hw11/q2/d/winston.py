from scapy.all import *
import socket
import base64

# the Alpahbet for base64 encoding
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# dictionary for translating each base64 character to 6 bits string
B64_CHAR_BIT_ENCODING = dict([(ALPHABET[i], '{0:06b}'.format(i))for i in range(64)])

MESSAGE = 'I love you'

def send_message(ip, port):
    # TODO: Reimplement me! (question 2d)
    message_encdoed_bits = encode_message_to_bits_string(MESSAGE) 
    message_encdoed_bits_len = len(message_encdoed_bits) # how many bits in the message
    total_triplets = message_encdoed_bits_len / 3 # always divided by 3!
    triplets = [message_encdoed_bits[i-3:i] for i in range(3, message_encdoed_bits_len+3, 3)]

    # send a separate tcp packet for each triplet
    for i in range(total_triplets):
    	triplet = triplets[i]
    	reserved_value = int(triplet,2) # encode the triplet as the reserved bits
    	packet = IP(dst=ip) / TCP(dport=port,sport=65000, 
    		flags='A',reserved=reserved_value, seq=i, ack=total_triplets) # seq indicates current message index
    	send(packet)


def encode_message_to_bits_string(message):
	'''
	Return a string representing the bits of the base64 encoding of the message
	Beacuse the bits represent base64 chars the nubmer of bits will always divide by 6 (and thus also by 3)
	'''
	message_bits = ""
	b64_encoded_message = base64.b64encode(message) # first encdode to base64
	for b64_char in b64_encoded_message: # then encode each base64 encoded character to 6 bits string
		if b64_char != '=': # padding will be considered during decoding
			message_bits += B64_CHAR_BIT_ENCODING[b64_char]
	return message_bits

def decode_message_bits_to_string(message_bits):
	'''
	Accepts as input a string representing the bits of the base64 encoding of the message
	and returns the original message
	'''
	base64_message = ""
	for i in range(6, len(message_bits)+6, 6): # iterate over sequences of 6 bits
		six_bits = message_bits[i-6:i]
		b64_char = B64_CHAR_BIT_DECODING[six_bits] # translate 6 bits back to base64 encoded char using our dictionary
		base64_message += b64_char

	# now we have a base64 encoded message - but still need to handle padding
	base64_message_len = len(base64_message)

	reminder = base64_message_len % 4 # if there is no need for padding this will be 0, else we need padding
	if reminder > 0: 
		base64_padded_message_len = (base64_message_len - reminder + 4)
		padding_bytes_needed = base64_padded_message_len - base64_message_len
		base64_message += '=' * padding_bytes_needed # add '=' times the number of bytes we need to padd 

	# now we have a valid base64 encoded messagge, including padding - now we just need to decode it
	message = base64.b64decode(base64_message)
	return message


def main():
    send_message('127.0.0.1', 1984)


if __name__ == '__main__':
    main()

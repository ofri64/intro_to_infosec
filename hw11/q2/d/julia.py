from scapy.all import *
import socket
import base64

# the Alpahbet for base64 encoding
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

# dictionary for translating 6 bits strings to base64 characters
B64_CHAR_BIT_DECODING = dict([('{0:06b}'.format(i), ALPHABET[i])for i in range(64)])

# global variables to use in packet handler and stop filter functions
message_bits_array = None
total_packets = None


def receive_message(port):
    # TODO: Reimplement me! (question 2d)
	sniff(lfilter=packet_filter, prn=handle_data, stop_filter=stop_packet_filter)

	# At this point all the packets arrived and the encoded bits are save in the data array
	message_bits_string = "".join(message_bits_array) # join to bits string
	message = decode_message_bits_to_string(message_bits_string) # decode it and return
	return message

def packet_filter(packet):
	'''
	filter only packet with TCP layer, with source port 65,000 (i.e from winston presumably)
	'''
	tcp_layer = packet.getlayer(TCP)
	if tcp_layer and tcp_layer.sport == 65000:
		return True

	return False

def handle_data(packet):
	'''
	itercept packet, collect encoded data from the reserved bits and aggregate them in an array
	'''
	tcp_layer = packet.getlayer(TCP)
	global message_bits_array # have to indicate we are going to change our global/out of functin scop variable
	global total_packets # another global variable
	if not message_bits_array: # first message presumably - initiate data array
		total_packets = tcp_layer.ack
		message_bits_array = [0] * total_packets
	index = tcp_layer.seq
	pckt_message = '{0:03b}'.format(tcp_layer.reserved) # convert from int to 3 bits string
	message_bits_array[index] = pckt_message # add to data array

def stop_packet_filter(packet):
	'''
	Julia want to stop sniffing after ensuring she got all the packets
	after the global variable 'total packets' was initiated is tells how many packets the message includes 
	'''
	tcp_layer = packet.getlayer(TCP)
	if tcp_layer and tcp_layer.sport == 65000 and total_packets:
		if tcp_layer.seq == total_packets - 1: # stop if it is the last packet - using seq number in the tcp header
			return True

	return False

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
    message = receive_message(1984)
    print('received: %s' % message)


if __name__ == '__main__':
    main()

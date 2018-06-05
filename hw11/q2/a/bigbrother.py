from scapy.all import *


LOVE = 'love'
unpersons = set()


def spy(packet):
    """Check for love packets.

    For each packet containing the word 'love', add the packet to the
    `unpersons` set.
    """
    # TODO: Implement me (question 2a)
    raw_data = packet.getlayer(Raw) # check if packet contains data layer
    if raw_data:
    	str_data = str(raw_data)
    	if LOVE in str_data: # look for the work love in the data layer
    		unpersons.add(packet) # add the entire packet to the unpersons set

    		# ip = packet.getlayer(IP)
    		# src_ip = ip.src
    		# unpersons.add(src_ip)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()

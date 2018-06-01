import math
from scapy.all import *


LOVE = 'love'
unpersons = set()
ENTROPY_THRESHOLD = 3.0


def spy(packet):
    """Check for love packets and encrypted packets.

    For each packet containing the word 'love' (or a packet which is encrypted),
    add the packet to the `unpersons` set.
    """
    # TODO: Implement me (question 2c)
    raw_data = packet.getlayer(Raw)
    if raw_data:
        str_data = str(raw_data)
        if LOVE in str_data:
            unpersons.add(packet)
            print "packet added becasue of love"
        else:
            payload_entropy = entropy(str_data)
            if payload_entropy > ENTROPY_THRESHOLD:
                unpersons.add(packet)
                print payload_entropy
                print "packet added because of entropy"


def entropy(string):
    distribution = [float(string.count(c)) / len(string)
                    for c in set(string)]
    return -sum(p * math.log(p) / math.log(2.0) for p in distribution)


def main():
    sniff(prn=spy)


if __name__ == '__main__':
    main()

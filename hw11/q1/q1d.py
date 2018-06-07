from scapy.all import *


def on_packet(packet):
    """Implement this to send a SYN ACK packet for every SYN."""
    # TODO: Implement me
    # WARNING: Use only the `send` function from scapy to send the packet. Do
    #          not use any other function to send/receive packets.
    tcp_layer = packet.getlayer(TCP)
    if not tcp_layer or tcp_layer.flags != 2:
        return # don't replay if it is not a TCP SYN packet

    # Extract from incoming packet fileds we need to send via our response
    dts_ip = packet[IP].src
    dst_port = packet.sport
    src_port = packet.dport
    ack_value = packet.seq + 1

    # Craft a SYN + ACK response and sent it
    response = IP(dst=dts_ip) / TCP(sport=src_port, dport=dst_port, seq=0, ack=ack_value, flags='SA')
    send(response)

def main(argv):
    sniff(prn=on_packet)


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))


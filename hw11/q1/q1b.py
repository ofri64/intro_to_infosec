import time
from scapy.all import *


WINDOW       = 60
MAX_ATTEMPTS = 15


# Initialize your data structures here
# TODO: Initialize your data structures

class SynNode():
    '''
    A node of a linked list representing a SYN request sent in a specific timestamp
    '''
    def __init__(self, timestamp):
        self.timestamp = timestamp
        self.next = None

    def check_old_node(self, other_timestamp, window=WINDOW):
        '''
        Check if a specific node is "too old" meaning it's timestamp is not inside
        the given window infered by the timestamp given
        parameters:
        other_timestamp - a datetime.datetime object
        window = window size in seconds unit
        '''
        diff_seconds = other_timestamp - self.timestamp # subtructing two dateime object result in timedelta object
        return diff_seconds > window # check whether delta total seconds is greater than window

class LinkedList():
    '''
    A linked list of Syn nodes.
    holds pointers to the head and tail of the list and a counter for numer of nodes in the list
    '''
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
        self.total_requests_window = 0

    def remove_old_requests(self, timestamp):
        '''
        Iterate over the nodes in the list and check if a node is outside the current timeframe window
        the nodes are sorted in ascending order so when we reach a node that is inside the window 
        we can stop the iterator.
        '''
        if not self.head:
            return
        current_node = self.head
        while current_node is not None and current_node.check_old_node(timestamp):
            next_node = current_node.next
            self.head = next_node # effectively remove current node from list
            current_node = next_node
            self.total_requests_window -= 1 # must not forget to decrease total nodes counter by one

    def add_request_log(self, timestamp):
        '''
        Create a new SynNode and add it to the end of our list
        '''
        node = SynNode(timestamp)
        if not self.head: # if it is the first node in our list
            self.head = node
            self.tail = node
            self.total_requests_window += 1
        else: # just update tail
            self.tail.next = node
            self.tail = node
            self.total_requests_window += 1

ip_syn_lists = {} # dictionary for every ip key - value will be timestamps list

blocked = set()  # We keep blocked IPs in this set


def on_packet(packet):
    """This function will be called for each packet.
    Use this function to analyze how many packets were sent from the sender
    during the last window, and if needed, call the 'block(ip)' function to
    block the sender."""
    # TODO: Implement me
    # WARNING: You must call block(ip) to do the blocking.
    tcp = packet.getlayer(TCP) # ignore icmp and so on
    if not tcp:
        return
    tcp_flags = tcp.flags
    if not tcp_flags == 2: # It is not a tcp SYN packet - ignore
        return
    src_ip = packet[IP].src

    # now use our linked list data structure to check how many requests were sent by this ip
    # current_timestamp will be our 'point in time' for checking the logic

    if src_ip not in ip_syn_lists:
        ip_syn_lists[src_ip] = LinkedList() # creaete new list if the it is the first SYN request from this ip

    ip_lst = ip_syn_lists[src_ip]
    current_timestamp = int(time.time())
    ip_lst.remove_old_requests(current_timestamp) # first we remove old requests
    ip_lst.add_request_log(current_timestamp) # then add current SYN request to list


    if is_blocked(src_ip):
        return # no need to add an iptable rule if this ip is already blocked

    if ip_lst.total_requests_window > MAX_ATTEMPTS: # if the list is too long block the ip 
            block(src_ip) # add a rule to block this ip

def generate_block_command(ip):
    """Generate a command that when executed in the shell, blocks this IP.
    The blocking will be based on `iptables` and must drop all incoming traffic
    from the specified IP."""
    # TODO: Implement me
    return 'iptables -A INPUT -p tcp -s {0} -j DROP'.format(ip)


def block(ip):
    os.system(generate_block_command(ip))
    blocked.add(ip)


def is_blocked(ip):
    return ip in blocked


def main():
    sniff(prn=on_packet)


if __name__ == '__main__':
    main()
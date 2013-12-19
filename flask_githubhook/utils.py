import socket
import struct


def ip_to_int(ip):
    "Convert decimal dotted quad string to long integer."
    if isinstance(ip, int):
        return ip
    return struct.unpack('!I', socket.inet_aton(ip))[0]

def network_mask(ip, bits):
    "Convert a network address to a long integer." 
    return ip_to_int(ip) & ((2 << bits - 1) - 1)

def addr_in_network(ip, net):
    "Is an address in a network."
    return ip_to_int(ip) & net == net

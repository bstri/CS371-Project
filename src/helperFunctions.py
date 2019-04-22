import socket


def getsrcdst(pkt):
    """Extract src and dst addresses"""
    srcport = ''
    dstport = ''
    if 'TCP' in pkt:
        srcport = pkt['TCP'].sport
        dstport = pkt['TCP'].dport
    if 'UDP' in pkt:
        srcport = pkt['UDP'].sport
        dstport = pkt['UDP'].dport

    if 'IP' in pkt:
        return pkt['IP'].src, srcport, pkt['IP'].dst, dstport
    if 'IPv6' in pkt:
        return pkt['IPv6'].src, srcport, pkt['IPv6'].dst, dstport
    if 'ARP' in pkt:
        return pkt['ARP'].psrc, srcport, pkt['ARP'].pdst, dstport
    raise TypeError()


def getProtocol(pkt):
    if 'TCP' in pkt:
        return 'TCP'
    elif 'UDP' in pkt:
        return 'UDP'
    # elif 'ICMP' in pkt:
    #     return 'ICMP'
    else:
        return 'other'


def getLocalMachineIP():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    localIP = s.getsockname()[0]
    s.close()
    return localIP

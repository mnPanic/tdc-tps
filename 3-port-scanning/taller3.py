#!/usr/bin/env python3

import sys
import scapy.all as scp

# 53: dns
# 80: http
ports = [19, 20, 21, 22, 23, 53, 80]
ip = sys.argv[1]

# ack  syn
# 0001 0010
TCP_FLAG_SYN_ACK = 0x12

# ack  rst
# 0001 0100
TCP_FLAG_RST_ACK = 0x14

ICMP_TYPE_DEST_UNREACHABLE = 3
ICMP_CODE_PORT_UNREACHABLE = 3

def scan_tcp(port: int) -> str:
    p = scp.IP(dst=ip)/scp.TCP(dport=port, flags='S')
    resp = scp.sr1(p, verbose=False, timeout=1.0)

    if not resp:
        return "filtrado"

    if resp.haslayer(scp.TCP):
        tcp_layer = resp.getlayer(scp.TCP)

        if tcp_layer.flags == TCP_FLAG_SYN_ACK:
            scp.sr1(scp.IP(dst=ip)/scp.TCP(dport=port, flags='AR'), verbose=False, timeout=1)
            return f"abierto {tcp_layer.flags}"
        elif tcp_layer.flags == TCP_FLAG_RST_ACK:
            return f"cerrado {tcp_layer.flags}"

def scan_udp(port: int) -> str:
    # https://nmap.org/book/scan-methods-udp-scan.html
    p = scp.IP(dst=ip)/scp.UDP(sport=port, dport=port)
    resp = scp.sr1(p, verbose=False, timeout=1.0)

    if not resp:
        return "abierto|filtrado"

    if resp.haslayer(scp.UDP):
        return "abierto"
    
    if resp.haslayer(scp.ICMP):
        icmp_layer = resp.getlayer(scp.ICMP)
        if icmp_layer.type == ICMP_TYPE_DEST_UNREACHABLE:
            if icmp_layer.code == ICMP_CODE_PORT_UNREACHABLE:
                return "cerrado"
            
            return "filtrado"
    
    # Que paso?
    print(resp.summary())

for i in ports:
    print(i, end='')

    # tcp
    print("/ TCP ", end='')
    result = scan_tcp(i)
    print(result, end='')
    
    # udp
    print(" / UDP ", end = '')
    result = scan_udp(i)
    print(result)

   
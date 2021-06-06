#!/usr/bin/env python3

import csv
import sys
import scapy.all as scp
from multiprocessing import Pool

from typing import Tuple

# 53: dns
# 80: http
#ports = [19, 20, 21, 22, 23, 53, 80]
ports = range(1, 1025)

well_known = {
    21: "FTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
}

# https://en.wikipedia.org/wiki/Transmission_Control_Protocol
TCP_FLAG_SYN_ACK = 0x12 # 0001 (ack) 0010 (syn)
TCP_FLAG_RST_ACK = 0x14 # 0001 (ack) 0100 (rst)

# https://en.wikipedia.org/wiki/Internet_Control_Message_Protocol
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
    resp = scp.sr1(p, verbose=False, timeout=0.3)

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

def scan_port(port: int) -> Tuple[int, dict]:
    # tcp
    result_tcp = scan_tcp(port)
    
    # udp
    result_udp = scan_udp(port)

    output = str(port)
    if port in well_known:
        output += f" ({well_known[port]})"
    
    if result_tcp != "filtrado" or result_udp != "abierto|filtrado":
        output += f"/ TCP {result_tcp} / UDP {result_udp}"
        print(output)
    
    return port, {"tcp": result_tcp, "udp": result_udp}

if __name__ == "__main__":
    ip = sys.argv[1]
    with open(f"out/results-{ip}.csv", "w+") as w:
        print("port,tcp,udp", file=w)
        with Pool(processes=16) as pool:
            results = pool.map(scan_port, ports)
            for (port, result) in results:
                print(f"{port},{result['tcp']},{result['udp']} ", file=w)

   
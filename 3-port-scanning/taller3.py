#!/usr/bin/env python3


import sys
import scapy.all as scp
import os.path
from typing import Tuple
from multiprocessing import Pool

import pandas as pd

# 53: dns
# 80: http
#ports = [19, 20, 21, 22, 23, 53, 80]
ports = range(1, 1025)

# https://en.wikipedia.org/wiki/List_of_TCP_and_UDP_port_numbers
well_known = {
    21: "FTP",
    53: "DNS",
    80: "HTTP",
    443: "HTTPS",
    853: "DNS TLS",
    162: "SNMPTRAP",
    201: "AppleTalk"
}

# https://en.wikipedia.org/wiki/Transmission_Control_Protocol
TCP_FLAG_SYN_ACK = 0x12
TCP_FLAG_RST_ACK = 0x14

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

    if resp.haslayer(scp.ICMP):
        icmp_layer = resp.getlayer(scp.ICMP)
        return f"filtrado (icmp t:{icmp_layer.type} c:{icmp_layer.code})"

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
            
            return f"filtrado {icmp_layer.code}"

    # Que paso?
    print(resp.summary())

def print_scan_result(port: int, result_udp: str, result_tcp: str):
    output = str(port)
    if port in well_known:
        output += f" ({well_known[port]})"
    
    if result_tcp != "filtrado" or result_udp != "abierto|filtrado":
        output += f"/ TCP {result_tcp} / UDP {result_udp}"
        print(output)

def scan_port(port: int) -> Tuple[int, dict]:
    # tcp
    result_tcp = scan_tcp(port)
    
    # udp
    result_udp = scan_udp(port)

    print_scan_result(port, result_udp, result_tcp)
    return port, {"tcp": result_tcp, "udp": result_udp}

if __name__ == "__main__":
    ip = sys.argv[1]
    filename = f"out/results-{ip}.csv"
    if not os.path.exists(filename):
        with open(filename, "w+") as w:
            print("port,tcp,udp", file=w)
            with Pool(processes=16) as pool:
                results = pool.map(scan_port, ports)
                for (port, result) in results:
                    print(f"{port},{result['tcp']},{result['udp']}", file=w)

    with open(filename) as f:
        count_by_result = {"tcp": {}, "udp": {}} # tcp|udp: {result: count}
        for line in f.readlines()[1:]:
            port, tcp_result, udp_result = line[:-1].split(',')
            print_scan_result(port, udp_result, tcp_result)
    
    df = pd.read_csv(filename)
    print("tcp\n", df["tcp"].value_counts())
    print("udp\n", df["udp"].value_counts())

"""
- distribucion de abiertas / cerradas / filtradas / etc.
- (nueva) que protocolos devuelven respuesta significativa.
- criterios de firewall
"""
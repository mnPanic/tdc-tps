#!/usr/bin/env python3

MAX_PACKETS = 15000
MAX_PACKETS_S2 = 100

import math
import scapy.all as scapy

S1 = {}
S2_src = {}
S2_dst = {}
S2_hw_dst = {}
S2_hw_src = {}
ops = {}

def mostrar_fuente(S):
    N = sum(S.values())
    simbolos = sorted(S.items(), key=lambda x: -x[1])
    print("\n".join([ f"{d}: p: {k/N:.5f}, i: {-math.log(k/N, 2):.5f}" for d,k in simbolos ]))
    
    entropia = 0
    for _, k in simbolos:
        entropia += -math.log(k/N, 2) * k/N

    print("Entropia:", entropia)
    print(N)
    print()

def analyze_pkg(pkt):
    if pkt.haslayer(scapy.Ether):
        dire = "BROADCAST" if pkt[scapy.Ether].dst=="ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[scapy.Ether].type       # El campo type del frame tiene el protocolo
        s_i = (dire, proto)                 # Aca se define el simbolo de la fuente

    if s_i not in S1:
        S1[s_i] = 0.0

    S1[s_i] += 1.0

def analyze_pkg_S2(pkt):
    arp_pkt = pkt[scapy.ARP]
    hw_src = arp_pkt.hwsrc
    hw_dst = arp_pkt.hwdst
    ip_src = arp_pkt.psrc
    ip_dst = arp_pkt.pdst

    if ip_dst not in S2_dst:
        S2_dst[ip_dst] = 0
    
    S2_dst[ip_dst] += 1

    if ip_src not in S2_src:
        S2_src[ip_src] = 0
    
    S2_src[ip_src] += 1
    
    if hw_dst not in S2_hw_dst:
        S2_hw_dst[hw_dst] = 0
    
    S2_hw_dst[hw_dst] += 1

    if hw_src not in S2_hw_src:
        S2_hw_src[hw_src] = 0
    
    S2_hw_src[hw_src] += 1

    # https://github.com/secdev/scapy/blob/11832deee0067e1db2660ff1f61e5d4e979adf27/scapy/layers/l2.py#L391
    if arp_pkt.op not in ops:
        ops[arp_pkt.op] = 0
    
    ops[arp_pkt.op] += 1


def callback_s2(pkt):
    analyze_pkg_S2(pkt)

    print("src:")
    mostrar_fuente(S2_src)
    print("dst:")
    mostrar_fuente(S2_dst)
    print("src_hw:")
    mostrar_fuente(S2_hw_src)
    print("dst_hw:")
    mostrar_fuente(S2_hw_dst)

    print("ARP operations")
    print(ops)

    if sum(S2_src.values()) == MAX_PACKETS_S2:
        quit()

def callback(pkt):
    analyze_pkg(pkt)
    mostrar_fuente(S1)

    if sum(S1.values()) == MAX_PACKETS:
        quit()

def main():
    #scapy.sniff(prn=callback)
    scapy.sniff(prn=callback_s2, filter="arp", store=0)

if __name__ == "__main__":
    main()


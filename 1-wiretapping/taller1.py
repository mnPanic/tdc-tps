#!/usr/bin/env python3

"""
extender el código para que calcule la información de cada símbolo y la entropía
de la fuente.
"""

import math
import scapy.all as scapy

S1 = {}

def mostrar_fuente(S):
    N = sum(S.values())
    simbolos = sorted(S.items(), key=lambda x: -x[1])
    print("\n".join([ f"{d}: p: {k/N:.5f}, i: {-math.log(k/N):.5f}" for d,k in simbolos ]))
    
    entropia = 0
    for _, k in simbolos:
        entropia += -math.log(k/N) * k/N

    print("Entropia:", entropia)
    print(N)
    print()

    if N > 15000:
        quit()

def analyze_pkg(pkt):
    if pkt.haslayer(scapy.Ether):
        dire = "BROADCAST" if pkt[scapy.Ether].dst=="ff:ff:ff:ff:ff:ff" else "UNICAST"
        proto = pkt[scapy.Ether].type       # El campo type del frame tiene el protocolo
        s_i = (dire, proto)                 # Aca se define el simbolo de la fuente

    if s_i not in S1:
        S1[s_i] = 0.0

    S1[s_i] += 1.0

def callback(pkt):
    analyze_pkg(pkt)
    mostrar_fuente(S1)

def main():
    # Para filtrar
    # sniff(prn=arp_monitor_callback, filter="arp", store=0)
    scapy.sniff(prn=callback)


if __name__ == "__main__":
    main()


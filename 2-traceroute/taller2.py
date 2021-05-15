#!/usr/bin/env python3

import statistics
import sys
import scapy.all as scp
import time


TTL_MAX = 31
ITERATIONS = 5

hops = [{} for i in range(TTL_MAX)]
output = [{} for i in range(TTL_MAX)]

print("HOLA, ESTE ES EL TP DE TRACEROUTE")
print()

for ttl in range(1, TTL_MAX):
    for i in range(ITERATIONS):
        request = scp.IP(dst=sys.argv[1], ttl=ttl) / scp.ICMP()

        t_i = time.time()
        response = scp.sr1(request, verbose=False, timeout=0.8)
        t_f = time.time()

        rtt = (t_f - t_i)*1000

        if response is not None:
            ip = response.src

            if ip not in hops[ttl]:
                hops[ttl][ip] = []

            hops[ttl][ip].append(rtt)

    if hops[ttl] != {}:
        max_key, max_value = max(hops[ttl].items(), key=lambda t : len(t[1]))

        output[ttl] = {
            "IP": max_key,
            "median": statistics.median(max_value),
            "sd": statistics.stdev(max_value),
        }

        print(f'{ttl:2} {output[ttl]["IP"]:15} \t\t {output[ttl]["median"]:.2f} ms \t {output[ttl]["sd"]:.2f} ms')
    else:
        print(f'{ttl:2} * * *')
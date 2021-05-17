#!/usr/bin/env python3

import statistics
import sys
import scapy.all as scp
import time

from typing import List, Dict, Tuple

TTL_MAX = 30
ITERATIONS = 5

def stdev(l: List[float]):
    if len(l) == 1:
        return 0

    return statistics.stdev(l)

def traceroute(dst_ip: str) -> Tuple[List[Dict[str, List[float]]], List[Dict[str, dict]]]:

    hops = [{} for i in range(TTL_MAX + 1)]
    hops_stats = [{} for i in range(TTL_MAX + 1)]

    for ttl in range(1, TTL_MAX + 1):
        for i in range(ITERATIONS):
            request = scp.IP(dst=dst_ip, ttl=ttl) / scp.ICMP()

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

            hops_stats[ttl] = {
                "IP": max_key,
                "median": statistics.median(max_value),
                "sd": stdev(max_value),
            }

            print(f'{ttl:2} {hops_stats[ttl]["IP"]:15} \t\t {hops_stats[ttl]["median"]:.2f} ms \t {hops_stats[ttl]["sd"]:.2f} ms')
        else:
            print(f'{ttl:2} * * *')

    return hops, hops_stats

def rtt_hops(hops_stats: List[Dict[str, dict]]) -> List[float]:
    print()
    print("RTT por saltos")

    rtt_hops = []

    for ttl in range(1, TTL_MAX):
        if "median" not in hops_stats[ttl]:
            rtt_hops.append(-1)
            continue

        actual_rtt = hops_stats[ttl]["median"]
        next_rtt = 0

        for next_ttl in range(ttl, TTL_MAX):
            if "median" not in hops_stats[next_ttl]:
                continue

            next_rtt = hops_stats[next_ttl]["median"]

            if next_rtt - actual_rtt > 0:
                break

        rtt_hops.append(next_rtt - actual_rtt)

    for step, rtt_hop in enumerate(rtt_hops):
        print(f'{step+1:2} {rtt_hop:.2f}')

if __name__ == "__main__":
    _, stats = traceroute(sys.argv[1])
    rtt_hops(stats)
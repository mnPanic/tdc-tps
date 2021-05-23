#!/usr/bin/env python3

import click
import ipinfo
import json
import os
import os.path
import statistics
import sys
import scapy.all as scp
import time

from typing import List, Dict, Tuple

TTL_MAX = 30
ITERATIONS = 5

def get_ipinfo_at():
    at = os.getenv("IPINFO_ACCESS_TOKEN")
    if at is None:
        raise Exception("No esta seteada la env IPINFO_ACCESS_TOKEN con el access token de ipinfo.io")


ipinfo_access_token = get_ipinfo_at()

def stdev(l: List[float]):
    if len(l) == 1:
        return 0

    return statistics.stdev(l)


Hops = List[Dict[str, List[float]]]
Stats = List[Dict[str, dict]]

def traceroute(dst_ip: str) -> Tuple[Hops, Stats]:

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

def d_rtt(hops_stats: Stats):
    print()
    print("RTT por saltos")

    for ttl in range(1, TTL_MAX):
        if "median" not in hops_stats[ttl]:
            continue

        actual_rtt = hops_stats[ttl]["median"]
        next_rtt = -1

        for next_ttl in range(ttl, TTL_MAX):
            if "median" not in hops_stats[next_ttl]:
                continue

            next_rtt = hops_stats[next_ttl]["median"]

            if next_rtt - actual_rtt > 0:
                break

        if next_rtt == -1:
            continue

        hops_stats[ttl]["d_rtt"] = next_rtt - actual_rtt

def view_d_rtt(stats: Stats):
    for step, rtt_hop in enumerate(hops_stats):
        print(f"{step+1:2} {hops_stats[step]['d_rtt']:.2f}")

def serialize(ip: str, hops: Hops, stats: Stats):
    with open(f"out/{ip}-hops.json", 'w+') as f:
        json.dump(hops, f)
    
    with open(f"out/{ip}-stats.json", 'w+') as f:
        json.dump(stats, f)

def deserialize(ip: str) -> Tuple[Hops, Stats]:
    with open(f"out/{ip}-hops.json", 'r') as f:
        hops = json.load(f)
    
    with open(f"out/{ip}-stats.json", 'r') as f:
        stats = json.load(f)
    
    return hops, stats

def get_ipinfo(ip: str) -> dict:
    """
    {
        "asn": "AS7303", 
        "city": "Buenos Aires", 
        "country": "Argentina", 
        "country_code": "AR", 
        "hostname": "213-30-137-186.fibertel.com.ar", 
        "ip": "186.137.30.213", 
        "latitude": -34.6011, 
        "longitude": -58.3847, 
        "organization": "Telecom Argentina S.A."
    }
    """
    handler = ipinfo.getHandler()
    # info.all devuelve todo como dict
    return handler.getDetails(ip)

def extend_with_geo(stats: Stats):
    for i, hop in enumerate(stats):
        if "IP" not in hop:
            continue

        info = get_ipinfo(hop["IP"])
        if "bogon" in info.all and info.bogon:
            continue
        
        
        hop["city"] = info.city
        hop["country_name"] = info.country_name
        hop["org"] = info.org

def view_route(stats: Stats):
    for i, hop in enumerate(stats):
        if "IP" not in hop:
            print(f"{i:2} *")
            continue

        ip = hop["IP"]
        median = hop["median"]
    
        if "city" not in hop:
            print(f"{i:2} {ip:<15} {median:.2f}")
            continue

        print(f"{i:2} {ip:<15} {median:.2f} ({hop['city']} - {hop['country_name']}, {hop['org']})")

if __name__ == "__main__":
    ip = sys.argv[1]
    # activate_hops = sys.argv[2]

    if not os.path.exists(f'out/{ip}-hops.json'):
        hops, stats = traceroute(ip)
        serialize(ip, hops, stats)

    hops, stats = deserialize(ip)
    # if activate_hops:
    extend_with_geo(stats)
    d_rtt(stats)
    view_d_rtt(stats)
    view_route(stats)

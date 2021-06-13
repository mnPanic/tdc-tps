import sys
import scapy.all as scp

from typing import List

# https://en.wikipedia.org/wiki/List_of_DNS_record_types
RECORD_TYPE_ADDRESS = "A"
RECORD_TYPE_CNAME = "CNAME"
RECORD_TYPE_MX = "MX"

TYPE_TO_CODE = {
    RECORD_TYPE_ADDRESS: 1,
    RECORD_TYPE_MX: 15,
}

ROOT_NAME_SERVERS = [
    ("198.41.0.4", "a.root-servers.net"),
    ("199.9.14.201", "b.root-servers.net"),
    ("192.33.4.12", "c.root-servers.net"),
    ("199.7.91.13", "d.root-servers.net"),
    ("192.203.230.10", "e.root-servers.net"),
    ("192.5.5.241", "f.root-servers.net"),
    ("192.112.36.4", "g.root-servers.net"),
    ("198.97.190.53", "h.root-servers.net"),
    ("192.36.148.17", "i.root-servers.net"),
    ("192.58.128.30", "j.root-servers.net"),
    ("193.0.14.129", "k.root-servers.net"),
    ("199.7.83.42", "l.root-servers.net"),
    ("202.12.27.33", "m.root-servers.net"),
]

def get_data(r: scp.DNSRR):
    if r.type == 15: # MX
        return r.exchange.decode()
    
    if r.type == 1: # A
        return r.rdata

    if r.type == 6: # SOA
        return "-"

    return r.rdata

def print_dns_record(r: scp.DNSRR):
    # Para saber los campos que tiene r.fields_desc
    # https://stackoverflow.com/questions/41490875/scapy-get-dnsqr-dnsrr-field-values-in-symbolic-string-form
    print(f"{r.rrname.decode()} {r.get_field('type').i2repr(r, r.type)} {get_data(r)}")  

def find_answer(answers: dict, qname: str, record_type: str, path: List[str]) -> str:
    """
    www.dc.uba.ar. CNAME b'www-1.dc.uba.ar.'
    www-1.dc.uba.ar. CNAME b'dc.uba.ar.'
    dc.uba.ar. A 157.92.27.128
    """

    r_type, r_data = answers[qname]
    if r_type == record_type:
        return r_data
    
    if r_type == RECORD_TYPE_CNAME:
        if r_data.decode() in answers:
            return find_answer(answers, r_data.decode(), record_type, path)        
    return None

def rqdns(qname: str, record_type: str):
    for ip, name in ROOT_NAME_SERVERS:
        ans, path = qdns(ip, name, qname, record_type, [ip])
        if ans is not None:
            return ans, path

    return None, None

def qdns(resolver_ip: str, resolver_name: str, qname: str, record_type: str, path: List[str]):
    print(f"\n\nQuerying DNS resolver {resolver_ip} ({resolver_name}) for qname {qname}")
    dns = scp.DNS(rd=0, qd=scp.DNSQR(qname=qname, qtype=record_type))
    udp = scp.UDP(sport=scp.RandShort(), dport=53)
    ip = scp.IP(dst=resolver_ip)

    answer = scp.sr1( ip / udp / dns , verbose=0, timeout=10)

    if answer and answer.haslayer(scp.DNS) and answer[scp.DNS].qd.qtype == TYPE_TO_CODE[record_type]:
        print("Answer")
        for i in range(answer[scp.DNS].ancount):
            print_dns_record(answer[scp.DNS].an[i])

        answers = {}
        for i in range(answer[scp.DNS].ancount):
            r = answer[scp.DNS].an[i]
            r_name = r.rrname.decode()
            r_type = r.get_field('type').i2repr(r, r.type)
            r_data = get_data(r)

            answers[r_name] = (r_type, r_data)

        # Find answer
        if qname in answers:
            ans = find_answer(answers, qname, record_type, path)
            if ans is not None:
                return ans, path

        print("Additional Records")
        additional_records = {}
        for i in range(answer[scp.DNS].arcount):
            r = answer[scp.DNS].ar[i]
            print_dns_record(r)

            r_name = r.rrname.decode()
            r_type = r.get_field('type').i2repr(r, r.type)
            r_data = get_data(r)

            if r_name not in additional_records:
                additional_records[r_name] = {}

            additional_records[r_name][r_type] = r_data

        print("Name Servers")
        for i in range(answer[scp.DNS].nscount):
            print_dns_record(answer[scp.DNS].ns[i])

        # Recursive search
        for i in range(answer[scp.DNS].nscount):
            r = answer[scp.DNS].ns[i]
            r_type = r.get_field('type').i2repr(r, r.type)
            if r_type == "SOA":
                print(f"Found SOA, no {record_type} record. Path: {path}")
                quit()

            r_data = get_data(r).decode()

            if r_data in additional_records:
                ip = additional_records[r_data][RECORD_TYPE_ADDRESS]
            else:
                ip, _ = rqdns(r_data, RECORD_TYPE_ADDRESS)
                if ip is None:
                    continue

            # Detección de ciclos entre resolvers
            if ip in path:
                #print(f"Already looked at {ip}")
                continue

            ans, path = qdns(ip, r_data, qname, record_type, path + [ip])
            if ans is not None:
                return ans, path

    return None, path

if __name__ == "__main__":
    qname = sys.argv[1]
    record_type = sys.argv[2]
    print("\nAnswer:", rqdns(qname+".", record_type))

    
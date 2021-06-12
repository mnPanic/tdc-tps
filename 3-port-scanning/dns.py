import sys
import scapy.all as scp

from typing import List

# https://en.wikipedia.org/wiki/List_of_DNS_record_types
RECORD_TYPE_ADDRESS = "A"
RECORD_TYPE_CNAME = "CNAME"

def print_dns_record(r: scp.DNSRR):
    # Para saber los campos que tiene r.fields_desc
    # https://stackoverflow.com/questions/41490875/scapy-get-dnsqr-dnsrr-field-values-in-symbolic-string-form
    print(f"{r.rrname.decode()} {r.get_field('type').i2repr(r, r.type)} {r.rdata}")  

def find_answer(answers: dict, qname: str, record_type: str) -> str:
    """
    www.dc.uba.ar. CNAME b'www-1.dc.uba.ar.'
    www-1.dc.uba.ar. CNAME b'dc.uba.ar.'
    dc.uba.ar. A 157.92.27.128
    """

    r_type, r_data = answers[qname]
    if r_type == record_type:
        return r_data
    
    if r_type == RECORD_TYPE_CNAME:
        return find_answer(answers, r_data.decode(), record_type)
    
    return None

def qdns(resolver_ip: str, resolver_name: str, qname: str, record_type: str, path: List[str]):
    print(f"\n\nQuerying DNS resolver {resolver_ip} ({resolver_name}) for qname {qname}")
    dns = scp.DNS(rd=1,qd=scp.DNSQR(qname=qname))
    udp = scp.UDP(sport=scp.RandShort(), dport=53)
    ip = scp.IP(dst=resolver_ip)

    answer = scp.sr1( ip / udp / dns , verbose=0, timeout=10)

    if answer and answer.haslayer(scp.DNS) and answer[scp.DNS].qd.qtype == 1: # reply
        print("Answer")
        for i in range(answer[scp.DNS].ancount):
            print_dns_record(answer[scp.DNS].an[i])
        
        answers = {}
        for i in range(answer[scp.DNS].ancount):
            r = answer[scp.DNS].an[i]
            r_name = r.rrname.decode()
            r_type = r.get_field('type').i2repr(r, r.type)
            r_data = r.rdata

            answers[r_name] = (r_type, r_data)
            
        # Find answer
        if qname in answers:
            ans = find_answer(answers, qname, record_type)
            if ans is not None:
                return ans, path

        print("Additional Records")
        additional_records = {}
        for i in range(answer[scp.DNS].arcount):
            r = answer[scp.DNS].ar[i]
            print_dns_record(r)

            r_name = r.rrname.decode()
            r_type = r.get_field('type').i2repr(r, r.type)
            r_data = r.rdata

            if r_name not in additional_records:
                additional_records[r_name] = {}

            additional_records[r_name][r_type] = r_data

        print("Name Servers")
        for i in range(answer[scp.DNS].nscount):
            print_dns_record(answer[scp.DNS].ns[i])

        # Recursive search
        for i in range(answer[scp.DNS].nscount):
            r = answer[scp.DNS].ns[i]
            r_data = r.rdata.decode()

            # TODO: Llamar a qdns
            ip = ""
            if r_data in additional_records:
                ip = additional_records[r_data][RECORD_TYPE_ADDRESS]
            else:
                ip, _ = qdns("199.9.14.201", "b.root-servers.net", r_data, RECORD_TYPE_ADDRESS, [])
                if ip is None:
                    continue

            # Detección de ciclos entre resolvers
            if ip in path:
                continue

            ans, path = qdns(ip, r_data, qname, record_type, path + [ip])
            if ans is not None:
                return ans, path

    return None, path

if __name__ == "__main__":
    qname = sys.argv[1]
    record_type = sys.argv[2]
    print("\nAnswer:", qdns("199.9.14.201", "b.root-servers.net", qname+".", record_type, []))

    
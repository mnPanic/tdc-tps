import scapy.all as scp

dns = scp.DNS(rd=1,qd=scp.DNSQR(qname="www.dc.uba.ar"))
udp = scp.UDP(sport=scp.RandShort(), dport=53)
ip = scp.IP(dst="199.9.14.201")

answer = scp.sr1( ip / udp / dns , verbose=0, timeout=10)
print(answer[scp.DNS].summary())

def print_dns_record(r: scp.DNSRR):
    # Para saber los campos que tiene r.fields_desc
    # https://en.wikipedia.org/wiki/List_of_DNS_record_types
    # https://stackoverflow.com/questions/41490875/scapy-get-dnsqr-dnsrr-field-values-in-symbolic-string-form
    print(f"{r.rrname.decode()} {r.get_field('type').i2repr(r, r.type)} {r.rdata}")

if answer.haslayer(scp.DNS) and answer[scp.DNS].qd.qtype == 1:
    print("Additional Records")
    for i in range(answer[scp.DNS].arcount):
        print_dns_record(answer[scp.DNS].ar[i])
    
    print("Name Servers")
    for i in range(answer[scp.DNS].nscount):
        print_dns_record(answer[scp.DNS].ns[i])

    print("Answer")
    for i in range(answer[scp.DNS].ancount):
        print_dns_record(answer[scp.DNS].an[i])

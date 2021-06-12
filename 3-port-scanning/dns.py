import scapy.all as scp

dns = scp.DNS(rd=1,qd=scp.DNSQR(qname="www.dc.uba.ar"))
udp = scp.UDP(sport=scp.RandShort(), dport=53)
ip = scp.IP(dst="199.9.14.201")

answer = scp.sr1( ip / udp / dns , verbose=0, timeout=10)
print(answer[scp.DNS].summary())

if answer.haslayer(scp.DNS) and answer[scp.DNS].qd.qtype == 1:
    print("Additional Records")
    for i in range(answer[scp.DNS].arcount):
        print(answer[scp.DNS].ar[i].rrname, answer[scp.DNS].ar[i].rdata)
    
    print("Name Servers")
    for i in range(answer[scp.DNS].nscount):
        print(answer[scp.DNS].ns[i].rrname, answer[scp.DNS].ns[i].rdata)

    print("Answer")
    for i in range(answer[scp.DNS].ancount):
        print(answer[scp.DNS].an[i].rrname, answer[scp.DNS].an[i].rdata)

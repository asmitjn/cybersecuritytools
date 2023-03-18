from scapy.all import srp, sr1
from scapy.layers.l2 import ARP, Ether
from scapy.layers.inet import IP, ICMP
import sys
import ipaddress

target_network=sys.argv[1]
online_clients=[]

ether=Ether(dst='ff:ff:ff:ff:ff:ff')
arp=ARP(pdst=target_network)
probe=ether/arp

result=srp(probe, timeout=3, verbose=0)
answered=result[0]

# [answered, unanswered]
# answered consists of [sent, received]

for sent, received in answered:
    online_clients.append({'ip':received.psrc, 'mac':received.hwsrc})

print('[+] Available hosts:')
print('IP '+ ' '*22 +'MAC')

for client in online_clients:
    print('{}\t\t{}'.format(client['ip'], client['mac']))


# Scanning with ICMP packet is very lengthy and time consuming as it scans each and every packet individually, hence we use ARP packet sniffing because it scans live hosts by broadcasting

# print('[+] Scanning with ICMP.....')
#
# ip_list=[str(ip) for ip in ipaddress.IPv4Network(target_network, False)]
#
# for ip in ip_list:
#     probe=IP(dst=ip)/ICMP()
#     result=sr1(probe, timeout=3)
#     if result:
#         print('[+] {} is online'.format(ip))




from scapy.all import *
from scapy.layers.l2 import ARP, Ether

NETWORK_ID = "192.168.1."

for i in range(255):
    ip = f"192.168.1.{i}"
    p = Ether()/ARP(pdst=ip)
    try:
        print(f"looking for {ip}")
        r = srp1(p, timeout=0.5, verbose=0)
        print(f"ip: {r[ARP].psrc}\nmac: {r[ARP].hwsrc}")
    except:
        pass

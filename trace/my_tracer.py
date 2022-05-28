from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import sr1
from scapy.all import *
import sys


def alt():

    destination = sys.argv[1]
    i = 1
    while True:
        packet = IP(ttl=i, dst=destination) / ICMP(id=5)
        try:
            res = sr1(packet, verbose=0, timeout=2)
            print(res[IP].src)
            if res[ICMP].type == 0:
                break
        except:
            print("No response")
        i += 1


def main():
    import sys
    # remove self reference argument
    dst_ip = sys.argv[1]
    curr_ttl = 1
    while True:
        print(f'ttl: {curr_ttl}')
        p = IP(dst=dst_ip, ttl=curr_ttl) / ICMP(id=5)
        r = sr1(p, timeout=2, verbose=0)
        if r is not None:
            print(r[IP].src)
            if r[ICMP].type == 0:
                break
        curr_ttl += 1
        if curr_ttl > 120:
            print('too muck ttl, exiting...')
            break


if __name__ == '__main__':
    alt()

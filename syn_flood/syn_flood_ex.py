import json

from scapy.layers.inet import IP, TCP
from scapy.utils import rdpcap

SUSPECT_IPS = []
SYN_COUNTERS = {}
SYN_LIMIT = 2


def main():
    pcap_file = rdpcap("SynFloodSample.pcap")

    for pkt in pcap_file:
        # first enter all known ips to follow their syn count
        if pkt[IP].src not in SYN_COUNTERS.keys():
            SYN_COUNTERS[pkt[IP].src] = []
        # add the syn port to the syn counters
        if pkt[TCP].flags == 'S':
            # document every syn
            SYN_COUNTERS[pkt[IP].src].append(pkt[TCP].sport)
        # if we get an ack
        if pkt[TCP].flags == 'A':
            # i dont care about my own acks
            if pkt[TCP].sport == 80:
                continue
            print(f'found flag A from {pkt[IP].src}:{pkt[TCP].sport} : {SYN_COUNTERS[pkt[IP].src]}')
            # if got syn previously then it is saved, so delete it because the ack closed the syn
            if pkt[TCP].sport in SYN_COUNTERS[pkt[IP].src]:
                # p.s. really no such acks were found in the file
                print(f'removing {pkt[TCP].sport}')
                SYN_COUNTERS[pkt[IP].src].remove(pkt[TCP].sport)

    # get all the ips and the ports of every ip that have more than 2 open syn requests
    suspect_ips = {key: val for key, val in SYN_COUNTERS.items() if len(val) > SYN_LIMIT}
    for key, value in suspect_ips.items():
        print(key, ':', value)
    with open('suspects.json', 'w') as suspects_file:
        suspects_file.write(json.dumps(suspect_ips))


if __name__ == '__main__':
    main()

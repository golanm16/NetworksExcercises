# author: Golan Matuf
# date: 08.12.2021
import validators
from scapy.all import *
from scapy.layers.dns import *

# choose the dns server as nslookup
ROOT_SERVER = '198.41.0.4'
DNS_SERVER = '192.168.100.1'
DOMAIN = '.'
PORT = 55121
TRANSACTION_ID = random.randint(2048, 65535)


def filter_dns_response(p):
    # filter only the dns request with my own transaction id
    return DNS in p and p[DNS].id == TRANSACTION_ID


def create_dns_packet(domain, dst):
    # create a dns request packet with the domain
    return IP(dst=dst) / UDP(dport=53, sport=PORT) / DNS(id=TRANSACTION_ID, qd=DNSQR(qname=domain))


def create_rev_dns_packet(domain_ip, dst):
    # create a dns type PTR request packet
    return IP(dst=dst) / UDP(dport=53, sport=PORT) / DNS(id=TRANSACTION_ID, qd=DNSQR(qname=domain_ip, qtype=12))


def handle_dns(query, is_reverse):
    if is_reverse:
        query_packet = create_rev_dns_packet(query, DNS_SERVER)
    # create normal dns request
    else:
        query_packet = create_dns_packet(query, DNS_SERVER)
    send(query_packet)
    # get the dns response
    packets = sniff(1, lfilter=filter_dns_response)
    p = packets[0]
    mult_dnsrr = p[DNS].an

    # if reverse dns request return the answer
    if is_reverse:
        return mult_dnsrr[p[DNS].ancount - 1].rdata.decode(), ''

    # if normal dns request
    multi_ans_str = ''
    # get all the ip from the response packet
    for i in range(p[DNS].ancount):
        ans = mult_dnsrr[i].rdata
        if type(ans) == str:
            multi_ans_str += '\n· ' + ans
    # return ip collection and cname
    return multi_ans_str, mult_dnsrr[p[DNS].ancount - 1].rrname.decode()


def handle_rev_nslookup(domain_ip):
    # reverse the ip for reverse dns request and send
    rev_ip = domain_ip.split('.')
    rev_ip.reverse()
    rev_ip = '.'.join(rev_ip)+'.in-addr.arpa'
    return handle_dns(rev_ip, is_reverse=True)[0]


def main():
    # check that an argument was sent to the script
    if len(sys.argv) < 2:
        print('script must get an argument! exiting....')
        return

    # validate normal dns arguments
    if len(sys.argv) == 2 and validators.domain(sys.argv[1]):
        domain = sys.argv[1]
        domain_ip, cname = handle_dns(domain, is_reverse=False)
        print(f'CNAME: {cname}\nIP: {domain_ip}')

    # validate reverse dns arguments
    elif len(sys.argv) == 3 and sys.argv[1] == '-type=PTR' and validators.ipv4(sys.argv[2]):
        domain = handle_rev_nslookup(sys.argv[2])
        print(f'Domain: {domain}')

    # in case of some invalid arguments,print error message, and exit the script
    else:
        print('invalid input. exiting...')


if __name__ == '__main__':
    main()

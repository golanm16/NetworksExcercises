# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from scapy.all import *
from scapy.layers.dns import *


def print_domain(p):
    print(p.show())


def filter_dns_qa(p):
    if (DNS in p) and (DNSQR in p):
        return p[DNS].opcode == 0 and p[DNSQR].qtype == 1



p = sniff(2, lfilter=filter_dns_qa, prn=print_domain)


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
''
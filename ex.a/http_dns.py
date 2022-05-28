# test moed a
# Author: golan matuf 311188585
# Date: 20220204 04.02.2022

import validators
from scapy.all import *
from scapy.layers.dns import *

DNS_SERVER = '1.1.1.1'
HTTP_PORT = 8153
SOCKET_TIMEOUT = 0.2


def get_content_length_header(size):
    return f'Content-Length: {str(size)}\r\n'


HEADERS = {
    'http_ok': 'HTTP/1.1 200 OK\r\n',
    'not_found': 'HTTP/1.1 404 Not Found\r\n',
    'server_error': 'HTTP/1.1 500 Server Error\r\n',
    'html': 'Content-Type: text/html; charset=UTF-8\r\n',
    'len': get_content_length_header,
    'header_end': '\r\n'

           }


# dns handlers functions

def create_dns_packet(domain, dst):
    # create a dns request packet with the domain
    return IP(dst=dst) / UDP(dport=53) / DNS(qd=DNSQR(qname=domain))


def create_rev_dns_packet(domain_ip, dst):
    # create a dns type PTR request packet
    return IP(dst=dst) / UDP(dport=53) / DNS(qd=DNSQR(qname=domain_ip, qtype=12))


def handle_dns(query, is_reverse):
    if is_reverse:
        query_packet = create_rev_dns_packet(query, DNS_SERVER)
    # create normal dns request
    else:
        query_packet = create_dns_packet(query, DNS_SERVER)
    p = sr1(query_packet)
    mult_dnsrr = p[DNS].an

    #if no dns response
    if mult_dnsrr is None:
        return "no domain found", ""
    # if reverse dns request return the answer
    if is_reverse:

        return mult_dnsrr[p[DNS].ancount-1].rdata.decode(), ''

    # if normal dns request
    multi_ans_str = ''
    # get all the ip from the response packet
    for i in range(p[DNS].ancount):
        ans = mult_dnsrr[i].rdata
        if type(ans) == str:
            multi_ans_str += '\n- ' + ans
    # return ip collection and cname
    return multi_ans_str, mult_dnsrr[p[DNS].ancount - 1].rrname.decode()


def handle_rev_nslookup(domain_ip):
    # reverse the ip for reverse dns request and send
    rev_ip = domain_ip.split('.')
    rev_ip.reverse()
    rev_ip = '.'.join(rev_ip)+'.in-addr.arpa'
    return handle_dns(rev_ip, is_reverse=True)[0]


def ns_lookup(ns_req, is_reverse=False):

    # validate normal dns arguments
    if not is_reverse:
        domain_ip, cname = handle_dns(ns_req, is_reverse)
        return f'CNAME: {cname}\nIP: {domain_ip}'

    # validate reverse dns arguments
    else:
        domain = handle_rev_nslookup(ns_req)
        return f'Domain: {domain}'


def validate_http_request(request):
    """
    Check if request is a valid HTTP request and returns TRUE / FALSE and the requested URL
    """
    # split the request to [GET, URL, HTTP_Ver\r\n]
    request = str(request)
    # print(request)
    request_arr = request.split()
    if len(request_arr) >= 3 and request_arr[0] == 'GET' and request_arr[2] == 'HTTP/1.1':
        return True, request_arr[1][1:]

    return False, ''


def handle_client_request(resource, client_socket):
    print(f'url:\n{resource}')

    # handle 200 ok http response
    if resource != "" and resource != "favicon.ico":
        is_reverse = validators.ipv4(resource)
        ns_response = f"<!DOCTYPE html><body>{ns_lookup(resource,is_reverse)}</body>"

        html_file = open("index.html", 'w')
        html_file.write(ns_response)
        html_file.close()
        http_header = HEADERS['http_ok']
        http_header += HEADERS['html']
        # handle all other headers
        http_header += f"Content-Length: {len(ns_response)}\r\n"
        http_header += HEADERS['header_end']

        # read the data from the file
        data = open("index.html", 'rb').read(os.path.getsize("index.html"))

        http_response = http_header.encode() + data
        print(f'resp: \n{http_response}')
        # send response
        client_socket.send(http_response)

    # handle 404 not found
    else:
        header = HEADERS['not_found']+HEADERS['header_end']
        client_socket.send(header.encode())



def handle_client(client_socket):
    """ Handles client requests: verifies client's requests are legal HTTP, calls function to handle the requests """
    print('Client connected')
    while True:
        try:
            client_request = client_socket.recv(1024).decode()
        except:
            print("server timeout")
            return
        valid_http, resource = validate_http_request(client_request)
        if valid_http:
            print('Got a valid HTTP request')
            handle_client_request(resource, client_socket)
            break
        else:
            client_socket.send((HEADERS['server_error']+HEADERS['header_end']).encode())
            print('Error: Not a valid HTTP request')
            break
    # client_socket.send(FIXED_RESPONSE.encode())
    print('Closing connection')
    client_socket.close()


def http_server():
    # Open a socket and loop forever while waiting for clients
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", HTTP_PORT))
    server_socket.listen()
    print(f"Listening for connections on port {HTTP_PORT}")

    while True:
        print("waiting for client...")
        client_socket, client_address = server_socket.accept()
        print('New connection received')
        client_socket.settimeout(SOCKET_TIMEOUT)
        handle_client(client_socket)


def main():
    http_server()


if __name__ == '__main__':
    main()
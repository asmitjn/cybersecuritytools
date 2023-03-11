import whois
import dns.resolver
import shodan
import requests
import argparse
import socket

argparse=argparse.ArgumentParser(description='This is a simple info gathering tool.', usage='python3 info_gathering.py -d DOMAIN [-s IP]')
argparse.add_argument('-d','--domain',help='Enter the domain name for footprinting',required=True)
argparse.add_argument('-s','--shodan',help='Enter the IP address for shodan search')
argparse.add_argument('-o','--output',help='Enter the file to save output to')

args=argparse.parse_args()                                         #( This parses the command-line arguments provided to the script using the ArgumentParser instance and assigns the resulting namespace object to the args variable.)
domain=args.domain                                                 #(This extracts the value of the domain argument from the args namespace object and assigns it to the domain variable.)
ip=args.shodan                                                     #(This extracts the value of the shodan argument from the args namespace object and assigns it to the ip variable. If the --shodan option was not provided on the command-line, the ip variable will be set to None.)
output=args.output

#whois module
print('[+] Getting whois info...')
whois_result=''
# using whois library, creating instance

try:
    py=whois.query(domain)
    print('[+] whois info found.')
    whois_result+=('Name: {}'.format(py.name)) + '\n'
    whois_result+=('Registrar: {}'.format(py.registrar)) + '\n'
    whois_result+=('Creation date: {}'.format(py.creation_date)) + '\n'
    whois_result+=('Expiration date: {}'.format(py.expiration_date)) + '\n'
    whois_result+=('Registrant: {}'.format(py.registrant)) + '\n'
    whois_result+=('Registrant country: {}'.format(py.registrant_country)) + '\n'
except:
    pass
print(whois_result)
# DNS module

print('[+] Getting dns info...')
dns_result=''

#implementing dns.resolver from dnspython

try:
    for a in dns.resolver.resolve(domain,'A'):
        dns_result+=('[+] A record: {}'.format(a.to_text())) + '\n'
    for ns in dns.resolver.resolve(domain, 'NS'):
        dns_result+=('[+] NS record: {}'.format(ns.to_text())) + '\n'
    for mx in dns.resolver.resolve(domain, 'MX'):
        dns_result+=('[+] MX record: {}'.format(mx.to_text())) + '\n'
    for txt in dns.resolver.resolve(domain, 'TXT'):
        dns_result+=('[+] TXT record: {}'.format(txt.to_text())) + '\n'
except:
    pass
print(dns_result)

# Geolocation module
print('[+] Getting geolocation info..')
georesult=''

# implementing requests for web request
try:
    response=requests.request('GET','http://geolocation-db.com/json/' + socket.gethostbyname(domain)).json()
    georesult+=('[+] Country: {}'.format(response['country_name'])) + '\n'
    georesult+=('[+] Latitude: {}'.format(response['latitude'])) + '\n'
    georesult+=('[+] Longitude: {}'.format(response['longitude'])) + '\n'
    georesult+=('[+] State: {}'.format(response['state'])) + '\n'
    georesult+=('[+] City: {}'.format(response['city'])) + '\n'
except:
    pass
print(georesult)

#Shodan module


if ip:
    #shodan API
    api=shodan.Shodan('VSXWz9MYngVCZlLxsZ7qJwKJxCCadkx9')
    print('[+] Getting info from shodan for IP {}.'.format(ip))
    try:
        results=api.search(ip)
        print('[+] Results found: {}'.format(results['total']))
        for result in results['matches']:
            print('[+] IP: {}'.format(result['ip_str']))
            print('[+] Data \n{}'.format(result['data']))
    except:
        print('[-] Shodan search error.')

if(output):
    with open(output, 'w') as file:
        file.write(whois_result + '\n\n')
        file.write(dns_result + '\n\n')
        file.write(georesult + '\n\n')

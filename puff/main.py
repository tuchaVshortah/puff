import argparse
import json
from rich.console import Console
from subdomainslookup import *

def main():
    parser = argparse.ArgumentParser(prog="puff", description="Yet another subdomain enumeration tool")
    
    parser.add_argument(
        "domains", 
        help="Specify domain to enumerate",
        default=[],
        type=str,
        nargs="+"
    )

    parser.add_argument(
        "-q","--quiet",
        help="Do not show output in the terminal",
        action="store_true"
    )

    parser.add_argument(
        "-j","--json",
        help="Output in the JSON format",
        action="store_true"
    )

    parser.add_argument(
        "-x","--xml",
        help="Output in the XML format",
        action="store_true"
    )

    parser.add_argument(
        "-o", "--output",
        dest="output_file",
        help="Save results to the specified file",
        default=None,
        nargs='?',
        type=argparse.FileType(mode='wt',encoding='utf-8'),
    )

    args = parser.parse_args()

    print(args.quiet)
    client = Client("api_key")

    if(args.json == True):
        for domain in args.domains:
            response = client.get_raw(domain, output_format=Client.JSON_FORMAT)
            print("Subdomains for " + domain)
            for record in response.result.records:
                print("    " + record.domain)
    elif(args.xml == True):
        for domain in args.domains:
            response = client.get_raw(domain, output_format=Client.XML_FORMAT)
            print("Subdomains for " + domain)
            for record in response.result.records:
                print("    " + record.domain)
    else:
        for domain in args.domains:
            response = client.get(domain)
            print("Subdomains for " + domain)
            for record in response.result.records:
                print("    " + record.domain)

main()
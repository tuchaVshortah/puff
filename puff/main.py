import argparse
import json
import xml
from rich.console import Console
from subdomainslookup import *

def main():
    parser = argparse.ArgumentParser(prog="puff", description="Yet another subdomain enumeration tool")
    
    parser.add_argument(
        "domain", 
        help="Specify domain to enumerate",
        default=[],
        type=str,
        nargs=1
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-q","--quiet",
        help="Do not show formatted (beautified) output in the terminal",
        action="store_true"
    )

    group.add_argument(
        "-r", "--raw",
        help="Output raw data to the terminal",
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
        "-f", "--file",
        help="Save results to the specified file",
        default=None,
        nargs='?',
        type=argparse.FileType(mode='a+',encoding='utf-8'),
    )

    args = parser.parse_args()

    client = Client("api_key")
    domain = args.domain[0]

    if(args.json == True):
        response = client.get_raw(domain, output_format=Client.JSON_FORMAT)
        response_data = json.loads(response)
        pretty_response = json.dumps(response_data, indent=2)
        print(pretty_response)

        if(args.file is not None):
            args.file.write(pretty_response)

        elif(args.file is None):
                with open("subdomains" + domain + ".json", "a+") as file:
                    file.write(pretty_response)

    elif(args.xml == True):
        response = client.get_raw(domain, output_format=Client.XML_FORMAT)
        
        if(args.file is not None):
            args.file.write(response.text)

        elif(args.file is None):
                with open("subdomains" + domain + ".xml", "a+") as file:
                    file.write(response.text)
        
    else:
        response = client.get(domain)
        print("Subdomains for " + domain)
        
        for record in response.result.records:
            print("    " + record.domain)

            if(args.file is not None):
                args.file.write(record.domain + "\n")

            elif(args.file is None):
                with open("subdomains" + domain + ".txt", "a+") as file:
                    file.write(record.domain + "\n")

main()
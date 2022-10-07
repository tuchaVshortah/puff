import re
import requests
import argparse
import validators

def main():
    parser = argparse.ArgumentParser(prog="puff", description="Yet another subdomain enumeration tool")
    
    parser.add_argument(
        "domains", 
        help="Specify domain to enumerate",
        default=[],
        type=str,
        nargs="+"
    )

    args = parser.parse_args()

    for domain in args.domains:
        if(not (validators.domain(domain))):
            print("Invalid domain name(s)")


main()
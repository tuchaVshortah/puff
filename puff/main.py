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

    parser.add_argument(
        "-o", "--output",
        dest='output_file_name',
        help="Save results to the specified file",
        default=None,
        nargs='?',
        type=argparse.FileType(mode='wt',encoding='utf-8'),
    )

    args = parser.parse_args()

    for domain in args.domains:
        if(not (validators.domain(domain))):
            print("Invalid domain name(s)")


main()
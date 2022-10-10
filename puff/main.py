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
        "-q", "--quiet",
        dest='output_file',
        help="Do not show output in the terminal",
        default=None,
        type=argparse.FileType(mode='wt',encoding='utf-8'),
    )

    parser.add_argument(
        "-o", "--output",
        dest='output_file',
        help="Save results to the specified file",
        default=None,
        nargs='?',
        type=argparse.FileType(mode='wt',encoding='utf-8'),
    )

    args = parser.parse_args()
    client = Client('api_key')

    for domain in args.domains:
        response = client.get(domain)

        for record in response.result.records:
            print("Domain: " + record.domain)

main()
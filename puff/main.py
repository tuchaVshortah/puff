import argparse
import json
import xml
from requests import request, Response, Session
import base64
from rich.console import Console
from subdomainslookup import *

class PuffApiRequester(ApiRequester):
    def post(self, data: dict) -> str:
        headers = {
            "User-Agent": ApiRequester.__user_agent,
            "Connection": "close"
        }
        if "apiKey" in data:
            headers["X-CSRF-TOKEN"] = data.pop("csrf_token")
        
        response = request(
            "POST",
            "https://subdomains.whoisxmlapi.com/api/web",
            json=data,
            headers=headers,
            timeout=(ApiRequester.__connect_timeout, self.timeout)
        )

        return ApiRequester._handle_response(response)

def getCsrfToken():
    session = Session()
    response = session.get("https://subdomains.whoisxmlapi.com/api/")
    cookies = session.cookies.get_dict()
    XSRF_TOKEN = cookies["XSRF-TOKEN"]
    return XSRF_TOKEN
    

def main():
    parser = argparse.ArgumentParser(prog="puff", description="Yet another subdomain enumeration tool")

    parser.add_argument(
        "-d", "--domain",
        help="Specify the domain to enumerate",
        default=None,
        required=True,
        type=str,
        nargs=1
    )

    parser.add_argument(
        "-x", "--no-api-keys",
        help="Pass this argument if you don't have API keys",
        action="store_true",
        dest="no_api_keys"
    )

    output_format_group = parser.add_mutually_exclusive_group()
    output_format_group.add_argument(
        "-q","--quiet",
        help="Do not show formatted (beautified) output in the terminal",
        action="store_true"
    )

    output_format_group.add_argument(
        "-r", "--raw",
        help="Output raw data to the terminal",
        action="store_true"
    )

    output_format_group.add_argument(
        "-j","--json",
        help="Output in the JSON format",
        action="store_true"
    )

    output_format_group.add_argument(
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
    domain = args.domain

    if(args.json == True):
        response = client.get_raw(domain, output_format=Client.JSON_FORMAT)
        response_data = json.loads(response)
        pretty_response = json.dumps(response_data, indent=2)
        print("JSON data for: " + domain)
        print(pretty_response)

        if(args.file is not None):
            args.file.write(pretty_response)

        elif(args.file is None):
                with open("subdomains." + domain + ".json", "a+") as file:
                    file.write(pretty_response)

    elif(args.xml == True):
        response = client.get_raw(domain, output_format=Client.XML_FORMAT)
        print("XML data for: " + domain)
        print(response)
        if(args.file is not None):
            args.file.write(response)

        elif(args.file is None):
                with open("subdomains." + domain + ".xml", "a+") as file:
                    file.write(response)
    
    elif(argparse.no_api_keys):
        api_requester = ApiRequester("https://subdomains.whoisxmlapi.com/api/web")

    else:
        response = client.get(domain)
        print("Subdomains for: " + domain)
        
        for record in response.result.records:
            print("    " + record.domain)

            if(args.file is not None):
                args.file.write(record.domain + "\n")
                
            elif(args.file is None):
                with open("subdomains." + domain + ".txt", "a+") as file:
                    file.write(record.domain + "\n")
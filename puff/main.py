import argparse
from json import *
import xml
from requests import request, Response, Session
from bs4 import BeautifulSoup
import base64
from rich.console import Console
from subdomainslookup import *

class PuffApiRequester(ApiRequester):
    def post(self, data: dict) -> str:

        response = getResponse()

        soup = BeautifulSoup(response.text, "lxml")

        csrf_token = soup.find("meta", {"name":"csrf-token"})["content"]

        cookies = response.cookies.get_dict()

        headers = {
            "Host": "subdomains.whoisxmlapi.com",
            "Cookie": "XSRF-TOKEN=" + cookies["XSRF-TOKEN"] + "; " + \
                    "emailverification_session=" + cookies["emailverification_session"],
            "Sec-Ch-Ua": '"Chromium";v="105", "Not)A;Brand";v="8"',
            "X-Csrf-Token": csrf_token,
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36",
            "Connection": "close",
            "Content-Type": "application/json",
            "Accept": "application/json, text/plain, */*",
            "X-Requested-With": "XMLHttpRequest",
            "Sec-Ch-Ua-Platform": "Windows",
            "Origin": "https://subdomains.whoisxmlapi.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://subdomains.whoisxmlapi.com/",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-US,en;q=0.9"
        }


        response = request(
            "POST",
            "https://subdomains.whoisxmlapi.com/api/web",
            json=data,
            headers=headers,
            timeout=(10, self.timeout)
        )

        return ApiRequester._handle_response(response)

def getResponse() -> Response:
    session = Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
        "Connection": "keep-alive"
    }
    response = session.get("https://subdomains.whoisxmlapi.com/api/")
    
    return response
    
def buildPayload(domain) -> dict:
    payload = {
        "domainName": domain,
        "g-recaptcha-response": None,
        "search": domain,
        "web-lookup-search": True
    }

    return payload

def saveJsonResponse(file, domain, response: Response):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".json", "a+") as file:
            file.write(response)

def saveXmlResponse(file, domain, response: Response):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".xml", "a+") as file:
            file.write(response)

def saveTxtResponse(file, domain, response: Response):
    for record in response.result.records:
        print("    " + record.domain)

        if(file is not None):
            file.write(record.domain + "\n")
            
        elif(file is None):
            with open("subdomains." + domain + ".txt", "a+") as file:
                file.write(record.domain + "\n")


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

    api_group = parser.add_mutually_exclusive_group()

    api_group.add_argument(
        "-wak", "--whoisxmlapi-api-key",
        help="Specify your API key for whoisxmlapi.com",
        dest="whoisxmlapi_api_key",
        type=str,
        nargs=1
    )

    api_group.add_argument(
        "-X", "--no-api-keys",
        help="Pass this argument if you don't have API keys",
        default=False,
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

    client = None
    if(args.whoisxmlapi_api_key):
        client = Client(args.whoisxml_api_key)
        
    domain = args.domain[0]

    if(args.json == True):
        response = client.get_raw(domain, output_format=Client.JSON_FORMAT)
        response_data = loads(response)
        pretty_response = dumps(response_data, indent=2)
        print("JSON data for: " + domain)
        print(pretty_response)

        saveJsonResponse(args.file, domain, pretty_response)

    elif(args.xml == True):
        response = client.get_raw(domain, output_format=Client.XML_FORMAT)
        print("XML data for: " + domain)
        print(response)

        saveXmlResponse(args.file, domain, response)
    
    elif(args.no_api_keys):
        puff_api_requester = PuffApiRequester()
        payload = buildPayload(domain)
        response = puff_api_requester.post(payload)

        try:
            response_data = loads(response)
            pretty_response = dumps(response_data, indent=2)

            print("JSON data for: " + domain)
            print(pretty_response)

            saveJsonResponse(args.file, domain, pretty_response)
            """

            if 'result' in parsed:
                print(Response(parsed))
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)

            """
        except JSONDecodeError as error:
            raise UnparsableApiResponseError("Could not parse API response", error)

    else:
        response = client.get(domain)
        print("Subdomains for: " + domain)
        
        saveTxtResponse(args.file, response)

main()
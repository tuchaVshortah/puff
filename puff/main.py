import argparse
from json import *
import xml.dom.minidom
from requests import request, Response, Session
from bs4 import BeautifulSoup
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
    
def buildPayload(domainName, outputFormat="json") -> dict:
    payload = {
        "domainName": domainName,
        "g-recaptcha-response": None,
        "search": domainName,
        "web-lookup-search": True,
        "outputFormat": outputFormat
    }

    return payload

def saveJsonResponse(file, domain, response: str):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".json", "a+") as file:
            file.write(response)

def saveXmlResponse(file, domain, response: str):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".xml", "a+") as file:
            file.write(response)

def saveTxtResponse(file, domain, response: Response):
    
    if(file is not None):
        for record in response.result.records:
            file.write(record.domain + "\n")
        
    elif(file is None):
        with open("subdomains." + domain + ".txt", "a+") as file:
            for record in response.result.records:
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
        default=None,
        type=str,
        nargs=1
    )

    api_group.add_argument(
        "-X", "--no-api-keys",
        help="Pass this argument if you don't have API keys",
        default=False,
        action="store_true",
    )

    output_format_group = parser.add_mutually_exclusive_group()
    output_format_group.add_argument(
        "-q","--quiet",
        help="Do not show any output in the terminal",
        default=False,
        action="store_true"
    )

    output_format_group.add_argument(
        "-r", "--raw",
        help="Output raw data to the terminal",
        default=False,
        action="store_true"
    )

    output_format_group.add_argument(
        "-j","--json",
        help="Output in the JSON format",
        default=False,
        action="store_true"
    )

    output_format_group.add_argument(
        "-x","--xml",
        help="Output in the XML format",
        default=False,
        action="store_true"
    )

    output_file_group = parser.add_mutually_exclusive_group()
    output_file_group.add_argument(
        "-f", "--file",
        help="Save results to the specified file",
        default=None,
        nargs="?",
        type=argparse.FileType(mode="a+",encoding="utf-8")
    )

    output_file_group.add_argument(
        "-df", "--default-file",
        help="Save results in the subdomains.<domain>.txt files",
        default=False,
        action="store_true"
    )

    args = parser.parse_args()
    
    client = None
    domain = args.domain[0]

    if(args.whoisxmlapi_api_key is not None):

        client = Client(args.whoisxmlapi_api_key[0])

        if(args.json == True):

            response = client.get_raw(domain, output_format=Client.JSON_FORMAT)
            response_data = loads(response)
            pretty_response = dumps(response_data, indent=2)
            
            response = pretty_response

            if(not args.quiet):
                print("JSON data for: " + domain)
                print(response)

            if(args.file is not None):
                saveJsonResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveJsonResponse(None, domain, response)


        elif(args.xml == True):

            response = client.get_raw(domain, output_format=Client.XML_FORMAT)
            
            if(not args.quiet):
                print("XML data for: " + domain)
                print(response)

            if(args.file is not None):
                saveXmlResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveXmlResponse(None, domain, response)

        else:

            response = client.get(domain)

            if(not args.quiet):
                print("Subdomains for: " + domain)
            
            if(args.file is not None):
                saveTxtResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveTxtResponse(None, domain, response)


    
    elif(args.no_api_keys == True):

        puff_api_requester = PuffApiRequester()

        if(args.json == True):

            payload = buildPayload(domain, "json")
            response = puff_api_requester.post(payload)

            try:

                response_data = loads(response)
                pretty_response = dumps(response_data, indent=2)

                response = pretty_response

            except error:

                raise UnparsableApiResponseError("Could not parse API response", error)

            if(not args.quiet):

                print("JSON data for: " + domain)
                print(response)

            if(args.file is not None):
                saveJsonResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveJsonResponse(None, domain, response)


            """

            if 'result' in parsed:
                print(Response(parsed))
            raise UnparsableApiResponseError(
                "Could not find the correct root element.", None)

            """

            
        elif(args.xml == True):

            payload = buildPayload(domain, "xml")
            response = puff_api_requester.post(payload)

            try:

                response_data = xml.dom.minidom.parseString(response)
                pretty_response = response_data.toprettyxml()

                response = pretty_response

            except error:

                print("Could not parse API response", error)

            if(not args.quiet):

                print("XML data for: " + domain)
                print(response)

            if(args.file is not None):
                saveXmlResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveXmlResponse(None, domain, response)


        else:

            payload = buildPayload(domain, "json")
            response = puff_api_requester.post(payload)

            try:

                response_data = loads(response)

            except error:

                raise UnparsableApiResponseError("Could not parse API response", error)

            if(not args.quiet):

                response = Response(response_data)

                print("Subdomains for: " + domain)
                for record in response.result.records:
                    print("Domain: " + record.domain)

            if(args.file is not None):
                saveTxtResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveTxtResponse(None, domain, response)


main()
from subdomainslookup import ApiRequester
from subdomainslookup.models.response import Response as ApiResponse
from requests import request, Session
from bs4 import BeautifulSoup

class PuffApiRequester(ApiRequester):
    def post(self, data: dict) -> str:

        response = self.__getResponse()

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

    def __getResponse(self) -> ApiResponse:
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

def saveTxtResponse(file, domain, response: ApiResponse):
    
    if(file is not None):
        for record in response.result.records:
            file.write(record.domain + "\n")
        
    elif(file is None):
        with open("subdomains." + domain + ".txt", "a+") as file:
            for record in response.result.records:
                file.write(record.domain + "\n")
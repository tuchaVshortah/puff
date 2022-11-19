from subdomainslookup import ApiRequester, Client
from subdomainslookup.models.response import Response as ApiResponse
from requests import request, Session, Response
from bs4 import BeautifulSoup
from threading import Thread
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT

class PuffApiRequester(Thread, ApiRequester):

    __payload = None
    __response = None
    __results = None

    def __init__(self, domainName:str, outputFormat:str):
        Thread.__init__(self)
        ApiRequester.__init__(self)

        self.__payload = self.__buildPayload(domainName, outputFormat)


    def post(self) -> str:
        
        self.__response = self.__getResponse()

        soup = BeautifulSoup(self.__response.text, "lxml")

        csrf_token = soup.find("meta", {"name":"csrf-token"})["content"]

        cookies = self.__response.cookies.get_dict()

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
            json=self.__payload,
            headers=headers,
            timeout=(10, self.timeout)
        )

        return ApiRequester._handle_response(response)


    def __getResponse(self) -> Response:
        session = Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Connection": "keep-alive"
        }
        response = session.get("https://subdomains.whoisxmlapi.com/api/")
        
        return response

    def __buildPayload(self, domainName, outputFormat="json") -> dict:

        if(outputFormat == RAW_FORMAT):
            outputFormat = JSON_FORMAT
            
        payload = {
            "domainName": domainName,
            "g-recaptcha-response": None,
            "search": domainName,
            "web-lookup-search": True,
            "outputFormat": outputFormat
        }

        return payload

    def run(self):
        self.__results = self.post()

    def join(self):
        Thread.join(self)
        return self.__results

class PuffClient(Thread, Client):

    __client = None
    __domain = None
    __outputFormat = None
    __results = None
    
    def __init__(self, api_key: str, domain: str, outputFormat: str or None = None):
        Thread.__init__(self)
        self.__client = Client.__init__(self, api_key)

        self.__domain = domain
        self.__outputFormat = outputFormat

    def get_raw(self):
        if(self.__outputFormat == XML_FORMAT):

            return self.__client.get_raw(self, self.__domain, XML_FORMAT)

        elif(self.__outputFormat == JSON_FORMAT or self.__outputFormat == RAW_FORMAT):
            
            return self.__client.get_raw(self, self.__domain, JSON_FORMAT)

    def run(self):
        self.__results = self.get_raw()

    def join(self):
        Thread.join(self)
        return self.__results
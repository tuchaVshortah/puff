from subdomainslookup import ApiRequester
from subdomainslookup.models.response import Response as ApiResponse
from requests import request, Session
from bs4 import BeautifulSoup
from threading import Thread

class PuffApiRequester(Thread, ApiRequester):

    self.__payload = None
    self.__response
    self.__results = None

    def __init__(self, domainName:str, outputFormat:str):
        Thread.__init__(self)

        self.__payload = self.__buildPayload(domainName, outputFormat)
        self.__response = self.__getResponse()


    def post(self) -> ApiResponse:

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

        
    def __getResponse(self) -> ApiResponse:
        session = Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Connection": "keep-alive"
        }
        response = session.get("https://subdomains.whoisxmlapi.com/api/")
        
        return response

    def __buildPayload(self, domainName, outputFormat="json") -> dict:
        payload = {
            "domainName": domainName,
            "g-recaptcha-response": None,
            "search": domainName,
            "web-lookup-search": True,
            "outputFormat": outputFormat
        }

        return payload

    def run(self):
        self.__results = self.post(self.__payload)

    def join(self):
        Thread.join(self)
        return self.__results
from apis.bases.WhoIsXmlApiBase import Base, WhoIsXmlApiBase
from subdomainslookup import ApiRequester, Client
from subdomainslookup.models.response import Result, Record, Response as ApiResponse
import requests
from requests import request
from json import loads, dumps
import xml.dom.minidom
from xml.dom.minidom import Document
from bs4 import BeautifulSoup
from threading import Thread
from constants.outputformats import JSON_FORMAT


class WhoisXmlApiRequester(Thread, ApiRequester, WhoIsXmlApiBase):

    __payload = None
    __csrfToken = None
    __xsrfToken = None
    __emailVerification_session = None
    

    def __init__(self, domainName:str):
        Thread.__init__(self)
        ApiRequester.__init__(self)
        WhoIsXmlApiBase.__init__(self, domainName)

        self.__payload = {
            "domainName": self._domainName,
            "g-recaptcha-response": None,
            "search": self._domainName,
            "web-lookup-search": True,
            "outputFormat": JSON_FORMAT
        }


    def getSubdomains(self) -> list:
        try:

            return self.__getSubdomains()
            
        except:

            return []


    def __getSubdomains(self) -> list:
        self.__setSessionTokens()

        headers = {
            "Host": "subdomains.whoisxmlapi.com",
            "Cookie": f'XSRF-TOKEN={self.__xsrfToken}; emailverification_session={self.__emailVerification_session}',
            "Sec-Ch-Ua": '"Chromium";v="105", "Not)A;Brand";v="8"',
            "X-Csrf-Token": self.__csrfToken,
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

        response_data = loads(ApiRequester._handle_response(response))

        subdomains = WhoIsXmlApiBase._parseSubdomains(self, response_data)
        
        return subdomains


    def __setSessionTokens(self):

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
            "Connection": "keep-alive"
        }

        response = requests.get("https://subdomains.whoisxmlapi.com/api/", headers)

        soup = BeautifulSoup(response.text, "lxml")
        self.__csrfToken = soup.find("meta", {"name":"csrf-token"})["content"]

        cookies = response.cookies.get_dict()

        self.__xsrfToken = cookies["XSRF-TOKEN"]
        self.__emailVerification_session = cookies["emailverification_session"]


    def run(self):
        self._results = self.getSubdomains()


    def join(self):
        Thread.join(self)
        return self._results


class WhoIsXmlClientApiRequester(Thread, Client, WhoIsXmlApiBase):
    
    def __init__(self, api_key: str, domainName: str, outputFormat: str or None = JSON_FORMAT):
        Thread.__init__(self)
        Client.__init__(self, api_key)
        WhoIsXmlApiBase.__init__(self, domainName)


    def getSubdomains(self) -> list:

        try:

            return self.__getSubdomains()
            
        except:
            
            return []
        

    def __getSubdomains(self) -> list:
            
        response = Client.get_raw(self, self._domainName, JSON_FORMAT)
        response_data = loads(response)

        subdomains = WhoIsXmlApiBase._parseSubdomains(self, response_data)

        return subdomains

    def run(self):
        self._results = self.getSubdomains()


    def join(self):
        Thread.join(self)
        return self._results
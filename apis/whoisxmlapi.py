from apis.bases.WhoIsXmlApiBase import WhoIsXmlApiBase
from subdomainslookup import ApiRequester, Client
from subdomainslookup.models.response import Result, Record, Response as ApiResponse
from requests import request, Session, Response
import xml.dom.minidom
from xml.dom.minidom import Document
from bs4 import BeautifulSoup
from threading import Thread
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT


class WhoisXmlApiRequester(Thread, ApiRequester, WhoIsXmlApiBase):

    _payload = None

    def __init__(self, domainName:str, outputFormat:str = JSON_FORMAT):
        Thread.__init__(self)
        ApiRequester.__init__(self)
        WhoIsXmlApiBase.__init__(self)

        self._domainName = domainName
        self._outputFormat = outputFormat

        self._payload = self.__buildPayload()


    def post(self) -> dict or Document or ApiResponse:
        try:

            response = self.__post()
            response_data = WhoIsXmlApiBase._loadResponse(self, response)
            WhoIsXmlApiBase._checkRecords(self, response_data)

            if(self._outputFormat == RAW_FORMAT):
                response_data = ApiResponse(response_data)
            
        except:
            
            default_response = WhoIsXmlApiBase._buildDefaultResponse(self)
            response_data = default_response

        return response_data
        


    def __post(self) -> str:
        
        self._response = self.__getResponse()

        soup = BeautifulSoup(self._response.text, "lxml")

        csrf_token = soup.find("meta", {"name":"csrf-token"})["content"]

        cookies = self._response.cookies.get_dict()

        headers = {
            "Host": "subdomains.whoisxmlapi.com",
            "Cookie": f'XSRF-TOKEN={cookies["XSRF-TOKEN"]}; emailverification_session={cookies["emailverification_session"]}',
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
            json=self._payload,
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


    def __buildPayload(self) -> dict:
        payload = {
            "domainName": self._domainName,
            "g-recaptcha-response": None,
            "search": self._domainName,
            "web-lookup-search": True
        }

        if(self._outputFormat == XML_FORMAT):

                payload["outputFormat"] = XML_FORMAT

        else:

            payload["outputFormat"] = JSON_FORMAT

        return payload

    def run(self):
        self._results = self.post()

    def join(self):
        Thread.join(self)
        return self._results


class WhoIsXmlClientApiRequester(Thread, Client, WhoIsXmlApiBase):
    
    def __init__(self, api_key: str, domainName: str, outputFormat: str or None = JSON_FORMAT):
        Thread.__init__(self)
        Client.__init__(self, api_key)
        WhoIsXmlApiBase.__init__(self)

        self._domainName = domainName
        self._outputFormat = outputFormat

    def get_raw(self) -> dict or Document or ApiResponse:

        try:

            response = self.__get_raw()
            response_data = WhoIsXmlApiBase._loadResponse(self, response)
            WhoIsXmlApiBase._checkRecords(self, response_data)

            if(self._outputFormat == RAW_FORMAT):
                response_data = ApiResponse(response_data)
            
        except:
            
            default_response = WhoIsXmlApiBase._buildDefaultResponse(self)
            response_data = default_response

        return response_data
        

    def __get_raw(self):
        if(self._outputFormat == XML_FORMAT):

            return Client.get_raw(self, self._domainName, XML_FORMAT)

        else:
            
            return Client.get_raw(self, self._domainName, JSON_FORMAT)

    def run(self):
        self._results = self.get_raw()

    def join(self):
        Thread.join(self)
        return self._results
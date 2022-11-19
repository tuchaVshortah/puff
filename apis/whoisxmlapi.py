from subdomainslookup import ApiRequester, Client
from subdomainslookup.models.response import Response as ApiResponse
from requests import request, Session, Response
from bs4 import BeautifulSoup
from threading import Thread
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT


class PuffHelper():

    def _buildDefaultResponse(self) -> str:
        response = None


        if(self._outputFormat == XML_FORMAT):
            response = f'''\
<?xml version="1.0" ?>
<xml>
    <search>{self._domainName}</search>
    <result>
        <count>10000</count>
        <records>
        </records>
    </result>
</xml>'''
    
        elif(self._outputFormat == JSON_FORMAT):
            response = f'''\
{{
    "search": "{self._domainName}",
    "result": {{
        "count": 0,
        "records": []
    }}
}}'''

        return response


class PuffApiRequester(Thread, ApiRequester, PuffHelper):

    _domainName = None
    _outputFormat = None
    __payload = None
    __response = None
    __results = None

    def __init__(self, domainName:str, outputFormat:str = JSON_FORMAT):
        Thread.__init__(self)
        ApiRequester.__init__(self)
        PuffHelper.__init__(self)

        self._domainName = domainName
        self._outputFormat = outputFormat

        if(self._outputFormat == RAW_FORMAT):

            self._outputFormat = JSON_FORMAT

        self.__payload = self.__buildPayload()


    def post(self) -> str:
        try:

            return self.__post()

        except:
            
            return PuffHelper._buildDefaultResponse(self)


    def __post(self) -> str:
        
        self.__response = self.__getResponse()

        soup = BeautifulSoup(self.__response.text, "lxml")

        csrf_token = soup.find("meta", {"name":"csrf-token"})["content"]

        cookies = self.__response.cookies.get_dict()

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

    def __buildPayload(self) -> dict:

        payload = {
            "domainName": self._domainName,
            "g-recaptcha-response": None,
            "search": self._domainName,
            "web-lookup-search": True,
            "outputFormat": self._outputFormat
        }

        return payload

    def run(self):
        self.__results = self.post()

    def join(self):
        Thread.join(self)
        return self.__results


class PuffClient(Thread, Client, PuffHelper):

    __client = None
    _domainName = None
    _outputFormat = None
    __results = None
    
    def __init__(self, api_key: str, domainName: str, outputFormat: str or None = JSON_FORMAT):
        Thread.__init__(self)
        self.__client = Client.__init__(self, api_key)

        self._domainName = domainName
        self._outputFormat = outputFormat

    def get_raw(self):
        
        try:

            return self.__get_raw()

        except:
            
            return PuffHelper._buildDefaultResponse(self)

    def __get_raw(self):
        if(self._outputFormat == XML_FORMAT):

            return self.__client.get_raw(self, self._domainName, XML_FORMAT)

        elif(self._outputFormat == JSON_FORMAT or self._outputFormat == RAW_FORMAT):
            
            return self.__client.get_raw(self, self._domainName, JSON_FORMAT)

    def run(self):
        self.__results = self.get_raw()

    def join(self):
        Thread.join(self)
        return self.__results
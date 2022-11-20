from apis.Base import Base
import requests
from json import loads
from threading import Thread
from bs4 import BeautifulSoup

class DnsRepoApiRequester(Thread, Base):

    def __init__(self, domainName: str = None):
        Thread.__init__(self)

        self._domainName = domainName

    def getSubdomains(self) -> list:
        
        try:
            
            return self.__getSubdomains()

        except:

            return []

    def __getSubdomains(self) -> list:

        url = "https://dnsrepo.noc.org/?domain={}".format(self._domainName)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36"
        }

        response = requests.get(url, headers)

        soup = BeautifulSoup(response.text, "lxml")

        subdomains = []
        if(response.ok):
            try:
            
                response = response.content.decode("utf-8")

                rows = soup.find_all("tr")

                for row in rows:
                    if row:
                        row_element = row.find("td")
                        if row_element:
                            link = row_element.find("a")
                            if(link):
                                subdomains.append(link.string.rstrip("."))

            except:
                pass

        unique_subdomains = list(set(subdomains))

        return unique_subdomains

    def run(self):
        self._results = self.getSubdomains()

    def join(self):
        Thread.join(self)
        return self._results
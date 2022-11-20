from apis.Base import Base
import requests
from json import loads
from threading import Thread

class HackerTargetApiRequester(Thread, Base):

    def __init__(self, domainName: str = None):
        Thread.__init__(self)

        self._domainName = domainName

    def getSubdomains(self) -> list:
        
        try:
            
            return self.__getSubdomains()

        except:
            
            return []

    def __getSubdomains(self) -> list:

        url = "https://api.hackertarget.com/hostsearch/?q={}".format(self._domainName)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36"
        }

        response = requests.get(url, headers)


        subdomains = []
        if(response.ok):
            try:
                
                response = response.content.decode("utf-8")

                records = response.splitlines()

                for record in records:
                    subdomain = record.split(",")[0]

                    subdomains.append(subdomain)

            except:
                pass

        unique_subdomains = list(set(subdomains))

        return unique_subdomains

    def run(self):
        self._results = self.getSubdomains()

    def join(self):
        Thread.join(self)
        return self._results
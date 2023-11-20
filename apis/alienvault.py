from apis.bases.Base import Base
import requests
from json import loads
from threading import Thread

class AlienVaultApiRequester(Thread, Base):

    def __init__(self, domainName: str = None):
        Thread.__init__(self)
        Base.__init__(self, domainName)

    def getSubdomains(self) -> list:
        
        try:
            
            return self.__getSubdomains()

        except:
            
            return []

    def __getSubdomains(self) -> list:

        url = "https://otx.alienvault.com/api/v1/indicators/domain/{}/passive_dns".format(self._domainName)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36"
        }

        response = requests.get(url, headers)


        subdomains = []
        if(response.ok):
            try:
                
                response = response.content.decode("utf-8")

                response_data = loads(response)

                records = response_data["passive_dns"]

                for record in records:
                    try:

                        subdomain = record["hostname"]
                        
                        if(Base._checkSubdomain(self, subdomain)):
                            subdomains.append(subdomain)

                    except:
                        pass

            except:
                pass

        unique_subdomains = list(set(subdomains))

        return unique_subdomains

    def run(self):
        self._results = self.getSubdomains()

    def join(self):
        Thread.join(self)
        return self._results

from apis.bases.Base import Base
import requests
from json import loads
from threading import Thread

class UrlscanApiRequester(Thread, Base):

    def __init__(self, domainName: str = None):
        Thread.__init__(self)
        Base.__init__(self, domainName)

    def getSubdomains(self) -> list:
        
        try:
            
            return self.__getSubdomains()

        except:
            
            return []

    def __getSubdomains(self) -> list:

        url = "https://urlscan.io/api/v1/search/?q=domain:{}".format(self._domainName)

        response = requests.get(url)

        subdomains = []
        if(response.ok):
            try:
                
                response = response.content.decode("utf-8")
                
                response_data = loads(response)

                records = response_data["results"]

                for record in records:

                    try:
                        domain = record["task"]["domain"]
                        
                        if(Base._checkSubdomain(self, domain)):
                            subdomains.append(domain)
                    except:
                        pass    

                    try:
                        apexDomain = record["task"]["apexDomain"]

                        if(Base._checkSubdomain(self, apexDomain)):   
                            subdomains.append(apexDomain)
                    except:
                        pass

                    try:
                        domain = record["page"]["domain"]
                        
                        if(Base._checkSubdomain(self, domain)):
                            subdomains.append(domain)
                    except:
                        pass

                    try:
                        apexDomain = record["page"]["apexDomain"]

                        if(Base._checkSubdomain(self, apexDomain)):   
                            subdomains.append(apexDomain)
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
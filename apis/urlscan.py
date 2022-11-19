import requests
from json import loads
from threading import Thread

class UrlscanApiRequester(Thread):

    __domain = None 
    __results = None

    def __init__(self, domain:str = None):
        Thread.__init__(self)

        self.__domain = domain

    def getSubdomains(self) -> list:

        url = "https://urlscan.io/api/v1/search/?q=domain:{}".format(self.__domain)

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
                        
                        if(domain.endswith(self.__domain)):
                            subdomains.append(domain)
                    except:
                        pass
                        

                    try:
                        apexDomain = record["task"]["apexDomain"]

                        if(apexDomain.endswith(self.__domain)):   
                            subdomains.append(apexDomain)
                    except:
                        pass

            except:
                pass

        unique_subdomains = list(set(subdomains))

        return unique_subdomains

    def run(self):
        self.__results = self.getSubdomains()

    def join(self):
        Thread.join(self)
        return self.__results

import requests
from json import loads
from threading import Thread

class CrtshApiRequester(Thread):

    __domainName = None 
    __results = None

    def __init__(self, domainName: str = None):
        Thread.__init__(self)

        self.__domainName = domainName

    def getSubdomains(self) -> list:
        
        try:
            
            return self.__getSubdomains()

        except:
            
            return []

    def __getSubdomains(self) -> list:

        url = "https://crt.sh/?q={}&output=json".format(self.__domainName)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36"
        }

        response = requests.get(url, headers)


        subdomains = []
        if(response.ok):
            try:
                
                response = response.content.decode("utf-8")

                response_data = loads(response)

                for data in response_data:
                    try:
                        
                        parsed = data["name_value"].split("\n")

                    except:

                        continue

                    for subdomain in parsed:
                        subdomains.append(subdomain.replace("*.", "", 1))

            except:
                pass

        unique_subdomains = list(set(subdomains))

        return unique_subdomains

    def run(self):
        self.__results = self.getSubdomains()

    def join(self):
        Thread.join(self)
        return self.__results

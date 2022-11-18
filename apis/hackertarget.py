import requests
from json import loads
from threading import Thread

class HackerTargetApiRequester(Thread):

    __domain = None 
    __results = None

    def __init__(self, domain:str = None):
        Thread.__init__(self)

        self.__domain = domain

    def getSubdomains(self) -> list:

        url = "https://api.hackertarget.com/hostsearch/?q={}".format(self.__domain)

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

            except Exception as e:
                print(e)

        unique_subdomains = list(set(subdomains))

        return unique_subdomains

    def run(self):
        self.__results = self.getSubdomains()

    def join(self):
        Thread.join(self)
        return self.__results
import requests
from requests.exceptions import RequestException
from concurrent.futures import ThreadPoolExecutor
from errors.SubdomainLookupError import SubdomainLookupError
from errors.BadError import BadError

class LookupWrapper():

    __executor = None

    def __init__(self, maxWorkers: int or None = None):

        if(maxWorkers is None):

            self.__executor = ThreadPoolExecutor()

        else:

            self.__executor = ThreadPoolExecutor(maxWorkers)

    def lookupSubdomains(self, subdomains: list) -> list:

        futures = [
            self.__executor.submit(self.__lookupSubdomain, subdomain) for subdomain in subdomains
        ]

        self.__executor.shutdown(wait=False)

        return futures

        

    def __lookupSubdomain(self, subdomain: str) -> dict:
        output = {
            "subdomain": subdomain,
            "statusCode": None,
            "title": None,
            "backend": None
        }

        try:

            url = "http://{}".format(subdomain)
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
                "Connection": "keep-alive"
            }

            response = requests.get(url, headers=headers, timeout=10)

            output["statusCode"] = response.status_code

            return output
        
        except RequestException:
            raise SubdomainLookupError()

        except:
            raise BadError()

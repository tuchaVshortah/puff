import random
import requests
import sys
import queue
import time
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

from requests.exceptions import RequestException
from errors.SubdomainLookupError import SubdomainLookupError

class LookupWrapper():

    __executor = None
    __probingSleepTime = None
    __offsetSleepTime = None

    def __init__(self, maxWorkers: int or None = None, probingSleepTime: float = 0.0):

        if(maxWorkers is None):

            self.__executor = ThreadPoolExecutor()

        else:

            self.__executor = ThreadPoolExecutor(maxWorkers)

        if(probingSleepTime is None):
            self.__probingSleepTime = 0.0
        else:
            self.__probingSleepTime = probingSleepTime

        self.__offsetSleepTime = 0.0

    def lookupSubdomains(self, subdomains: list, number: int or None = None, randomizedSubdomainProbing: bool = False) -> list:

        '''
        futures = [
            self.__executor.submit(self.__lookupSubdomain, subdomain) for subdomain in subdomains
        ]
        '''

        if(number is not None):
            subdomains = subdomains[:number]

        if(randomizedSubdomainProbing):
            random.shuffle(subdomains)

        futures = []
        for subdomain in subdomains:

            future = self.__executor.submit(self.__lookupSubdomain, subdomain, self.__offsetSleepTime)
            futures.append(future)

            self.__offsetSleepTime += self.__probingSleepTime

        self.__executor.shutdown(wait=False)

        return futures

        

    def __lookupSubdomain(self, subdomain: str, sleepTime: float = 0.0) -> dict:
        
        time.sleep(sleepTime)

        output = {
            "subdomain": subdomain,
            "statusCode": "N/A",
            "title": "N/A",
            "backend": "N/A"
        }

        try:

            url = "http://{}/".format(subdomain)

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0",
                "Connection": "keep-alive"
            }

            response = requests.get(url, headers=headers, timeout=10)

            output["statusCode"] = str(response.status_code)

            soup = BeautifulSoup(response.text, "lxml")

            title = None
            title = soup.find("title")

            try:

                title = title.getText()
                
            except:
                pass

            backend = None
            try:

                backend = response.headers["Server"]

            except:
                pass
            
            if(title is not None):
                output["title"] = str(title)

            if(backend is not None):
                output["backend"] = str(backend)

            return output
        
        except RequestException:
            raise SubdomainLookupError()

    def killThreads(self):
        py_version = sys.version_info
        if ( py_version.major == 3 ) and ( py_version.minor < 9 ):
            # py versions less than 3.9
            # Executor#shutdown does not accept
            # cancel_futures keyword
            # manually shutdown
            # code taken from https://github.com/python/cpython/blob/3.9/Lib/concurrent/futures/thread.py#L210
            while True:
                # cancel all waiting tasks
                try:
                    work_item = self.__executor._work_queue.get_nowait()
                                    
                except queue.Empty:
                    break
                                    
                if work_item is not None:
                    work_item.future.cancel()

        else:
            self.__executor.shutdown(cancel_futures=True)

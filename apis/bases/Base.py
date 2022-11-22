import requests
from requests.exceptions import ConnectTimeout, ConnectionError

class Base():

    _domainName = None
    _outputFormat = None
    _response = None
    _results = None

    def __init__(self, domainName: str, outputFormat: str):
        self._domainName = domainName
        self._outputFormat = outputFormat

    def _checkSubdomain(self, subdomain: str) -> bool:
        return subdomain.endswith(".{}".format(self._domainName))

    def _getSubdomainStatusCode(self, subdomain: str, timeout = 10) -> int:

        headers = {
            "Host": subdomain,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.5304.63 Safari/537.36"
        }

        try:

            response = requests.get("http://{}".format(subdomain), headers, timeout=timeout)
        
        except ConnectTimeout:

            return -1

        except ConnectionError:

            return -2

        except:

            return -100

        return response.status_code

import requests
from requests.exceptions import ConnectTimeout, ConnectionError

class Base():

    _domainName = None
    _results = None

    def __init__(self, domainName: str):
        self._domainName = domainName

    def _checkSubdomain(self, subdomain: str) -> bool:
        return subdomain.endswith(".{}".format(self._domainName))


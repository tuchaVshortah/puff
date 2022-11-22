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
class Base():

    _domainName = None
    _outputFormat = None
    _response = None
    _results = None

    def _checkSubdomain(self, subdomain: str) -> bool:
        return subdomain.endswith(".{}".format(self._domainName))
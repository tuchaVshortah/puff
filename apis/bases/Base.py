class Base():

    _domainName = None
    _outputFormat = None
    _response = None
    _results = None

    def _checkSubdomain(self, domain: str) -> bool:
        return domain.endswith(".{}".format(self._domainName))
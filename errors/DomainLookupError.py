class DomainLookupError(Exception):
    def __init__(self, domain) -> None:
        self.domain = domain
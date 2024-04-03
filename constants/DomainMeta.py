class DomainMetaInformation():

    domain = None
    statusCode = None
    title = None
    backend = None

    def __init__(self, domain: str = "N/A", statusCode: str = "N/A", title: str = "N/A", backend: str = "N/A"):
        self.domain = domain
        self.statusCode = statusCode
        self.title = title
        self.backend = backend

    def toDictionary(self) -> dict:
        return {
            "domain": self.domain,
            "statusCode": self.statusCode,
            "title": self.title,
            "backend": self.backend
        }


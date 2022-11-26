from apis.bases.Base import Base
from json import loads, dumps
import xml.dom.minidom
from xml.dom.minidom import Document

class WhoIsXmlApiBase(Base):

    def __init__(self, domainName: str):
        Base.__init__(self, domainName)

    
    def _parseSubdomains(self, response_data: dict) -> list:

        subdomains = []


        records = response_data["result"]["records"]

        for record in records:
            
            subdomain = record["domain"]
            if(Base._checkSubdomain(self, subdomain)):
                subdomains.append(subdomain)


        return subdomains
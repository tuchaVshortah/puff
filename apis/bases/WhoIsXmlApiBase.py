from apis.bases.Base import Base
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT
from json import loads, dumps
import xml.dom.minidom
from xml.dom.minidom import Document

class WhoIsXmlApiBase(Base):

    def __init__(self, domainName: str, outputFormat: str):
        Base.__init__(self, domainName, outputFormat)

    def _checkRecords(self, response_data: dict or Document):

        records = self._getRecords(response_data)
        if(self._outputFormat == XML_FORMAT):

            count = response_data.getElementsByTagName("count")[0]

            for record in records.getElementsByTagName("record"):
                
                subdomain = record.firstChild.lastChild.data

                if(not Base._checkSubdomain(self, subdomain)):

                    record.removeChild(record)
                    count -= 1

        else:

            count = response_data["result"]["count"]

            for i in range(len(records)):

                subdomain = records[i]["domain"]

                if(not Base._checkSubdomain(self, subdomain)):
                    
                    records.pop(i)
                    count -= 1

    def _getRecords(self, response_data: dict or Document) -> Document or list:

        records = None
        if(self._outputFormat == XML_FORMAT):
            records = response_data.getElementsByTagName("records")[0]

        else:
            records = response_data["result"]["records"]

        return records

    def _loadResponse(self, response: str) -> Document or dict:

        response_data = None
        if(self._outputFormat == XML_FORMAT):
            response_data = self.__loadXmlResponse(response)
        
        else:
            response_data = self.__loadJsonResponse(response)

        return response_data

    def __loadXmlResponse(self, response: str) -> Document:
        response_data = xml.dom.minidom.parseString(response)

        return response_data

    def __loadJsonResponse(self, response: str) -> dict:
        response_data = loads(response)

        return response_data

    def _buildDefaultResponse(self) -> str:
        response = None


        if(self._outputFormat == XML_FORMAT):
            response = f'''\
<?xml version="1.0" ?>
<xml>
    <search>{self._domainName}</search>
    <result>
        <count>10000</count>
        <records>
        </records>
    </result>
</xml>'''
    
        else:
            response = f'''\
{{
    "search": "{self._domainName}",
    "result": {{
        "count": 0,
        "records": []
    }}
}}'''

        return response

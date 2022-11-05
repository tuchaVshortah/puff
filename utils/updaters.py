from json import loads, dumps
import xml.dom.minidom
from xml.etree import ElementTree as ET
from subdomainslookup.models.response import Response as ApiResponse

def updateJsonResponse(json_response: str, new_subdomains: list) -> str:
    
    response_data = loads(json_response)
    records = response_data["records"]

    old_subdomains = []
    for record in records:
        old_subdomains.append(record["domain"])

    subdomains = []
    subdomains.extend(old_subdomains)
    subdomains.extend(new_subdomains)

    unique_subdomains = list(set(subdomains))

    for subdomain in unique_subdomains:
        response_data["records"].append(
            {
                "domain": subdomain
            }
        )

    json_response = dumps(response_data)

    return json_response

def updateXmlResponse(xml_response: str, new_subdomains: list) -> str:
    
    response_data = xml.dom.minidom.parseString(xml_response)
    old_subdomains = response_data.getElementsByTagName("domain")
    
    subdomains = []
    subdomains.extend(old_subdomains)
    subdomains.extend(new_subdomains)

    unique_subdomains = list(set(subdomains))

    records = response_data.getElementsByTagName("records")[0]
    for subdomain in subdomains:
        new_record = ET.Element("record")

        new_domain = ET.Element("domain")
        new_domain.text = subdomain

        new_record.append(new_domain)

        records.append(new_record)
        

def updateRawResponse(raw_response: ApiResponse, new_subdomains: list) -> ApiResponse:

    subdomains = []
    subdomains.extend(raw_response.result.records)
    subdomains.extend(new_subdomains)

    unique_subdomains = list(set(subdomains))
    raw_response.result.records = unique_subdomains

    return raw_response
from json import loads, dumps
import xml.dom.minidom
from subdomainslookup.models.response import Response as ApiResponse

def updateJsonResponse(json_response: str, new_subdomains: list) -> str:
    
    response_data = loads(json_response)
    records = response_data["records"]

    old_subdomains = []
    for record in records:
        old_subdomains.append(record["domain"])

    subdomains = []
    subdomains.append(old_subdomains)
    subdomains.append(new_subdomains)

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
    pass

def updateRawResponse(raw_response: ApiResponse, new_subdomains: list) -> ApiResponse:

    subdomains = raw_response.result.records
    subdomains.append(new_subdomains)

    unique_subdomains = list(set(subdomains))
    raw_response.result.records = unique_subdomains

    return raw_response
from json import loads, dumps
import xml.dom.minidom
from xml.dom.minidom import Document
from subdomainslookup.models.response import Result, Record, Response as ApiResponse
from subdomainslookup.models.response import _list_of_objects

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

def updateXmlResponse(xml_response: Document, new_subdomains: list) -> str:
    
    old_subdomains = []
    old_subdomains_xml = xml_response.getElementsByTagName("domain")
    for subdomain in old_subdomains_xml:
        old_subdomains.append(subdomain.firstChild.nodeValue)      
    
    print("Printing an element from parsed old_subdomains_xml: " + old_subdomains[0])

    subdomains = []
    subdomains.extend(old_subdomains)
    subdomains.extend(new_subdomains)

    unique_subdomains = list(set(subdomains))

    records = xml_response.getElementsByTagName("records")[0]
    for subdomain in unique_subdomains:
        new_record = xml_response.createElement("record")

        new_subdomain = xml_response.createElement("domain")
        subdomain_text_node = xml_response.createTextNode(subdomain)
        new_subdomain.appendChild(subdomain_text_node)
        
        first_seen = xml_response.createElement("first_seen")
        first_seen_text_node = xml_response.createTextNode("0")
        first_seen.appendChild(first_seen_text_node)
        
        last_seen = xml_response.createElement("last_seen")
        first_seen_text_node = xml_response.createTextNode("0")
        last_seen.appendChild(first_seen_text_node)


        new_record.appendChild(new_subdomain)
        new_record.appendChild(first_seen)
        new_record.appendChild(last_seen)

        records.appendChild(new_record)
        

def updateRawResponse(raw_response: ApiResponse, new_subdomains: list):

    subdomains = []

    old_subdomains = []
    for record in raw_response.result.records:
        old_subdomains.append(record["domain"])

    subdomains.extend(old_subdomains)
    subdomains.extend(new_subdomains)

    unique_subdomains = list(set(subdomains))
    
    new_records = {
        "records": []
    }

    for subdomain in unique_subdomains:
        new_record = {
            "domain": subdomain,
            "first_seen": None,
            "last_seen": None
        }

        new_records["records"].append(new_record)

    raw_response.result.records.extend(_list_of_objects(new_records, "records", "Record"))

        

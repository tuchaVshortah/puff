from puff.apis.whoisxmlapi import PuffApiRequester
from puff.apis.crtsh import CrtshApiRequester
from puff.constants.outputformats import XML_FORMAT, JSON_FORMAT
from threading import Thread
from json import loads, dumps
import xml.dom.minidom
from xml.dom.minidom import Document
from subdomainslookup.models.response import Result, Record, Response as ApiResponse
from subdomainslookup.models.response import _list_of_objects

class ApiWrapper():

    self.__target = None
    self.__outputFormat = None
    self.__boost = None

    def __init__(self, target:str = None, outputFormat:str = JSON_FORMAT, boost:bool = False):
        self.__target = target
        self.__outputFormat = outputFormat
        self.__boost = boost
    
    def run(self):
        if(self.__boost):
            pass
            
    def __slowTasks(self):
        
        puff_api_requester = PuffApiRequester(self.__target, self.__outputFormat)
        crtsh_api_requester = CrtshApiRequester(self.__target)

        puff_api_response = puff_api_requester.post()
        crtsh_api_response = crtsh_api_requester.getSubdomains()

    def __fastTasks(self):
        pass

    def __updateJsonResponse(json_response: dict, new_subdomains: list):
    
        records = json_response["result"]["records"]

        old_subdomains = []
        for record in records:
            old_subdomains.append(record["domain"])

        subdomains = []
        subdomains.extend(old_subdomains)
        subdomains.extend(new_subdomains)

        unique_subdomains = list(set(subdomains))

        for subdomain in unique_subdomains:
            json_response["result"]["records"].append(
                {
                    "domain": subdomain,
                    "first_seen": "0",
                    "last_seen": "0"
                }
            )


    def __updateXmlResponse(xml_response: Document, new_subdomains: list) -> str:
        
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
            

    def __updateRawResponse(raw_response: ApiResponse, new_subdomains: list):

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
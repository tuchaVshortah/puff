from puff.apis.whoisxmlapi import PuffApiRequester
from puff.apis.crtsh import CrtshApiRequester
from puff.constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT
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
    self.__results = None

    def __init__(self, target: str = None, outputFormat: str = JSON_FORMAT, boost: bool = False):
        self.__target = target
        self.__outputFormat = outputFormat
        self.__boost = boost
    
    def run(self):
        if(self.__boost):
            self.__results = self.__fastTasks()

        else:
            self.__results = self.__slowTasks()
        
        try:
        
            return self.__beautify(self.__results)
        
        except:

            print("Could not return a beautified API response\n", error)
            exit()

    def __beautify(self, response_data):

        beautified_response_data = None
        if(self.__outputFormat == XML_FORMAT):
            beautified_response_data = response_data.toprettyxml()
        
        elif(self.__outputFormat == JSON_FORMAT):
            beautified_response_data = dumps(response_data, indent=2)

        elif(self.__outputFormat == RAW_FORMAT):
            records = response_data.result.records
            beautified_response_data = "\n".join(records)

        return beautified_response_data
            
    def __slowTasks(self):
        
        puff_api_requester = PuffApiRequester(self.__target, self.__outputFormat)
        crtsh_api_requester = CrtshApiRequester(self.__target)

        puff_api_response = puff_api_requester.post()
        crtsh_subdomains = crtsh_api_requester.getSubdomains()

        return self.__updateResponse(puff_api_response, new_subdomains)
        
    def __fastTasks(self):

        puff_api_requester = PuffApiRequester(self.__target, self.__outputFormat)
        crtsh_api_requester = CrtshApiRequester(self.__target)

        puff_api_requester.run()
        crtsh_api_requester.run()

        puff_api_response = puff_api_requester.join()
        crtsh_subdomains = crtsh_api_requester.join()

        return self.__updateResponse(puff_api_response, new_subdomains)

    def __updateResponse(self, response, new_subdomains):
        
        try:

            response_data = self.__loadResponse(response)
        
        except:

            print("Could not parse the API response\n", error)
            exit()

        try:

            self.__updateResponseData(response, new_subdomains)

        except:
            print("Could not add new records to the API response\n", error)
            exit()
        
        return response_data

    def __loadResponse(self, response):

        response_data = None
        if(self.__outputFormat == XML_FORMAT):
            response_data = self.__loadXmlResponse(response)
        
        elif(self.__outputFormat == JSON_FORMAT):
            response_data = self.__loadJsonResponse(response)
        
        elif(self.__outputFormat == RAW_FORMAT):
            response_data = self.__loadRawResponse(response)

        return response_data

    def __loadXmlResponse(self, response: str) -> Document:
        response_data = xml.dom.minidom.parseString(response)

        return response_data

    def __loadJsonResponse(self, response: str) -> dict:
        response_data = loads(response)

        return response_data

    def __loadRawResponse(self, response: str) -> ApiResponse:
        response_data = self.__loadJsonResponse(response)
        response = ApiResponse(response_data)

        return response

    def __updateResponseData(self, response_data, new_subdomains):

        if(self.__outputFormat == XML_FORMAT):
            self.__updateXmlResponseData(response_data, new_subdomains)
        
        elif(self.__outputFormat == JSON_FORMAT):
            self.__updateJsonResponseData(response_data, new_subdomains)
        
        elif(self.__outputFormat == RAW_FORMAT):
            self.__updateRawResponseData(response_data, new_subdomains)


    def __updateJsonResponseData(self, json_response_data: dict, new_subdomains: list):
    
        records = json_response_data["result"]["records"]

        old_subdomains = []
        for record in records:
            old_subdomains.append(record["domain"])

        subdomains = []
        subdomains.extend(old_subdomains)
        subdomains.extend(new_subdomains)

        unique_subdomains = list(set(subdomains))

        for subdomain in unique_subdomains:
            json_response_data["result"]["records"].append(
                {
                    "domain": subdomain,
                    "first_seen": "0",
                    "last_seen": "0"
                }
            )


    def __updateXmlResponseData(self, xml_response_data: Document, new_subdomains: list) -> str:
        
        old_subdomains = []
        old_subdomains_xml = xml_response_data.getElementsByTagName("domain")
        for subdomain in old_subdomains_xml:
            old_subdomains.append(subdomain.firstChild.nodeValue)      
        
        print("Printing an element from parsed old_subdomains_xml: " + old_subdomains[0])

        subdomains = []
        subdomains.extend(old_subdomains)
        subdomains.extend(new_subdomains)

        unique_subdomains = list(set(subdomains))

        records = xml_response_data.getElementsByTagName("records")[0]
        for subdomain in unique_subdomains:
            new_record = xml_response_data.createElement("record")

            new_subdomain = xml_response_data.createElement("domain")
            subdomain_text_node = xml_response_data.createTextNode(subdomain)
            new_subdomain.appendChild(subdomain_text_node)
            
            first_seen = xml_response_data.createElement("first_seen")
            first_seen_text_node = xml_response_data.createTextNode("0")
            first_seen.appendChild(first_seen_text_node)
            
            last_seen = xml_response_data.createElement("last_seen")
            first_seen_text_node = xml_response_data.createTextNode("0")
            last_seen.appendChild(first_seen_text_node)


            new_record.appendChild(new_subdomain)
            new_record.appendChild(first_seen)
            new_record.appendChild(last_seen)

            records.appendChild(new_record)
            

    def __updateRawResponseData(self, raw_response_data: ApiResponse, new_subdomains: list):

        subdomains = []

        old_subdomains = []
        for record in raw_response_data.result.records:
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

        raw_response_data.result.records.extend(_list_of_objects(new_records, "records", "Record"))
from apis.whoisxmlapi import PuffClient, PuffApiRequester
from apis.crtsh import CrtshApiRequester
from apis.urlscan import UrlscanApiRequester
from apis.alienvault import AlienVaultApiRequester
from apis.anubis import AnubisApiRequester
from apis.hackertarget import HackerTargetApiRequester
from apis.dnsrepo import DnsRepoApiRequester
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT
from threading import Thread
from json import loads, dumps
import xml.dom.minidom
from xml.dom.minidom import Document
from subdomainslookup.models.response import Result, Record, Response as ApiResponse
from subdomainslookup.models.response import _list_of_objects

class ApiWrapper():

    __target = None
    __puff_client = None
    __puff_api_requester = None
    __crtsh_api_requester = None
    __urlscan_api_requester = None
    __alienvault_api_requester = None
    __anubis_api_requester = None
    __hackertarget_api_requester = None
    __dnsrepo_api_requester = None
    __outputFormat = None
    __count = 0
    __boost = None
    __verbose = None
    __results = None

    def __init__(self, target: str = None, outputFormat: str = JSON_FORMAT, boost: bool = False, verbose: bool = False, whoisxmlapi_key: str or None = None):

        self.__target = target
        self.__outputFormat = outputFormat
        self.__boost = boost
        self.__verbose = verbose

        if(whoisxmlapi_key is not None):

            self.__puff_client = PuffClient(whoisxmlapi_key, self.__target, self.__outputFormat)

        elif(whoisxmlapi_key is None):
            
            self.__puff_api_requester = PuffApiRequester(self.__target, self.__outputFormat)
        
        self.__crtsh_api_requester = CrtshApiRequester(self.__target)
        self.__urlscan_api_requester = UrlscanApiRequester(self.__target)
        self.__alienvault_api_requester = AlienVaultApiRequester(self.__target)
        self.__anubis_api_requester = AnubisApiRequester(self.__target)
        self.__hackertarget_api_requester = HackerTargetApiRequester(self.__target)
        self.__dnsrepo_api_requester = DnsRepoApiRequester(self.__target)

    
    def run(self):

        self.__status("Running tasks...")

        if(self.__boost):
            self.__results = self.__fastTasks()

        else:
            self.__results = self.__slowTasks()
        
        self.__status("Done!")
        self.__status("{} subdomains were found!".format(self.__count))
        try:
        
            return self.__beautify(self.__results)
        
        except:

            self.__status("Could not return beautified output...")
            self.__status("Exiting...")
            exit()

    def __beautify(self, response_data: dict or Document or ApiResponse):

        self.__status("Trying to beautify data...")

        beautified_response_data = None
        if(self.__outputFormat == XML_FORMAT):
            beautified_response_data = response_data.toprettyxml()
        
        elif(self.__outputFormat == JSON_FORMAT):
            beautified_response_data = dumps(response_data, indent=2)

        elif(self.__outputFormat == RAW_FORMAT):
            records = response_data.result.records

            subdomains = []

            for record in records:
                subdomains.append(record.domain)

            beautified_response_data = "\n".join(subdomains)

        self.__status("Done!")

        return beautified_response_data

    def __status(self, message: str):
        if(self.__verbose == True):
            print("//=> {}".format(message))
            
    def __slowTasks(self):

        data_object = None

        if(self.__puff_client is None):

            data_object = self.__puff_api_requester.post()
        
        elif(self.__puff_client is not None):

            data_object = self.__puff_client.get_raw()

        crtsh_subdomains = self.__crtsh_api_requester.getSubdomains()
        urlscan_subdomains = self.__urlscan_api_requester.getSubdomains()
        alienvault_subdomains = self.__alienvault_api_requester.getSubdomains()
        anubis_subdomains = self.__anubis_api_requester.getSubdomains()
        hackertarget_subdomains = self.__hackertarget_api_requester.getSubdomains()
        dnsrepo_subdomains = self.__dnsrepo_api_requester.getSubdomains()


        self.__updateDataObject(data_object, crtsh_subdomains)
        self.__updateDataObject(data_object, urlscan_subdomains)
        self.__updateDataObject(data_object, alienvault_subdomains)
        self.__updateDataObject(data_object, anubis_subdomains)
        self.__updateDataObject(data_object, hackertarget_subdomains)
        self.__updateDataObject(data_object, dnsrepo_subdomains)

        return data_object

        
    def __fastTasks(self):

        self.__crtsh_api_requester.start()
        self.__urlscan_api_requester.start()
        self.__alienvault_api_requester.start()
        self.__anubis_api_requester.start()
        self.__hackertarget_api_requester.start()
        self.__dnsrepo_api_requester.start()

        data_object = None

        if(self.__puff_client is None):

            self.__puff_api_requester.start()
            
            data_object = self.__puff_api_requester.join()
            
        elif(self.__puff_client is not None):

            self.__puff_client.start()

            data_object = self.__puff_client.join()


        crtsh_subdomains = self.__crtsh_api_requester.join()
        urlscan_subdomains = self.__urlscan_api_requester.join()
        alienvault_subdomains = self.__alienvault_api_requester.join()
        anubis_subdomains = self.__anubis_api_requester.join()
        hackertarget_subdomains = self.__hackertarget_api_requester.join()
        dnsrepo_subdomains = self.__dnsrepo_api_requester.join()


        self.__updateDataObject(data_object, crtsh_subdomains)
        self.__updateDataObject(data_object, urlscan_subdomains)
        self.__updateDataObject(data_object, alienvault_subdomains)
        self.__updateDataObject(data_object, anubis_subdomains)
        self.__updateDataObject(data_object, hackertarget_subdomains)
        self.__updateDataObject(data_object, dnsrepo_subdomains)

        return data_object


    def __updateDataObject(self, response_data: dict or Document or ApiResponse, new_subdomains):

        try:

            self.__updateResponseData(response_data, new_subdomains)

        except:
            self.__status("Could not update subdomain records...")
            self.__status("Exiting...")
            exit()


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
            if(subdomain not in old_subdomains):
                json_response_data["result"]["records"].append(
                    {
                        "domain": subdomain,
                        "first_seen": "0",
                        "last_seen": "0"
                    }
                )
                json_response_data["result"]["count"] += 1
        
        self.__count = json_response_data["result"]["count"]


    def __updateXmlResponseData(self, xml_response_data: Document, new_subdomains: list) -> str:
        
        old_subdomains = []
        old_subdomains_xml = xml_response_data.getElementsByTagName("domain")
        for subdomain in old_subdomains_xml:
            old_subdomains.append(subdomain.firstChild.nodeValue)      

        subdomains = []
        subdomains.extend(old_subdomains)
        subdomains.extend(new_subdomains)

        unique_subdomains = list(set(subdomains))

        records = xml_response_data.getElementsByTagName("records")[0]
        count = xml_response_data.getElementsByTagName("count")[0]
        for subdomain in unique_subdomains:
            if(subdomain in old_subdomains):
                continue

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
            
            count.lastChild.data = str(int(count.lastChild.data) + 1)
        
        self.__count = count.lastChild.data
            

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
            if subdomain not in old_subdomains:
                new_record = {
                    "domain": subdomain,
                    "first_seen": None,
                    "last_seen": None
                }

                new_records["records"].append(new_record)

                raw_response_data.result.count += 1

        raw_response_data.result.records.extend(_list_of_objects(new_records, "records", "Record"))

        self.__count = raw_response_data.result.count
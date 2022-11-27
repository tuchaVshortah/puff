from apis.whoisxmlapi import WhoIsXmlClientApiRequester, WhoisXmlApiRequester
from apis.crtsh import CrtshApiRequester
from apis.urlscan import UrlscanApiRequester
from apis.alienvault import AlienVaultApiRequester
from apis.anubis import AnubisApiRequester
from apis.hackertarget import HackerTargetApiRequester
from apis.dnsrepo import DnsRepoApiRequester

from wrappers.LookupWrapper import LookupWrapper
from wrappers.OutputWrapper import OutputWrapper

from constants.outputformats import JSON_FORMAT, TXT_FORMAT

from threading import Thread

from errors.SomeError import SomeError

class ApiWrapper():

    __target = None
    __outputFormat = None
    __boost = None
    __colorize = None
    __verbose = None
    __alive = None
    __file = None
    __default_file = None

    __whois_xml_client_api_requester = None
    __whois_xml_api_requester = None
    __crtsh_api_requester = None
    __urlscan_api_requester = None
    __alienvault_api_requester = None
    __anubis_api_requester = None
    __hackertarget_api_requester = None
    __dnsrepo_api_requester = None

    __lookup_wrapper = None
    __output_wrapper = None


    def __init__(self, target: str = None, outputFormat: str = JSON_FORMAT,\
        boost: bool = False, colorize: bool = False, verbose: bool = False, alive: bool = False,\
        file = None, defaultFile: bool = False, whoisxmlapi_key: str or None = None):

        self.__target = target
        self.__outputFormat = outputFormat
        self.__boost = boost
        self.__colorize = colorize
        self.__verbose = verbose
        self.__alive = alive
        self.__file = file
        self.__defaultFile = defaultFile

        if(whoisxmlapi_key is not None):

            self.__whois_xml_client_api_requester = WhoIsXmlClientApiRequester(whoisxmlapi_key, self.__target)

        elif(whoisxmlapi_key is None):
            
            self.__whois_xml_api_requester = WhoisXmlApiRequester(self.__target)
        
        self.__crtsh_api_requester = CrtshApiRequester(self.__target)
        self.__urlscan_api_requester = UrlscanApiRequester(self.__target)
        self.__alienvault_api_requester = AlienVaultApiRequester(self.__target)
        self.__anubis_api_requester = AnubisApiRequester(self.__target)
        self.__hackertarget_api_requester = HackerTargetApiRequester(self.__target)
        self.__dnsrepo_api_requester = DnsRepoApiRequester(self.__target)

    
    def run(self):

        if(self.__boost):
            self.__fastTasks()

        else:
            self.__slowTasks()



    def killLookupWrapperThreads(self):
        self.__lookup_wrapper.killThreads()

            
    def __slowTasks(self):

        whoisxmlapi_subdomains = None

        if(self.__whois_xml_client_api_requester is None):

            whoisxmlapi_subdomains = self.__whois_xml_api_requester.getSubdomains()
        
        elif(self.__whois_xml_client_api_requester is not None):

            whoisxmlapi_subdomains = self.__whois_xml_client_api_requester.getSubdomains()

        crtsh_subdomains = self.__crtsh_api_requester.getSubdomains()
        urlscan_subdomains = self.__urlscan_api_requester.getSubdomains()
        alienvault_subdomains = self.__alienvault_api_requester.getSubdomains()
        anubis_subdomains = self.__anubis_api_requester.getSubdomains()
        hackertarget_subdomains = self.__hackertarget_api_requester.getSubdomains()
        dnsrepo_subdomains = self.__dnsrepo_api_requester.getSubdomains()

        subdomains = []

        subdomains.extend(whoisxmlapi_subdomains)
        subdomains.extend(crtsh_subdomains)
        subdomains.extend(urlscan_subdomains)
        subdomains.extend(alienvault_subdomains)
        subdomains.extend(anubis_subdomains)
        subdomains.extend(hackertarget_subdomains)
        subdomains.extend(dnsrepo_subdomains)

        if(self.__alive):
            self.__lookup_wrapper = LookupWrapper(1)

            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__file, self.__defaultFile, self.__lookup_wrapper.killThreads)

            futures = self.__lookup_wrapper.lookupSubdomains(subdomains)

            try:

                self.__output_wrapper.outputFutures(futures)

            except SomeError:
                self.__lookup_wrapper.killThreads()
        
        else:
            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__file, self.__defaultFile)
            self.__output_wrapper.outputSubdomains(subdomains)

        
    def __fastTasks(self):

        self.__crtsh_api_requester.start()
        self.__urlscan_api_requester.start()
        self.__alienvault_api_requester.start()
        self.__anubis_api_requester.start()
        self.__hackertarget_api_requester.start()
        self.__dnsrepo_api_requester.start()

        whoisxmlapi_subdomains = None

        if(self.__whois_xml_client_api_requester is None):

            self.__whois_xml_api_requester.start()
            
            whoisxmlapi_subdomains = self.__whois_xml_api_requester.join()
            
        elif(self.__whois_xml_client_api_requester is not None):

            self.__whois_xml_client_api_requester.start()

            whoisxmlapi_subdomains = self.__whois_xml_client_api_requester.join()


        crtsh_subdomains = self.__crtsh_api_requester.join()
        urlscan_subdomains = self.__urlscan_api_requester.join()
        alienvault_subdomains = self.__alienvault_api_requester.join()
        anubis_subdomains = self.__anubis_api_requester.join()
        hackertarget_subdomains = self.__hackertarget_api_requester.join()
        dnsrepo_subdomains = self.__dnsrepo_api_requester.join()

        subdomains = []

        subdomains.extend(whoisxmlapi_subdomains)
        subdomains.extend(crtsh_subdomains)
        subdomains.extend(urlscan_subdomains)
        subdomains.extend(alienvault_subdomains)
        subdomains.extend(anubis_subdomains)
        subdomains.extend(hackertarget_subdomains)
        subdomains.extend(dnsrepo_subdomains)

        if(self.__alive):
            self.__lookup_wrapper = LookupWrapper()

            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__file, self.__defaultFile, self.__lookup_wrapper.killThreads)

            futures = self.__lookup_wrapper.lookupSubdomains(subdomains)

            try:

                self.__output_wrapper.outputFutures(futures)

            except SomeError:
                self.__lookup_wrapper.killThreads()

        else:
            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__file, self.__defaultFile)
            self.__output_wrapper.outputSubdomains(subdomains)
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

from rich.progress import Progress
from rich import print as rprint

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

        with Progress() as progress:

            task = None
            if(self.__colorize):
                task = progress.add_task("[red]Working...", total=600)
            
            else:
                task = progress.add_task("Working...", total=600)

            progress.update(task, advance=20)
            crtsh_subdomains = self.__crtsh_api_requester.getSubdomains()
            progress.update(task, advance=80)

            urlscan_subdomains = self.__urlscan_api_requester.getSubdomains()
            progress.update(task, advance=100)

            alienvault_subdomains = self.__alienvault_api_requester.getSubdomains()
            progress.update(task, advance=100)

            anubis_subdomains = self.__anubis_api_requester.getSubdomains()
            progress.update(task, advance=100)

            hackertarget_subdomains = self.__hackertarget_api_requester.getSubdomains()
            progress.update(task, advance=100)

            dnsrepo_subdomains = self.__dnsrepo_api_requester.getSubdomains()
            progress.update(task, advance=100)

        subdomains = []

        if(self.__verbose):
            if(self.__colorize):
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(whoisxmlapi_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [red]whoisxmlapi.com[/red]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(crtsh_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [green]crt.sh[/green]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(urlscan_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [yellow]urlscan.io[/yellow]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(alienvault_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [blue]otx.alienvault.com[/blue]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(anubis_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [magenta]jonlu.ca[/magenta]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(dnsrepo_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [cyan]dnsrepo.noc.org[/cyan]")

            else:
                rprint(f"{len(whoisxmlapi_subdomains)} subdomains from whoisxmlapi.com")
                rprint(f"{len(crtsh_subdomains)} subdomains from crt.sh")
                rprint(f"{len(urlscan_subdomains)} subdomains from] urlscan.io")
                rprint(f"{len(alienvault_subdomains)} subdomains from otx.alienvault.com")
                rprint(f"{len(anubis_subdomains)} subdomains from jonlu.ca")
                rprint(f"{len(dnsrepo_subdomains)} subdomains from dnsrepo.noc.org")


        subdomains.extend(whoisxmlapi_subdomains)
        subdomains.extend(crtsh_subdomains)
        subdomains.extend(urlscan_subdomains)
        subdomains.extend(alienvault_subdomains)
        subdomains.extend(anubis_subdomains)
        subdomains.extend(hackertarget_subdomains)
        subdomains.extend(dnsrepo_subdomains)

        subdomains = list(set(subdomains))

        if(self.__alive):
            self.__lookup_wrapper = LookupWrapper(1)
            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__verbose, self.__file, self.__defaultFile, self.__lookup_wrapper.killThreads)
                    
            futures = self.__lookup_wrapper.lookupSubdomains(subdomains)

            try:

                self.__output_wrapper.outputFutures(futures)

            except SomeError:
                self.__lookup_wrapper.killThreads()
        
        else:
            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__verbose, self.__file, self.__defaultFile)
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

        with Progress() as progress:

            task = None
            if(self.__colorize):
                task = progress.add_task("[red]Working...", total=600)
            
            else:
                task = progress.add_task("Working...", total=600)
            
            progress.update(task, advance=20)
            crtsh_subdomains = self.__crtsh_api_requester.join()
            progress.update(task, advance=80)

            urlscan_subdomains = self.__urlscan_api_requester.join()
            progress.update(task, advance=100)

            alienvault_subdomains = self.__alienvault_api_requester.join()
            progress.update(task, advance=100)

            anubis_subdomains = self.__anubis_api_requester.join()
            progress.update(task, advance=100)

            hackertarget_subdomains = self.__hackertarget_api_requester.join()
            progress.update(task, advance=100)

            dnsrepo_subdomains = self.__dnsrepo_api_requester.join()
            progress.update(task, advance=100)

        subdomains = []

        if(self.__verbose):
            if(self.__colorize):
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(whoisxmlapi_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [red]whoisxmlapi.com[/red]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(crtsh_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [green]crt.sh[/green]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(urlscan_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [yellow]urlscan.io[/yellow]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(alienvault_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [blue]otx.alienvault.com[/blue]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(anubis_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [magenta]jonlu.ca[/magenta]")
                rprint(f"\t[deep_sky_blue1]Got[/deep_sky_blue1] [dark_red underline]{len(dnsrepo_subdomains)}[/dark_red underline] [deep_sky_blue1]subdomains from[/deep_sky_blue1] [cyan]dnsrepo.noc.org[/cyan]")

            else:
                rprint(f"{len(whoisxmlapi_subdomains)} subdomains from whoisxmlapi.com")
                rprint(f"{len(crtsh_subdomains)} subdomains from crt.sh")
                rprint(f"{len(urlscan_subdomains)} subdomains from] urlscan.io")
                rprint(f"{len(alienvault_subdomains)} subdomains from otx.alienvault.com")
                rprint(f"{len(anubis_subdomains)} subdomains from jonlu.ca")
                rprint(f"{len(dnsrepo_subdomains)} subdomains from dnsrepo.noc.org")


        subdomains.extend(whoisxmlapi_subdomains)
        subdomains.extend(crtsh_subdomains)
        subdomains.extend(urlscan_subdomains)
        subdomains.extend(alienvault_subdomains)
        subdomains.extend(anubis_subdomains)
        subdomains.extend(hackertarget_subdomains)
        subdomains.extend(dnsrepo_subdomains)

        subdomains = list(set(subdomains))

        if(self.__alive):
            self.__lookup_wrapper = LookupWrapper()
            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__verbose, self.__file, self.__defaultFile, self.__lookup_wrapper.killThreads)

            futures = self.__lookup_wrapper.lookupSubdomains(subdomains)

            try:

                self.__output_wrapper.outputFutures(futures)

            except SomeError:
                self.__lookup_wrapper.killThreads()

        else:
            self.__output_wrapper = OutputWrapper(self.__target, self.__outputFormat, self.__colorize, self.__verbose, self.__file, self.__defaultFile)
            self.__output_wrapper.outputSubdomains(subdomains)
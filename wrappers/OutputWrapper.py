from rich.console import Console
from rich.table import Table
from rich.status import Status
from rich import print as rprint

import random

from concurrent.futures import as_completed
from json import dumps

from constants.outputformats import JSON_FORMAT, TXT_FORMAT
from constants.spinners import SPINNERS

from errors.SubdomainLookupError import SubdomainLookupError


class OutputWrapper(Console):

    __domain = None
    __matchCode = None
    __outputFormat = None
    __colorize = None
    __verbose = None
    __file = None
    __defaultFile = None
    __killLookupThreadsCallBack = None

    def __init__(self, domain: str, matchCode: list or None = None, outputFormat: str = TXT_FORMAT, colorize: bool = False, verbose: bool = False,  file = None, defaultFile: bool = False, killLookupThreadsCallBack = None):
        Console.__init__(self)

        self.__domain = domain
        
        if(matchCode is not None):
            self.__matchCode = [str(code) for code in matchCode]

        self.__outputFormat = outputFormat
        self.__colorize = colorize
        self.__verbose = verbose
        self.__file = file
        self.__defaultFile = defaultFile
        self.__killLookupThreadsCallBack = killLookupThreadsCallBack

    def __listToJsonString(self, someList: list) -> str:
        return dumps(someList, indent=2)

    def __saveOutputToFile(self, output: str or Table):

        if(type(output) is str):
            self.__file.write(output)

        elif(type(output) is Table):
            rprint(output, file=self.__file)

    def __saveOutputToDefaultFile(self, output: str or Table):

        if(type(output) is str):
            with open("subdomains." + self.__domain + "." + self.__outputFormat, "w") as file:
                    file.write(output)

        elif(type(output) is Table):
            with open("subdomains." + self.__domain + "." + self.__outputFormat, "w") as file:
                rprint(output, file=file)

    def __killLookupThreadsSignal(self):
        if(self.__verbose):
            if(self.__colorize):
                Console.print(self, "[dark_red]Killing unfinished lookup jobs...")

            else:
                Console.print(self, "Killing unfinished lookup jobs...")
        self.__killLookupThreadsCallBack()

    def outputSubdomains(self, subdomains):

        output = None
        
        if(self.__outputFormat == JSON_FORMAT):

            output = self.__listToJsonString(subdomains)

            if(self.__colorize):
                Console.print_json(self, output)

            else:
                Console.print_json(self, output, highlight=False)
        
        elif(self.__outputFormat == TXT_FORMAT):
            
            table = Table(title="Subdomains")

            if(self.__colorize):
                table.add_column("Subdomain", justify="left", style="cyan", no_wrap=True)

            else:
                table.add_column("Subdomain", justify="left", no_wrap=True)

            for subdomain in subdomains:
                table.add_row(subdomain)

            output = table
            Console.print(self, output)

        if(self.__file is not None):
            self.__saveOutputToFile(output)
        
        elif(self.__defaultFile):
            self.__saveOutputToDefaultFile(output)


    def outputFutures(self, futures):
        table = None
        if(self.__outputFormat == TXT_FORMAT):
            table = Table(title="Alive subdomains")

            if(self.__colorize):
                table.add_column("Subdomain", justify="left", style="cyan", no_wrap=True)
                table.add_column("Status code", justify="center", style="magenta")
                table.add_column("Title", justify="center", style="green")
                table.add_column("Backend", justify="right", style="red")

            else:
                table.add_column("Subdomain", justify="left", no_wrap=True)
                table.add_column("Status code", justify="center")
                table.add_column("Title", justify="center")
                table.add_column("Backend", justify="right")

        output = []
        subdomainLookupErrorCounter = 0

        if(futures):

            status = Console.status(self, "Preparing alive subdomains...", spinner=random.choice(SPINNERS))
                
            if(self.__colorize):
                status.update(status="[yellow]Preparing alive subdomains...")
                    
            status.start()
            for index, future in enumerate(as_completed(futures), start=1):
                
                if(subdomainLookupErrorCounter >= 10):
                    status.stop()

                    if(self.__colorize):

                        Console.print(self, "[bright_red]You might have been rate limited")
                        Console.print(self, "[deep_sky_blue3]Outputing probed subdomains")

                    else:

                        Console.print(self, "You might have been rate limited")
                        Console.print(self, "Outputing probed subdomains")
                
                result = None

                try:

                    result = future.result()
                        
                    subdomainLookupErrorCounter = 0

                except SubdomainLookupError:

                    subdomainLookupErrorCounter += 1
                    continue
                
                if(self.__outputFormat == JSON_FORMAT):
                    if(self.__matchCode is not None):
                        if(result["statusCode"] in self.__matchCode):
                            output.append(result)
                    else:
                        output.append(result)
                    
                elif(self.__outputFormat == TXT_FORMAT):
                    if(self.__matchCode is not None):
                        if(result["statusCode"] in self.__matchCode):
                            table.add_row(result["subdomain"], result["statusCode"], result["title"], result["backend"])
                    else:
                        table.add_row(result["subdomain"], result["statusCode"], result["title"], result["backend"])

            status.stop()
                    
        if(self.__outputFormat == JSON_FORMAT):
            output = self.__listToJsonString(output)
            
            if(self.__colorize):
                Console.print_json(self, output)
                
            else:
                Console.print_json(self, output, highlight=False)

        elif(self.__outputFormat == TXT_FORMAT):
            output = table
            Console.print(self, output)

        if(self.__file is not None):
            self.__saveOutputToFile(output)
        
        elif(self.__defaultFile):
            self.__saveOutputToDefaultFile(output)

    
from rich.console import Console
from rich.table import Table
from rich import print as rprint
from constants.outputformats import JSON_FORMAT, TXT_FORMAT
from concurrent.futures import as_completed
from json import dumps
from errors.BadError import BadError
from errors.SubdomainLookupError import SubdomainLookupError
from errors.RateLimitError import RateLimitError
from errors.SomeError import SomeError

class OutputWrapper(Console):

    __domain = None
    __outputFormat = None
    __colorize = None
    __file = None
    __defaultFile = None
    __alive_subdomains = None

    def __init__(self, domain: str, outputFormat: str = TXT_FORMAT, colorize: bool = False,  file = None, defaultFile: bool = False):
        Console.__init__(self)

        self.__domain = domain
        self.__outputFormat = outputFormat
        self.__colorize = colorize
        self.__file = file
        self.__defaultFile = defaultFile

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
                rprint(output, file)

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
        badErrorCounter = 0

        if(futures):

            for index, future in enumerate(as_completed(futures), start=1):
                
                if(subdomainLookupErrorCounter >= 10):
                    Console.print(self, "You might have been rate limited, try again later")
                    Console.print(self, "Shutting down...")
                    raise RateLimitError()

                if(badErrorCounter >= 10):
                    Console.print(self, "Something went wrong...")
                    Console.print(self, "Shutting down...")
                    raise SomeError()

                try:

                    result = future.result()
                        
                    subdomainLookupErrorCounter = 0
                    badErrorCounter = 0

                except SubdomainLookupError:

                    subdomainLookupErrorCounter += 1
                    continue

                except BadError:

                    badErrorCounter += 1
                    continue

                if(self.__outputFormat == JSON_FORMAT):
                    output.append(result)
                
                elif(self.__outputFormat == TXT_FORMAT):
                    table.add_row(result["subdomain"], result["statusCode"], result["title"], result["backend"])
                    
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

    
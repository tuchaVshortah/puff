from rich.console import Console
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

    def __subdomainsToPrettyJson(self, subdomains: list) -> str:
        return dumps(subdomains, indent=2)

    def __subdomainsToPrettyTxt(self, subdomains: list) -> str:
        return "\n".join(subdomains)

    def __futureResultToPrettyJson(self, result) -> str:
        return dumps(result, indent=2)

    def __futureResultToPrettyTxt(self, result) -> str:

        string = f'\\[{result["subdomain"]}]\t[{result["statusCode"]}]\t[{result["title"]}]\t[{result["backend"]}]'
        
        return string

    def __saveOutputToFile(self, output: str):
        self.__file.write(output)

    def __saveOutputToDefaultFile(self, output: str):
        with open("subdomains." + self.__domain + "." + self.__outputFormat, "w") as file:
                file.write(output)

    def outputSubdomains(self, subdomains):
        output = None
        
        if(self.__outputFormat == JSON_FORMAT):
            output = self.__subdomainsToPrettyJson(subdomains)
            Console.print_json(self, output)
        
        elif(self.__outputFormat == TXT_FORMAT):
            output = self.__subdomainsToPrettyTxt(subdomains)
            Console.print(self, output)

        if(self.__file is not None):
            self.__saveOutputToFile(output)
        
        elif(self.__defaultFile):
            self.__saveOutputToDefaultFile(output)


    def outputFutures(self, futures):
        output = None
        subdomainLookupErrorCounter = 0
        badErrorCounter = 0

        if(futures):

            for index, future in enumerate(as_completed(futures), start=1):
                
                if(subdomainLookupErrorCounter >= 10):
                    Console.print(self, "You might have been rate limited, try again later")
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
                    output = self.__futureResultToPrettyJson(result)
                    Console.print_json(self, output)
                
                elif(self.__outputFormat == TXT_FORMAT):
                    output = self.__futureResultToPrettyTxt(result)
                    Console.print(self, output)
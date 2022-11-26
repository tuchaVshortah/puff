from constants.outputformats import JSON_FORMAT, TXT_FORMAT
from concurrent.futures import as_completed
from json import dumps
from errors.BadError import BadError
from errors.SubdomainLookupError import SubdomainLookupError

class OutputWrapper():

    __domain = None
    __outputFormat = None
    __file = None
    __defaultFile = None
    __alive_subdomains = None

    def __init__(self, domain: str, outputFormat: str = TXT_FORMAT, file = None, defaultFile: bool = False):
        self.__domain = domain
        self.__outputFormat = outputFormat
        self.__file = file
        self.__defaultFile = defaultFile

    def __subdomainsToPrettyJson(self, subdomains: list) -> str:
        return dumps(subdomains, indent=2)

    def __subdomainsToPrettyTxt(self, subdomains: list) -> str:
        return "\n".join(subdomains)

    def __futureToPrettyJson(self, future):
        pass

    def __futureToPrettyTxt(self, future):
        pass

    def __saveOutputToFile(self, output: str):
        self.__file.write(output)

    def __saveOutputToDefaultFile(self, output: str):
        with open("subdomains." + self.__domain + "." + self.__outputFormat, "w") as file:
                file.write(output)

    def outputSubdomains(self, subdomains):
        output = None
        
        print(self.__outputFormat)
        if(self.__outputFormat == JSON_FORMAT):
            output = self.__subdomainsToPrettyJson(subdomains)
        
        elif(self.__outputFormat == TXT_FORMAT):
            output = self.__subdomainsToPrettyTxt(subdomains)

        print(output)

        if(self.__file is not None):
            self.__saveOutputToFile(output)
        
        elif(self.__defaultFile):
            self.__saveOutputToDefaultFile(output)


    def outputFutures(self, futures):
        subdomainLookupErrorCounter = 0
        badErrorCounter = 0

        if(futures):

            for index, future in enumerate(as_completed(futures), start=1):
                
                if(subdomainLookupErrorCounter >= 10):
                    print("You might have been rate limited, try again later")
                    break

                if(badErrorCounter >= 10):
                    print("Something went wrong...")
                    break

                try:

                    print(future.result())
                    subdomainLookupErrorCounter = 0
                    badErrorCounter = 0

                except SubdomainLookupError:

                    subdomainLookupErrorCounter += 1

                except BadError:

                    badErrorCounter += 1
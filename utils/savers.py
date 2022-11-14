from constants.outputformats import *

def saveResponseToFile(file, domain: str, reponse: str):
    if(file is not None):
        file.write(response)

def saveResponseToDefaultFile(domain: str, response: str, outputFormat: str):
    with open("subdomains." + domain + "." + outputFormat, "w") as file:
            file.write(response)
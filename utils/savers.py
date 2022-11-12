from constants.outputformats import *

def saveResponseToFile(file, domain: str, reponse: str):
    if(file is not None):
        file.write(response)

def saveResponseToDefaultFile(domain: str, response: str, outputFormat: str):
    with open("subdomains." + domain + "." + outputFormat, "w") as file:
            file.write(response)

def saveJsonResponse(file, domain, response: str):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".json", "w") as file:
            file.write(response)

def saveXmlResponse(file, domain, response: str):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".xml", "w") as file:
            file.write(response)

def saveTxtResponse(file, domain, response: ApiResponse or str):
    
    if(file is not None):
        if(type(response) is ApiResponse):
            for record in response.result.records:
                file.write(record.domain + "\n")
        
        elif(type(response) is str):
            file.write(response)
        
    elif(file is None):
        with open("subdomains." + domain + ".txt", "w") as file:
            if(type(response) is ApiResponse):
                for record in response.result.records:
                    file.write(record.domain + "\n")
            
            elif(type(response) is str):
                file.write(response)
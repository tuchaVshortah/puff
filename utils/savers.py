from subdomainslookup.models.response import Response as ApiResponse

def saveJsonResponse(file, domain, response: str):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".json", "a+") as file:
            file.write(response)

def saveXmlResponse(file, domain, response: str):
    if(file is not None):
        file.write(response)

    elif(file is None):
        with open("subdomains." + domain + ".xml", "a+") as file:
            file.write(response)

def saveTxtResponse(file, domain, response: ApiResponse or str):
    
    if(file is not None):
        if(type(response) is ApiResponse):
            for record in response.result.records:
                file.write(record.domain + "\n")
        
        elif(type(response) is str):
            file.write(response)
        
    elif(file is None):
        with open("subdomains." + domain + ".txt", "a+") as file:
            if(type(response) is ApiResponse):
                for record in response.result.records:
                    file.write(record.domain + "\n")
            
            elif(type(response) is str):
                file.write(response)
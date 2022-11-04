import requests
from json import loads

def getSubdomains(domain):

    url = "https://crt.sh/?q={}&output=json".format(domain)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.5195.102 Safari/537.36"
    }

    response = requests.get(url, headers)


    subdomains = []
    if(response.ok):
        try:
            
            response = response.content.decode("utf-8")

            response_data = loads(response)

            for data in response_data:
                parsed = data["name_value"].split("\n")
                for subdomain in parsed:
                    subdomains.append(subdomain.replace("*.", "", 1))

        except Exception as e:
            print(e)

    return list(set(subdomains))

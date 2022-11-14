import argparse
from wrappers.apiwrapper import ApiWrapper
from utils.savers import *
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT


def puff():
    parser = argparse.ArgumentParser(prog="Puff", description="Yet another subdomain enumeration tool")

    parser.add_argument(
        "-d", "--domain",
        help="Specify the domain to enumerate",
        default=None,
        required=True,
        type=str,
        nargs=1
    )

    parser.add_argument(
        "-q","--quiet",
        help="Do not show any output in the terminal",
        default=False,
        action="store_true"
    )

    parser.add_argument(
        "-b", "--boost",
        help="Allow Puff to optimize workload by dividing it into several threads",
        default=False,
        action="store_true"
    )

    api_group = parser.add_mutually_exclusive_group()

    api_group.add_argument(
        "-wak", "--whoisxmlapi-key",
        help="Specify your API key for whoisxmlapi.com",
        default=None,
        type=str,
        nargs=1
    )

    api_group.add_argument(
        "-X", "--no-api-keys",
        help="Pass this argument if you don't have API keys",
        default=True,
        action="store_true",
    )

    format_group = parser.add_mutually_exclusive_group()

    format_group.add_argument(
        "-r", "--raw",
        help="Output raw data to the terminal",
        default=True,
        action="store_true"
    )

    format_group.add_argument(
        "-j","--json",
        help="Output in the JSON format",
        default=False,
        action="store_true"
    )

    format_group.add_argument(
        "-x","--xml",
        help="Output in the XML format",
        default=False,
        action="store_true"
    )

    output_file_group = parser.add_mutually_exclusive_group()
    output_file_group.add_argument(
        "-f", "--file",
        help="Save results to the specified file",
        default=None,
        nargs="?",
        type=argparse.FileType(mode="a+",encoding="utf-8")
    )

    output_file_group.add_argument(
        "-df", "--default-file",
        help="Save results in the subdomains.<domain>.txt files",
        default=False,
        action="store_true"
    )

    args = parser.parse_args()
    
    client = None
    domain = args.domain[0]

    if(args.whoisxmlapi_api_key is not None):

        client = Client(args.whoisxmlapi_api_key[0])

        if(args.json == True):

            response = client.get_raw(domain, output_format=Client.JSON_FORMAT)

            try:

                response_data = loads(response)
                pretty_response = dumps(response_data, indent=2)

                response = pretty_response

            except Exception as error:

                print("Could not parse API response\n", error)
                exit()

            if(not args.quiet):
                print(response)

            if(args.file is not None):
                saveJsonResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveJsonResponse(None, domain, response)


        elif(args.xml == True):

            response = client.get_raw(domain, output_format=Client.XML_FORMAT)

            try:

                response_data = xml.dom.minidom.parseString(response)
                pretty_response = response_data.toprettyxml()

                response = pretty_response

            except Exception as error:

                print("Could not parse API response\n", error)
                exit()
            
            if(not args.quiet):
                print(response)

            if(args.file is not None):
                saveXmlResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveXmlResponse(None, domain, response)

        elif(args.raw == True):

            response = client.get(domain)

            if(not args.quiet):
                
                for record in response.result.records:
                    print(record.domain)
            
            if(args.file is not None):
                saveTxtResponse(args.file, domain, response)
            elif(args.default_file == True):
                saveTxtResponse(None, domain, response)


    
    elif(args.no_api_keys == True):

        if(args.json == True):

            api_wrapper = ApiWrapper(domain, JSON_FORMAT, args.boost)
            response = api_wrapper.run()

            if(not args.quiet):

                print(response)

            if(args.file is not None):

                saveResponseToFile(args.file, domain, response)

            elif(args.default_file == True):

                saveResponseToDefaultFile(domain, response, JSON_FORMAT)

            
        elif(args.xml == True):

            api_wrapper = ApiWrapper(domain, XML_FORMAT, args.boost)
            response = api_wrapper.run()

            if(not args.quiet):

                print(response)

            if(args.file is not None):

                saveResponseToFile(args.file, domain, response)

            elif(args.default_file == True):
                
                saveResponseToDefaultFile(domain, response, XML_FORMAT)


        elif(args.raw == True):

            api_wrapper = ApiWrapper(domain, RAW_FORMAT, args.boost)
            response = api_wrapper.run()

            if(not args.quiet):

                print(response)

            if(args.file is not None):

                saveResponseToFile(args.file, domain, response)

            elif(args.default_file == True):
                
                saveResponseToDefaultFile(domain, response, RAW_FORMAT)


puff()
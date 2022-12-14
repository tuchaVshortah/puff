import argparse
from wrappers.apiwrapper import ApiWrapper
from utils.savers import *
from constants.outputformats import XML_FORMAT, JSON_FORMAT, RAW_FORMAT


def puff():
    parser = argparse.ArgumentParser(prog="puff", description="Yet another passive subdomain enumeration tool")

    parser.add_argument(
        "-d", "--domain",
        help="Specify the domain to enumerate",
        default=None,
        required=True,
        type=str,
        nargs=1
    )

    
    parser.add_argument(
        "-b", "--boost",
        help="Allow puff to optimize workload by dividing it into several threads",
        default=False,
        action="store_true"
    )

    verbosity_group = parser.add_mutually_exclusive_group()

    verbosity_group.add_argument(
        "-q","--quiet",
        help="Do not show any output in the terminal",
        default=False,
        action="store_true"
    )

    verbosity_group.add_argument(
        "-v", "--verbose",
        help="Allow puff to output status messages to the terminal",
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
        help="Save results in the subdomains.<domain>.<format> files",
        default=False,
        action="store_true"
    )

    args = parser.parse_args()
    
    domain = None
    if(args.domain is not None):
        domain = args.domain[0]
    
    whoisxmlapi_key = None
    if(args.whoisxmlapi_key is not None):
        whoisxmlapi_key = args.whoisxmlapi_key[0]

    api_wrapper = None
    outputFormat = None

    if(whoisxmlapi_key is not None):

        if(args.json == True):
            outputFormat = JSON_FORMAT

            api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.verbose, whoisxmlapi_key)

            
        elif(args.xml == True):
            outputFormat = XML_FORMAT

            api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.verbose, whoisxmlapi_key)
            

        elif(args.raw == True):
            outputFormat = RAW_FORMAT

            api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.verbose, whoisxmlapi_key)

    
    elif(args.no_api_keys == True):

        if(args.json == True):
            outputFormat = JSON_FORMAT

            api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.verbose)

            
        elif(args.xml == True):
            outputFormat = XML_FORMAT

            api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.verbose)


        elif(args.raw == True):
            outputFormat = RAW_FORMAT

            api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.verbose)
            

    response = api_wrapper.run()

    if(not args.quiet):
        print(response)

    if(args.file is not None):

        saveResponseToFile(args.file, domain, response)

    elif(args.default_file == True):

        saveResponseToDefaultFile(domain, response, outputFormat)

puff()
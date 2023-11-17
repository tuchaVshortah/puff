import argparse
from wrappers.ApiWrapper import ApiWrapper
from constants.outputformats import JSON_FORMAT, TXT_FORMAT


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
        "-a", "--alive",
        help="Check if subdomains are alive and get meta information about each one of them -> [statusCode, title, backend]",
        default=False,
        action="store_true"
    )

    parser.add_argument(
        "-mc", "--match-code",
        help="Match the specified status code/codes when testing for alive subdomains",
        default=None,
        type=int,
        nargs="+"
    )


    parser.add_argument(
        "-pst", "--probing-sleep-time",
        help="Pass the time in seconds to stay in the sleep mode. May help in avoiding rate limiting",
        default=None,
        type=int,
        nargs="?"
    )


    parser.add_argument(
        "-rsp", "--randomized-subdomain-probing",
        help="Randomize the order of subdomains to probe",
        default=False,
        action="store_true"
    )

    
    parser.add_argument(
        "-b", "--boost",
        help="Allow puff to optimize workload by dividing it into several threads",
        default=False,
        action="store_true"
    )


    parser.add_argument(
        "-v", "--verbose",
        help="Allow puff to output status messages to the terminal",
        default=False,
        action="store_true"
    )


    parser.add_argument(
        "-n", "--number",
        help="Specify the max number of subdomains to probe. Due to the fact that not all of the subdomains may be alive,\
            you have to expect that the number of probed subdomains may be less than the specified number",
        default=None,
        type=int,
        nargs="?"
    )


    parser.add_argument(
        "-c", "--colorize",
        help="Colorize output",
        default=False,
        action="store_true"
    )


    parser.add_argument(
        "-wak", "--whoisxmlapi-key",
        help="Specify your API key for whoisxmlapi.com",
        default=None,
        type=str,
        nargs=1
    )


    format_group = parser.add_mutually_exclusive_group()

    format_group.add_argument(
        "-t", "--txt",
        help="Output data as text to the terminal",
        default=True,
        action="store_true"
    )
    

    format_group.add_argument(
        "-j","--json",
        help="Output in the JSON format",
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

    if(not args.alive):
        if(args.match_code is not None or args.probing_sleep_time is not None\
            or args.randomized_subdomain_probing or args.number is not None):
            parser.error("the -a/--alive flag has to be set")
    
    domain = None
    if(args.domain is not None):
        domain = args.domain[0]
    
    whoisxmlapi_key = None
    if(args.whoisxmlapi_key is not None):
        whoisxmlapi_key = args.whoisxmlapi_key[0]

    api_wrapper = None
    outputFormat = None

    if(args.json == True):
        outputFormat = JSON_FORMAT     


    elif(args.txt == True):
        outputFormat = TXT_FORMAT

    api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.colorize,
                            args.verbose, args.alive, args.probing_sleep_time, 
                            args.match_code, args.randomized_subdomain_probing, 
                            args.file, args.default_file, args.number, whoisxmlapi_key)

    api_wrapper.run()

puff()
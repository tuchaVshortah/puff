import argparse
from wrappers.ApiWrapper import ApiWrapper
from wrappers.ProbingWrapper import ProbingWrapper
from constants.outputformats import JSON_FORMAT, TXT_FORMAT
from rich import print as rprint

def puff():
    parser = argparse.ArgumentParser(prog="puff", description="Yet another passive subdomain enumeration tool")

    scan_group = parser.add_mutually_exclusive_group()

    scan_group.add_argument(
        "-d", "--domain",
        help="Specify the domain to enumerate",
        default=None,
        type=str,
        nargs=1
    )

    scan_group.add_argument(
        "-pt", "--probing-targets",
        help="Specify custom targets to probe. Use this if you want to probe a list of subdomains",
        default=None,
        type=str,
        nargs="+"
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
        help="Specify the max number of subdomains to probe or the exact number of subdomains to output in passive mode. Due to the fact that not all of the subdomains may be alive,\
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
        type=str,
        nargs=1
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
            or args.randomized_subdomain_probing):
            if(args.colorize):
                rprint("[red]the -a/--alive flag has to be set")
            else:
                print("the -a/--alive flag has to be set")
            exit(0)

    if (args.alive):
        if(args.number == 0):
            if(args.colorize):
                rprint("[red]the -n/--number flag has to be greater than 0")
            else:
                print("the -n/--number flag has to be greater than 0")
            exit(0)
    
    whoisxmlapi_key = None
    if(args.whoisxmlapi_key is not None):
        whoisxmlapi_key = args.whoisxmlapi_key[0]

    outputFormat = None
    if(args.json == True):
        outputFormat = JSON_FORMAT     
    elif(args.txt == True):
        outputFormat = TXT_FORMAT

    file = None
    if(args.file is not None):
        file = args.file[0]

    domain = None
    if(args.domain is not None):
        domain = args.domain[0]

        api_wrapper = ApiWrapper(domain, outputFormat, args.boost, args.colorize,
                                args.verbose, args.alive, args.probing_sleep_time, 
                                args.match_code, args.randomized_subdomain_probing, 
                                file, args.default_file, args.number, whoisxmlapi_key)

        api_wrapper.run()

    elif(args.probing_targets is not None):
        probing_targets = args.probing_targets
        print(probing_targets)

        probing_wrapper = ProbingWrapper(probing_targets, outputFormat, args.boost, args.colorize, 
                                        args.verbose, args.probing_sleep_time, args.match_code, 
                                        args.randomized_subdomain_probing, file, args.default_file, args.number)

        probing_wrapper.run()

if __name__ == "__main__":
    puff()
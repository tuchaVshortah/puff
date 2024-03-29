
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich import print as rprint

from concurrent.futures import as_completed
from json import dumps, loads

from constants.outputformats import JSON_FORMAT, TXT_FORMAT
from constants.spinners import SPINNERS

from errors.SubdomainLookupError import SubdomainLookupError
import copy

import os

class OutputWrapper(Console):

    __domain = None
    __matchCode = None
    __outputFormat = None
    __colorize = None
    __verbose = None
    __file = None
    __defaultFile = None
    __killLookupThreadsCallBack = None

    def __init__(self, domain: str, matchCode: list or None = None, outputFormat: str = TXT_FORMAT, colorize: bool = False, verbose: bool = False,  file = None, defaultFile: bool = False, killLookupThreadsCallBack = None):
        Console.__init__(self)

        self.__domain = domain
        
        if(matchCode is not None):
            self.__matchCode = [str(code) for code in matchCode]

        self.__outputFormat = outputFormat
        self.__colorize = colorize
        self.__verbose = verbose
        self.__file = file
        self.__defaultFile = defaultFile
        self.__killLookupThreadsCallBack = killLookupThreadsCallBack

    def __listToJsonString(self, someList: list) -> str:
        return dumps(someList, indent=2)

    def __saveOutputToFile(self, file_name: str or None, output: str or Table):

        OUTPUT_DIR = "./scan/"

        if(not os.path.exists(OUTPUT_DIR)):
            os.makedirs(OUTPUT_DIR)

        if(file_name is not None):
            if(type(output) is str):
                with open(OUTPUT_DIR + file_name, "w") as file:
                    file.write(output)

            elif(type(output) is Table):
                with open(OUTPUT_DIR + file_name, "w") as file:
                    rprint(output, file=file)
        
        else:
            #handle json output for probing wrapper
            json_output = loads(output)

            for j in json_output:
                subdomain = j["subdomain"]
                with open(f"{OUTPUT_DIR}backend.{subdomain}.json", "w") as file:
                    file.write(dumps(j, indent=2))

    def __killLookupThreadsSignal(self):
        if(self.__verbose):
            if(self.__colorize):
                Console.print(self, "[dark_red]Killing unfinished lookup jobs...")

            else:
                Console.print(self, "Killing unfinished lookup jobs...")
        self.__killLookupThreadsCallBack()

    def outputSubdomains(self, subdomains, number: int or None = None):

        output = None
        cli_output = None

        if(self.__outputFormat == JSON_FORMAT):

            if(number is None or (number is not None and number > len(subdomains))):
                output = self.__listToJsonString(subdomains)
                cli_output = output
            elif(number is not None and number <= len(subdomains)):
                output = self.__listToJsonString(subdomains)
                cli_output = self.__listToJsonString(subdomains[:number])

            if(number is None or (number is not None and number > 0)):
                if(self.__colorize):
                    Console.print_json(self, cli_output)
                else:
                    Console.print_json(self, cli_output, highlight=False)
        
        elif(self.__outputFormat == TXT_FORMAT):
            
            table = Table(title="Subdomains")
            cli_table = None

            if(self.__colorize):
                table.add_column("Number", justify="left", style="light_sea_green")
                table.add_column("Subdomain", justify="left", style="cyan", no_wrap=True)

            else:
                table.add_column("Number", justify="left")
                table.add_column("Subdomain", justify="left", no_wrap=True)

            with Progress() as progress:

                if(self.__colorize):
                    task = progress.add_task("[red]Preparing subdomains...        ", total=len(subdomains))
                else:
                    task = progress.add_task("Preparing subdomains...         ", total=len(subdomains))

                for index, subdomain in enumerate(subdomains):
                    table.add_row(str(index + 1), subdomain)
                    if(number is not None and index + 1 == number):
                        cli_table = copy.deepcopy(table)
                    progress.update(task, advance=1)

            if(number is None or (number is not None and number > len(subdomains))):
                cli_table = table

            if table.row_count > 0:
                output = table
                if(number is None or (number is not None and number > 0)):
                    Console.print(self, cli_table)
            else:
                Console.print(self, "[i]No data...[/i]")

        if(self.__file is not None):
            self.__saveOutputToFile(output)
        
        elif(self.__defaultFile):
            self.__saveOutputToDefaultFile(output)


    def outputFutures(self, futures):
        table = None
        if(self.__outputFormat == TXT_FORMAT):
            table = Table(title="Alive subdomains")

            if(self.__colorize):
                table.add_column("Number", justify="left", style="light_sea_green")
                table.add_column("Subdomain", justify="left", style="cyan", no_wrap=True)
                table.add_column("Status code", justify="center", style="magenta")
                table.add_column("Title", justify="center", style="green")
                table.add_column("Backend", justify="right", style="red")

            else:
                table.add_column("Number", justify="left", style="light_sea_green")
                table.add_column("Subdomain", justify="left", no_wrap=True)
                table.add_column("Status code", justify="center")
                table.add_column("Title", justify="center")
                table.add_column("Backend", justify="right")

        output = []
        subdomainLookupErrorCounter = 0

        if(futures):
            completed_futures = []
            with Progress() as progress: 

                if(self.__colorize):
                    task = progress.add_task("[red]Completing concurrent.futures...", total=len(futures))
                else:
                    task = progress.add_task("Completing concurrent.futures...", total=len(futures))

                for index, future in enumerate(as_completed(futures), start=1):
                    progress.update(task, advance=1)
                    completed_futures.append(future)

            index = 0
            with Progress() as progress:    

                if(self.__colorize):
                    task = progress.add_task("[red]Preparing alive subdomains...   ", total=len(completed_futures))
                else:
                    task = progress.add_task("Preparing alive subdomains...   ", total=len(completed_futures))

                for future in completed_futures:
                    if(subdomainLookupErrorCounter >= 10):

                        if(self.__colorize):

                            Console.print(self, "[bright_red]You might have been rate limited")
                            Console.print(self, "[deep_sky_blue3]Outputing probed subdomains")

                        else:

                            Console.print(self, "You might have been rate limited")
                            Console.print(self, "Outputing probed subdomains")
                    
                    result = None

                    progress.update(task, advance=1)
                    try:

                        result = future.result()
                        index += 1

                        subdomainLookupErrorCounter = 0

                    except SubdomainLookupError:

                        subdomainLookupErrorCounter += 1
                        continue
                    
                    if(self.__outputFormat == JSON_FORMAT):
                        if(self.__matchCode is not None):
                            if(result["statusCode"] in self.__matchCode):
                                output.append(result)
                        else:
                            output.append(result)
                        
                    elif(self.__outputFormat == TXT_FORMAT):
                        if(self.__matchCode is not None):
                            if(result["statusCode"] in self.__matchCode):
                                table.add_row(str(index), result["subdomain"], result["statusCode"], result["title"], result["backend"])
                        else:
                            table.add_row(str(index), result["subdomain"], result["statusCode"], result["title"], result["backend"])

                    
        if(self.__outputFormat == JSON_FORMAT):
            if len(output) > 0:
                output = self.__listToJsonString(output)

                if(self.__colorize):
                    Console.print_json(self, output)             
                else:
                    Console.print_json(self, output, highlight=False)
            else:
                Console.print(self, "[i]All probed subdomains were dead...[/i]")
                
                if(self.__colorize):
                    Console.print(self, "[bright_red]Try again...")
                else:
                    Console.print(self, "Try again...")

        elif(self.__outputFormat == TXT_FORMAT):
            if table.row_count > 0:
                output = table
                Console.print(self, output)
            else:
                Console.print(self, "[i]All probed subdomains were dead...[/i]")
                if(self.__colorize):
                    Console.print(self, "[bright_red]Try again...")
                else:
                    Console.print(self, "Try again...")
        
        if(self.__file is not None):
            self.__saveOutputToFile(self.__file, output)
        
        elif(self.__defaultFile):
            if(type(self.__domain) is not list):
                file_name = f"subdomains.{self.__domain}.{self.__outputFormat}"
                self.__saveOutputToFile(file_name, output)
            elif(type(self.__domain) is list):
                self.__saveOutputToFile(None, output)

    
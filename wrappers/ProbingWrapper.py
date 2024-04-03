from wrappers.LookupWrapper import LookupWrapper
from wrappers.OutputWrapper import OutputWrapper

from constants.outputformats import JSON_FORMAT, TXT_FORMAT


class ProbingWrapper():

    __probingTargets = None
    __outputFormat = None
    __boost = None
    __colorize = None
    __verbose = None
    __alive = None
    __probingSleepTime = None
    __matchCode = None
    __randomizedSubdomainProbing = None
    __file = None
    __defaultFile = None
    __number = None

    __lookup_wrapper = None
    __output_wrapper = None


    def __init__(self, probingTargets: list or None = None, outputFormat: str = JSON_FORMAT,
        boost: bool = False, colorize: bool = False, verbose: bool = False,
        probingSleepTime: float or None = None, matchCode: list or None = None, 
        randomizedSubdomainProbing: bool = False, file: str or None = None, defaultFile: bool = False, 
        number: int or None = None):

        self.__probingTargets = probingTargets
        self.__outputFormat = outputFormat
        self.__boost = boost
        self.__colorize = colorize
        self.__verbose = verbose
        self.__probingSleepTime = probingSleepTime
        self.__matchCode = matchCode
        self.__randomizedSubdomainProbing = randomizedSubdomainProbing
        self.__file = file
        self.__defaultFile = defaultFile
        self.__number = number

    
    def run(self):

        if(self.__boost):
            self.__fastTasks()

        else:
            self.__slowTasks()
            
            
    def __slowTasks(self):

        
        self.__lookup_wrapper = LookupWrapper(1, self.__probingSleepTime)
        self.__output_wrapper = OutputWrapper(self.__probingTargets, self.__matchCode, self.__outputFormat,
                                                self.__colorize, self.__verbose, self.__file, self.__defaultFile,
                                                self.__lookup_wrapper.killThreads)
                
        futures = self.__lookup_wrapper.lookupDomains(self.__probingTargets, self.__number, self.__randomizedSubdomainProbing)
        self.__output_wrapper.outputFutures(futures)

        
    def __fastTasks(self):

        self.__lookup_wrapper = LookupWrapper(probingSleepTime=self.__probingSleepTime)
        self.__output_wrapper = OutputWrapper(self.__probingTargets, self.__matchCode, self.__outputFormat,
                                            self.__colorize, self.__verbose, self.__file, self.__defaultFile,
                                            self.__lookup_wrapper.killThreads)

        futures = self.__lookup_wrapper.lookupDomains(self.__probingTargets, self.__number, self.__randomizedSubdomainProbing)
        self.__output_wrapper.outputFutures(futures)

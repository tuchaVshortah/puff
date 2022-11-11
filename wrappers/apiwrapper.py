from puff.apis.whoisxmlapi import PuffApiRequester
from puff.apis.crtsh import CrtshApiRequester
from puff.constants.outputformats import XML_FORMAT, JSON_FORMAT
from threading import Thread

class ApiWrapper():

    self.__target = None
    self.__outputFormat = None
    self.__boost = None

    def __init__(self, target:str = None, outputFormat:str = JSON_FORMAT, boost:bool = False):
        self.__target = target
        self.__outputFormat = outputFormat
        self.__boost = boost
    
    def run(self):
        if(self.__boost):
            pass
            
    def __slowTasks(self):
        pass

    def __fastTasks(self):
        pass
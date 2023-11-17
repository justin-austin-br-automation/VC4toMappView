# C:\VC4toMappView\VC4toMappView\Logical\VisuVC4\Pages\PageEmpty.page
from functions import *


class VC4Page:

    def __init__(self, path):
        
        self.path = path
        self.pageData, self.controlElements = getInfoFromVC4Page(self.path)
        
        

    def createMVLayout(self):
        pass

    def createMVPage(self):
        pass

    def createMVContent(self):
        pass
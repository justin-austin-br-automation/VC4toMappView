# C:\VC4toMappView\VC4toMappView\Logical\VisuVC4\Pages\PageEmpty.page
from functions import *


class VC4Page:

    def __init__(self, path):
        
        self.path = path
        self.pageData, self.controlElements = getInfoFromVC4Page(self.path)
        self.mVLayoutID = self.pageData['PageName'] + "Layout"
        self.mVContentID = self.pageData['PageName'] + "Content"
        self.mVPageID = self.pageData['PageName'] + "Page"
        

    def createMVLayout(self):
        ET.register_namespace('ldef', "http://www.br-automation.com/iat2015/layoutDefinition/v2")
        
        # grab the tree from the xml doc
        tree = ET.parse('TemplateLayout.layout')

        # get the root of the tree
        root = tree.getroot()

        # set layout resolution and name
        root.set('height', self.pageData['Height'])
        root.set('width', self.pageData['Width'])
        root.set('id', self.mVLayoutID)

        # Set area sizes
        root[0][0].set('height', self.pageData['Height'])
        root[0][0].set('width', self.pageData['Width'])

        tree.write(self.mVLayoutID + '.layout', xml_declaration=True, encoding='utf-8')

    def createMVContent(self):
        ET.register_namespace('', "http://www.br-automation.com/iat2015/contentDefinition/v2")
        ET.register_namespace('pdef', "http://www.br-automation.com/iat2015/pageDefinition/v2")
        
        # grab the tree from the xml doc
        tree = ET.parse('TemplateContent.content')

        # get the root of the tree
        root = tree.getroot()

        # set content ratio and name
        root.set('height', self.pageData['Height'])
        root.set('width', self.pageData['Width'])
        root.set('id', self.mVContentID)

        # add in any widgets
        for widget in self.controlElements:
            pass

        # widget = ET.SubElement(root[0], 'Widget')
        # widget.set('xsi:type', "widgets.brease.Label")
        # widget.set('id', "Label")
        # widget.set('top', "20")
        # widget.set('left', "140")
        # widget.set('zIndex', "0")
        # widget.set('text', "Label")

        # widget = ET.SubElement(root[0], 'Widget')
        # widget.set('xsi:type', "widgets.brease.MomentaryPushButton")
        # widget.set('id', "MomentaryPushButton")
        # widget.set('top', "20")
        # widget.set('left', "20")
        # widget.set('zIndex', "1")
        # widget.set('text', "Button")

        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        tree.write(self.mVContentID + '.content', xml_declaration=True, encoding='utf-8')

        # editing output file to be usable by AS
        textToFind = "/><"
        textToReplaceWith = "/>\n<"

        with open(self.mVContentID + '.content', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace(textToFind, textToReplaceWith)

        with open(self.mVContentID + '.content', 'w') as file:
            file.write(filedata)

    def createMVPage(self):
        # grab the tree from the xml doc
        tree = ET.parse('TemplatePage.page')

        # get the root of the tree
        root = tree.getroot()

        # set page name and layout
        root.set('id', self.mVPageID)
        root.set('layoutRefId', self.mVLayoutID)

        # set all Assignment values
        root[0][0].set('baseContentRefId', self.mVContentID)

        tree.write(self.mVPageID + '.page', xml_declaration=True, encoding='utf-8')
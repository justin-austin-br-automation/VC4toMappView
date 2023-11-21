# C:\VC4toMappView\VC4toMappView\Logical\VisuVC4\Pages\PageEmpty.page
from functions import *
from numpy import genfromtxt
import csv


class VC4Page:

    def __init__(self, path):
        
        self.path = path
        self.pageData, self.components = getInfoFromVC4Page(self.path)
        self.mVLayoutID = self.pageData['PageName'] + "Layout"
        self.mVContentID = self.pageData['PageName'] + "Content"
        self.mVPageID = self.pageData['PageName'] + "Page"
        self.translationDict = {"0x00001004": {"0": "Label"},
                                "0x00001002": {"0x0000016B": "MomentaryPushButton"}}
        self.attribTranslationDict = {"Label": {"top": "Top",
                                                "left": "Left",
                                                "width": "Width",
                                                "height": "Height",
                                                "zIndex": "",
                                                "text": "text"},
                                      "MomentaryPushButton": {"top": "Top",
                                                "left": "Left",
                                                "width": "Width",
                                                "height": "Height",
                                                "zIndex": "",
                                                "text": "text"}}
        # print(self.translationDict)
        # print(self.translationDict['0x00001002']['0x0000016B'])
        # print(self.components['Label'])
        # print()
        # print(self.components['MomentaryPushButton'])
        # for item in self.components:
        #     component = self.components[item]
        #     for at in component:
        #         if component[at] != '':
        #             print(at + ": ")
        #             print(component[at])
        #     print()

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
        i = 0
        for componentName in self.components:
            # print(self.translationDict[self.components[widget]['ClassId']][str(self.components[widget]['KeyId'])])
            # print(widget)
            component = self.components[componentName]
            widgetType = self.translationDict[component['ClassId']][str(component['KeyId'])]
            self.insertWidget(self.attribTranslationDict[widgetType], componentName, root, i)
            i = i + 1

        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        print(root)
        print()
        print(tree)
        tree.write(self.mVContentID + '.content', xml_declaration=True, encoding='utf-8')

        # editing output file to be usable by AS
        textToFind = "/><"
        textToReplaceWith = "/>\n<"

        with open(self.mVContentID + '.content', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace(textToFind, textToReplaceWith)

        with open(self.mVContentID + '.content', 'w') as file:
            file.write(filedata)

    def insertWidget(self, widgetTranslation, componentName, content, i):
        component = self.components[componentName]

        widget = ET.SubElement(content[0], 'Widget')
        widget.set('xsi:type', "widgets.brease." + componentName)
        widget.set('id', componentName)
        for attribName in widgetTranslation:
            if attribName == "text":
                widget.set(attribName, component['text']['en'])
            elif attribName == "zIndex":
                widget.set(attribName, str(i))
            else:
                attrib = widgetTranslation[attribName]
                temp = component[attrib]
                widget.set(attribName, temp)

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
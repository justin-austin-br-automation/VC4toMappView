# C:\VC4toMappView\VC4toMappView\Logical\VisuVC4\Pages\PageEmpty.page
from functions import *


class VC4Page:

    def __init__(self, path):
        
        self.path = path
        self.pageData, self.components = getInfoFromVC4Page(self.path)
        self.mVLayoutID = self.pageData['PageName'] + "Layout"
        self.mVContentID = self.pageData['PageName'] + "Content"
        self.mVPageID = self.pageData['PageName'] + "Page"

        # manually creating lookup table and widget translation dictionary (this will be changed later)
        self.lookupTable = {"0x00001004": {"0": "Label"},
                                "0x00001002": {"0x0000016B": "MomentaryPushButton"}}
        self.widgetTranslations = {"Label": {"top": "Top",
                                                "left": "Left",
                                                "width": "Width",
                                                "height": "Height",
                                                "zIndex": "zIndex",
                                                "text": "text"},
                                      "MomentaryPushButton": {"top": "Top",
                                                "left": "Left",
                                                "width": "Width",
                                                "height": "Height",
                                                "zIndex": "zIndex",
                                                "text": "text"}}

    # creates a mappView layout from VC4 data
    def createMVLayout(self, path):
        ET.register_namespace('ldef', "http://www.br-automation.com/iat2015/layoutDefinition/v2")
        
        # grab the tree from the xml doc
        os.chdir(os.path.dirname(__file__))
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

        path = path + '\Layouts'
        os.chdir(path)
        tree.write(self.mVLayoutID + '.layout', xml_declaration=True, encoding='utf-8')

    # creates a mappView content file from VC4 data
    def createMVContent(self, path):
        ET.register_namespace('', "http://www.br-automation.com/iat2015/contentDefinition/v2")
        ET.register_namespace('xsi', "http://www.w3.org/2001/XMLSchema-instance")
        
        # grab the tree from the xml doc
        os.chdir(os.path.dirname(__file__))
        tree = ET.parse('TemplateContent.content')

        # get the root of the tree
        root = tree.getroot()

        # set content ratio and name
        root.set('height', self.pageData['Height'])
        root.set('width', self.pageData['Width'])
        root.set('id', self.mVContentID)

        # add in any widgets
        for componentName in self.components:
            component = self.components[componentName]
            widgetType = self.lookupTable[component['ClassId']][str(component['KeyId'])]
            self.insertWidget(widgetType, self.widgetTranslations[widgetType], componentName, root)

        root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

        path = path + '\Pages\\' + self.mVPageID
        if not os.path.exists(path):
            os.makedirs(path)
        os.chdir(path)
        tree.write(self.mVContentID + '.content', xml_declaration=True, encoding='utf-8')

        # editing output file to be usable by AS
        textToFind = "/><"
        textToReplaceWith = "/>\n<"

        with open(self.mVContentID + '.content', 'r') as file:
            filedata = file.read()

        filedata = filedata.replace(textToFind, textToReplaceWith)

        with open(self.mVContentID + '.content', 'w') as file:
            file.write(filedata)

    # uses a translation dictionary to generate and insert a mappView widget
    def insertWidget(self, widgetType, widgetTranslation, componentName, content):
        # get component dictionary
        component = self.components[componentName]

        # create widget in the content xml tree and add necessary attributes
        widget = ET.SubElement(content[0], 'Widget')
        widget.set('xsi:type', "widgets.brease." + widgetType)
        widget.set('id', componentName)
        for attribName in widgetTranslation:
            if attribName == "text":
                widget.set(attribName, component['text']['en'])
            else:
                attrib = widgetTranslation[attribName]
                attribValue = component[attrib]
                widget.set(attribName, str(attribValue))

    # creates a mappView page from VC4 data
    def createMVPage(self, path):
        ET.register_namespace('pdef', 'http://www.br-automation.com/iat2015/pageDefinition/v2')

        # grab the tree from the xml doc
        os.chdir(os.path.dirname(__file__))
        tree = ET.parse('TemplatePage.page')

        # get the root of the tree
        root = tree.getroot()

        # set page name and layout
        root.set('id', self.mVPageID)
        root.set('layoutRefId', self.mVLayoutID)

        # set all Assignment values
        root[0][0].set('baseContentRefId', self.mVContentID)

        path = path + '\Pages\\' + self.mVPageID
        os.chdir(path)
        tree.write(self.mVPageID + '.page', xml_declaration=True, encoding='utf-8')
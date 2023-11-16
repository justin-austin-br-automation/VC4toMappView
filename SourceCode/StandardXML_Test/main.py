import xml.etree.ElementTree as ET

ET.register_namespace('ldef', "http://www.br-automation.com/iat2015/layoutDefinition/v2")
ET.register_namespace('', "http://www.br-automation.com/iat2015/contentDefinition/v2")
ET.register_namespace('pdef', "http://www.br-automation.com/iat2015/pageDefinition/v2")

# grab the tree from the xml doc
tree = ET.parse('TemplateLayout.layout')

# get the root of the tree
root = tree.getroot()

# setting variables that would be pulled from VC4 info
height = "600"
width = "800"
layoutId = "layoutManTest"

root.set('id', layoutId)
root.set('height', height)
root.set('width', width)

# loop through all the children of the Areas tag
root[0][0].set('height', height)
root[0][0].set('width', width)

tree.write('ManTest.layout', xml_declaration=True, encoding='utf-8')





# making content file

# grab the tree from the xml doc
tree = ET.parse('TemplateContent.content')

# get the root of the tree
root = tree.getroot()

# setting variables that would be pulled from VC4 info
height = "600"
width = "800"
contentId = "contentManTest"

root.set('id', contentId)
root.set('height', height)
root.set('width', width)

# add in any widgets
widget = ET.SubElement(root[0], 'Widget')
widget.set('xsi:type', "widgets.brease.Label")
widget.set('id', "Label")
widget.set('top', "20")
widget.set('left', "140")
widget.set('zIndex', "0")
widget.set('text', "Label")

widget = ET.SubElement(root[0], 'Widget')
widget.set('xsi:type', "widgets.brease.MomentaryPushButton")
widget.set('id', "MomentaryPushButton")
widget.set('top', "20")
widget.set('left', "20")
widget.set('zIndex', "1")
widget.set('text', "Button")

root.set('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")

tree.write('ManTest.content', xml_declaration=True, encoding='utf-8')

# editing output file to be usable by AS
textToFind = "/><"
textToReplaceWith = "/>\n<"

with open('ManTest.content', 'r') as file:
    filedata = file.read()

filedata = filedata.replace(textToFind, textToReplaceWith)

with open('ManTest.content', 'w') as file:
    file.write(filedata)




# making the page file

# grab the tree from the xml doc
tree = ET.parse('TemplatePage.page')

# get the root of the tree
root = tree.getroot()

# setting variables that would be pulled from VC4 info
pageId = "pageManTest"

root.set('id', pageId)
root.set('layoutRefId', layoutId)

# set all Assignment values
root[0][0].set('baseContentRefId', contentId)

tree.write('ManTest.page', xml_declaration=True, encoding='utf-8')
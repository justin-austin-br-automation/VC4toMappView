import xml.etree.ElementTree as ET

# grab the tree from the xml doc
tree = ET.parse('TemplateLayout.layout')

# get the root of the tree
root = tree.getroot()
#print(f"The root of this tree is: {root.tag}")

#print()

# show all tags in the tree
#print("All tags in the tree:")
#print([elem.tag for elem in root.iter()])

#print()

# setting variables that would be pulled from VC4 info
height = "600"
width = "800"
layoutId = "ManTest"

root.set('id', layoutId)
root.set('height', height)
root.set('width', width)

# loop through all the children of the Areas tag
for item in root.find('Areas'):
    item.set('height', height)
    item.set('width', width)

    # You can find specific elements of the Area tag
    #print(f"Height = {item.get('height')}")
    #print(f"Width = {item.get('width')}")

tree.write('ManTest.layout')

# editing output file to be usable by AS
textToFind = "ns0"
textToReplaceWith = "ldef"
textToInsert = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

with open('ManTest.layout', 'r') as file:
    filedata = file.read()

filedata = filedata.replace(textToFind, textToReplaceWith)

filedata = textToInsert + filedata

with open('ManTest.layout', 'w') as file:
    file.write(filedata)





# making page file

# grab the tree from the xml doc
tree = ET.parse('TemplatePage.page')

# get the root of the tree
root = tree.getroot()
print(f"The root of this tree is: {root.tag}")

print()

# show all tags in the tree
print("All tags in the tree:")
print([elem.tag for elem in root.iter()])

print()

# setting variables that would be pulled from VC4 info
height = "600"
width = "800"
pageId = "ManTest"

root.set('id', pageId)
root.set('height', height)
root.set('width', width)

# loop through all the children of the Areas tag
for item in root.find('Areas'):
    item.set('height', height)
    item.set('width', width)

    # You can find specific elements of the Area tag
    print(f"Height = {item.get('height')}")
    print(f"Width = {item.get('width')}")

tree.write('ManTest.layout')

# editing output file to be usable by AS
textToFind = "ns0"
textToReplaceWith = "ldef"
textToInsert = "<?xml version=\"1.0\" encoding=\"utf-8\"?>\n"

with open('ManTest.layout', 'r') as file:
    filedata = file.read()

filedata = filedata.replace(textToFind, textToReplaceWith)

filedata = textToInsert + filedata

with open('ManTest.layout', 'w') as file:
    file.write(filedata)
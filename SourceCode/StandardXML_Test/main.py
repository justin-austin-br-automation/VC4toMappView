import xml.etree.ElementTree as ET

# grab the tree from the xml doc
tree = ET.parse('TemplateLayout.layout')

# get the root of the tree
root = tree.getroot()
print(f"The root of this tree is: {root.tag}")

print()

# show all tags in the tree
print("All tags in the tree:")
print([elem.tag for elem in root.iter()])

print()

# loop through all the children of the Areas tag
for item in root.find('Areas'):

    # You can find specific elements of the Area tag
    print(f"Height = {item.get('height')}")
    print(f"Width = {item.get('width')}")
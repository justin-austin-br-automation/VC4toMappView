import os
from pathlib import Path
import xml.etree.ElementTree as ET
ET.register_namespace('', "http://br-automation.co.at/AS/Package")

# a test function (can be deleted)
def TestFunction():
    print("I am a test function. Rawr.")

# A function that makes a package file (.pkg) by reading the name of its
# current folder and the names of the files or folders within
def PackageCreator(PathToFolder):
    # change to the correct directory
    os.chdir(PathToFolder)
    path = Path(PathToFolder)

    # delete old package file if it exists
    for child in PathToFolder.iterdir():
        if child.name == "Package.pkg":
            child.unlink()

    # Making template package file xml tree
    # Type attribute naming format is different
    # for the layouts folder than the others
    if PathToFolder.name == "Layouts":
        emptyPackageText = """<Package SubType="{folderName}" PackageType="{folderName}" xmlns="http://br-automation.co.at/AS/Package">
  <Objects />
</Package>""".format(folderName = os.path.basename(PathToFolder))
    else:
        emptyPackageText = """<Package SubType="{folderName}" PackageType="{folderName}" xmlns="http://br-automation.co.at/AS/Package">
  <Objects />
</Package>""".format(folderName = os.path.basename(PathToFolder) + "Package")

    # Making and filling the xml tree
    packageXmlRoot = ET.fromstring(emptyPackageText)
    PackageItemAdder(path, packageXmlRoot)

    # Writing the xml tree to a .pkg file
    os.chdir(PathToFolder)
    packageXmlTree = ET.ElementTree()
    packageXmlTree._setroot(packageXmlRoot)
    packageXmlTree.write('Package.pkg', xml_declaration=True, encoding='utf-8')

    # editing output file to be usable by AS and more easily readable
    doubleBrackets = "><"
    newlineBrackets = ">\n<"
    ASInfoIdentifier = "?>"
    ASInfo = "?>\n<?AutomationStudio FileVersion=\"4.9\"?>"

    with open('Package.pkg', 'r') as pkg:
        filedata = pkg.read()

    filedata = filedata.replace(doubleBrackets, newlineBrackets)
    filedata = filedata.replace(ASInfoIdentifier, ASInfo)
    filedata = filedata.replace("'", "\"")

    with open('Package.pkg', 'w') as pkg:
        pkg.write(filedata)

# Recursive function used to find all files/directories and add them to the xml tree
def PackageItemAdder(Path, PackageXml):
    # Change to proper folder
    os.chdir(Path)

    # Add each file and folder to the package file
    for child in Path.iterdir():
        if child.is_file():
            file = ET.SubElement(PackageXml[0], 'Object')
            file.set('Type', "Package")
            file.text = child.name
        if child.is_dir():
            dir = ET.SubElement(PackageXml[0], 'Object')
            dir.set('Type', "Package")
            dir.text = child.name

            # Call the function to build a package file
            # in any folders found
            PackageCreator(child)
            os.chdir(Path)
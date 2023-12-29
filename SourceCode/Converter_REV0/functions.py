import os
from pathlib import Path
import xml.etree.ElementTree as ET
import numpy
import tkinter
ET.register_namespace('', "http://br-automation.co.at/AS/Package")


# A Function to find the MV Vis and VC4 Visu Folders within a Given AS Project
def VisFinder(ProjectPath, Vc4Path, MvPath):

    # Function to save the User input from popup
    def CommandSubmit():
        ProjectPath = UserEntry.get()
        print(ProjectPath)

    #Create the popup window for user submission of path
    window = tkinter.Tk()

    HeaderLabel = tkinter.Label(window, text='Input Filepath to Target Automation Studio Project:')
    HeaderLabel.config(font=('TkHeadingFont',15))
    HeaderLabel.pack(side = 'top')

    UserEntry = tkinter.Entry()
    UserEntry.config(font=('TkTextFont',15))
    UserEntry.insert(0,'E.G: C:\projects\VC4toMappView')
    UserEntry.config(width=30)
    UserEntry.pack()


    submit = tkinter.Button(window, text='Submit', command=CommandSubmit,height=2, width=15)
    submit.pack(side='bottom')

    window.mainloop()

    Vc4Path = 1
    MvPath = 2


        




def getInfoFromVC4Page(path):

    tree = ET.parse(path)

    # I'm assuming this namespace is the same for every VC4 page
    namespace = '{http://br-automation.co.at/AS/VC/Project}'
    root = tree.getroot()

    # Create the pageData dictionary
    pageData = {}

    # Get the page name
    pageData['PageName'] = root.get('Name')

    # Fill up the page data dictionary with property attribs that are
    # children of the Page tag
    for property in root.findall(namespace + 'Property'):
        pageData[property.get('Name')] = property.get('Value')

    # Create the controlsElements dictionary.
    # It will be a nested dictionary. You can access it with the format:
    # controlsElements['elementName']['elementAttribute']
    components = {}

    controlIndex = 0
    for control in root.iter(namespace + 'Control'):

        # get the name and classId of the control element for later use
        name = control.get('Name')

        # create a new dictionary for each control element to hold the different attributes
        components[name] = {}

        # get the class id of the control element
        components[name]['ClassId'] = control.get('ClassId')

        # grab each control element and stick it in the dictionary
        for item in control:
            components[name][item.get('Name')] = item.get('Value')

        # This is kind of dumb. The text of the 'widget' itself is not included with
        # the rest of the 'widget' info. Instead, you have to reference the TextLayer tags
        # under the TextGroup tag.
        # I'm assuming order of the text matches the order of the Control elements.
        # Otherwise, we can grab the text index or text index offset from the control element.
        components[name]['text'] = {}
        for textLayer in root.iter(namespace + 'TextLayer'):
            components[name]['text'][textLayer.get('LanguageId')] = textLayer[controlIndex].get('Value')

        components[name]['zIndex'] = controlIndex
        controlIndex += 1

        # Dealing with default values from VC4 that won't populate in the xml unless they are changed
        if not "AlignmentHorizontal" in components[name]:
            components[name]["AlignmentHorizontal"] = "Left"
        if not "AlignmentVertical" in components[name]:
            components[name]["AlignmentVertical"] = "Center"


        # Don't love this code. We need to extract the virtual key class id and tie it with the
        # working component. So I am gathering the VirtualKey embedded reference from the control element,
        # then parsing the page file for the matching Virtual Key
        if 'VirtualKey' in components[name]:

            # extract the virtual key name
            # e.g. Source[local].VirtualKey[%embVirtualKey_2] => %embVirtualKey_2
            VirtualKey = components[name]['VirtualKey']
            parsedVirtualKey = str(VirtualKey).split("VirtualKey", 1)[1][1:-1]
            components[name]['ParsedVirtualKey'] = parsedVirtualKey
    
            for virtualKey in root.iter(namespace + 'VirtualKey'):
                if virtualKey.get('Name') == components[name]['ParsedVirtualKey']:
                    for keyAction in virtualKey.iter(namespace + 'KeyAction'):
                        components[name]['KeyId'] = keyAction.get('ClassId')
        else:   # if there is no virtual key for the element, add one with a value of 0 for lookup purposes
            components[name]['KeyId'] = 0

    
    return (pageData, components)


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




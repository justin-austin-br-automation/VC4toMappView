import xml.etree.ElementTree as ET

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
    controlElements = {}

    controlIndex = 0
    for control in root.iter(namespace + 'Control'):

        # get the name and classId of the control element for later use
        name = control.get('Name')

        # create a new dictionary for each control element to hold the different attributes
        controlElements[name] = {}

        # get the class id of the control element
        controlElements[name]['ClassId'] = control.get('ClassId')

        # grab each control element and stick it in the dictionary
        for item in control:
            controlElements[name][item.get('Name')] = item.get('Value')

        # This is kind of dumb. The text of the 'widget' itself is not included with
        # the rest of the 'widget' info. Instead, you have to reference the TextLayer tags
        # under the TextGroup tag.
        # I'm assuming order of the text matches the order of the Control elements.
        # Otherwise, we can grab the text index or text index offset from the control element.
        controlElements[name]['text'] = {}
        for textLayer in root.iter(namespace + 'TextLayer'):
            controlElements[name]['text'][textLayer.get('LanguageId')] = textLayer[controlIndex].get('Value')

        controlElements[name]['zIndex'] = controlIndex
        controlIndex += 1


        # Don't love this code. We need to extract the virtual key class id and tie it with the
        # working component. So I am gathering the VirtualKey embedded reference from the control element,
        # then parsing the page file for the matching Virtual Key
        if 'VirtualKey' in controlElements[name]:

            # extract the virtual key name
            # e.g. Source[local].VirtualKey[%embVirtualKey_2] => %embVirtualKey_2
            VirtualKey = controlElements[name]['VirtualKey']
            parsedVirtualKey = str(VirtualKey).split("VirtualKey", 1)[1][1:-1]
            controlElements[name]['ParsedVirtualKey'] = parsedVirtualKey
    
            for virtualKey in root.iter(namespace + 'VirtualKey'):
                if virtualKey.get('Name') == controlElements[name]['ParsedVirtualKey']:
                    for keyAction in virtualKey.iter(namespace + 'KeyAction'):
                        controlElements[name]['KeyId'] = keyAction.get('ClassId')

    
    return (pageData, controlElements)
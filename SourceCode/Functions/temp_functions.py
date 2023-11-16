# a test function (can be deleted)
def TestFunction():
    print("I am a test function. Rawr.")

# A function that makes a package file (.pkg) by reading the name of its
# current folder and the names of the files or folders within
def PackageCreator(PathToFolder):
    print(PathToFolder)
    # This should work with any folder.
    # Use the auto-generated mappview .pkg files for reference
    # Do something along the following steps:
    # 
    # Get the folder name
    # Create the file
    #   SubType="FolderNamePackage" 
    #   PackageType="FolderNamePackage"
    #   xmlns="http://br-automation.co.at/AS/Package"
    # Read each file or directory in the in the folder and create a file called Package.pkg

    pass # remove me

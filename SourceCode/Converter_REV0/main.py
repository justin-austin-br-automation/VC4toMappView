from VC42MV import *

if __name__ == "__main__":
        
    # !!!!CHANGE THIS TO YOUR PATH!!!!!
    path = 'C:\projects\\4.11\VC4toMappView\VC4toMappView\Logical\VisuVC4\Pages\PageEmpty.page'
    page = VC4Page(path)

    page.createMVLayout()
    page.createMVContent()
    page.createMVPage()

    # path = Path("C:\projects\\4.11\mappViewTest\mappViewTest\Logical\mappView\Visualization")
    # PackageCreator(path)
from VC42MV import *

if __name__ == "__main__":
    
    ProjectPath_testEmpty = ''
    VCPath_testEmpty = ''
    MVPath_testEmpty = ''

    VisFinder(ProjectPath_testEmpty, VCPath_testEmpty, MVPath_testEmpty)
    
    
    # !!!!CHANGE THIS TO YOUR PATH!!!!!
    path = 'C:\projects\\4.11\mappViewTest\mappViewTest\Logical\Visu\Pages\PageEmpty.page'
    page = VC4Page(path)

    page.startVisFile()

    path = "C:\projects\\4.11\mappViewTest\mappViewTest\Logical\mappView\Visualization"
    page.createMVLayout(path)
    page.createMVContent(path)
    page.createMVPage(path)

    path = Path("C:\projects\\4.11\mappViewTest\mappViewTest\Logical\mappView\Visualization")
    PackageCreator(path)

    path = Path("C:\projects\\4.11\mappViewTest\mappViewTest\Physical\Config1\PC\mappView")
    page.genVisFile(path)
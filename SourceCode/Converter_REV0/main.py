from VC42MV import *

if __name__ == "__main__":
    # !!!!CHANGE THIS TO YOUR PATH!!!!!
    path = 'C:\projects\\4.11\mappViewTest\mappViewTest\Logical\Visu\Pages\PageEmpty.page'
    page = VC4Page(path)

    path = "C:\projects\\4.11\mappViewTest\mappViewTest\Logical\mappView\Visualization"
    page.createMVLayout(path)
    page.createMVContent(path)
    page.createMVPage(path)

    path = Path("C:\projects\\4.11\mappViewTest\mappViewTest\Logical\mappView\Visualization")
    PackageCreator(path)
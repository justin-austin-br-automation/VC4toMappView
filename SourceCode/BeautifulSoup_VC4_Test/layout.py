from bs4 import BeautifulSoup


# Reading the data inside the xml
# file to a variable under the name 
# data
with open('PageEmpty.page', 'r') as f:
    data = f.read()

# Reading in a template layout file to be editted
with open('TemplateLayout.layout', 'r') as f:
    Layout = f.read()
print(Layout)

# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
Bs_data = BeautifulSoup(data, "xml")
Bs_Layout = BeautifulSoup(Layout, "xml")
print(Bs_Layout)

# Finding all instances of tag 
# `unique`
b_unique = Bs_data.find_all('Page')

#print(b_unique)

page_height = Bs_data.find('Property', {'Name':'Height'}).get('Value')
page_width = Bs_data.find('Property', {'Name':'Width'}).get('Value')

print(Bs_Layout.Areas)

print(f'Page Height = {page_height}')
print(f'Page Width = {page_width}')
# pip install beautifulsoup4
# pip install lxml


from bs4 import BeautifulSoup
 
 
# Reading the data inside the xml
# file to a variable under the name 
# data
with open('PageEmpty.page', 'r') as f:
    data = f.read()
 
# Passing the stored data inside
# the beautifulsoup parser, storing
# the returned object 
Bs_data = BeautifulSoup(data, "xml")
 
# Finding all instances of tag 
# `unique`
b_unique = Bs_data.find_all('Page')
 
#print(b_unique)

page_height = Bs_data.find('Property', {'Name':'Height'}).get('Value')
page_width = Bs_data.find('Property', {'Name':'Width'}).get('Value')

print(f'Page Height = {page_height}')
print(f'Page Width = {page_width}')


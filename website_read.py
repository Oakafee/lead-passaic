'''
import urllib.request

depurl = 'https://www9.state.nj.us/DEP_WaterWatch_public/JSP/PBCUSummary.jsp?tinwsys=127'
weather = 'https://www.weather.gov/'
html = ''

with urllib.request.urlopen(weather) as response:
   html = response.read()
   
print(html)
'''

'''
import webbrowser
webbrowser.open(depurl, new=2)
'''

from selenium.webdriver import Firefox

driver = Firefox(executable_path='/Applications/geckodriver')
driver.get('https://www9.state.nj.us/DEP_WaterWatch_public/')
leadtable = driver.find_elements_by_name("mainform")
print(leadtable)
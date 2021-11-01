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

'''
from selenium.webdriver import Firefox

driver = Firefox(executable_path='/Applications/geckodriver')
driver.get('https://www9.state.nj.us/DEP_WaterWatch_public/JSP/WSDetail.jsp?tinwsys=117')
pws_input = driver.find_element(By.NAME, "number")
print('pwsid', pws_input[0])
#pws_input.send_keys("0714001" + Keys.ENTER)
'''


import requests

x = requests.get('https://www9.state.nj.us/DEP_WaterWatch_public/JSP/WSDetail.jsp?tinwsys=117')
print(x.status_code)
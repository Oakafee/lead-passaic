import numpy as np
import pandas as pd

'''
lead_page = open('/Users/Oakafee/Documents/Grad_school/gisProgramming/project/newark.html')

lead_table = pd.read_html(lead_page, attrs = {'style': 'background:#99CCFF;'})
lead_table = pd.DataFrame(lead_table[0])


lead_table.to_pickle('/Users/Oakafee/Documents/Grad_school/gisProgramming/project/table-test.pkl')
'''
ws_table = pd.read_pickle('/Users/Oakafee/Documents/Grad_school/gisProgramming/project/table-test.pkl')
pwsid = ws_table[1][0]
wsname = ws_table[1][1]
wsname = wsname.lower()
wsname = wsname.replace(" ","-")

print(pwsid + '-' + wsname)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

table = pd.read_pickle('/Users/Oakafee/Documents/Grad_school/gisProgramming/project/ws_data/meowwolf.pkl')

start = table.loc[:,['Start dates','Lead in mg/L']]
end = table.loc[:,['End dates','Lead in mg/L']]

start.rename(columns = {'Start dates':'date'}, inplace = True)
end.rename(columns = {'End dates':'date'}, inplace = True)

alldates = pd.concat([start,end], ignore_index=True, sort=True)
alldates.sort_values(by='date', inplace=True)

print(alldates)

plt.plot(alldates['date'],alldates['Lead in mg/L'])
plt.show()

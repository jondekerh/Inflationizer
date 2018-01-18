import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import filedialog

#using prompts, make user select proper files
root = tk.Tk()
root.withdraw()

catPrompt = filedialog.askopenfilenames(title = 'choose ALL catalog files')
catList = list(catPrompt)

invPrompt = filedialog.askopenfilename(title = 'now select the inventory file')

finalCat = pd.DataFrame(columns = ['Item', 'VarRetail'])

#loop to append shortened contents of each selected catalog file into one dataframe (finalCat)
for index, i in enumerate(catList):
  importCat = pd.read_csv(i)
  cat = importCat[['Item', 'Retail']]
  cat.columns = ['Item', 'VarRetail']
  cat['Item'] = cat['Item'].str.replace('-','')
  finalCat = finalCat.append(cat)
  print(i + ' appended successfully!')

#set up the inventory dataframe
importInv = pd.read_csv(invPrompt)
inv = importInv[['SKU', 'Retail']]

#make a new dataframe with 3 columns: SKU, Retail, and VarRetail. Then remake it with only rows where Retail < VarRetail
df = pd.merge(inv, finalCat, left_on='SKU', right_on='Item').drop('Item', axis=1)
df = df.loc[df['Retail'].astype(float) < df['VarRetail'].astype(float)]

#write it
df.to_csv(path_or_buf = './new_prices.csv')
print('new_prices.csv has been created in this file\'s directory!')

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

#start of loop to make docs for each catalog file imported
for index, i in enumerate(catList):

  importCat = pd.read_csv(i)
  importInv = pd.read_csv(invPrompt)

  #set up the catalog dataframe
  cat = importCat[['Item', 'Retail']]
  cat.columns = ['Item', 'VarRetail']
  cat['Item'] = cat['Item'].str.replace('-','')

  #set up the inventory dataframe
  inv = importInv[['SKU', 'Retail']]

  #make a new dataframe with only the SKU, Retail, and VarRetail columns, then only keep columns where Retail < VarRetail
  df = pd.merge(inv, cat, left_on='SKU', right_on='Item').drop('Item', axis=1)
  df = df.loc[df['Retail'].astype(float) < df['VarRetail'].astype(float)]

  print ('SUCCESS ' + i)

  #write it:
  df.to_csv(path_or_buf = './inventory_new' + str(index) + '.csv')

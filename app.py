import pandas as pd
import numpy as np
import tkinter as tk
import os 
from tkinter import filedialog
from tkinter import messagebox
import datetime

#using prompts, make user selects proper files
root = tk.Tk()
root.withdraw()

catPrompt = filedialog.askopenfilenames(title = 'Use SHIFT or CTRL click to select ALL catalog files')
catList = list(catPrompt)

invPrompt = filedialog.askopenfilename(title = 'Now select the inventory file')

#create a blank dataframe with appropriate column names to store data from all the catalog files
finalCat = pd.DataFrame(columns = ['Item', 'VarRetail', 'Retail Dept'])

#loop to append shortened contents of each selected catalog file into one dataframe (finalCat)
for i in catList:
  importCat = pd.read_csv(i)
  cat = importCat[['Item', 'Retail', 'Retail Dept']]
  cat.columns = ['Item', 'VarRetail', 'Retail Dept']
  cat['Item'] = cat['Item'].str.replace('-', '')
  finalCat = finalCat.append(cat)

#set up the inventory dataframe and drop rows where the last sale happened more than a few years ago
importInv = pd.read_csv(invPrompt, parse_dates = ['Date Last Sale'])
inv = importInv[['SKU', 'Description', 'Retail', 'Date Last Sale', 'Stk U/M', 'Pur U/M', 'Fineline #']]
inv = inv.dropna(subset = ['Date Last Sale'])    #drop all rows where date data is NaN/blank

for i, row in inv.iterrows():
  if (row['Date Last Sale'].year <= 2015):
    inv = inv.drop([i])
    
#merge the two dataframes and drop the Item column. Then remake it with only rows where Retail < VarRetail
newPrices = pd.merge(inv, finalCat, left_on = 'SKU', right_on = 'Item').drop('Item', axis = 1)
newPrices = newPrices.loc[newPrices['Retail'].astype(float) < newPrices['VarRetail'].astype(float)]

#order newPrices by the Dept #, and within that by Fineline #
newPrices = newPrices.sort_values(by = ['Retail Dept', 'Fineline #']) 

#if Stk U/M and Pur U/M are not equal (designating an item bought in bulk and priced individually) append that row to newPricesBulk and drop it from newPrices
newPricesBulk = pd.DataFrame(columns = ['SKU', 'Description', 'Retail', 'VarRetail', 'Stk U/M', 'Pur U/M'])

for i, row in newPrices.iterrows():
  if (row['Stk U/M'] != row['Pur U/M']):
    newPricesBulk = newPricesBulk.append(row)
    newPrices = newPrices.drop([i])

#remove columns that are no longer needed for user-friendly viewing
newPrices = newPrices.drop(['Date Last Sale', 'Stk U/M', 'Pur U/M', 'Fineline #'], axis = 1)
newPricesBulk = newPricesBulk.drop(['Date Last Sale', 'Stk U/M', 'Pur U/M', 'Fineline #'], axis = 1)

#reset indexes
newPrices = newPrices.reset_index(drop = True)
newPricesBulk = newPricesBulk.reset_index(drop = True)

#write files
newPrices.to_csv(path_or_buf = './new_prices.csv')
newPricesBulk.to_csv(path_or_buf = './new_prices_bulk.csv')

if os.path.exists('./new_prices.csv') and os.path.getsize('./new_prices.csv') > 0:
  print('new_prices.csv has been created in this program\'s directory!')

if os.path.exists('./new_prices_bulk.csv') and os.path.getsize('./new_prices_bulk.csv') > 0:
  print('new_prices_bulk.csv has been created in this program\'s directory!')

import pandas as pd
import numpy as np
import tkinter as tk
import os
from tkinter import filedialog
from tkinter import messagebox


#using prompts, make user selects proper CSV files
root = tk.Tk()
root.withdraw()

catPrompt = filedialog.askopenfilenames(title = 'Use SHIFT or CTRL click to select ALL catalog files')
catList = list(catPrompt)

invPrompt = filedialog.askopenfilename(title = 'Now select the inventory file')


#create a blank dataframe to store data from all the catalog files
finalCat = pd.DataFrame(columns = ['Item', 'Variable Retail', 'Retail Dept'])


def makeCatalog():
  #loop to append shortened contents of each selected catalog file into one dataframe (finalCat)
  for i in catList:
    global finalCat
    importCat = pd.read_csv(i)
    cat = importCat[['Item', 'Retail', 'Retail Dept']]
    cat.columns = ['Item', 'Variable Retail', 'Retail Dept']
    cat['Item'] = cat['Item'].str.replace('-', '')
    finalCat = finalCat.append(cat)

makeCatalog()


#crete a blank dataframe to store inventory data
inv = pd.DataFrame(columns = ['SKU', 'Description', 'Retail', 'Date Last Sale', 'Fineline #'])

def makeInventory():
  #add data to the inventory dataframe
  global inv
  importInv = pd.read_csv(invPrompt, parse_dates = ['Date Last Sale'])
  inv = importInv[['SKU', 'Description', 'Retail', 'Date Last Sale', 'Fineline #']]

makeInventory()


#drop all rows where Date Last Sale data is NaN/blank (meaning either the item is too old or too new to worry about)
inv = inv.dropna(subset = ['Date Last Sale'])

#remove any row where the item was last sold more than a few years ago
for i, row in inv.iterrows():
  if (row['Date Last Sale'].year <= 2015):
    inv = inv.drop([i])


#merge the two dataframes as newPrices and drop the Item column
newPrices = pd.merge(inv, finalCat, left_on = 'SKU', right_on = 'Item').drop('Item', axis = 1)

#drop any rows where Retail < Variable Retail
newPrices = newPrices.loc[newPrices['Retail'].astype(float) < newPrices['Variable Retail'].astype(float)]

#create a blank dataframe to store any bulk prices removed from newPrices
newPricesBulk = pd.DataFrame(columns = ['SKU', 'Description', 'Retail', 'Variable Retail', 'Retail Dept'])


#order newPrices by the Dept #, and within that by Fineline #
newPrices = newPrices.sort_values(by = ['Retail Dept', 'Fineline #'])

#create a new dataframe and order it by Date Last Sale and within that by Fineline #
newPricesDate = newPrices.sort_values(by = ['Date Last Sale', 'Fineline #'], ascending = False)


#drop Date Last Sale and Fineline # in newPrices as it is no longer needed
newPrices = newPrices.drop(['Date Last Sale', 'Fineline #'], axis = 1)

#drop Fineline # and Retail Dept in newPricesDate for same reason
newPricesDate = newPricesDate.drop(['Fineline #', 'Retail Dept'], axis = 1)

#make the Date Last Sale column the left-most column for readability
newPricesDate = newPricesDate.set_index('Date Last Sale')


#if Variable Retail is greater than 5 times Retail (designating an item bought as a pack but sold invidually) append that row to newPricesBulk and drop it from newPrices
for i, row in newPrices.iterrows():
  if (float(row['Variable Retail']) > float(row['Retail']) * 5):
    newPricesBulk = newPricesBulk.append(row)
    newPrices = newPrices.drop([i])


#write files
newPrices.to_csv(path_or_buf = './new-prices.csv', index = False)
newPricesDate.to_csv(path_or_buf = './new-prices-by-priority.csv', index = True)
newPricesBulk.to_csv(path_or_buf = './new-prices-bulk.csv', index = False)

if os.path.exists('./new-prices.csv') and os.path.getsize('./new-prices.csv') > 0:
  print('new-prices.csv has been created in this program\'s directory!')

if os.path.exists('./new-prices-bulk.csv') and os.path.getsize('./new-prices-bulk.csv') > 0:
  print('new-prices-bulk.csv has been created in this program\'s directory!')

if os.path.exists('./new-prices-by-priority.csv') and os.path.getsize('./new-prices-by-priority.csv') > 0:
  print('new-prices-by-priority.csv has been created in this program\'s directory!')

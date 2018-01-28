import pandas as pd
import numpy as np
import tkinter as tk
import os 
from tkinter import filedialog
from tkinter import messagebox

#using prompts, make user selects proper files
root = tk.Tk()
root.withdraw()

catPrompt = filedialog.askopenfilenames(title = 'Use SHIFT or CTRL click to select ALL catalog files')
catList = list(catPrompt)

invPrompt = filedialog.askopenfilename(title = 'Now select the inventory file')

#create a blank dataframe with appropriate column names to store data from all the catalog files
finalCat = pd.DataFrame(columns = ['Item', 'VarRetail'])

#loop to append shortened contents of each selected catalog file into one dataframe (finalCat)
for i in catList:
  importCat = pd.read_csv(i)
  cat = importCat[['Item', 'Retail']]
  cat.columns = ['Item', 'VarRetail']
  cat['Item'] = cat['Item'].str.replace('-','')
  finalCat = finalCat.append(cat)
  print(i + ' appended successfully!')

#set up the inventory dataframe
importInv = pd.read_csv(invPrompt)
inv = importInv[['SKU', 'Description', 'Retail']]

#make a new dataframe with 4 columns: SKU, , Description, Retail, and VarRetail. Then remake it with only rows where Retail < VarRetail
newPrices = pd.merge(inv, finalCat, left_on = 'SKU', right_on = 'Item').drop('Item', axis = 1)
newPrices = newPrices.loc[newPrices['Retail'].astype(float) < newPrices['VarRetail'].astype(float)]

#if price makrup is higher than 5 times the original price, create a prompt asking the user if they want to ignore that row or not
for i, row in newPrices.iterrows():
  if (float(row['VarRetail']) > float(row['Retail']) * 5):
    result = messagebox.askquestion('BULK ITEM FLAG', row['Description'] + ' (SKU:' + str(row['SKU']) + ') is currently ' +  str(row['Retail']) + ' and will be changed to ' + str(row['VarRetail']) + '. Extremely steep changes like this could result from pricing items individually or by-the-foot while the catalog uses the box price. Would you like to ignore this item?')
    if result == 'yes':
      newPrices = newPrices.drop([i])
      print ('Removing ' + str(row['SKU']) + '...')
    else:
      print ('Keeping ' + str(row['SKU']) + '...')

#reset indexes
newPrices = newPrices.reset_index(drop = True)

#write it
newPrices.to_csv(path_or_buf = './new_prices.csv')

if os.path.exists('./new_prices.csv') and os.path.getsize('./new_prices.csv') > 0:
  print('new_prices.csv has been created in this program\'s directory!')
else:
  print('ERROR: new_prices.csv was not written correctly!')

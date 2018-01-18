import pandas as pd
import numpy as np

importCat = pd.read_csv('./Temp/catalog_auto.csv')
importInv = pd.read_csv('./Temp/inventory_12-24-17.csv')

#set up the catalog dataframe
cat = importCat[['Item', 'Retail']]
cat.columns = ['Item', 'VarRetail']
cat['Item'] = shortCat['Item'].str.replace('-','')

#set up the inventory dataframe
inv = inportInv[['SKU', 'Retail']]

#make a new dataframe with only the SKU, Retail, and VarRetail columns, then only keep columns where Retail < VarRetail
df = pd.merge(inv, cat, left_on='SKU', right_on='Item').drop('Item', axis=1)
df = df.loc[df['Retail'].astype(float) < df['VarRetail'].astype(float)]

#write it:
df.to_csv(path_or_buf = './inventory_new.csv')

# Inflationizer
Inflationizer was designed for Tweedy and Popp Hardware to automate the process of checking prices for markup according to True Value's catalog.

Previously one would have to do all price checks by hand, referencing prices listed on True Value's website. Because an API is not available for the website CSV documents containing catalog data have to be downloaded manually using Epicor Eagle Browser. An inventory CSV is also obtained from our local system. This program then loads the CSV documents, strips them of irrelevant data, combines them, and compares the values to return a new CSV document. A macro in Eagle Browser can then be used to read the files created by this program, update prices in the system accordingly, and even load a set of new labels to be printed.

This program saves hours upon hours of tedius work and ensures prices can easily be kept current.

Cheers!

NOTE: This program requires Python 3.6.3 installed locally in order to run. If Python isn't installed on your system you can get it [here](https://www.python.org/downloads/release/python-363/). Once it's installed you'll also need to use pip to install required libraries. When testing on my computer just running `pip install pandas` seemed to install all required libraries. 

## How To Use It
1. Make sure you've downloaded the **COMPLETE** CSVs for each catalog department, along with the **COMPLETE** CSV for local inventory. This script will not work unless **ALL** the available data is present in each CSV.
2. Run Inflationizer.bat.
3. When the first prompt appears to select the catalog files, use either SHIFT or CTRL click to select all relevant catalog CSVs at the same time.
4. When the second prompt appears to select the inventory file, simply select the inventory CSV.
5. Allow up to a minute or two for the program to run depending on your system. Ignore any warnings that appear in the console.
6. When the program has finished it will create three different CSV files in the same folder that Inflationizer.bat is located in. These files are:
* **new-prices.csv:** This file contains all items that need adjustment, organized by retail department and then grouped by fineline code.
* **new-prices-bulk.csv:** This file contains any items where we may have purchased a package and sold its contents individually, thus leading to massive differences in our price and the catalog price. These should be looked over and adjusted by hand as there is no reliable way to do it automatically. 
* **new-prices-by-priority.csv** This file is the same as new-prices.csv but it has been organized so that the items on top are the ones which are most frequently sold, and thus take priority for adjustment.
7. After the CSV files have been created they can be used in an Eagle Browser macro to update all items in either file, or segments can be extracted by department and put into smaller files which can update only the selected departments. 

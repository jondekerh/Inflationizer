# markup
Markup was designed for Tweedy and Popp Hardware to automate the process of checking prices for markup according to True Value's catalog.

Previously one would have to do all price checks by hand, referencing prices listed on True Value's website. Because an API is not available for the website CSV documents containing catalog data have to be downloaded manually using Epicor Eagle Browser. An inventory CSV is also obtained from our local system. This program then loads the CSV documents, strips them of irrelevant data, combines them, and compares the values to return a new CSV document. The document contains the SKU of any underpriced item, its current price in our system, and the price it should have. A macro in Eagle Browser can then be used to read the document, update prices in the system accordingly, and even load a set of new labels to be printed.

This program saves hours upon hours of tedius work and ensures prices can easily be kept current.

Cheers!

%reset -f
import pandas as pd
import numpy as np

# import dataframe without the first row being taken as variable names.
df = pd.read_excel("wash_park.xlsx", header=None)
df.head()

# Create a list with the 0th column, which is the only column in the dataframe, split at each space.
lister = df[0].str.split(" ")
lister

lister[0]
# Create a second DataFrame that contains the variables of interest.
df_2 = pd.DataFrame(
    columns=[
        "Listing_ID",
        "Address",
        "Close_Date",
        'Ttl',
        'Fin',
        "Orig_Price",
        "List_Price",
        "Close_Price",
    ]
)


# Set the Listing_ID variable to the 0th element of each row in lister.
df_2["Listing_ID"] = lister.apply(lambda x: x[0])

# Set the street address to the 1st through 4th elements. 
df_2["Address"] = lister.apply(
    lambda x: x[1] + " " + x[2] + " " + x[3] + " " + x[4]
)


df_2

# Per manual inspection above, 751 S Race was not entered with "ST"

df_2['Address'].iloc[15]= '751 S Race St'

df_2['Close_Date']= lister.apply(lambda x: x[11])

df_2

# Again, 751 S Race poses a problem. 
df_2['Close_Date'].iloc[15]= lister[15][10]

df_2

df_2['Orig_Price']= lister.apply(lambda x: x[-4])

# Below needs to strip off the leading dollar signs for the List Price and Close Price columns. 
df_2['List_Price']= lister.apply(lambda x: x[-3][1:])
df_2['Close_Price']= lister.apply(lambda x: x[-2][1:])

df_2

df_2.info()

df_2['Close_Date']= pd.to_datetime(df_2['Close_Date'], format='%m/%d/%y')
df_2

df_2['Close_Date']= df_2['Close_Date'].dt.date


df_2= df_2.sort_values(by= 'Close_Date', ascending=False)
df_2

df_2['Ttl'] = lister.apply(lambda x: x[-11])
df_2['Fin'] = lister.apply(lambda x: x[-10])


df_2
# Need to scrape chain of title records. Ex: https://www.denvergov.org/property/realproperty/chainoftitle/0514128017000

df_2.to_excel('wash_park_export.xlsx')

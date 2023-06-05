%reset -f
import pandas as pd
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as plt 

pd.options.display.float_format = "{:,}".format

df = pd.read_excel("wash_park_export_data_pull.xlsx")

df

df.rename(columns={df.columns[0]: "Org_Index"}, inplace=True)

df.head()

df["Buyer"].value_counts()
df["Address"].value_counts()

# Close_Price is a string, but just to see.
df["Close_Price"].describe()
df.groupby("Is_Developer")["Close_Price"].describe()

# Need to remove white spaces
df["Is_Developer"] = df["Is_Developer"].str.strip()

# Close_Price is a string, but just to see.
df["Close_Price"].describe()
df.groupby("Is_Developer")["Close_Price"].describe()


# 566 York was sold twice in the time period. On 5/10/22 and 10/20/20.

# Convert strings to numbers
df["Ttl"] = df["Ttl"].str.replace(",", "")
df["Fin"] = df["Fin"].str.replace(",", "")
df["Orig_Price"] = df["Orig_Price"].str.replace(",", "")
df["List_Price"] = df["List_Price"].str.replace(",", "")
df["Close_Price"] = df["Close_Price"].str.replace(",", "")

df

df[df['Ttl'].isna()]
df["Ttl"] = df["Ttl"].astype(int)
df["Fin"] = df["Fin"].astype(int)
df["Orig_Price"] = df["Orig_Price"].astype(int)
df["List_Price"] = df["List_Price"].astype(int)
df["Close_Price"] = df["Close_Price"].astype(int)


df
df.info()

# Price if sold to developer or not, all years. 
df.groupby("Is_Developer")["Close_Price"].describe().round()

# Above is some evidence that developers pay a little less based on median and mean. 

# Below create a year variable.
df["Year"] = df["Close_Date"].dt.year


# Summary stats by developer sale and year for closing price. 
df.groupby(["Is_Developer", "Year"])["Close_Price"].describe().round()

# 2021 has the largest spread between developer and non-developer sales, but a $2M sale is included in 
# the non-developer which couldn't have been a house like ours. 


# Mean only for developer sale and year for closing price. 
df.groupby(["Is_Developer", "Year"])["Close_Price"].describe().round()['mean']

# Median only for developer sale and year for closing price. 
df.groupby(["Is_Developer", "Year"])["Close_Price"].describe().round()['50%']


df.head()

df['Is_Developer'].value_counts()
df['Is_Developer'].isna().sum()
df.shape
df.info()


# Mean for the three years. 
df['Close_Price'].describe().round()['mean']


# Median for the three years 
df['Close_Price'].describe().round()['50%']

# Mean for each year. 
df.groupby('Year')['Close_Price'].describe().round()

# Median only for each year. 
df.groupby('Year')['Close_Price'].describe().round()['50%']


# Need to go through the neighborhood and mark houses I can see were recently developed and
# see if these agree to the dataset. 

# Matt and Susan at 695 S Gaylord was sold on 5/25/21 and is not in the dataset. Verify the 
# dataset is complete. 


# Create a graphics DataFrame

df_graphics= df[(df['Is_Developer'] != '?') & (df['Is_Developer'].notnull())]

df_graphics

df_graphics.groupby('Is_Developer')['Close_Price'].describe()

df_graphics.groupby('Is_Developer')['Close_Price'].describe().index[0]

df_graphics.groupby('Is_Developer')['Close_Price'].describe()['mean'].loc['No']

# Using the OOP approach

'''
######################
# Medians All Years-- hardcoded strings in the right format. 
###########
fig, ax= plt.subplots()
# initialize the first bar of the bar chart below for group1
bar1= ax.bar(df_graphics.groupby('Is_Developer')['Close_Price'].describe().index[0]
, df_graphics.groupby('Is_Developer')['Close_Price'].describe()['50%'].loc['No']

)

ax.bar_label(bar1, fmt='$1,322,500')

# initialize the second bar of the bar chart for group2
bar2= ax.bar(df_graphics.groupby('Is_Developer')['Close_Price'].describe().index[1]
, df_graphics.groupby('Is_Developer')['Close_Price'].describe()['50%'].loc['Yes']

)

# Feed in the label for group2
ax.bar_label(bar2, fmt='$1,300,000')

# ax.bar(df_graphics['Is_Developer'], df_graphics['Close_Price'].mean())
# Include dollar signs and commas. 
ax.yaxis.set_major_formatter(mp.ticker.StrMethodFormatter("${x:,.0f}"))
ax.set_title('Median Developer vs. Non-Developer Sales- All Years')
ax.set_ylabel('Closing Price')
ax.set_ylim(1200000, 1375000)
ax.legend(loc='upper left', labels= ['Developer', 'Non-Developer'])
ax.set_xticklabels(['Developer', 'Non-Developer'])
fig.show()
'''

######################
# Medians All Years -- automated without scientific notation.
###########
fig, ax= plt.subplots()


# initialize the first bar of the bar chart below for group1
bar1= ax.bar(df_graphics.groupby('Is_Developer')['Close_Price'].describe().index[0]
, df_graphics.groupby('Is_Developer')['Close_Price'].describe()['50%'].loc['No']

)

#ax.bar_label(bar1, fmt= '%.0f')
ax.bar_label(bar1, fmt='${:,.0f}')

# initialize the second bar of the bar chart for group2
bar2= ax.bar(df_graphics.groupby('Is_Developer')['Close_Price'].describe().index[1]
, df_graphics.groupby('Is_Developer')['Close_Price'].describe()['50%'].loc['Yes']

)

# Feed in the label for group2
#ax.bar_label(bar2, fmt= '%.0f')
ax.bar_label(bar2, fmt= '${:,.0f}')

# ax.bar(df_graphics['Is_Developer'], df_graphics['Close_Price'].mean())
# Include dollar signs and commas. 
ax.yaxis.set_major_formatter(mp.ticker.StrMethodFormatter("${x:,.0f}"))
ax.set_title('Median Developer vs. Non-Developer Sales- All Years')
ax.set_ylabel('Closing Price')
ax.set_ylim(1200000, 1400000)
ax.set_xticklabels(['Non-Developer', 'Developer'])
fig.show()
fig.savefig('Median_All_Years.pdf', format='pdf', bbox_inches='tight')

#####################
# Medians by Year 
################

# The below approach uses the setup here:

#  https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

# To pull the values from the DataFrame into a dictionary and then
# use the dictionary for plotting. 

# Create a DataFrame with the summary stats by year. 
df_graphics.groupby(['Is_Developer', 'Year'])['Close_Price'].describe()

df_graphics.groupby(['Is_Developer', 'Year'])['Close_Price'].describe()['50%']

# Note that for 2020 there were only two sales and both of these were non-developer sales. These may pose problems later. 

df_graphics_year= df_graphics.groupby(['Is_Developer', 'Year'])['Close_Price'].describe()
df_graphics_year

df_graphics_year.index[0][0]
df_graphics_year.index[1][0]
df_graphics_year.index[2][0]
df_graphics_year.index[3][0]
# below switches to yes. 
df_graphics_year.index[4][0]

df_graphics_year.index[1][1]
df_graphics_year.index[6]

# Return the MultiIndex
df_graphics_year.index[:][:]
len(df_graphics_year.index[:][:])

# both elements of the MultiIndex
df_graphics_year.index[:][:][0]
# first element of multiindex and first element of the tuple at that position
df_graphics_year.index[:][:][0][0]
# first element of multiindex and second element of the tuple at that position. 
df_graphics_year.index[:][:][0][1]


df_graphics_year.loc['No', 2020]['count']
# pull the count variable based on the MultiIndex
df_graphics_year.loc['No', 2020]['count']
df_graphics_year.loc['No', 2020]['50%']


dicter= {}
# create a list to contain the No means for each year. 
temp_list_no= []
# create a list to contain the Yes means for each year.
temp_list_yes = []
# since 2020 has no data for Yes sales, manually insert 0 
# as the first item of the list
temp_list_yes.append(0)
        
df_graphics_year.index[0][0]

for i in range(len(df_graphics_year.index[:][:])): 
    # No condition list append operation
    if df_graphics_year.index[i][0]== 'No':
        # set temp_year equal to the year element of the ith item of
        # the  tuple list
        temp_year= df_graphics_year.index[i][1]
        print(temp_year)
        # below manually feeds in No for the first element of the ith 
        # item. This is fine because of the logic condition
        temp_list_no.append(df_graphics_year.loc['No', temp_year]['50%'])
    # Yes condition list append operation
    if df_graphics_year.index[i][0]== 'Yes':
        # set temp_year equal to the year element of the ith item of
        # the  tuple list
        temp_year= df_graphics_year.index[i][1]
        print(temp_year)
        # below manually feeds in No for the first element of the ith 
        # item. This is fine because of the logic condition
        temp_list_yes.append(df_graphics_year.loc['Yes', temp_year]['50%'])


temp_list_no
temp_list_yes

# Create a dictionary with the No: (all values) and then Yes: (all values) and a separate list or tuple of years. 

no_tup= tuple(temp_list_no)
yes_tup= tuple(temp_list_yes)


no_tup
yes_tup

dicter['No']= no_tup
dicter['Yes']=yes_tup
dicter

year_list= ['2020', '2021', '2022', '2023']

x= np.arange(len(year_list))
width= 0.25
multiplier= 0 

# below shows dictionary structure. 
dicter.items()

fig, ax= plt.subplots()
for sale_type, closing_price in dicter.items():
    print(sale_type, closing_price)
    offset= width * multiplier
    rects= ax.bar(x+ offset, closing_price, width, label=sale_type)
    # increase the padding for 2022 Yes
    # format with dollar signs. 
    ax.bar_label(rects, fmt='${:,.0f}', padding=0)
    multiplier +=1

ax.yaxis.set_major_formatter(mp.ticker.StrMethodFormatter("${x:,.0f}"))
ax.set_title('Median Developer vs. Non-Developer Sales- By Year')
ax.set_ylabel('Closing Price')
ax.set_ylim(1200000, 1500000)
ax.set_xticks(x, year_list)
ax.legend(loc='upper left', labels= ['Non-Developer', 'Developer'])
fig.show()
fig.savefig('Median_All_Years_By_Year.pdf', format='pdf', bbox_inches='tight')

'''
################
# Works but need to change no and yes to non-developer and developer
###################
fig, ax= plt.subplots()
for sale_type, closing_price in dicter.items():
    print(sale_type, closing_price)
    offset= width * multiplier
    rects= ax.bar(x+ offset, closing_price, width, label=sale_type)
    # increase the padding for 2022 Yes
    # format with dollar signs. 
    ax.bar_label(rects, fmt='${:,.0f}', padding=0)
    multiplier +=1

ax.yaxis.set_major_formatter(mp.ticker.StrMethodFormatter("${x:,.0f}"))
ax.set_title('Median Developer vs. Non-Developer Sales- By Year')
ax.set_ylabel('Closing Price')
ax.set_ylim(1200000, 1500000)
ax.set_xticks(x, year_list)
ax.legend(loc='upper left')
fig.show()
'''

# https://stackoverflow.com/questions/70515542/adding-comma-to-bar-labels

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

# https://stackoverflow.com/questions/71221204/change-format-of-bar-label-to-percent

# https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.bar_label.html

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/barchart.html#sphx-glr-gallery-lines-bars-and-markers-barchart-py

# https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_label_demo.html

#####################
# Analysis Without 2020 and without the 2021 outlier. 
##################

df_nonoutlier=df[(df['Year'] != 2020) & (df['Close_Price'] != 2000000)]

# Mean for the three years. 
df_nonoutlier['Close_Price'].describe().round()['mean']


# Median for the three years 
df_nonoutlier['Close_Price'].describe().round()['50%']

# Mean for each year. 
df_nonoutlier.groupby('Year')['Close_Price'].describe().round()

# Median only for each year. 
df_nonoutlier.groupby('Year')['Close_Price'].describe().round()['50%']


# Create a graphics DataFrame

df_graphics_nonoutlier= df_nonoutlier[(df['Is_Developer'] != '?') & (df_nonoutlier['Is_Developer'].notnull())]

df_graphics_nonoutlier

df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe()

df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe().index[0]

df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe()['mean'].loc['No']


######################
# Medians All Years Without Outliers-- automated without scientific notation.
###########
fig, ax= plt.subplots()
# initialize the first bar of the bar chart below for group1
bar1= ax.bar(df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe().index[0]
, df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe()['50%'].loc['No']

)

#ax.bar_label(bar1, fmt= '%.0f')
ax.bar_label(bar1, fmt='${:,.0f}')

# initialize the second bar of the bar chart for group2
bar2= ax.bar(df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe().index[1]
, df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe()['50%'].loc['Yes']

)

# Feed in the label for group2
#ax.bar_label(bar2, fmt= '%.0f')
ax.bar_label(bar2, fmt= '${:,.0f}')

# ax.bar(df_graphics['Is_Developer'], df_graphics['Close_Price'].mean())
# Include dollar signs and commas. 
ax.yaxis.set_major_formatter(mp.ticker.StrMethodFormatter("${x:,.0f}"))
ax.set_title('Median Developer vs. Non-Developer Sales- Exc. 2020 & Outliers')
ax.set_xticklabels(['Non-Developer', 'Developer'])
ax.set_ylim(1200000, 1400000)
fig.show()
fig.savefig('Median_No_Outlier.pdf', format='pdf', bbox_inches='tight')

#####################
# Medians by Year Without Outliers
################


df_graphics_year_nonoutlier= df_graphics_nonoutlier.groupby(['Is_Developer', 'Year'])['Close_Price'].describe()
dicter_nonoutiler= {}
# create a list to contain the No means for each year. 
temp_list_no_nonoutlier= []
# create a list to contain the Yes means for each year.
temp_list_yes_nonoutlier = []

        
for i in range(len(df_graphics_year_nonoutlier.index[:][:])): 
    # No condition list append operation
    if df_graphics_year_nonoutlier.index[i][0]== 'No':
        # set temp_year equal to the year element of the ith item of
        # the  tuple list
        temp_year= df_graphics_year_nonoutlier.index[i][1]
        print(temp_year)
        # below manually feeds in No for the first element of the ith 
        # item. This is fine because of the logic condition
        temp_list_no_nonoutlier.append(df_graphics_year_nonoutlier.loc['No', temp_year]['50%'])
    # Yes condition list append operation
    if df_graphics_year_nonoutlier.index[i][0]== 'Yes':
        # set temp_year equal to the year element of the ith item of
        # the  tuple list
        temp_year= df_graphics_year_nonoutlier.index[i][1]
        print(temp_year)
        # below manually feeds in No for the first element of the ith 
        # item. This is fine because of the logic condition
        temp_list_yes_nonoutlier.append(df_graphics_year_nonoutlier.loc['Yes', temp_year]['50%'])


# Create a dictionary with the No: (all values) and then Yes: (all values) and a separate list or tuple of years. 

no_tup_nonoutlier= tuple(temp_list_no_nonoutlier)
yes_tup_nonoutlier= tuple(temp_list_yes_nonoutlier)

dicter_nonoutiler['No']= no_tup_nonoutlier
dicter_nonoutiler['Yes']=yes_tup_nonoutlier

year_list_nonoutlier= ['2021', '2022', '2023']

x_nonoutlier= np.arange(len(year_list_nonoutlier))
width= 0.25
multiplier= 0 

dicter_nonoutiler

# below shows dictionary structure. 
dicter_nonoutiler.items()

fig, ax= plt.subplots()
for sale_type, closing_price in dicter_nonoutiler.items():
    print(sale_type, closing_price)
    offset= width * multiplier
    rects= ax.bar(x_nonoutlier+ offset, closing_price, width, label=sale_type)
    # increase the padding for 2022 Yes
    # format with dollar signs. 
    ax.bar_label(rects, fmt='${:,.0f}', padding=0)
    multiplier +=1

ax.yaxis.set_major_formatter(mp.ticker.StrMethodFormatter("${x:,.0f}"))
ax.set_title('Median Developer vs. Non-Developer Sales- By Year Exc. 2020 & Outliers')
ax.set_ylabel('Closing Price')
ax.set_ylim(1200000, 1500000)
ax.set_xticks(x_nonoutlier, year_list_nonoutlier)
ax.legend(loc='upper left', labels= ['Non-Developer', 'Developer'])
fig.show()
fig.savefig("Median_No_Outlier_By_Year.pdf", format='pdf', bbox_inches='tight')

df_graphics.groupby('Is_Developer')['Close_Price'].describe()
df_graphics.groupby(['Is_Developer', 'Year'])['Close_Price'].describe()


df_graphics_nonoutlier.groupby('Is_Developer')['Close_Price'].describe()

df_graphics_nonoutlier.groupby(['Is_Developer', 'Year'])['Close_Price'].describe()

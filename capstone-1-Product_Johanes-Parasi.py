import pandas as pd
import glob
import numpy as np

#EXCTRACTION
#define file path
path = 'D:\data_sources\data_products'

#get csv file within path
getFile = glob.glob(path + '/*.csv')
listFile = []

#extract all csv file within path and make dataframe for each file and put it in list
for rec in getFile:
    df_temp = pd.read_csv(rec)
    listFile.append(df_temp)

#concat all dataframe within list
df = pd.concat(listFile)

#reset index to make sure that already ordered
df.reset_index(drop=True, inplace=True)

#drop unnecessary columm with no meaning that appear after reading from csv file
df.drop(columns={'Unnamed: 0'}, inplace=True)


# ================================================================================================================================================ #

#TRANSFORMATION
#convert name using str.title
df['name'] = df['name'].apply(lambda x: x.title())

#remove duplicate data by name
df.drop_duplicates(subset=['name'], keep='first', inplace=True)

#convert data into string first to standarize all values data type
df['discount_price'] = df['discount_price'].astype(str)
df['actual_price'] = df['actual_price'].astype(str)
df['no_of_ratings'] = df['no_of_ratings'].astype(str)
df['ratings'] = df['ratings'].astype(str)

#add Currency column which value extracted from discount_price column
df['currency'] = df['discount_price'].apply(lambda x: np.nan if x == 'nan' else x[0])

#cleansing data
df['discount_price'] = df['discount_price'].apply(lambda x: np.nan if x == 'nan' else x[1:].replace(',',''))
df['actual_price'] = df['actual_price'].apply(lambda x: np.nan if x == 'nan' else x[1:].replace(',',''))
df['no_of_ratings'] = df['no_of_ratings'].apply(lambda x: np.nan if x == 'nan' else x.replace(',',''))
df['ratings'] = df['ratings'].apply(lambda x: np.nan if x == 'nan' else np.nan if x[0].isalpha() else x[1:] if not x[0].isdigit() else x)

#convert data into numeric, so these columns can use for aggregation
df['discount_price'] = pd.to_numeric(df['discount_price'], errors='coerce')
df['actual_price'] = pd.to_numeric(df['actual_price'], errors='coerce')
df['no_of_ratings'] = pd.to_numeric(df['no_of_ratings'], errors='coerce')
df['ratings'] = pd.to_numeric(df['ratings'], errors='coerce')

#add discount percentage column 
df['discount_percentage'] = (((df['actual_price'] - df['discount_price']) * 100) / df['actual_price']).round(2)


# ================================================================================================================================================ #

#DEMOGRAPHY
print('1. Top 10 largest discount (in percentage) of subcategory')
print(60 * '=')
grp_by = df.groupby(['main_category','sub_category']).mean()
print(grp_by['discount_percentage'].nlargest(10))

print('')
print('2. How many product name in every sub_category')
print(60 * '=')
print(df['sub_category'].value_counts())

print('')
print("3. How many product name that doesn't has actual_price")
print(60 * '=')
print(len(df.loc[df['actual_price'].isnull()]))

print('')
print('4. Product name that has highest ratings')
print(60 * '=')
print(df.sort_values(by='ratings', ascending=False).head(1))

print('')
print('5. Lowest actual_price for all products name in every sub_category')
print(60 * '=')

grp_by2 = df.groupby('sub_category')
print(grp_by2['actual_price'].min())

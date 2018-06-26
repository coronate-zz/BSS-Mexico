
import pandas as pd
import numpy as np

df = pd.read_csv("2014.txt", sep = '|')
df = df.append(pd.read_csv("2015.txt", sep = '|'))
df = df.append(pd.read_csv("2016.txt", sep = '|'))
df = df.append(pd.read_csv("2017.txt", sep = '|'))

columns_dict = {
       'PERIOD':'date',
       'MARKET':'market',
       'UPC':'product_id',
       'DESCRIPTION': 'description',
       'BRAND': 'brand',
       'CATEGORY SUBGROUP': 'subcategory',
       'CB PRODUCT SEGMENT': 'segment',
       'MANUFACTURER':'manufacturer',
       'SUB BRAND':'sub_brand',
       '$ Vol':'vol',
       'Unit Vol':'unit_vol',
       'Avg Retail Unit Price': 'avg_reatail_unit_price',
       'AC Dist':'ac_dist',
       'Tl Dist Pts': 'tl_dist_pts'}
df = df.rename(columns= columns_dict)

string_colums =    ['market','description','brand','subcategory','segment','manufacturer']


for col in string_colums:
    df[col]    = df[col].str.lower()
    df[col] =  df[col].str.replace( " ", "_")
    df[col] =  df[col].str.replace( " ", "_")
    df[col] =  df[col].str.replace( ".", "_")
    df[col] =  df[col].str.replace( "-", "_")
    df[col] =  df[col].str.replace( "/", "_")
    df[col] =  df[col].str.replace( ",",  "_")
    df[col] =  df[col].str.replace( "`", "_")
    df[col] =  df[col].str.replace( ")", "_")
    df[col] =  df[col].str.replace( "(", "_")
    df[col] =  df[col].str.replace( "+", "_plus_")
    df[col] =  df[col].str.replace( "%", "pct")
    df[col] =  df[col].str.replace( "__", "_")
    df[col] =  df[col].str.replace( "__", "_")

df["year"] = df.date.str[5:7] + 2000
df["month"] = df.date.str[2:5]
df["day"] = df.date.str[0:2] 

df.to_csv("wholesome_strclean.csv")


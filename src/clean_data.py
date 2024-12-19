import os
from bs4 import BeautifulSoup
import numpy as np
import pandas as pd
import regex as re
import requests
import seaborn as sns
import matplotlib.pyplot as plt
import folium 
import plotly.express as px
from collections import defaultdict
from get_data import load_data
from utils import detect_outliers_iqr, get_fmr



def clean_data(df_combined, FMR_aggregated: pd.DataFrame) -> pd.DataFrame:

    """Clean the input data."""

    print(df_combined.isnull().sum())
    print(df_combined.shape)


    #Lets check column names and data types

    print(df_combined.columns) 
    print(df_combined.dtypes) 


    #Lets get rid of the following columns as we are not going to use them

    df_combined = df_combined.drop(columns=['zpid', 'Status Type', 'Time On Zillow', 'Zestimate' , 'Zestimate Price Per Sqft', 'Rent Zestimate', 
                                            'Broker Name','is zillow owned', 'Image URL', 'Detail URL', 'Search Page URL', 'Sold Date', 'Sold Price'])



    #Lets get an overview of numerical features

    df_combined.describe()


    # As the overview suggests that we are dealing with outliers such as 37000 sqft house, or 52 beds 33 bath house, we need to Identify Outliers using Statistical Methods


    """
    The IQR is calculated as the difference between the 75th percentile (Q3) and the 25th percentile (Q1).

    Lower Bound = Q1 - 1.5 * IQR
    Upper Bound = Q3 + 1.5 * IQR

    """


    numerical_columns = ['Price', 'Area', 'Price Per Sqft', 'Lot Area', 'Beds', 'Bathrooms']

    

    outliers = detect_outliers_iqr(df_combined, numerical_columns)

    # Print the number of outliers per column
    for col, data in outliers.items():
        print(f'Outliers in {col}: {data.shape[0]}')



    #Before handling outliers, visualize them to understand the extent of the problem and confirm if they are true anomalies or part of the valid data distribution.


    # Create boxplots for each numerical column
    plt.figure(figsize=(12, 8))
    for i, col in enumerate(numerical_columns, 1):
        plt.subplot(2, 3, i)
        sns.boxplot(x=df_combined[col])
        plt.title(f'Boxplot of {col}')
    plt.tight_layout()
    


    """
    Before dealing with null values lets apply couple of filters which will help tp deal with outliers as well.  The Section 8 investment program is for fuding low income tenants so we will be concentrating on 


    1. houses for sale only

    2.  price <= 200,000$
    3. city is one of: 

    Birmingham        
    Indianapolis      
    Memphis           
    Cleveland         
    Detroit 
    """

    # Filter for House for Sale Status Text

    df_combined = df_combined[df_combined['Status Text'] == 'House for sale']

    cities = ['Birmingham', 'Indianapolis', 'Memphis', 'Cleveland', 'Detroit']

    # Filter rows where 'city' is one of the specified cities
    df_combined = df_combined[df_combined['City'].isin(cities)]

    #Filter for <= 200,000 price
    df_combined = df_combined[df_combined['Price'] <= 200000]

    df_combined.head()


    # For categorical columns (like status text, city), let's check the frequency distribution:

    print(df_combined['Status Text'].value_counts())  
    print(df_combined['City'].value_counts())


    #After applying desired filters, it is clear that although city Indianapolis is a investor friendly city, it is not recommended for section 8 investment. We will concentrate on other 4 cities.



    #Check for Missing Data
    print(df_combined.isnull().sum())


    #As The Area is one of the most important features for our analysis, let's use imputation to fill missing values, using the median of the Area column. 
    # Median is often preferred over the mean because it is less sensitive to outliers. Let's do the same for Lot Area

    df_combined['Area'] = df_combined['Area'].fillna(df_combined['Area'].median())
    df_combined['Lot Area'] = df_combined['Lot Area'].fillna(df_combined['Lot Area'].median())


    #Price Per Sqft is Price / Area
    df_combined['Price Per Sqft'] = df_combined['Price Per Sqft'].fillna(df_combined['Price'] / df_combined['Area'])

    # Drop rows where 'Beds', 'Bathrooms', or 'Latitude' are missing
    df_combined = df_combined.dropna(subset=['Beds', 'Bathrooms', 'Latitude'])


    print(df_combined.isnull().sum())
    print(df_combined.shape)


    """
    now let's get rid of column Status Text as we already filtered out houses for sale. For column Lot Area Unit, 
    let's filter out all the ones that are acres, convert it to sqft and get rid of Lot Area Unit as well
    """

    df_combined.loc[df_combined['Lot Area Unit'] == 'acres', 'Lot Area'] *= 43560
    df_combined = df_combined.drop(columns=['Lot Area Unit'])


    df_combined = df_combined.drop(columns=['Status Text']).reset_index(drop = True)



    #Now Lets add new row "FMR" to the dataframe df_combined, which whill pull the value from FRM-aggeggated dataframe based on the bed count. 
    # But Before that we need to filter for houses that are <= 4 bedrooms

    df_combined = df_combined[df_combined['Beds'] <= 4]


    # Make sure Zipcode in df_combined and Zip in FMR_aggregated are both strings for compatibility
    df_combined['Zipcode'] = df_combined['Zipcode'].astype(str)
    FMR_aggregated['Zip'] = FMR_aggregated['Zip'].astype(str)



    # Apply the function to each row in df_combined to get the fair market rent
    df_combined['FMR'] = df_combined.apply(get_fmr, axis=1, fmr_df=FMR_aggregated)

    return df_combined
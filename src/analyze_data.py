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
from utils import get_utilities


def analyze_data(df_combined: pd.DataFrame) -> pd.DataFrame:


    """
    Now that we have clear picture of what our data represents, lets integrate investment property cashflow calculator, to be able to calculate monthly cashflow for each house.

    Cash flow = Rental Income - (Mortgage Payment + Operating Expenses)

    To calculate the mortgage payment, we will use the following formula

    𝑀 = P x (r(1+r)**n)/((1+r)**n) -1
    
    Where:


    M = Monthly mortgage payment 

    P = Loan principal (amount borrowed) (assume 90 % of total price)

    r = Monthly interest rate (annual rate divided by 12) (6.7/12 = 0.56 %  monthly for 30 year fixed rate) 

    n = Number of payments (loan term in years × 12 months) (12 x 30 = 360)
    """

    df_combined['monthly_mortgage_payment'] = df_combined['Price'] * 0.9 * ( 0.0056 * (1 + 0.0056)**360 ) / ( (1 + 0.0056)**360 -1 )


    df_combined.head()


    """
    Now that we have a mortgage payment we also need operating expenses to calculate monthly cash flow.
    To calculate monthly operating expenses we will use the following market average numbers:

    Homeowners Insurance: 0.5 % of house price annual -> 0.042 % monthly of house price
    Property Management Fees: 10 % of monthly rent
    Maintenance/Repairs: Estimate for monthly upkeep.  A common rule of thumb is to budget $1 per square foot per year, which can be divided by 12 for monthly expenses.
    Utilities: for moderate climates (Memphis, Indianapolis, Birmingham) we would use approximate 325 dollar for average household, for non-moderate climates (Detroit and Cleveland) we will use 450 dollar for monthly utilities. 
    HOA Fees: for single family homes without extensive amenities we will calculate 75$ monthly

    """

    df_combined['Maintenance'] = (df_combined['Area'] / 12 )
    df_combined['HOA_fees'] = 75
    df_combined['Monthly_Insurance'] = df_combined['Price'] * ( 0.005 / 12 )
    df_combined['Monthly_property_mgmt'] = df_combined['FMR'] * 0.1


    data = {
        'City': ['Memphis', 'Indianapolis', 'Birmingham', 'Detroit', 'Cleveland'],
        'Other_Column': [1, 2, 3, 4, 5]
    }
    # Define the custom function to apply to each row
    

    # Apply the function to create the new column
    df_combined['Monthly_Utilities'] = df_combined['City'].apply(get_utilities)


    """
    Once we have all the required info let's calculate monthly cashflow after all th expenses which is:

    Rental Income - (Mortgage payment + Operating Exepnses)
    """

    df_combined['Monthly_cashflow'] = df_combined['FMR'] - (
        df_combined['monthly_mortgage_payment'] 
        + df_combined['Maintenance'] 
        + df_combined['HOA_fees'] 
        + df_combined['Monthly_Insurance'] 
        + df_combined['Monthly_property_mgmt'] 
        + df_combined['Monthly_Utilities'] 
    )


    # Filter out properties with monthly cashflow > 500 to exclude demoli9shed or burned houses

    print(f"Properties with cashflow > $500: {df_combined[df_combined['Monthly_cashflow'] > 500].value_counts().sum()}")
    print(f"Total properties: {len(df_combined)}")

    # Remove properties with price less than $50,000
    df_combined = df_combined[df_combined['Price'] >= 50000]

    # List properties suitable for passive income seekers
    list_for_passive_income_seeker = df_combined[df_combined['Monthly_cashflow'] > 500].reset_index(drop=True)

    # Save the filtered DataFrame to a CSV file in the current directory
    RESULTS_DIR = os.path.join(os.getcwd(), "results")



    # Save the filtered DataFrame to a CSV file in the 'results' folder
    output_file = os.path.join(RESULTS_DIR, "passive_income_properties.csv")
    list_for_passive_income_seeker.to_csv(output_file, index=False)

    print(f"Filtered properties saved to: {os.path.abspath(output_file)}")

    return list_for_passive_income_seeker
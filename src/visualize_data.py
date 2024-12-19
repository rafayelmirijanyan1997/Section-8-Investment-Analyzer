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
from utils import ensure_directory_exists, save_plot









def visualize_data(df_combined: pd.DataFrame) -> pd.DataFrame:
    # Ensure the results folder exists

    RESULTS_DIR = "results"
    ensure_directory_exists(RESULTS_DIR)


    # Histogram for Price distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(df_combined['Price'], kde=True, color='skyblue')
    plt.title('Distribution of Property Prices')
    plt.xlabel('Price')
    plt.ylabel('Frequency')
    
    save_plot()  # Save the plot


    # Scatter plot for Price vs. Area
    plt.figure(figsize=(10, 6))
    sns.scatterplot(x='Area', y='Price', data=df_combined, color='purple')
    sns.regplot(x='Area', y='Price', data=df_combined, scatter=False, color='red')
    plt.title('Price vs. Area')
    plt.xlabel('Area (sqft)')
    plt.ylabel('Price ($)')
    
    save_plot()  # Save the plot


    # Histogram for Price per Sqft
    plt.figure(figsize=(10, 6))
    sns.histplot(df_combined['Price Per Sqft'], kde=True, color='orange')
    plt.title('Distribution of Price Per Sqft')
    plt.xlabel('Price per Sqft')
    plt.ylabel('Frequency')
    
    save_plot()  # Save the plot



    # Violin plot for Price vs. Beds
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Beds', y='Price', data=df_combined, inner='quart')
    plt.title('Price Distribution for Number of Bedrooms')
    plt.xlabel('Number of Bedrooms')
    plt.ylabel('Price ($)')

    save_plot()  # Save the plot
    

    #3 and 4 bedroom houses have similar price distribution. 

    # Interactive scatter plot of Price vs Area
    fig = px.scatter(df_combined, 
                    x="Area", 
                    y="Price", 
                    color="Price Per Sqft", 
                    hover_data=["Address", "Beds", "Bathrooms", "FMR"], 
                    title="Price vs Area (Price Per Sqft)",
                    labels={"Price": "Price (USD)", "Area": "Area (sq ft)", "Price Per Sqft": "Price per Sqft"})

# Customize the traces
    fig.update_traces(marker=dict(size=12, opacity=0.8, line=dict(width=2, color='DarkSlateGrey')))

# Define the output path for the HTML file
    map_file_path = os.path.join(RESULTS_DIR, "Price_vs_Area.html")

# Save the figure as an interactive HTML file
    fig.write_html(map_file_path)



    fig = px.box(df_combined, 
                x="City", 
                y="Price", 
                color="City", 
                title="Price Distribution by City",
                labels={"Price": "Price (USD)", "City": "City"})
    
    map_file_path = os.path.join(RESULTS_DIR, "Price_Distribution_by_City.html")
    fig.write_html(map_file_path)
    


    #Indianapois had only 2 houses after thorough filtering. The boxplot above states that Memphis has more expensive houses among other cities. 

    # Create a map centered at an average location
    m = folium.Map(location=[df_combined['Latitude'].mean(), df_combined['Longitude'].mean()], zoom_start=6)

    # Add markers for each property in the dataset
    for idx, row in df_combined.iterrows():
        folium.Marker([row['Latitude'], row['Longitude']], 
                    popup=f"Address: {row['Address']}<br>Price: ${row['Price']}<br>FMR: {row['FMR']}<br>Bedrooms: {row['Beds']}<br>Bathrooms: {row['Bathrooms']}").add_to(m)

    # Save the map as an HTML file
    map_file_path = os.path.join(RESULTS_DIR, "real_estate_map.html")
    m.save(map_file_path)


    return df_combined

    

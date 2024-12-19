import os
import re
import pandas as pd
import matplotlib.pyplot as plt
import uuid




def ensure_directory_exists(dir_path: str):
    """Ensure the given directory exists. If not, create it."""
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
        print(f"Directory created: {dir_path}")
    else:
        print(f"Directory already exists: {dir_path}")

def extract_details(details):
        # Regular expressions for extracting beds, baths, and sqft
        beds = re.search(r'(\d+)\s*bds', details)
        baths = re.search(r'(\d+)\s*ba', details)
        sqft = re.search(r'(\d+)\s*sqft', details)
        
        
        return (
            int(beds.group(1)) if beds else None,
            int(baths.group(1)) if baths else None,
            int(sqft.group(1)) if sqft else None
        )

def detect_outliers_iqr(df, columns):
        outliers = {}
        for col in columns:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            # Identify the outliers
            outliers[col] = df[(df[col] < lower_bound) | (df[col] > upper_bound)]
        return outliers






    # Create a function to get the fair market rent based on Zip and Beds
def get_fmr(row, fmr_df):
    zip_code = row['Zipcode']
    num_beds = int(row['Beds'])  # Convert Beds to integer
        
        # Map the number of Beds to the corresponding column name in FMR_aggregated
    if num_beds == 0:
        column = 'Efficiency'
    elif num_beds == 1:
        column = 'One-Bedroom'
    elif num_beds == 2:
        column = 'Two-Bedroom'
    elif num_beds == 3:
        column = 'Three-Bedroom'
    elif num_beds == 4:
        column = 'Four-Bedroom'
    else:
        return pd.NA  # Return NaN if the number of beds is unexpected
        
        # Find the matching row in FMR_aggregated by Zip code
    fmr_row = fmr_df[fmr_df['Zip'] == zip_code]
        
    if not fmr_row.empty:
        fmr_value = fmr_row[column].values[0]  # Get the FMR value for the matching zip code
            
            # Remove the dollar sign, commas, and convert to numeric
        if isinstance(fmr_value, str):
                # Strip the '$' sign and commas, then convert to float
            fmr_value = fmr_value.replace('$', '').replace(',', '')
            try:
                fmr_value = float(fmr_value)  # Convert the cleaned value to a float
            except ValueError:
                return pd.NA  # Return NaN if conversion fails
        return fmr_value
    else:
        return pd.NA 
        






def ensure_directory_exists(directory: str):
    """
    Ensure the specified directory exists; create it if it doesn't.
    
    Parameters:
    - directory: Path to the directory to ensure its existence
    """
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory)
    else:
        print(f"Directory already exists: {directory}")


def save_plot():
    """
    Save the current Matplotlib figure to the results folder with a unique name.

    Assumes the figure to be saved is the current figure (plt.gcf).
    """
    # Define the results folder
    RESULTS_DIR = "results"

    # Ensure the results folder exists
    os.makedirs(RESULTS_DIR, exist_ok=True)

    # Generate a unique name for the file
    unique_name = f"plot_{uuid.uuid4().hex}.png"  # e.g., plot_5f4dcc3b5aa765d61d8327deb882cf99.png
    output_path = os.path.join(RESULTS_DIR, unique_name)

    # Save the current figure
    plt.savefig(output_path, bbox_inches="tight")  # Use plt.savefig() to save the current active figure
    plt.close()  # Close the figure to free memory

    print(f"Plot saved as: {output_path}")

def get_utilities(city):
        if city in ['Memphis', 'Indianapolis', 'Birmingham']:
            return 325
        elif city in ['Detroit', 'Cleveland']:
            return 450
        else:
            return None  # Default value if city doesn't match any condition
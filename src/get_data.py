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
from utils import extract_details


def load_data() -> pd.DataFrame:
    
    
    

    #Scraping real estate data from zillow.com 



    pd.set_option('display.max_rows', None)
    pd.set_option('mode.chained_assignment',None)
    cookies = {
        'zguid': '24|%246c929c9f-fdb4-4976-bd83-3f654077f94f',
        '_ga': 'GA1.2.1016522082.1725402419',
        'zjs_anonymous_id': '%226c929c9f-fdb4-4976-bd83-3f654077f94f%22',
        'zjs_user_id': 'null',
        'zg_anonymous_id': '%228c212732-7438-4b2c-91ff-49444d139c64%22',
        '_gcl_au': '1.1.1947786712.1725402420',
        '_fbp': 'fb.1.1725402420228.407644125101747920',
        '_scid': 'fff6569e-0f7d-4c5b-88d9-067389496805',
        '_tt_enable_cookie': '1',
        '_pin_unauth': 'dWlkPU4yRXpPR0psWkdJdFltSmtZaTAwWkRrNExXSTJaRFF0WXpkbE16UmxOVEppWmpJNQ',
        'optimizelyEndUserId': 'oeu1725431435141r0.05720984425140996',
        'zgcus_aeut': 'AEUUT_31533399-6a87-11ef-a45d-d68e14d18a8a',
        'zgcus_aeuut': 'AEUUT_31533399-6a87-11ef-a45d-d68e14d18a8a',
        '_pxvid': '3157d807-6a87-11ef-8922-f0ea6b9b8d2c',
        '_cs_c': '0',
        '_cs_id': '8aa47304-2e7f-ac00-d622-1d5598bfe8f1.1725431435.1.1725431435.1725431435.1.1759595435525.1',
        '_lr_env_src_ats': 'false',
        'zgsession': '1|75555875-93a7-4858-9bd1-9cd6c12324f3',
        'pxcts': '4e84ad2d-97d8-11ef-8c4b-5cf56366f306',
        'DoubleClickSession': 'true',
        '_ScCbts': '%5B%22157%3Bchrome.2%3A2%3A5%22%2C%22289%3Bchrome.2%3A2%3A5%22%2C%22565%3Bchrome.2%3A2%3A5%22%5D',
        '_gid': 'GA1.2.1449310429.1731728211',
        '_ttp': 'o-i_aq8Yqjdi1za8GWFgPGq6Spi.tt.1',
        '_clck': '1av61rm%7C2%7Cfqx%7C0%7C1707',
        '_sctr': '1%7C1731657600000',
        '_lr_sampling_rate': '100',
        'JSESSIONID': 'AC47EACB26D5FD32086CCA06AED14F08',
        'tfpsi': 'ff720544-d09f-43a8-83bf-0bed0df46902',
        '_lr_retry_request': 'true',
        '_rdt_uuid': '1725402420199.39d57d7d-fac5-4bf9-9573-8cbd3cb2c7d2',
        '_scid_r': 'iHD_9laeD31SWxzZBnOJSWgFu39aMiVPwWuWlg',
        '__gads': 'ID=5ff3db212e30ecd9:T=1725402420:RT=1731794796:S=ALNI_MZr7Bt3q7lI5vvJO5c9suPnOdbdCw',
        '__gpi': 'UID=00000ee87f78b7b6:T=1725402420:RT=1731794796:S=ALNI_MZmZmdH2yU8gLLs26OyoJxh2Fmj_w',
        '__eoi': 'ID=5e56000c6ef86f48:T=1725402420:RT=1731794796:S=AA-Afja3ytIRxBcSj1zv5aTHAHGc',
        '_dd_s': 'rum=2&id=5218dc5c-32b3-47b4-ae40-f2aca2e8f65d&created=1731793530437&expire=1731795707334',
        'search': '6|1734386808624%7Crect%3D34.46381577596457%2C-117.7525528125%2C33.57600326379208%2C-119.0709121875%26rid%3D12447%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0912447%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09',
        '_uetsid': '04f1fdd0a3cc11efa4efe7885d6555b9',
        '_uetvid': 'a31276b06a4311ef8cf68fce98167c21',
        '_derived_epik': 'dj0yJnU9ZHhxTGRoQ0lOR3lQUXF3bExyQVhCeExoeEJhaGlUOHEmbj16NUJENlRLWFdCb3dXY3p4aERYTzFnJm09MSZ0PUFBQUFBR2M1RjNnJnJtPTEmcnQ9QUFBQUFHYzVGM2cmc3A9Mg',
        '_px3': '86d0ce4a48392a41a89248456b48eab1fcaa19c35dbb8d0eb4c937157111bbae:ZFFBEPN5O44+n6c5uZ8AQ1sXu080kn6EsYRtVXEK1JP544F6lLITlB1r5v568naLHtDoODzLYo5aAaIr9O15lg==:1000:HUB+UotiXWzgCaxgLal5kjP0h4S9addln/Pm2MLgXWTNU2XfQoh6oRUQvrQrHH+UCBsoMxAJYbv77Y8D2NOm4ZB+zi2YgksAHd9JAYzObovxYz6Obf2Zd10IWDK2Fy4HCWvSSpVo+dKnwNK++vvf9PV4H4iums7U26QbG1jwI0vb7E/BGzezMMFoFyPtqbgzyYKRxPY2IBoyF86fVemZFO7sXCmQ+nvE6rEBQkj+nGA=',
        '_clsk': 'w34jc8%7C1731794809133%7C30%7C0%7Cq.clarity.ms%2Fcollect',
        '_clsk': 'w34jc8%7C1731794809133%7C30%7C0%7Cq.clarity.ms%2Fcollect',
        '_clsk': 'w34jc8%7C1731794809133%7C30%7C0%7Cq.clarity.ms%2Fcollect',
        'AWSALB': 'zIn6eS+6/+Rvldwe/YGsP9KwLLVieIkpqXIIUhY4VbzO3I5a/BGu107c4T+TVqclgOOO5PKO5NOLs/7KX+z4WMCDwUl7zq4pysfErnFYFvqSdCw4eXdViW8rg4Z7',
        'AWSALBCORS': 'zIn6eS+6/+Rvldwe/YGsP9KwLLVieIkpqXIIUhY4VbzO3I5a/BGu107c4T+TVqclgOOO5PKO5NOLs/7KX+z4WMCDwUl7zq4pysfErnFYFvqSdCw4eXdViW8rg4Z7',
    }

    headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        # 'cookie': 'zguid=24|%246c929c9f-fdb4-4976-bd83-3f654077f94f; _ga=GA1.2.1016522082.1725402419; zjs_anonymous_id=%226c929c9f-fdb4-4976-bd83-3f654077f94f%22; zjs_user_id=null; zg_anonymous_id=%228c212732-7438-4b2c-91ff-49444d139c64%22; _gcl_au=1.1.1947786712.1725402420; _fbp=fb.1.1725402420228.407644125101747920; _scid=fff6569e-0f7d-4c5b-88d9-067389496805; _tt_enable_cookie=1; _pin_unauth=dWlkPU4yRXpPR0psWkdJdFltSmtZaTAwWkRrNExXSTJaRFF0WXpkbE16UmxOVEppWmpJNQ; optimizelyEndUserId=oeu1725431435141r0.05720984425140996; zgcus_aeut=AEUUT_31533399-6a87-11ef-a45d-d68e14d18a8a; zgcus_aeuut=AEUUT_31533399-6a87-11ef-a45d-d68e14d18a8a; _pxvid=3157d807-6a87-11ef-8922-f0ea6b9b8d2c; _cs_c=0; _cs_id=8aa47304-2e7f-ac00-d622-1d5598bfe8f1.1725431435.1.1725431435.1725431435.1.1759595435525.1; _lr_env_src_ats=false; zgsession=1|75555875-93a7-4858-9bd1-9cd6c12324f3; pxcts=4e84ad2d-97d8-11ef-8c4b-5cf56366f306; DoubleClickSession=true; _ScCbts=%5B%22157%3Bchrome.2%3A2%3A5%22%2C%22289%3Bchrome.2%3A2%3A5%22%2C%22565%3Bchrome.2%3A2%3A5%22%5D; _gid=GA1.2.1449310429.1731728211; _ttp=o-i_aq8Yqjdi1za8GWFgPGq6Spi.tt.1; _clck=1av61rm%7C2%7Cfqx%7C0%7C1707; _sctr=1%7C1731657600000; _lr_sampling_rate=100; JSESSIONID=AC47EACB26D5FD32086CCA06AED14F08; tfpsi=ff720544-d09f-43a8-83bf-0bed0df46902; _lr_retry_request=true; _rdt_uuid=1725402420199.39d57d7d-fac5-4bf9-9573-8cbd3cb2c7d2; _scid_r=iHD_9laeD31SWxzZBnOJSWgFu39aMiVPwWuWlg; __gads=ID=5ff3db212e30ecd9:T=1725402420:RT=1731794796:S=ALNI_MZr7Bt3q7lI5vvJO5c9suPnOdbdCw; __gpi=UID=00000ee87f78b7b6:T=1725402420:RT=1731794796:S=ALNI_MZmZmdH2yU8gLLs26OyoJxh2Fmj_w; __eoi=ID=5e56000c6ef86f48:T=1725402420:RT=1731794796:S=AA-Afja3ytIRxBcSj1zv5aTHAHGc; _dd_s=rum=2&id=5218dc5c-32b3-47b4-ae40-f2aca2e8f65d&created=1731793530437&expire=1731795707334; search=6|1734386808624%7Crect%3D34.46381577596457%2C-117.7525528125%2C33.57600326379208%2C-119.0709121875%26rid%3D12447%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26listPriceActive%3D1%26fs%3D1%26fr%3D0%26mmm%3D0%26rs%3D0%26singlestory%3D0%26housing-connector%3D0%26parking-spots%3Dnull-%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%26showcase%3D0%26featuredMultiFamilyBuilding%3D0%26onlyRentalStudentHousingType%3D0%26onlyRentalIncomeRestrictedHousingType%3D0%26onlyRentalMilitaryHousingType%3D0%26onlyRentalDisabledHousingType%3D0%26onlyRentalSeniorHousingType%3D0%26commuteMode%3Ddriving%26commuteTimeOfDay%3Dnow%09%0912447%09%7B%22isList%22%3Atrue%2C%22isMap%22%3Atrue%7D%09%09%09%09%09; _uetsid=04f1fdd0a3cc11efa4efe7885d6555b9; _uetvid=a31276b06a4311ef8cf68fce98167c21; _derived_epik=dj0yJnU9ZHhxTGRoQ0lOR3lQUXF3bExyQVhCeExoeEJhaGlUOHEmbj16NUJENlRLWFdCb3dXY3p4aERYTzFnJm09MSZ0PUFBQUFBR2M1RjNnJnJtPTEmcnQ9QUFBQUFHYzVGM2cmc3A9Mg; _px3=86d0ce4a48392a41a89248456b48eab1fcaa19c35dbb8d0eb4c937157111bbae:ZFFBEPN5O44+n6c5uZ8AQ1sXu080kn6EsYRtVXEK1JP544F6lLITlB1r5v568naLHtDoODzLYo5aAaIr9O15lg==:1000:HUB+UotiXWzgCaxgLal5kjP0h4S9addln/Pm2MLgXWTNU2XfQoh6oRUQvrQrHH+UCBsoMxAJYbv77Y8D2NOm4ZB+zi2YgksAHd9JAYzObovxYz6Obf2Zd10IWDK2Fy4HCWvSSpVo+dKnwNK++vvf9PV4H4iums7U26QbG1jwI0vb7E/BGzezMMFoFyPtqbgzyYKRxPY2IBoyF86fVemZFO7sXCmQ+nvE6rEBQkj+nGA=; _clsk=w34jc8%7C1731794809133%7C30%7C0%7Cq.clarity.ms%2Fcollect; _clsk=w34jc8%7C1731794809133%7C30%7C0%7Cq.clarity.ms%2Fcollect; _clsk=w34jc8%7C1731794809133%7C30%7C0%7Cq.clarity.ms%2Fcollect; AWSALB=zIn6eS+6/+Rvldwe/YGsP9KwLLVieIkpqXIIUhY4VbzO3I5a/BGu107c4T+TVqclgOOO5PKO5NOLs/7KX+z4WMCDwUl7zq4pysfErnFYFvqSdCw4eXdViW8rg4Z7; AWSALBCORS=zIn6eS+6/+Rvldwe/YGsP9KwLLVieIkpqXIIUhY4VbzO3I5a/BGu107c4T+TVqclgOOO5PKO5NOLs/7KX+z4WMCDwUl7zq4pysfErnFYFvqSdCw4eXdViW8rg4Z7',
        'origin': 'https://www.zillow.com',
        'priority': 'u=1, i',
        'referer': 'https://www.zillow.com/homes/for_sale/',
        'sec-ch-ua': '"Chromium";v="130", "Google Chrome";v="130", "Not?A_Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
    }

    json_data = {
        'searchQueryState': {
            'pagination': {},
            'isMapVisible': False,
            'mapBounds': {
                'west': -119.0709121875,
                'east': -117.7525528125,
                'south': 33.57600326379208,
                'north': 34.46381577596457,
            },
            'regionSelection': [
                {
                    'regionId': 12447,
                    'regionType': 6,
                },
            ],
            'filterState': {
                'sortSelection': {
                    'value': 'globalrelevanceex',
                },
            },
            'isListVisible': True,
        },
        'wants': {
            'cat1': [
                'listResults',
            ],
            'cat2': [
                'total',
            ],
        },
        'requestId': 3,
        'isDebugRequest': False,
    }

    response = requests.put('https://www.zillow.com/async-create-search-page-state', cookies=cookies, headers=headers, json=json_data)




    #Let's test to scrape Los Angeles listings 


    with requests.session() as s:
        city = 'los-angeles/'
        page = 1
        end_page = 5
        url = ''
        url_list = []
        
        while page <= end_page:
            url = 'https://www.zillow.com/homes/for_sale/' +city+ f'{page}_p/'
            url_list.append(url)
            page += 1
        
        request = ''
        request_list = []
        
        for url in url_list:
            request = s.get(url, headers=headers)
            request_list.append(request)
        
    soup = ''
    soup_list = []

    for request in request_list:
        soup = BeautifulSoup(request.content, 'html.parser')
        soup_list.append(soup)



    # Next, let's extract info for address, price, and details


    df_list = []
    for soup in soup_list:
        df = pd.DataFrame()
        for i in soup:
            
            address_tags = soup.find_all('address', {"data-test": "property-card-addr"})
            address = [tag.text.strip() for tag in address_tags]


            price_tags = soup.find_all('span', {"data-test": "property-card-price"})

            prices = [tag.text.strip() for tag in price_tags]

            

            details_tags = soup.find_all('div', class_ =  'StyledPropertyCardDataArea-c11n-8-107-0__sc-10i1r6-0 eLqtVY')

            details = [tag.text.strip() for tag in details_tags]


    # Extract and print the href attribute of each matched link        
            df['prices'] = prices
            df['address'] = address
            df['details'] = details
            
        df_list.append(df)


    final_df = pd.DataFrame()

    # Iterate and concatenate
    for df in df_list:
        final_df = pd.concat([final_df, df], ignore_index=True)


    #from details column lets separate Zip Code as we will need that data later

    final_df['zip_code'] = final_df['address'].str.extract(r'(\d{5})')



    #Besides Zip code, we will also need number of beds, baths and square foot, so lets get that data from details column with the help of regular expressions. 
    # Extract_details function will extract needed info.  



    final_df[['beds', 'baths', 'sqft']] = final_df['details'].apply(extract_details).apply(pd.Series)


    """


    For bigger amount of data, zillow blocks it for webscrapping, Instead of rotating IPs or using APIs, lets continue getting data from "zillow scraper" extension (https://zillow.scraper.plus/). 
    Let's concentrate on 5 best cities at this point, which are investor friendly. Then we get best of the best investment options within those 5 states. 

    data is exported and stored as {city_name}.csv and is attached to this project
    Before running next cell make sure you have dowloaded 5 csv files named {city_name}.csv.


    df_cleveland = pd.read_csv('cleveland.csv')
    df_detroit = pd.read_csv('detroit.csv')
    df_memphis = pd.read_csv('memphis.csv')
    df_indianapolis = pd.read_csv('indianapolis.csv')
    df_birmingham = pd.read_csv('birmingham.csv')
    """

    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # List of CSV filenames
    csv_files = ['cleveland.csv', 'detroit.csv', 'memphis.csv', 'indianapolis.csv', 'birmingham.csv']

    # Dictionary to store DataFrames
    dataframes = {}

    # Load each CSV into a DataFrame
    for file_name in csv_files:
        file_path = os.path.join(script_dir, file_name)  # Construct the absolute path
        try:
            dataframes[file_name.split('.')[0]] = pd.read_csv(file_path)  # Key is the file name without extension
            
        except FileNotFoundError:
            print(f"Error: {file_name} not found at {file_path}.")
        except Exception as e:
            print(f"Error loading {file_name}: {e}")

    # Access individual DataFrames by their names
    df_cleveland = dataframes.get('cleveland')
    df_detroit = dataframes.get('detroit')
    df_memphis = dataframes.get('memphis')
    df_indianapolis = dataframes.get('indianapolis')
    df_birmingham = dataframes.get('birmingham')


    df_combined = pd.concat([df_cleveland, df_detroit, df_memphis, df_indianapolis, df_birmingham], ignore_index=True)

    print(df_combined.head())

    
    
    #Now lets scrape data about Fair Market Rents for 2025 from huduser.gov website for 5 cities in our dataframe to understand how much US government pays for a specific zipz code and number of bedrooms

    # List of URLs for different cities
    urls = [
        ('Cleveland', 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2025_code/2025summary.odn?cbsasub=METRO17460M17460&year=2025&fmrtype=Final'),
        ('Birmingham', 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2025_code/2025summary.odn?cbsasub=METRO13820M13820&year=2025&fmrtype=Final'),
        ('Detroit', 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2025_code/2025summary.odn?cbsasub=METRO19820M19820&year=2025&fmrtype=Final'),
        ('Memphis', 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2025_code/2025summary.odn?cbsasub=METRO32820M32820&year=2025&fmrtype=Final'),
        ('Indianapolis', 'https://www.huduser.gov/portal/datasets/fmr/fmrs/FY2025_code/2025summary.odn?cbsasub=METRO26900M26900&year=2025&fmrtype=Final')
    ]

    # Initialize a list to hold all the DataFrames
    all_fmr_data = []

    # Iterate over each city URL and scrape the data
    for city_name, url in urls:
        with requests.Session() as s:
            headers = {"User-Agent": "Mozilla/5.0"}  # Add headers to mimic a real browser
            request = s.get(url, headers=headers)
            soup = BeautifulSoup(request.content, 'html.parser')

            # Find the table with the class "big_table"
            fmr_table = soup.find("table", {"class": "big_table"})
            rows = fmr_table.find_all("tr")

            # Extract column headers (first row)
            columns = [th.text.strip() for th in rows[1].find_all("th")]
            

            # Create a dictionary mapping column indices to category names
            columns_indices_to_categories = {index: category for index, category in enumerate(columns)}
            
            # Extract the ZIP code and data from the table rows
            zips = []
            fmr_data = defaultdict(list)

            for row in rows[2:]:
                zip_code = row.find("th").text.strip()  # Extract ZIP code
                zips.append(zip_code)

                # Extract data for each column
                for index, td in enumerate(row.find_all("td")):
                    size = columns_indices_to_categories[index+1]
                    fmr_data[size].append(td.text.strip())

            # Create a DataFrame from the extracted data
            fmr_df = pd.DataFrame({"Zip": zips, **fmr_data})

            

            # Append this city's DataFrame to the list
            all_fmr_data.append(fmr_df)

    # Combine all city DataFrames into a single DataFrame
    FMR_aggregated = pd.concat(all_fmr_data, ignore_index=True)

    # Display the first few rows of the combined DataFrame
    print(FMR_aggregated.head())

    return df_combined, FMR_aggregated



import os
import requests
import pandas as pd
from bs4 import BeautifulSoup

def data_wrangler():
   
    # STEP 1
    # Use the following Wikipedia page and get the data from the “European Union Road Safety Facts and Figures” table:
    # https://en.wikipedia.org/wiki/Road_safety_in_Europe

    # Make a request to the wikipedia url and store the html response in a variable
    
    # wikipedia url
    wiki_url="https://en.wikipedia.org/wiki/Road_safety_in_Europe"
   
    # get the table class name by inspecting the table on wikipedia webpage 
    table_class='wikitable sortable'

    # Check status code to be sure url is accessible, 200 means it's ok
    response = requests.get(wiki_url)
    print("Status Code", response.status_code)

    # read the html into a list of dataframe objects and get the particular class i.e the table class 
    soup = BeautifulSoup(response.text, 'html.parser')
    result = soup.find('table', {'class': table_class})

    # read the html into a list of dataframe objects
    df = pd.read_html(str(result))


    # convert the list into a dataframe
    df = pd.DataFrame(df[0])

    # STEP 2
    # clean dataset (i.e drop unwanted columns & rename columns)
    # Resulting CSV file should only include the following columns: Country, Year, Area, Population, GDP per capita,
    # Population density, Vehicle ownership, Total road deaths, Road deaths per Million Inhabitants.
    # Note that “Year” column value is always 2018.
    # Correct Cells with irregular data

    # drop unwanted columns 
    df = df.drop(["Road Network Length (in km) in 2013[26]", "Number of People Killed per Billion km[27]",
                    "Number of Seriously Injured in 2017/2018[27]"], axis=1)


    # rename columns
    df = df.rename(columns={"Area (thousands of km2)[21]": "Area",
                                "Population in 2018[22]": "Population",
                                "GDP per capita in 2018[23]": "GDP per capita",
                                "Population density (inhabitants per km2) in 2017[24]": "Population density",
                                "Vehicle ownership (per thousand inhabitants) in 2016[25]": "Vehicle ownership",
                                "Total Road Deaths in 2018[27]": "Total road deaths",
                                "Road deaths per Million Inhabitants in 2018[27]": "Road deaths per Million Inhabitants"
                                })

    # Added new column Year with row values of 2018
    df.insert(1, 'Year', 2018)
    

    # Correct irregular cell in GDP per capita Column from '11,500+a' to '11500'
    df['GDP per capita'] = df['GDP per capita'].map(lambda x: int(''.join(filter(str.isdigit, x))))
    
    # Correct irregular cell in Population Column from '82.792,351' to '82792351'
    df['Population'] = df['Population'].map(lambda x: int(''.join(filter(str.isdigit, x))))
    
    # STEP 3
    # Data should be sorted by “Road deaths per Million Inhabitants” column.

    # sorting in ascending order
    
    df = df.sort_values(
        "Road deaths per Million Inhabitants", ascending=True)

    # get current working directory and generate a filepath to the data folder
    path = os.getcwd()
    file_path = ''.join(path) + '/src/data/' + 'normalized.csv'

    # save the csv to the dataset folder
    df.to_csv(file_path, index=False)
    
    return df
data_wrangler()

# Documentation:
# name - Albert Kabugo
# link -
# App performs various functions to help clean and analyze the data for NYC
# collisions between 2015 and 2017.

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt
import numpy as np
import pprint as pp
from PIL import Image
from datetime import date, time, datetime
import plotly.graph_objects as go
import plotly.express as px
import plotly

# # Title and subheader
st.set_page_config(page_title="NYC Collision Data", layout = "wide")
st.markdown("<h1 style='text-align: center; color: blue;'>NYC Collision Data</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: blue;'>An Evaluation of the Types and Causes of Accidents in NYC from 2015 to 2017</h1>", unsafe_allow_html=True)

# Bringing data in
plt.style.use('ggplot')
plt.rcParams['figure.figsize'] = (15, 5)

# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
collisions = pd.read_csv("/Users/albertkabugo/pythonProject1/Collisions.csv")

# Clean data / drop unnecessary columns
    # Dropping unucessary columns
collisions.drop('UNIQUE KEY', inplace=True, axis=1)
collisions.drop('ON STREET NAME', inplace=True, axis=1)
collisions.drop('CROSS STREET NAME', inplace=True, axis=1)
collisions.drop('OFF STREET NAME', inplace=True, axis=1)
collisions.drop('VEHICLE 3 TYPE', inplace=True, axis=1)
collisions.drop('VEHICLE 4 TYPE', inplace=True, axis=1)
collisions.drop('VEHICLE 5 TYPE', inplace=True, axis=1)
collisions.drop('VEHICLE 3 FACTOR', inplace=True, axis=1)
collisions.drop('VEHICLE 4 FACTOR', inplace=True, axis=1)
collisions.drop('VEHICLE 5 FACTOR', inplace=True, axis=1)
    # Dropping certain blank rows
collisions.dropna(subset = ["BOROUGH"], inplace=True)
collisions.dropna(subset = ["LONGITUDE"], inplace=True)
collisions.dropna(subset = ["LATITUDE"], inplace=True)
collisions.dropna(subset = ["LOCATION"], inplace=True)
collisions.dropna(subset = ["VEHICLE 1 TYPE"], inplace=True)
collisions.dropna(subset = ["VEHICLE 2 TYPE"], inplace=True)
collisions.dropna(subset = ["VEHICLE 1 FACTOR"], inplace=True)
collisions.dropna(subset = ["VEHICLE 2 FACTOR"], inplace=True)
collisions = collisions.astype({"ZIP CODE": str}) # Converts ZIP CODE into str as isn't float
collisions['ZIP CODE'] = collisions['ZIP CODE'].str[:6] # Takes first five values of ZIP CODE after being converted to string
collisions['DATE'] = pd.to_datetime(collisions['DATE']) # Date to date format
collisions['DATE'] = collisions['DATE'].dt.strftime('%m-%d-%Y') # Date to date format
collisions['DAY'] = pd.DatetimeIndex(collisions['DATE']).day # Creating column for filtering
collisions['MONTH'] = pd.DatetimeIndex(collisions['DATE']).month # Creating column for filtering
collisions['YEAR'] = pd.DatetimeIndex(collisions['DATE']).year # Creating column for filtering
collisions['DAY'] = collisions['DAY'].astype('int')

# Functions to be called in the main function
def pull_maps(boroughs):
    if boroughs == "MANHATTAN":
        st.write(f"Click the link to learn more about {boroughs}: https://www.introducingnewyork.com/manhattan")
    elif boroughs == "QUEENS":
        st.write(f"Click the link to learn more about {boroughs}: https://www.introducingnewyork.com/queens?_gl=1*9f5cno*_up*MQ..*_ga*MTk0ODk4MzcwNi4xNjU5MjIwMzYy*_ga_J58CLTBWWF*MTY1OTIyMDM2MS4xLjAuMTY1OTIyMDM2MS4w")
    elif boroughs == "BRONX":
        st.write(f"Click the link to learn more about the {boroughs}: https://www.introducingnewyork.com/bronx?_gl=1*1518mmo*_up*MQ..*_ga*MTk0ODk4MzcwNi4xNjU5MjIwMzYy*_ga_J58CLTBWWF*MTY1OTIyMDM2MS4xLjEuMTY1OTIyMTAxMy4w")
    elif boroughs == "BROOKLYN":
        st.write(f"Click the link to learn more about {boroughs}: https://www.introducingnewyork.com/brooklyn?_gl=1*cs4y7x*_up*MQ..*_ga*MTk0ODk4MzcwNi4xNjU5MjIwMzYy*_ga_J58CLTBWWF*MTY1OTIyMDM2MS4xLjEuMTY1OTIyMTEwNi4w")
    else:
        st.write(f"Click the link to learn more about {boroughs}: https://www.introducingnewyork.com/staten-island?_gl=1*1bx6qy2*_up*MQ..*_ga*MTk0ODk4MzcwNi4xNjU5MjIwMzYy*_ga_J58CLTBWWF*MTY1OTIyMDM2MS4xLjEuMTY1OTIyMTE2Mi4w")
    image = Image.open(f"{boroughs}.jpeg")
    st.image(image, width = 700, caption=f'Map of {boroughs}')

    # Playing with python pillow
    image = image.convert("RGB")
    d = image.getdata()
    new_image = []
    for item in d:
        # change all white (also shades of whites)
        # pixels to yellow
        if item[0] in list(range(200, 256)):
            new_image.append((255, 224, 100))
        else:
            new_image.append(item)
    # update image data
    image.putdata(new_image)
    # save new image
    image.save("flower_image_altered.jpg")
    st.image(image)

def groupby_sum_month_year(month, year, column_name):
    collisionsfiltered1 = collisions.loc[collisions['YEAR'].isin(year)]
    collisionsfiltered1 = collisionsfiltered1.loc[collisionsfiltered1['MONTH'].isin(month)]
    collisions_group_sum = collisionsfiltered1.groupby("BOROUGH").sum()
    collisions_group_sum.drop('LONGITUDE', inplace=True, axis=1)
    collisions_group_sum.drop('LATITUDE', inplace=True, axis=1)
    collisions_group_sum.drop('YEAR', inplace=True, axis=1)
    collisions_group_sum.drop('DAY', inplace=True, axis=1)
    collisions_group_sum.drop('MONTH', inplace=True, axis=1)
    return collisions_group_sum[column_name]

def piechart_vehicle_factors(borough_selection, column_of_interest, morethaneqto_percentage = 0.03):
    collisionsfiltered3 = collisions.loc[collisions['BOROUGH'].isin(borough_selection)]
    collisions_vehiclefactors1 = collisionsfiltered3[column_of_interest].value_counts().reset_index()
    collisions_vehiclefactors1.columns = [column_of_interest, 'COUNT']
    total = collisions_vehiclefactors1['COUNT'].sum()
    collisions_vehiclefactors2 = collisions_vehiclefactors1.assign(PERCENTAGES = collisions_vehiclefactors1['COUNT'] / total)
    collisions_vehiclefactors3 = collisions_vehiclefactors2[collisions_vehiclefactors2['PERCENTAGES'] > float(morethaneqto_percentage)]

    factors =  collisions_vehiclefactors3[column_of_interest]
    count = collisions_vehiclefactors3['COUNT']

    pie_vehicle1factors = px.pie(collisions_vehiclefactors3, values=count, names=factors, title=f'{column_of_interest} PIE CHART')
    pie_vehicle1factors.update_traces(textposition='inside', textinfo='percent+label')
    pie_vehicle1factors.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    pie_vehicle1factors.update_layout(title_font_size = 25)
    return(pie_vehicle1factors)

def groupby_total_year_vehicle1type(year):
    collisionsfiltered1 = collisions.loc[collisions['YEAR'].isin(year)]
    collisions_group_sum = collisionsfiltered1.groupby("VEHICLE 1 TYPE").sum()
    collisions_group_sum.drop('LONGITUDE', inplace=True, axis=1)
    collisions_group_sum.drop('LATITUDE', inplace=True, axis=1)
    collisions_group_sum.drop('YEAR', inplace=True, axis=1)
    collisions_group_sum.drop('DAY', inplace=True, axis=1)
    collisions_group_sum.drop('MONTH', inplace=True, axis=1)
    return collisions_group_sum

def groupby_total_year_vehicle2type(year):
    collisionsfiltered1 = collisions.loc[collisions['YEAR'].isin(year)]
    collisions_group_sum = collisionsfiltered1.groupby("VEHICLE 2 TYPE").sum()
    collisions_group_sum.drop('LONGITUDE', inplace=True, axis=1)
    collisions_group_sum.drop('LATITUDE', inplace=True, axis=1)
    collisions_group_sum.drop('YEAR', inplace=True, axis=1)
    collisions_group_sum.drop('DAY', inplace=True, axis=1)
    collisions_group_sum.drop('MONTH', inplace=True, axis=1)
    return collisions_group_sum

def piechart_vehicle1type(morethaneqto_percentage, year_selection):
    collisionsfiltered3 = collisions.loc[collisions['YEAR'].isin(year_selection)]
    collisions_vehicle1type = collisionsfiltered3['VEHICLE 1 TYPE'].value_counts().reset_index()
    collisions_vehicle1type.columns = ['VEHICLE 1 TYPE', 'COUNT']
    total = collisions_vehicle1type['COUNT'].sum()
    collisions_vehicle1type = collisions_vehicle1type.assign(PERCENTAGES = collisions_vehicle1type['COUNT'] / total)
    collisions_vehicle1type2 = collisions_vehicle1type[collisions_vehicle1type['PERCENTAGES'] > float(morethaneqto_percentage)]

    factors =  collisions_vehicle1type2['VEHICLE 1 TYPE']
    count = collisions_vehicle1type2['COUNT']

    pie_vehicle1type = px.pie(collisions_vehicle1type2, values=count, names=factors, title='VEHICLE 1 TYPE PIE CHART')
    pie_vehicle1type.update_traces(textposition='inside', textinfo='percent+label')
    pie_vehicle1type.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    pie_vehicle1type.update_layout(title_font_size = 25)
    return(pie_vehicle1type)

def piechart_vehicle2type(morethaneqto_percentage, year_selection):
    collisionsfiltered3 = collisions.loc[collisions['YEAR'].isin(year_selection)]
    collisions_vehicle2type = collisionsfiltered3['VEHICLE 2 TYPE'].value_counts().reset_index()
    collisions_vehicle2type.columns = ['VEHICLE 2 TYPE', 'COUNT']
    total = collisions_vehicle2type['COUNT'].sum()
    collisions_vehicle2type = collisions_vehicle2type.assign(PERCENTAGES = collisions_vehicle2type['COUNT'] / total)
    collisions_vehicle2type2 = collisions_vehicle2type[collisions_vehicle2type['PERCENTAGES'] > float(morethaneqto_percentage)]

    factors =  collisions_vehicle2type2['VEHICLE 2 TYPE']
    count = collisions_vehicle2type2['COUNT']

    pie_vehicle2type = px.pie(collisions_vehicle2type2, values=count, names=factors, title='VEHICLE 2 TYPE PIE CHART')
    pie_vehicle2type.update_traces(textposition='inside', textinfo='percent+label')
    pie_vehicle2type.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    pie_vehicle2type.update_layout(title_font_size = 25)
    return(pie_vehicle2type)

# Main function
def main():

    with st.sidebar:
        section_selection = st.radio(
            "Welcome! Choose A Section of Interest:",
            ("1. Cleaned Dataset used in our analysis", "2. Learn more about the Boroughs", "3. Data Analysis: Stats Totals By Borough",
             "4. Data Analysis: Causes of Accidents", "5. Data Analysis: Vehicle 1 & 2 Types", "All Analysis", "Pivot Tables"))

    if section_selection == "1. Cleaned Dataset used in our analysis":
        st.write("")
        st.write("")
        st.header("1. Cleaned Dataset used in our analysis:")
        st.write(collisions)
        st.write(f"Notes:  \n"
                 f"- Our cleaned dataset has {collisions.shape[0]} rows / collision instances for two vehicle accidents that spans over three years: 2015, 2016 and 2017.  \n"
                 f"- We removed columns that we thought would not add value to our analysis - such as the names of cross streets or the third, fourth and fifth causes of the accident.   \n"
                 f"- And we removed rows for which there is no associated borough, and no associated Lattitude / Longitude / Location - as our analysis is centered around collisions within each part of NYC.  \n")
        st.write("Data Types:")
        st.write("DATE: ", collisions.dtypes['DATE'], "TIME: ", collisions.dtypes['TIME'], "BOROUGH: ", collisions.dtypes['BOROUGH'], "ZIP CODE: ",
                 collisions.dtypes['ZIP CODE'], "LATITUDE: ", collisions.dtypes['LATITUDE'], "LONGITUDE: ", collisions.dtypes['LONGITUDE'], "LOCATION: ",
                 collisions.dtypes['LOCATION'], "PERSONS INJURED: ", collisions.dtypes['PERSONS INJURED'], "PERSONS KILLED: ",
                 collisions.dtypes['PERSONS KILLED'], "PEDESTRIANS INJURED: ",
                 collisions.dtypes['PEDESTRIANS INJURED'], "PEDESTRIANS KILLED: ",collisions.dtypes['PEDESTRIANS KILLED'], "CYCLSTS INJURED: ", collisions.dtypes['CYCLISTS INJURED'],
                 "CYCLSTS KILLED: ", collisions.dtypes['CYCLISTS KILLED'], "MOTORISTS INJURED: ", collisions.dtypes['MOTORISTS KILLED'], "MOTORISTS KILLED: ", collisions.dtypes['MOTORISTS KILLED'],
                 "VEHICLE 1 TYPE: ",collisions.dtypes['VEHICLE 1 TYPE'], "VEHICLE 2 TYPE: ", collisions.dtypes['VEHICLE 2 TYPE'], "VEHICLE 1 FACTOR: ",
                 collisions.dtypes['VEHICLE 1 FACTOR'], "VEHICLE 2 FACTOR: ", collisions.dtypes['VEHICLE 2 FACTOR'], "DAY: ",
                 collisions.dtypes['DAY'], "MONTH: ", collisions.dtypes['MONTH'], "YEAR: ", collisions.dtypes['YEAR'])
    elif section_selection =="2. Learn more about the Boroughs":
        st.write("")
        st.header("2. Learn more about the Boroughs:")
        st.write("")
        borough1 = st.multiselect("What Borough are you Interested in Analyzing? "
                                  "Learn more about them by selecting them below:",
                         ["MANHATTAN", "BROOKLYN",
                         "BRONX", "QUEENS", "STATEN ISLAND"])
        for boroughs in borough1:
            pull_maps(boroughs)
    elif section_selection == "3. Data Analysis: Stats Totals By Borough":
        # Data Analysis by Totals
            # Analysis by Years
        st.write("")
        st.header("3. Data Analysis: Stats Totals By Borough:")
        st.write("")
        st.subheader(f"Table and chart displaying the injured / killed numbers for various categories, months and years"
                     f" in each borough:")
        column_of_interest1 = st.selectbox("What column within the dataset are you interested in? Choose one from"
                                            "the dropdown menu:",
                         ['PERSONS INJURED', 'PERSONS KILLED', 'PEDESTRIANS INJURED', 'PEDESTRIANS KILLED',
                          'CYCLISTS INJURED', 'CYCLISTS KILLED', 'MOTORISTS INJURED', 'MOTORISTS KILLED'])
        year1 = st.multiselect("What year are you interested in?",
                         [2015, 2016, 2017])
        month1 = st.multiselect("What month within the dataset are you interested in? Choose one from"
                                            "the dropdown menu:",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        st.write(year1)
        st.write(month1)
            # Calling groupby_sum(year1) and associated charts:
        output = groupby_sum_month_year(month1, year1, column_of_interest1)
        st.write(output)
        st.bar_chart(output)

    elif section_selection == "4. Data Analysis: Causes of Accidents":
        # Causes of accidents pie charts
            # Vehicle 1 Factors
        st.write("")
        st.header("4. Data Analysis: Causes of Accidents:")
        st.write("")
        st.subheader(f"Pie charts displaying the causes of accidents for the first vehicle involved: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. Please note "
                                         "that '10%' would be written as '0.01': ", 0.03)
        pie_borough_selection = st.multiselect("What column within the dataset are you interested in? Choose one from"
                                        "the dropdown menu:",
                     ['BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'])
        st.write(piechart_vehicle_factors(pie_borough_selection, 'VEHICLE 1 FACTOR', percentage_input))

                # Vehicle 2 Factors
        st.subheader(f"Pie charts displaying the causes of accidents for the second vehicle involved: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. Please note "
                                         "that '10%' would be written as '0.01':", 0.03)
        pie_borough_selection = st.multiselect("What column within the dataset are you interested in? Choose one from"
                                        "the dropdown menu:                      ",
                     ['BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'])
        st.write(piechart_vehicle_factors(pie_borough_selection, 'VEHICLE 2 FACTOR', percentage_input))

    elif section_selection == "5. Data Analysis: Vehicle 1 & 2 Types":
        # Vehicle Type Data Analysis
            # Vehicl 1 Analysis by Years
        st.write("")
        st.header("5. Data Analysis: Vehicle 1 & 2 Types:")
        st.write("")
        st.subheader(f"Table and chart displaying the injured / killed numbers for various vehicle 1 types and "
                     f"years within the dataset:")
        year4 = st.multiselect("What year are you interested in?                                    ",
                         [2015, 2016, 2017])
        st.write(year4)
            # Calling groupby_total_year_vehicle1type() and associated charts:
        output = groupby_total_year_vehicle1type(year4)
        st.write(output)
        colors = px.colors.qualitative.T10
        fig = px.bar(output,
                 x = output.index,
                 y = [c for c in output.columns],
                 template = 'plotly_dark',
                 color_discrete_sequence = colors,
                 title = 'Stacked bar Chart for Vehicle 1 Types and Injured Party Totals',
                 )
        fig.update_layout(
        autosize=False,
        width=900,
        height=700,
        yaxis=dict(title_text="Count", titlefont=dict(size=30)))
        fig.update_yaxes(automargin=True)
        st.write(fig)

            # Vehicle 2 Analysis by Years
        st.subheader(f"Table and chart displaying the injured / killed numbers for various vehicle 2 types and "
                     f"years within the dataset:     ")
        year5 = st.multiselect("What year are you interested in?    ",
                         [2015, 2016, 2017])
        st.write(year5)
            # Calling groupby_total_year_vehicle2type() and associated charts:
        output = groupby_total_year_vehicle2type(year5)
        st.write(output)
        colors = px.colors.qualitative.T10
        fig = px.bar(output,
                 x = output.index,
                 y = [c for c in output.columns],
                 template = 'plotly_dark',
                 color_discrete_sequence = colors,
                 title = 'Stacked bar Chart for Vehicle 2 Types and Injured Party Totals',
                 )
        fig.update_layout(
        autosize=False,
        width=900,
        height=700,
        yaxis=dict(
            title_text="Count",
            titlefont=dict(size=30)))
        fig.update_yaxes(automargin=True)
        st.write(fig)

            # Vehicle type 1 pie charts by year
        st.subheader(f"Pie chart displaying the frequencies of accidents for vehicle 1 types per year: "
                     f"within the dataset: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. "
                                         "Please note that '10%' would be written as '0.01':        ", 0.03)
        year6 = st.multiselect("What year are you interested in?                                ",
                         [2015, 2016, 2017])
        st.write(piechart_vehicle1type(percentage_input, year6))
            # Vehicle type 2 pie charts by year
        st.subheader(f"Pie chart displaying the frequencies of accidents for vehicle 2 types per year: "
                     f"within the dataset: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. Please note "
                                 "that '10%' would be written as '0.01':                 ", 0.03)
        year6 = st.multiselect("What year are you interested in?                                   ",
                         [2015, 2016, 2017])
        st.write(piechart_vehicle2type(percentage_input, year6))
    elif section_selection == "All Analysis":
        st.write("")
        st.write("")
        st.header("1. Cleaned Dataset used in our analysis:")
        st.write(collisions)
        st.write(f"Notes:  \n"
                 f"- Our cleaned dataset has {collisions.shape[0]} rows / collision instances for two vehicle accidents that spans over three years: 2015, 2016 and 2017.  \n"
                 f"- We removed columns that we thought would not add value to our analysis - such as the names of cross streets or the third, fourth and fifth causes of the accident.   \n"
                 f"- And we removed rows for which there is no associated borough, and no associated Lattitude / Longitude / Location - as our analysis is centered around collisions within each part of NYC.  \n")
        st.write("Data Types:")
        st.write("DATE: ", collisions.dtypes['DATE'], "TIME: ", collisions.dtypes['TIME'], "BOROUGH: ", collisions.dtypes['BOROUGH'], "ZIP CODE: ",
                 collisions.dtypes['ZIP CODE'], "LATITUDE: ", collisions.dtypes['LATITUDE'], "LONGITUDE: ", collisions.dtypes['LONGITUDE'], "LOCATION: ",
                 collisions.dtypes['LOCATION'], "PERSONS INJURED: ", collisions.dtypes['PERSONS INJURED'], "PERSONS KILLED: ",
                 collisions.dtypes['PERSONS KILLED'], "PEDESTRIANS INJURED: ",
                 collisions.dtypes['PEDESTRIANS INJURED'], "PEDESTRIANS KILLED: ",collisions.dtypes['PEDESTRIANS KILLED'], "CYCLSTS INJURED: ", collisions.dtypes['CYCLISTS INJURED'],
                 "CYCLSTS KILLED: ", collisions.dtypes['CYCLISTS KILLED'], "MOTORISTS INJURED: ", collisions.dtypes['MOTORISTS KILLED'], "MOTORISTS KILLED: ", collisions.dtypes['MOTORISTS KILLED'],
                 "VEHICLE 1 TYPE: ",collisions.dtypes['VEHICLE 1 TYPE'], "VEHICLE 2 TYPE: ", collisions.dtypes['VEHICLE 2 TYPE'], "VEHICLE 1 FACTOR: ",
                 collisions.dtypes['VEHICLE 1 FACTOR'], "VEHICLE 2 FACTOR: ", collisions.dtypes['VEHICLE 2 FACTOR'], "DAY: ",
                 collisions.dtypes['DAY'], "MONTH: ", collisions.dtypes['MONTH'], "YEAR: ", collisions.dtypes['YEAR'])
        st.write("")
        st.header("2. Learn more about the Boroughs:")
        st.write("")
        borough1 = st.multiselect("What Borough are you Interested in Analyzing? "
                                  "Learn more about them by selecting them below:",
                         ["MANHATTAN", "BROOKLYN",
                         "BRONX", "QUEENS", "STATEN ISLAND"])
        for boroughs in borough1:
            pull_maps(boroughs)
        # Data Analysis by Totals
            # Analysis by Years
        st.write("")
        st.header("3. Data Analysis: Stats Totals By Borough:")
        st.write("")
        st.subheader(f"Table and chart displaying the injured / killed numbers for various categories, months and years"
                     f" in each borough:")
        column_of_interest1 = st.selectbox("What column within the dataset are you interested in? Choose one from"
                                            "the dropdown menu:",
                         ['PERSONS INJURED', 'PERSONS KILLED', 'PEDESTRIANS INJURED', 'PEDESTRIANS KILLED',
                          'CYCLISTS INJURED', 'CYCLISTS KILLED', 'MOTORISTS INJURED', 'MOTORISTS KILLED'])
        year1 = st.multiselect("What year are you interested in?",
                         [2015, 2016, 2017])
        month1 = st.multiselect("What month within the dataset are you interested in? Choose one from"
                                            "the dropdown menu:",
                         [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        st.write(year1)
        st.write(month1)
            # Calling groupby_sum(year1) and associated charts:
        output = groupby_sum_month_year(month1, year1, column_of_interest1)
        st.write(output)
        st.bar_chart(output)
        # Causes of accidents pie charts
            # Vehicle 1 Factors
        st.write("")
        st.header("4. Data Analysis: Causes of Accidents:")
        st.write("")
        st.subheader(f"Pie charts displaying the causes of accidents for the first vehicle involved: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. Please note "
                                         "that '10%' would be written as '0.01': ", 0.03)
        pie_borough_selection = st.multiselect("What column within the dataset are you interested in? Choose one from"
                                        "the dropdown menu:",
                     ['BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'])
        st.write(piechart_vehicle_factors(pie_borough_selection, 'VEHICLE 1 FACTOR', percentage_input))

                # Vehicle 2 Factors
        st.subheader(f"Pie charts displaying the causes of accidents for the second vehicle involved: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. Please note "
                                         "that '10%' would be written as '0.01':", 0.03)
        pie_borough_selection = st.multiselect("What column within the dataset are you interested in? Choose one from"
                                        "the dropdown menu:                      ",
                     ['BROOKLYN', 'BRONX', 'MANHATTAN', 'QUEENS', 'STATEN ISLAND'])
        st.write(piechart_vehicle_factors(pie_borough_selection, 'VEHICLE 2 FACTOR', percentage_input))

        # Vehicle Type Data Analysis
            # Vehicl 1 Analysis by Years
        st.write("")
        st.header("5. Data Analysis: Vehicle 1 & 2 Types:")
        st.write("")
        st.subheader(f"Table and chart displaying the injured / killed numbers for various vehicle 1 types and "
                     f"years within the dataset:")
        year4 = st.multiselect("What year are you interested in?                                    ",
                         [2015, 2016, 2017])
        st.write(year4)
            # Calling groupby_total_year_vehicle1type() and associated charts:
        output = groupby_total_year_vehicle1type(year4)
        st.write(output)
        colors = px.colors.qualitative.T10
        fig = px.bar(output,
                 x = output.index,
                 y = [c for c in output.columns],
                 template = 'plotly_dark',
                 color_discrete_sequence = colors,
                 title = 'Stacked bar Chart for Vehicle 1 Types and Injured Party Totals',
                 )
        fig.update_layout(
        autosize=False,
        width=900,
        height=700,
        yaxis=dict(
            title_text="Count",
            titlefont=dict(size=30)))
        fig.update_yaxes(automargin=True)
        st.write(fig)

            # Vehicle 2 Analysis by Years
        st.subheader(f"Table and chart displaying the injured / killed numbers for various vehicle 2 types and "
                     f"years within the dataset:     ")
        year5 = st.multiselect("What year are you interested in?    ",
                         [2015, 2016, 2017])
        st.write(year5)
            # Calling groupby_total_year_vehicle2type() and associated charts:
        output = groupby_total_year_vehicle2type(year5)
        st.write(output)
        colors = px.colors.qualitative.T10
        fig = px.bar(output,
                 x = output.index,
                 y = [c for c in output.columns],
                 template = 'plotly_dark',
                 color_discrete_sequence = colors,
                 title = 'Stacked bar Chart for Vehicle 2 Types and Injured Party Totals',
                 )
        fig.update_layout(
        autosize=False,
        width=900,
        height=700,
        yaxis=dict(
            title_text="Count",
            titlefont=dict(size=30)))
        fig.update_yaxes(automargin=True)
        st.write(fig)

            # Vehicle type 1 pie charts by year
        st.subheader(f"Pie chart displaying the frequencies of accidents for vehicle 1 types per year: "
                     f"within the dataset: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. "
                                         "Please note that '10%' would be written as '0.01':        ", 0.03)
        year6 = st.multiselect("What year are you interested in?                                ",
                         [2015, 2016, 2017])
        st.write(piechart_vehicle1type(percentage_input, year6))
            # Vehicle type 2 pie charts by year
        st.subheader(f"Pie chart displaying the frequencies of accidents for vehicle 2 types per year: "
                     f"within the dataset: ")
        percentage_input = st.text_input("Input the minimum percentage you want to see in the pie chart below. "
                                         "Please note that '10%' would be written as '0.01':                 ", 0.03)
        year6 = st.multiselect("What year are you interested in?                                   ",
                         [2015, 2016, 2017])
        st.write(piechart_vehicle2type(percentage_input, year6))
    elif section_selection =="Pivot Tables":
        collisions_pivot = collisions
        collisions_pivot.drop('LATITUDE', inplace=True, axis=1)
        collisions_pivot.drop('LONGITUDE', inplace=True, axis=1)
        collisions_pivot.drop('DATE', inplace=True, axis=1)
        collisions_pivot.drop('LOCATION', inplace=True, axis=1)
        collisions_pivot['YEAR'] = collisions_pivot['YEAR'].astype(str)
        collisions_pivot['MONTH'] = collisions_pivot['MONTH'].astype(str)
        collisions_pivot['DAY'] = collisions_pivot['DAY'].astype(str)
        collisions_pivot['ZIP CODE'] = collisions_pivot['DAY'].astype(str)
        st.write("Raw data pandas table used in our Pivot Tables below:")
        st.write(collisions_pivot)
            # Adding raw data datatypes into an empty dictionary.
        dict_pivot = {}
        for items in collisions_pivot:
            dict_pivot[items] = collisions.dtypes[items]
        st.write(dict_pivot)

        sum_mean_count = st.selectbox("Select a 'summarized by' option for the numerical outputs within the "
                                      "pivot table:",
                 ['sum', 'mean', 'count'])
        if sum_mean_count =='sum':
            rows = st.multiselect("Select the desired row category(s) for the pivot table below:",
                                ['BOROUGH', 'VEHICLE 1 TYPE', 'VEHICLE 2 TYPE', 'VEHICLE 1 FACTOR', 'VEHICLE 2 FACTOR',
                                 'MONTH', 'YEAR'])
            pivot1 = pd.pivot_table(collisions_pivot[collisions_pivot != 0], index=rows, aggfunc=sum_mean_count)
            st.write(pivot1)
        elif sum_mean_count == 'mean':
            rows = st.multiselect("Select the desired row category(s) for the pivot table below:",
                                ['BOROUGH', 'VEHICLE 1 TYPE', 'VEHICLE 2 TYPE', 'VEHICLE 1 FACTOR', 'VEHICLE 2 FACTOR',
                                 'MONTH', 'YEAR'])
            pivot1 = pd.pivot_table(collisions_pivot[collisions_pivot != 0], index=rows, aggfunc=sum_mean_count)
            st.write(pivot1)
        elif sum_mean_count =='count':
            rows = st.selectbox("Select a row category for the pivot table below:",
                             ['BOROUGH', 'VEHICLE 1 TYPE', 'VEHICLE 2 TYPE', 'VEHICLE 1 FACTOR',
                              'VEHICLE 2 FACTOR', 'YEAR'])
            collisions_pivot = collisions_pivot.rename(columns={'ZIP CODE': 'ACCIDENT FREQUENCY'})
            pivot1 = pd.pivot_table(collisions_pivot[collisions_pivot != 0], index=rows, values = 'ACCIDENT FREQUENCY',
                                    aggfunc='count')
            st.write(pivot1)


main()

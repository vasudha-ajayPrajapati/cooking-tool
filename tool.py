import streamlit as st
import pandas as pd
import numpy as np
from pandas import DataFrame, Series 
from functools import total_ordering
from streamlit import components
from decimal import *
import openpyxl
import matplotlib.pyplot as plt
#from helper import generate_df, make_stacked_bar_horiz
from PIL import Image
import plotly.express as px
import urllib.request
import io
# from io import BytesIO

#import file 
energy_cooking = pd.read_excel('cooking_energy.xlsx',sheet_name='cooking energy',index_col=(0))
electricity_tariff_file = pd.read_excel('cooking_energy.xlsx',sheet_name='electricity tariff',index_col=(0))
stove_file = pd.read_excel('cooking_energy.xlsx',sheet_name='stoves',index_col=(0))

social_carbon_cost = 86 * 82 * 0.001 # Social carbon cost is 86 USD per ton of CO2

#____________ Page info________________________________________
about_markdown = 'This app has been developed by Vasudha Foundation.\n' + \
'Development Team - Vikas Kumar, Bikash Sahu.\n' + \
'For further details contact bikash@vasudhaindia.org.' + \
'Disclaimer: Do not replicate this without permission.'

# Set the page layout to be responsive
st.set_page_config(layout="wide", menu_items={'Get Help': None, 'Report a Bug': None, 'About': about_markdown})

#___________Main page__________________________________________
image_url = 'https://github.com/gitbik/cooking-tool/blob/main/Vasudha_Logo_PNG.png?raw=true'
image_data = urllib.request.urlopen(image_url).read()
img = Image.open(io.BytesIO(image_data))
# img = Image.open('Vasudha_Logo_PNG.PNG') # Load the image
resized_img = img.resize((300, 300))  # Adjust the width and height as needed
col1, col2 = st.columns([1,6]) # Create two columns

# Display the resized image in the first column
col1.image(resized_img, use_column_width=True)

# Display the title in the second column
col2.title('Techno Economic Analysis of Cooking Technologies')
col2.write('_Explore this web app to select your typical cooking needs and discover a comprehensive comparison of various cooking solutions' 
           + ' available in the Indian market._')

# extracting data from datafile (excel)
State_list = electricity_tariff_file['State'].tolist()
energy_source_list = stove_file['Fuel'].unique().tolist()

#burners or stoves list
firewood_stove=["Traditional cook stove (TCS)", "Improved cook stove (ICS - Natural)", "Improved cook stove (ICS - Forced)"]
livestock_stove=["Traditional cook stove (TCS)", "Improved cook stove (ICS - Natural)", "Improved cook stove (ICS - Forced)"]
lpg_stove=["LPG (2 burner)"]
png_stove=["PNG (2 burner)"]
bio_gas_stove=["Biogas (2 burner)"]
grid_electricity_stove=["Electric Induction (1 burner)", "Electric Induction (2 burner)", "Electric Pressure Cooker"]
microgrid_electricity_stove=["Electric Induction (1 burner)", "Electric Induction (2 burner)", "Electric Pressure Cooker"]

tab1, tab2 = st.tabs(["Basic Settings", "Further Information"])
with tab2:
    with st.expander('More about electric induction and its benefits'):
        st.markdown("""
            * **Faster cooking times:** Induction cooktops heat up much faster than traditional electric or gas cooktops. This is because the heat is generated directly in the pan, rather than in the cooktop itself.
            * **Precise temperature control:** Induction cooktops offer precise temperature control, which is ideal for delicate dishes or when you need to simmer something for a long period of time.
            * **Efficiency:** Induction cooktops are very efficient, meaning they use less energy than traditional cooktops. This can save you money on your energy bills.
            * **Safety:** Induction cooktops are very safe. There is no open flame or hot surface, so there is less risk of burns or fire.
            * **Easy cleanup:** Induction cooktops are very easy to clean. The smooth surface of the cooktop makes it easy to wipe down, and there are no spills or splatters to worry about.
            """ )

    st.subheader("Meal Energy Consumption")
    st.markdown('The meal energy consumption assumptions are provided in the following.' 
                + ' Please note the values mentioned are considered for a household comprising of 4 to 5 persons.')
    st.dataframe(energy_cooking.iloc[:,[1,2,3]])
    
    st.subheader("Cookstove Characteristics")

    stove_char = {
    'Stove Type': ['Traditional cook stove (TCS)','Improved cook stove (ICS - Natural)','Improved cook stove (ICS - Forced)','Biogas (2 burner)',
                   'PNG (2 burner)','LPG (2 burner)','Electric Induction (1 burner)','Electric Induction (2 burner)','Electric Pressure Cooker'],
    'Life (years)': [1, 3, 3, 10, 10, 10, 10, 10, 10],
    'Thermal Efficiency (percent)': ['15%', '25%', '35%', '70%', '70% to 80%', '70% to 80%', '80% to 90%', '80% to 90%', '80% to 90%'],
    'Capex (INR)': ['0','INR 750 to INR 900','INR 1000','INR 40,000 to INR 60,000','INR 1,100 to INR 2,500',
                    'INR 1,000 to INR 2,000','INR 1,000 to INR 2,900','INR 2,000 to INR 5,800','INR 5,000 to INR 10,000']
    }

    # stove_char_df = pd.DataFrame(stove_char, index = False)
    stove_char_df = pd.DataFrame(stove_char)
    st.dataframe(stove_char_df)
    
    
    st.subheader("Carbon Emission Factors")
    carbon_ef = {
    'Fuel Type': ['Firewood','Livestock Waste','Biogas','LPG','PNG','Grid electricity','Solar PV rooftop'],
    'Unit Carbon Emission (kgCO2eq./kWh)': [0.4, 0.4, 0.15, 0.23, 0.2, 0.72, 0],
    }

    carbon_ef_df = pd.DataFrame(carbon_ef)
    st.dataframe(carbon_ef_df)

    
    st.subheader("Statewise Grid Electricity Tariff of Indian States")
    st.dataframe(electricity_tariff_file.iloc[:,[1,2,3,4]])
    
    st.subheader("Daily IHAP")
    ihap = {
    'Stove Type': ['Traditional cook stove (TCS)','Improved cook stove (ICS - Natural)','Improved cook stove (ICS - Forced)',
                   'Biogas (2 burner)','PNG (2 burner)','LPG (2 burner)','Electric Induction','Electric Pressure Cooker'
    ],
    'Daily IHAP - PM 2.5 (μg/m3)': [1230, 410, 165, 60, 47, 64, 47, 35],
    }

    ihap_df = pd.DataFrame(ihap)
    st.dataframe(ihap_df)
    
    st.subheader('Annual Income of HH')
    income = {
    'Area Type': ['Rural','Rural','Rural','Urban','Urban','Urban'],
    'Socio-economic status': ['Lower','Middle','Higher','Lower','Middle','Higher'],
    'Annual Income (INR)': ['₹ 2,00,000','₹ 5,70,000','₹ 9,00,000','₹ 2,50,000','₹ 7,12,500','₹ 11,25,000']
    }
    income_df = pd.DataFrame(income)
    st.dataframe(income_df)

with tab1:
    #_______________basic settings_________________________________________
    st.subheader("Household Profile")
    c1, c2 = st.columns(2)
    with c1: 
        state_select = st.selectbox('Select State', State_list)
        with st.container():
            area_select = st.selectbox('Area Type', ('Urban', 'Rural'))
        monthly_income = st.number_input('Enter Monthly Income', min_value=0, max_value=1000000, value=30000, step=1000)
    annual_income = monthly_income * 12
    with c2:
        with st.container():
            cooking_source_options = energy_source_list
            cooking_source_select = st.multiselect('Cooking Fuel Used', cooking_source_options, default=['Grid electricity'])
            filtered_stoves = stove_file.loc[stove_file['Fuel'].isin(cooking_source_select), 'stoves'].unique().tolist()
            cookstove_select = st.multiselect('Cookstove Used', filtered_stoves, default=['Electric Induction (1 burner)']) 
            lpg_subsidy = st.selectbox('Are you eligible for an LPG subsidy?', ('No','Yes')) 

    if area_select=='Rural':
        if annual_income < 200000:
            category = "BoP"
        elif annual_income < 570000:
            category = "Lower"
        elif annual_income < 900000:
            category = "Middle"
        else:
            category = "Higher"
    else:
        if annual_income < 250000:
            category = "BoP"
        elif annual_income < 712500:
            category = "Lower"
        elif annual_income < 1125000:
            category = "Middle"
        else:
            category = "Higher"

    # Filter the DataFrame based on the selected state
    electricity_tariff = electricity_tariff_file[electricity_tariff_file["State"] == state_select]

    if not electricity_tariff.empty:
        # Select the tariff value from the filtered DataFrame
        electricity_tariff = electricity_tariff.iloc[0][category]
    else:
        electricity_tariff = None
# Stoves lists
    stove_file_list = stove_file[stove_file["Area"] == area_select]
    stove_file_list = stove_file_list[stove_file_list["Socio-Economic"] == category]
    stove_file_list = stove_file_list[stove_file_list["Fuel"].isin(cooking_source_select)]
    # stove_file_list
    # extracting data from datafile (excel)
    stove_list = stove_file_list['stoves'].tolist()

    st.subheader("Meal Profile")
    c1, c2, c3,c4 = st.columns(4)  
    with c1:
        st.write('Breakfast')
        items = ["Idli", "Puri", "Roti","Dosa","Rice","Dal","Veg Curry","Non-Veg Curry", "Dry Subji", "Fried Items"]
        # Create a form
        with st.form("my_form"):
            # Create a column for items
            quantity_bf = st.number_input('For no. of people', value =1, step =1 , format = "%d")
            items_column = st.multiselect("Dishes", items)
            # Create a column for the quantity
            quantities = {}
            energy_sources = {}
            for bf_item in items_column:
                # quantity = st.number_input(f"For no. of people {bf_item}", key=f"bf_{bf_item}", value=1, step=1, format="%d")
                quantities[bf_item] = quantity_bf
                energy_source = st.selectbox(f"Cooking energy source for {bf_item}", cookstove_select, key=f"bf_{bf_item}_energy")
                energy_sources[bf_item] = energy_source
            # If the user clicks the submit button, do something
            if st.form_submit_button("Submit Breakfast"):
                # Create a DataFrame from user input
                user_response_breakfast_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
                user_response_breakfast_df['stoves'] = user_response_breakfast_df['Dishes'].map(energy_sources)
                st.write("User input:")
                st.dataframe(user_response_breakfast_df)
            user_response_breakfast_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
            user_response_breakfast_df['stoves'] = user_response_breakfast_df['Dishes'].map(energy_sources)

    with c2:
        st.write('Lunch')
        items = ["Roti", "Rice","Puri","Dal","Veg Curry","Non-Veg Curry", "Dry Subji", "Fried Items"]
        # Create a form
        with st.form("my_form_lunch"):
            # Create a column for items
            quantity_lunch =  st.number_input('For no. of people', value =1, step =1 , format = "%d")
            items_column = st.multiselect("Dishes", items)
            # Create a column for the quantity
            quantities = {}
            energy_sources = {}
            for l_item in items_column:
                # quantity = st.number_input(f"For no. of people {l_item}", key=f"l_{l_item}", value=1, step=1, format="%d")
                quantities[l_item] = quantity_lunch
                energy_source = st.selectbox(f"Cooking energy source for {l_item}", cookstove_select, key=f"l_{l_item}_energy")
                energy_sources[l_item] = energy_source
            # If the user clicks the submit button, do something
            if st.form_submit_button("Submit Lunch"):
                # Create a DataFrame from user input
                user_response_lunch_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
                user_response_lunch_df['stoves'] = user_response_lunch_df['Dishes'].map(energy_sources)
                st.write("User input:")
                st.dataframe(user_response_lunch_df)
            user_response_lunch_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
            user_response_lunch_df['stoves'] = user_response_lunch_df['Dishes'].map(energy_sources)

    with c3:
        st.write('Dinner')
        items = ["Rice", "Roti", "Dosa", "Idli", "Puri", "Dal", "Veg Curry","Non-Veg Curry", "Dry Subji", "Fried Items"]
        # Create a form
        with st.form("my_form_dinner"):
            # Create a column for items
            quantity_dinner =  st.number_input('For no. of people', value =1, step =1 , format = "%d")
            items_column = st.multiselect("Dishes", items)
            # Create a column for the quantity
            quantities = {}
            energy_sources = {}
            for d_item in items_column:
                # quantity = st.number_input(f"For no. of people {d_item}", key=f"d_{d_item}", value=1, step=1, format="%d")
                quantities[d_item] = quantity_dinner
                energy_source = st.selectbox(f"Cooking energy source for {d_item}", cookstove_select, key=f"d_{d_item}_energy")
                energy_sources[d_item] = energy_source
            # If the user clicks the submit button, do something
            if st.form_submit_button("Submit Dinner"):
                # Create a DataFrame from user input
                user_response_dinner_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
                user_response_dinner_df['stoves'] = user_response_dinner_df['Dishes'].map(energy_sources)
                st.write("User input:")
                st.dataframe(user_response_dinner_df)
            user_response_dinner_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
            user_response_dinner_df['stoves'] = user_response_dinner_df['Dishes'].map(energy_sources)

    with c4:
        st.write('Beverages & Snacks')
        items = ["Milk","Tea/Coffee","Pakoda","Samosa","Pao bhaji"]
        # Create a form
        with st.form("my_form_snacks"):
            # Create a column for items
            quantity_snacks =  st.number_input('For no. of people', value =1, step =1 , format = "%d")
            items_column = st.multiselect("Dishes", items)
            # Create a column for the quantity
            quantities = {}
            energy_sources = {}
            for ts_item in items_column:
                # quantity = st.number_input(f"For no. of people {ts_item}", key=ts_item, value=1, step=1, format="%d")
                quantities[ts_item] = quantity_snacks
                energy_source = st.selectbox(f"Cooking energy source for {ts_item}",
                                            cookstove_select)
                energy_sources[ts_item] = energy_source
            # If the user clicks the submit button, do something
            if st.form_submit_button("Submit Snacks"):
                # Create a DataFrame from user input
                user_response_snacks_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
                user_response_snacks_df['stoves'] = user_response_snacks_df['Dishes'].map(energy_sources)
                st.write("User input:")
                st.dataframe(user_response_snacks_df)
            user_response_snacks_df = pd.DataFrame(list(quantities.items()), columns=['Dishes', 'Quantity(for no. of people)'])
            user_response_snacks_df['stoves'] = user_response_snacks_df['Dishes'].map(energy_sources)

    user_response_breakfast_df.columns = ['Dishes', 'Quantity (for number of people)','stoves']
    user_response_lunch_df.columns = ['Dishes', 'Quantity (for number of people)','stoves']
    user_response_dinner_df.columns = ['Dishes', 'Quantity (for number of people)','stoves']
    user_response_snacks_df.columns = ['Dishes', 'Quantity (for number of people)','stoves']

    # # Concatenate the DataFrames vertically
    user_response_df = pd.concat([user_response_breakfast_df, user_response_lunch_df, user_response_dinner_df,user_response_snacks_df], axis=0)


    result_container = st.container()
    # is_submit1 = st.button(label='Update results')
    #don't proceed until Update results has been pressed
    #if not is_submit1:
     #   st.stop()

    
    #_______________Results calculation______________________

    #making dataframe w/ calculate total energy required kWh dataframe

    #for induction
    df1=pd.merge(stove_file_list,user_response_df,  on=['stoves'])

#################################need to change quantity
    df=pd.merge(energy_cooking, df1,  on=['Dishes'])
############################## add if else condition for stove selection ###################
#add fuel condition on df



    selection_of_stoves=df['Fuel'].unique()
    selection_of_stoves= ', '.join(selection_of_stoves)
################################
    ############for no of people
    no_of_people=df['Quantity (for number of people)'].tolist()
    def replace_numbers(no_of_people, less, more, equ):
        new_list = []
        for item in no_of_people:
            try:
                number = int(item)
                if number <= 3:
                    new_list.append(less)
                elif number in [4,5,6]:
                    new_list.append(equ)
                elif number > 6:
                    new_list.append(more)
                else:
                    new_list.append(item)
            except ValueError:
                new_list.append(item)
        return new_list

    def replace_time_numbers(no_of_people, less, more, equ):
        new_list = []
        for item in no_of_people:
            try:
                number = int(item)
                if number <= 3:
                    new_list.append(less)
                elif number in [4,5,6]:
                    new_list.append(equ)
                elif number > 6:
                    new_list.append(more)
                else:
                    new_list.append(item)
            except ValueError:
                new_list.append(item)
        return new_list

    less = 0.75
    equ = 1
    more = 1.5
    new_people_list = replace_numbers(no_of_people, less, more, equ)
    less = 0.8
    equ = 1
    more = 1.2

    new_time_list = replace_time_numbers(no_of_people, less, more, equ)
    df["no of people"] = new_people_list
    df["new time"] = new_time_list
    df['total equantity (grams)'] = df['quantity (grams)'] * df['no of people']
    df['total energy required (for electric induction)'] = df['Energy (kWh)'] * df['no of people']
    df['total energy required'] = df['total energy required (for electric induction)'] / df['Thermal Efficiency']
    contains_electricity_df = df[df['Fuel'].str.contains('Grid electricity')]
    contains_electricity_df['RS(monthly)'] = contains_electricity_df['total energy required'] * electricity_tariff* 30 #30 days 

    does_not_contain_electricity_dff = df[~df['Fuel'].str.contains('Grid electricity')]
    does_not_contain_electricity_dff['RS(monthly)'] = does_not_contain_electricity_dff['total energy required'] * does_not_contain_electricity_dff['Unit cost'] * 30     

    df=pd.concat([contains_electricity_df, does_not_contain_electricity_dff], axis=0)
    df['daily time'] = (df['time (min)'] * df["new time"] * df['time_conversion']) / 60
    df['emissions'] = df['total energy required'] * df['Unit carbon emission']
    total_emissions = df['emissions'].sum()
    total_emissions_annual = total_emissions * 365 * 0.9
    total_energy = df['total energy required'].sum()
    present_EF = total_emissions / total_energy
    current_time_daily=df['daily time'].sum()
    df_time = ((df["new time"]*df['time (min)']).sum())/60 #hours
    total_energy_user = df['total energy required'].sum()
    current_cost = df['RS(monthly)'].sum()
    current_cost_annual = current_cost * 12 
    total_energy_induction = df['total energy required (for electric induction)'].sum()
    stove_file1=stove_file[stove_file["Area"] == area_select]
    stove_file1=stove_file1[stove_file1["Socio-Economic"] == category]

    #########Grid_Electricity#########
    Grid_electricity_data = stove_file1[stove_file1["Fuel"] == 'Grid electricity']
    Grid_electricity_data["Grid electricity_consumption"] = total_energy_induction/Grid_electricity_data['Thermal Efficiency']
    Grid_electricity_data["Grid electricity_RS"] = Grid_electricity_data["Grid electricity_consumption"]*electricity_tariff * 30 #30 days
    Grid_electricity_cost = Grid_electricity_data["Grid electricity_RS"].mean()
    Grid_electricity_cost_annual = Grid_electricity_cost * 12
    Grid_electricity_consumption_KWH = Grid_electricity_data["Grid electricity_consumption"].mean()
    Grid_electricity_time_conversion = Grid_electricity_data['time_conversion'][0]
    Grid_electricity_time = df_time * Grid_electricity_time_conversion
    Grid_electricity_efficiency = Grid_electricity_data['Thermal Efficiency'][0]
    Grid_electricity_capex = Grid_electricity_data['Capex'][1]
    Grid_electricity_emission = Grid_electricity_data['Unit carbon emission'][0]
    Grid_electricity_emission_annual = Grid_electricity_emission * Grid_electricity_consumption_KWH * 365 * 0.9
    Grid_electricity_ihap = Grid_electricity_data['Daily IHAP (PM2.5)'][0]
    Grid_electricity_pbp = (Grid_electricity_capex) / (current_cost_annual - Grid_electricity_cost_annual)
    
    #########Solar Induction#########
    Solar_rooftop_data=stove_file1[stove_file1["Fuel"] == 'Solar rooftop']
    Solar_rooftop_data["Solar rooftop_consumption"]=total_energy_induction/Solar_rooftop_data['Thermal Efficiency']
    Solar_rooftop_data["Solar rooftop_RS"]=Solar_rooftop_data["Solar rooftop_consumption"]*Solar_rooftop_data['Unit cost']*30 #30 days
    Solar_rooftop_cost=Solar_rooftop_data["Solar rooftop_RS"].mean()
    Solar_rooftop_cost_annual = Solar_rooftop_cost * 12
    Solar_rooftop_consumption_kwh=Solar_rooftop_data["Solar rooftop_consumption"].mean()
    Solar_rooftop_time_conversion = Solar_rooftop_data['time_conversion'][0]
    Solar_rooftop_time = df_time * Solar_rooftop_time_conversion
    Solar_rooftop_efficiency = Solar_rooftop_data['Thermal Efficiency'][0]
    Solar_rooftop_capex = Solar_rooftop_data['Capex'][1]
    Solar_rooftop_emission = Solar_rooftop_data['Unit carbon emission'][0]
    Solar_rooftop_emission_annual = Solar_rooftop_emission * Solar_rooftop_consumption_kwh * 365 * 0.9
    Solar_rooftop_ihap = Solar_rooftop_data['Daily IHAP (PM2.5)'][0]
    Solar_rooftop_pbp = Solar_rooftop_capex / (current_cost_annual - Solar_rooftop_cost_annual)
    
    #########LPG#########
    LPG_data=stove_file1[stove_file1["Fuel"] == 'LPG']
    LPG_data["lpg_consumption"]=total_energy_induction/LPG_data['Thermal Efficiency']
    LPG_water_heater_eff=LPG_data['Thermal Efficiency'].mean()  # for water heater
    LPG_data["lpg_RS"]=LPG_data["lpg_consumption"]*LPG_data['Unit cost']*30 #30 days
    LPG_cost=LPG_data["lpg_RS"].mean()
    LPG_cost_annual = LPG_cost * 12
    LPG_consumption_kwh=LPG_data["lpg_consumption"].mean()
    LPG_time = df_time * LPG_data["time_conversion"][0]
    LPG_efficiency = LPG_data['Thermal Efficiency'][0]
    LPG_capex = LPG_data['Capex'][0]
    LPG_emission = LPG_data['Unit carbon emission'][0]
    LPG_emission_annual = LPG_emission * LPG_consumption_kwh * 365 * 0.9
    LPG_ihap = LPG_data['Daily IHAP (PM2.5)'][0]
    LPG_pbp = LPG_capex / (current_cost_annual - LPG_cost_annual)

    #########PNG#########
    PNG_data=stove_file1[stove_file1["Fuel"] == 'PNG']
    PNG_data["png_consumption"]=total_energy_induction/PNG_data['Thermal Efficiency']
    PNG_data["png_RS"]=PNG_data["png_consumption"]*PNG_data['Unit cost']*30 #30 days
    PNG_water_heater_eff=PNG_data['Thermal Efficiency'].mean()# fo water heater
    PNG_cost=PNG_data["png_RS"].mean()
    PNG_cost_annual = PNG_cost * 12
    PNG_CONSUMPTON_KWH=PNG_data["png_consumption"].mean()
    PNG_time = df_time * PNG_data["time_conversion"][0]
    PNG_efficiency = PNG_data['Thermal Efficiency'][0]
    PNG_capex = PNG_data['Capex'][0]
    PNG_emission = PNG_data['Unit carbon emission'][0]
    PNG_emission_annual = PNG_emission * PNG_CONSUMPTON_KWH * 365 * 0.9
    PNG_ihap = PNG_data['Daily IHAP (PM2.5)'][0]
    PNG_pbp = PNG_capex / (current_cost_annual - PNG_cost_annual)

    #########Biogas#########
    Biogas_data=stove_file1[stove_file1["Fuel"] == 'Biogas']
    Biogas_data["Biogas_consumption"]=total_energy_induction/Biogas_data['Thermal Efficiency']
    Biogas_data["Biogas_RS"]=Biogas_data["Biogas_consumption"]*Biogas_data['Unit cost']*30 #30 days
    Biogas_water_heater_eff=Biogas_data['Thermal Efficiency'].mean()# for water heater
    Biogas_cost=Biogas_data["Biogas_RS"].mean()
    Biogas_cost_annual = Biogas_cost * 12
    Biogas_CONSUMPTION_KWH=Biogas_data["Biogas_consumption"].mean()
    Biogas_time = df_time * Biogas_data["time_conversion"][0]
    Biogas_efficiency = Biogas_data['Thermal Efficiency'][0]
    Biogas_capex = Biogas_data['Capex'][0]
    Biogas_emission = Biogas_data['Unit carbon emission'][0]
    Biogas_emission_annual = Biogas_emission * Biogas_CONSUMPTION_KWH * 365 * 0.9
    Biogas_ihap = Biogas_data['Daily IHAP (PM2.5)'][0]
    Biogas_pbp = Biogas_capex / (current_cost_annual - Biogas_cost_annual)

    #########Fire Wood#########
    Fire_Wood_data=stove_file1[stove_file1["Fuel"] == 'Firewood']
    Fire_Wood_data["Fire_Wood_consumption"]=total_energy_induction/Fire_Wood_data['Thermal Efficiency']
    Fire_Wood_data["Fire_Wood_RS"]=Fire_Wood_data["Fire_Wood_consumption"]*Fire_Wood_data['Unit cost']*30 #30 days
    Fire_wood_water_heater_eff=Fire_Wood_data['Thermal Efficiency'].mean()# for water heater
    Fire_Wood_cost=Fire_Wood_data["Fire_Wood_RS"].mean()
    Fire_Wood_cost_annual = Fire_Wood_cost * 12
    Fire_Wood_consumption_KWH=Fire_Wood_data["Fire_Wood_consumption"].mean()
    Firewood_time = df_time * Fire_Wood_data["time_conversion"][0]
    Firewood_efficiency = Fire_Wood_data['Thermal Efficiency'].mean()
    Firewood_capex = Fire_Wood_data['Capex'].mean()
    Firewood_emission = Fire_Wood_data['Unit carbon emission'][0]
    Firewood_emission_annual = Firewood_emission * Fire_Wood_consumption_KWH * 365 * 0.9
    Firewood_ihap = Fire_Wood_data['Daily IHAP (PM2.5)'][0]
    Firewood_pbp = Firewood_capex / (current_cost_annual - Fire_Wood_cost_annual)

    #########Livestock Waste#########
    Livestock_Waste_data=stove_file1[stove_file1["Fuel"] == 'Livestock Waste']
    Livestock_Waste_data["Livestock Waste_consumption"]=total_energy_induction/Livestock_Waste_data['Thermal Efficiency']
    Livestock_Waste_data["Livestock Waste_RS"]=Livestock_Waste_data["Livestock Waste_consumption"]*Livestock_Waste_data['Unit cost']*30 #30 days
    Livestock_Waste_cost=Livestock_Waste_data["Livestock Waste_RS"].mean()
    Livestock_Waste_cost_annual = Livestock_Waste_cost * 12
    Livestock_Waste_consumption_KWH=Livestock_Waste_data["Livestock Waste_consumption"].mean()
    Livestock_Waste_time = df_time * Livestock_Waste_data["time_conversion"][0]
    Livestock_Waste_efficiency = Livestock_Waste_data['Thermal Efficiency'][0]
    Livestock_capex = Livestock_Waste_data['Capex'].mean()
    Livestock_emission = Livestock_Waste_data['Unit carbon emission'][0]
    Livestock_emission_annual = Livestock_emission * Livestock_Waste_consumption_KWH * 365 * 0.9
    Livestock_ihap = Livestock_Waste_data['Daily IHAP (PM2.5)'][0]
    Livestock_pbp = Livestock_capex / (current_cost_annual - Livestock_Waste_cost_annual)

    ############average of firewood and livestocks#########
    firewood_livestock_cost_average=(Livestock_Waste_cost+Fire_Wood_cost)/2
    firewood_livestock_time = (Firewood_time+ Livestock_Waste_time)/2
    firewood_livestock_efficiency = (Firewood_efficiency + Livestock_Waste_efficiency)/2
    firewood_livestock_capex = (Firewood_capex + Livestock_capex)/2
    firewood_livestock_emission = (Firewood_emission + Livestock_emission)/2
    firewood_livestock_emission_annual = (Firewood_emission_annual + Livestock_emission_annual)/2
    firewood_livestock_ihap = (Firewood_ihap + Livestock_ihap) / 2
    firewood_livestock_pbp = (Firewood_pbp + Livestock_pbp) / 2

    ###
    # Update for induction (1 burner) only use case
    ###

    #______________Results SHOWING TO USER______________________
    with result_container:
        change_str2 = lambda v : '+' if v > 0 else '-'

        # st.header('_Energy Costs_')
        # st.subheader('Unit cost (INR/kWh)')
        # # st.markdown("## Unit cost (INR/kWh)")
        # c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
        # with c1:
        #     st.metric('Present Cost', f"₹{(current_cost/total_energy_user)/30:,.2f}",help="currently you have selected " +str(selection_of_stoves))
        # with c2:
        #     st.metric('Electric Induction', f"₹{electricity_tariff:,.2f}", help = 'Reference')
        # with c3:
        #     st.metric('Solar Induction', f"₹{0:,.2f}")
        # with c4:
        #     st.metric('LPG', f"₹{6.38:,.2f}")
        # with c5:
        #     st.metric('PNG', f"₹{5.86:,.2f}")
        # with c6:
        #     st.metric('Biogas', f"₹{1.5:,.2f}")
        # with c7:
        #     st.metric('Firewood & Livestock Waste', f"₹{1.32:,.2f}")  # AVERAGE of firewood and livestocks
        
        submit_button = st.button("Show Results")

        # Only execute code below if the submit button is clicked
        if submit_button:
            # st.write("Code execution after submit button is clicked.")

            st.subheader('Total operating cost for cooking (INR/month)')
            c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
            with c1:
                st.metric('Present Cost', f"₹{current_cost:,.0f}")
            with c2:
                dcost = -100*(current_cost - Grid_electricity_cost)/current_cost
                st.metric('Electric Induction', f"₹{Grid_electricity_cost:,.0f}", 
                delta=f"{change_str2(dcost)}₹{abs(current_cost - Grid_electricity_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
            with c3:
                dcost = -100*(current_cost - Solar_rooftop_cost)/current_cost
                st.metric('Solar Induction', f"₹{Solar_rooftop_cost:,.0f}", 
                delta=f"{change_str2(dcost)}₹{abs(current_cost - Solar_rooftop_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
            with c4:
                dcost = -100*(current_cost - LPG_cost)/current_cost
                st.metric('LPG', f"₹{LPG_cost:,.0f}", 
                delta=f"{change_str2(dcost)}₹{abs(current_cost - LPG_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse') 
            with c5:
                dcost = -100*(current_cost - PNG_cost)/current_cost
                st.metric('PNG', f"₹{PNG_cost:,.0f}", 
                delta=f"{change_str2(dcost)} ₹{abs(current_cost - PNG_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
            with c6:
                dcost = -100*(current_cost - Biogas_cost)/current_cost
                st.metric('Biogas', f"₹{Biogas_cost:,.0f}", 
                delta=f"{change_str2(dcost)} ₹{abs(current_cost - Biogas_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
            with c7:
                dcost = -100*(current_cost - firewood_livestock_cost_average)/current_cost
                st.metric('Firewood & Livestock Waste', f"₹{firewood_livestock_cost_average:,.0f}", 
                delta=f"{change_str2(dcost)} ₹{abs(current_cost - firewood_livestock_cost_average):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')

            # st.subheader('Percentage of cooking expenses with monthly income (%)')
            # c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
            # with c1:
            #     st.metric('Present Cost', f"{(current_cost/monthly_income)*100:,.2f}%")
            # with c2:
            #     st.metric('Electric Induction', f"{(Grid_electricity_cost/monthly_income)*100:,.2f}%")
            # with c3:
            #     st.metric('Solar Induction', f"{(Solar_rooftop_cost/monthly_income)*100:,.2f}%")
            # with c4:
            #     st.metric('LPG', f"{(LPG_cost/monthly_income)*100:,.2f}%")
            # with c5:
            #     st.metric('PNG', f"{(PNG_cost/monthly_income)*100:,.2f}%")
            # with c6:
            #     st.metric('Biogas', f"{(Biogas_cost/monthly_income)*100:,.2f}%")
            # with c7:
            #     st.metric('Firewood & Livestock Waste', f"{(firewood_livestock_cost_average/monthly_income)*100:,.2f}%")  # AVERAGE of firewood and livestocks

    
            # st.header('_Operating Specifics_')
            # st.subheader('Daily cooking duration (hours/day)')
            # c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
            # with c1:
            #     st.metric('Current Time', f"{current_time_daily:,.2f}")
            # with c2:
            #     st.metric('Electric Induction', f"{Grid_electricity_time:,.2f}")
            # with c3:
            #     st.metric('Solar Induction', f"{Solar_rooftop_time:,.2f}")
            # with c4:
            #     st.metric('LPG', f"{LPG_time:,.2f}")
            # with c5:
            #     st.metric('PNG', f"{PNG_time:,.2f}")
            # with c6:
            #     st.metric('Biogas', f"{Biogas_time:,.2f}")
            # with c7:
            #     st.metric('Firewood & Livestock Waste', f"{firewood_livestock_time:,.2f}")  # AVERAGE of firewood and livestocks

            # st.subheader('Daily energy consumption for cooking (kWh/day)')
            # c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
            # with c1:
            #     st.metric('Present Consumption', f"{total_energy:,.2f}")
            # with c2:
            #     st.metric('Electric Induction', f"{Grid_electricity_consumption_KWH:,.2f}")
            # with c3:
            #     st.metric('Solar Induction', f"{Solar_rooftop_consumption_kwh:,.2f}")
            # with c4:
            #     st.metric('LPG', f"{LPG_consumption_kwh:,.2f}")
            # with c5:
            #     st.metric('PNG', f"{PNG_CONSUMPTON_KWH:,.2f}")
            # with c6:
            #     st.metric('Biogas', f"{Biogas_CONSUMPTION_KWH:,.2f}")
            # with c7:
            #     st.metric('Firewood & Livestock Waste', f"{Fire_Wood_consumption_KWH:,.2f}")  # AVERAGE of firewood and livestocks

            # st.header('_Cookstove Characteristics_')
            # st.subheader('Thermal efficiency (%)')
            # c1, c2, c3,c4,c5,c6 = st.columns(6)
            # with c1:
            #     st.metric('Electric Induction', f"{Grid_electricity_efficiency:,.0%}",) 
            # with c2:
            #     st.metric('Solar Induction', f"{Solar_rooftop_efficiency:,.0%}",)
            # with c3:
            #     st.metric('LPG', f"{LPG_efficiency:,.0%}",)
            # with c4:
            #     st.metric('PNG', f"{PNG_efficiency:,.0%}",)
            # with c5:
            #     st.metric('Biogas', f"{Biogas_efficiency:,.0%}",)
            # with c6:
            #     st.metric('Firewood', f"{Firewood_efficiency:,.0%}",)

            # st.subheader('Cookstove and equipment cost (INR)')
            # c1, c2, c3,c4,c5,c6 = st.columns(6)
            # with c1:
            #     st.metric('Electric Induction', f"₹{Grid_electricity_capex:,.0f}",) 
            # with c2:
            #     st.metric('Solar Induction', f"₹{Solar_rooftop_capex:,.0f}",)
            # with c3:
            #     st.metric('LPG', f"₹{LPG_capex:,.0f}",)
            # with c4:
            #     st.metric('PNG', f"₹{PNG_capex:,.0f}",)
            # with c5:
            #     st.metric('Biogas', f"₹{Biogas_capex:,.0f}",)
            # with c6:
            #     st.metric('Firewood', f"₹{Firewood_capex:,.0f}",)

            # st.header('_Social & Environmental Aspects_')
            # st.subheader('Unit carbon emission	(kgCO2eq./kWh)')
            # c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
            # with c1:
            #     st.metric('Current Emission Factor', f"{present_EF:,.2f}")
            # with c2:
            #     st.metric('Electric Induction', f"{Grid_electricity_emission:,.2f}",)
            # with c3:
            #     st.metric('Solar Induction', f"{Solar_rooftop_emission:,.2f}",) 
            # with c4:
            #     st.metric('LPG', f"{LPG_emission:,.2f}",)
            # with c5:
            #     st.metric('PNG', f"{PNG_emission:,.2f}",)
            # with c6:
            #     st.metric('Biogas',f"{Biogas_emission:,.2f}")
            # with c7:
            #     st.metric('Firewood & Livestock', f"{firewood_livestock_emission:,.2f}",)
            
            st.subheader('Annual carbon emission (kgCO2eq./year)')
            c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
            with c1:
                st.metric('Present Emissions', f"{(total_emissions_annual):,.0f}")
            with c2:
                st.metric('Electric Induction', f"{Grid_electricity_emission_annual:,.0f}",)
            with c3:
                st.metric('Solar Induction', f"{Solar_rooftop_emission_annual:,.0f}",) 
            with c4:
                st.metric('LPG', f"{LPG_emission_annual:,.0f}",)
            with c5:
                st.metric('PNG', f"{PNG_emission_annual:,.0f}",)
            with c6:
                st.metric('Biogas',f"{Biogas_emission_annual:,.0f}")
            with c7:
                st.metric('Firewood & Livestock', f"{firewood_livestock_emission_annual:,.0f}",)

            
            # social_carbon_cost = 86 * 82 * 0.001 # Social carbon cost is 86 USD per ton of CO2
            
            # st.subheader('Social carbon cost (INR/year)')
            # c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
            # with c1:
            #     st.metric('Present', f"₹{(total_emissions_annual * social_carbon_cost):,.0f}")
            # with c2:
            #     st.metric('Electric Induction', f"₹{Grid_electricity_emission_annual * social_carbon_cost:,.0f}",) 
            # with c3:
            #     st.metric('Solar Induction', f"₹{Solar_rooftop_emission_annual * social_carbon_cost:,.0f}",)
            # with c4:
            #     st.metric('LPG', f"₹{LPG_emission_annual * social_carbon_cost:,.0f}",)
            # with c5:
            #     st.metric('PNG', f"₹{PNG_emission_annual * social_carbon_cost:,.0f}",)
            # with c6:
            #     st.metric('Biogas', f"₹{Biogas_emission_annual * social_carbon_cost:,.0f}",) 
            # with c7:
            #     st.metric('Firewood & Livestock', f"₹{firewood_livestock_emission_annual * social_carbon_cost:,.0f}",)

            # st.header('_Health Impacts_')
            st.subheader('Daily Indoor Household Air Pollution (IHAP) [PM 2.5] (μg/m3)')
            c1, c2,c3,c4,c5,c6 = st.columns(6)
            with c1:
                st.metric('Electric Induction', f"{Grid_electricity_ihap:,.0f}",)
            with c2:
                st.metric('Solar Induction', f"{Solar_rooftop_ihap:,.0f}",)
            with c3:
                st.metric('LPG', f"{LPG_ihap:,.0f}",)
            with c4:
                st.metric('PNG', f"{PNG_ihap:,.0f}",)
            with c5:
                st.metric('Biogas', f"{Biogas_ihap:,.0f}",) 
            with c6:
                st.metric('Firewood & Livestock Waste', f"{firewood_livestock_ihap:,.0f}",)
            
            # st.subheader('Health Hazards')
            st.markdown('_The updated WHO guidelines state that annual average concentrations of PM2.5 should not exceed 5 µg/m3,' 
                        + ' while 24-hour average exposures should not exceed 15 µg/m3 more than 3 - 4 days per year._')

            # st.header('_Financing_')
            # st.subheader('Payback period (years)')
            # c1, c2, c3, c4, c5, c6 = st.columns(6)
            # with c1:
            #     st.metric('Electric Induction', f"{Grid_electricity_pbp:,.0f}",) 
            # with c2:
            #     st.metric('Solar Induction', f"{Solar_rooftop_pbp:,.0f}",)
            # with c3:
            #     st.metric('LPG', f"{LPG_pbp:,.0f}",)
            # with c4:
            #     st.metric('PNG', f"{PNG_pbp:,.0f}",) 
            # with c5:
            #     st.metric('Biogas', f"{Biogas_pbp:,.0f}",)  
            # with c6:
            #     st.metric('Firewood', f"{Firewood_pbp:,.0f}",) 

            # st.subheader('Annual opex savings	(INR)')
            # c1, c2, c3, c4, c5, c6 = st.columns(6)
            # with c1:
            #     st.metric('Electric Induction', f"₹{(current_cost_annual - Grid_electricity_cost_annual):,.0f}",) 
            # with c2:
            #     st.metric('Solar Induction', f"₹{(current_cost_annual - Solar_rooftop_cost_annual):,.0f}",)
            # with c3:
            #     st.metric('LPG', f"₹{(current_cost_annual - LPG_cost_annual):,.0f}",)
            # with c4:
            #     st.metric('PNG', f"₹{(current_cost_annual - PNG_cost_annual):,.0f}",) 
            # with c5:
            #     st.metric('Biogas', f"₹{(current_cost_annual - Biogas_cost_annual):,.0f}",)  
            # with c6:
            #     st.metric('Firewood', f"₹{(current_cost_annual - Fire_Wood_cost_annual):,.0f}",)

            with st.container():
                # Sample data
                data = {
                    'Unit cost (INR/kWh)': [(current_cost/total_energy_user)/30, electricity_tariff, 0, 6.38, 5.86, 1.5,1.32],
                    'Total operating cost for cooking (INR/month)': [f"{current_cost:,.0f}", f"{Grid_electricity_cost:,.0f}", f"{Solar_rooftop_cost:,.0f}",
                                                                    f"{LPG_cost:,.0f}", f"{PNG_cost:,.0f}", f"{Biogas_cost:,.0f}", f"{firewood_livestock_cost_average:,.0f}"],
                    'Percentage of cooking expenses with monthly income (%)': [f"{(current_cost/monthly_income):,.2%}", f"{(Grid_electricity_cost/monthly_income):,.2%}", 
                                                                            f"{(Solar_rooftop_cost/monthly_income):,.2%}", f"{(LPG_cost/monthly_income):,.2%}", 
                                                                            f"{(PNG_cost/monthly_income):,.2%}", f"{(Biogas_cost/monthly_income):,.2%}", 
                                                                            f"{(firewood_livestock_cost_average/monthly_income):,.2%}"],
                    'Daily cooking duration (hours/day)': [f"{current_time_daily:,.2f}", f"{Grid_electricity_time:,.2f}", f"{Solar_rooftop_time:,.2f}", 
                                                        f"{LPG_time:,.2f}", f"{PNG_time:,.2f}", f"{Biogas_time:,.2f}", f"{firewood_livestock_time:,.2f}"],
                    'Daily energy consumption for cooking (kWh/day)': [f"{total_energy:,.2f}", f"{Grid_electricity_consumption_KWH:.2f}", f"{Solar_rooftop_consumption_kwh:.2f}", 
                                                                f"{LPG_consumption_kwh:,.2f}",f"{PNG_CONSUMPTON_KWH:.2f}", f"{Biogas_CONSUMPTION_KWH:.2f}", f"{Fire_Wood_consumption_KWH:.2f}"],
                    'Thermal efficiency (%)': ['-',f"{Grid_electricity_efficiency:,.0%}", f"{Solar_rooftop_efficiency:,.0%}", f"{LPG_efficiency:,.0%}", 
                                            f"{PNG_efficiency:,.0%}", f"{Biogas_efficiency:,.0%}", f"{Firewood_efficiency:,.0%}"],
                    'Cookstove and equipment cost (INR)': ['NA',f"{Grid_electricity_capex:,.0f}", f"{Solar_rooftop_capex:,.0f}", f"{LPG_capex:,.0f}", f"{PNG_capex:,.0f}",
                                                        f"{Biogas_capex:,.0f}",  f"{Firewood_capex:,.0f}"],
                    'Unit carbon emission (kgCO2eq./kWh)' : [f"{present_EF:.2f}", f"{Grid_electricity_emission:.2f}", f"{Solar_rooftop_emission:.2f}", f"{LPG_emission:.2f}", 
                                                            f"{PNG_emission:.2f}", f"{Biogas_emission:.2f}", f"{firewood_livestock_emission:.2f}"],
                    'Annual carbon emission (kgCO2eq./year)' : [f"{total_emissions_annual:.2f}", f"{Grid_electricity_emission_annual:.2f}", f"{Solar_rooftop_emission_annual:.2f}", 
                                                                f"{LPG_emission_annual:.2f}", f"{PNG_emission_annual:.2f}", f"{Biogas_emission_annual:.2f}", f"{firewood_livestock_emission_annual:.2f}"],
                    'Social carbon cost (INR/year)' : [f"{(total_emissions_annual * social_carbon_cost):,.0f}",  f"{Grid_electricity_emission_annual * social_carbon_cost:,.0f}",
                                                        f"{Solar_rooftop_emission_annual * social_carbon_cost:,.0f}",  f"{LPG_emission_annual * social_carbon_cost:,.0f}",
                                                            f"{PNG_emission_annual * social_carbon_cost:,.0f}",  f"{Biogas_emission_annual * social_carbon_cost:,.0f}",
                                                                f"{firewood_livestock_emission_annual * social_carbon_cost:,.0f}"],
                    'Daily IHAP [PM 2.5] (μg/m3)' : ['NA', f"{Grid_electricity_ihap:,.0f}",  f"{Solar_rooftop_ihap:,.0f}",  f"{LPG_ihap:,.0f}",  f"{PNG_ihap:,.0f}",
                                                    f"{Biogas_ihap:,.0f}",  f"{firewood_livestock_ihap:,.0f}"],

                    'Annual opex savings (INR)' : ['NA', f"{(current_cost_annual - Grid_electricity_cost_annual):,.0f}",  f"{(current_cost_annual - Solar_rooftop_cost_annual):,.0f}",
                                                    f"{(current_cost_annual - LPG_cost_annual):,.0f}",  f"{(current_cost_annual - PNG_cost_annual):,.0f}",  f"{(current_cost_annual - Biogas_cost_annual):,.0f}",
                                                        f"{(current_cost_annual - Fire_Wood_cost_annual):,.0f}"],
                    # 'Payback period (years)' : ['NA',f"{Grid_electricity_pbp:,.0f}", f"{Solar_rooftop_pbp:,.0f}", f"{LPG_pbp:,.0f}",  f"{PNG_pbp:,.0f}",  f"{Biogas_pbp:,.0f}",
                                                #   f"{Firewood_pbp:,.0f}"],
                    'Payback period (years)': ['NA','NA' if Grid_electricity_pbp > 15 else f"{Grid_electricity_pbp:,.2f}",
                                    'NA' if Solar_rooftop_pbp > 15 else f"{Solar_rooftop_pbp:,.2f}",
                                    'NA' if LPG_pbp > 15 else f"{LPG_pbp:,.2f}",
                                    'NA' if PNG_pbp > 15 else f"{PNG_pbp:,.2f}",
                                    'NA' if Biogas_pbp > 15 else f"{Biogas_pbp:,.2f}",
                                    'NA' if Firewood_pbp > 15 else f"{Firewood_pbp:,.2f}"]
                }
                df = pd.DataFrame(data)

                # Available variables for x and y
                available_variables = list(df.columns)

                # Select x and y variables
                x_variable =['Present - '+str(selection_of_stoves),'Electric Induction', 'Solar Induction', 'LPG', 'PNG', 'Biogas','Firewood']
                y_variable = st.selectbox('**Select a parameter**', available_variables)
                df['cooking stoves']=x_variable
                # Filter DataFrame based on selected x_variable and y_variable

                c1,c2= st.columns([5,3],gap="small")
                    # Generate bar plot
                    # Generate bar plot using Plotly
                with c1:
                    fig = px.bar(df, x='cooking stoves', y=y_variable)

                    # Rotate x-axis labels by 45 degrees
                    fig.update_layout(xaxis_tickangle = -45)

                    # Add tooltips for each bar
                    fig.update_traces(hovertemplate = 'Value: %{y}')

                    # Set x-axis label 
                    fig.update_layout(xaxis_title = 'Cooking Fuel')
                    # Set y-axis label
                    fig.update_layout(yaxis_title = y_variable)

                    st.plotly_chart(fig)
                with c2:
                    df_filtered = df[['cooking stoves', y_variable]].copy()
                    df_filtered.rename(columns={'cooking stoves': 'Cooking Fuel'}, inplace=True)
                    # df_filtered['cooking stoves'] = x_variable
                    df_filtered.reset_index()
                    df_filtered = df_filtered.set_index('Cooking Fuel')
                    # Display DataFrame as a table
                    st.dataframe(df_filtered)

                    # Save DataFrame as CSV
                    csv_data = df_filtered.to_csv(index=True)
                    st.download_button("Download CSV", data=csv_data, file_name="filtered_data.csv", mime="text/csv")

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
about_markdown = '''Development Team - Bikash Sahu, Vikas Kumar.
    For further details contact bikash@vasudhaindia.org.
    This analysis is a part of Deep Electrification initiative by Vasudha Foundation with support from SED Fund.'''
st.set_page_config(page_title = 'Cooking Energy Tool', page_icon = '🍛',layout="wide", menu_items={'Get Help': None, 'Report a Bug': None, 'About': about_markdown})
col1, col2 = st.columns([7,1])
with col2:
    language_select =st.selectbox("Select Language",["English","Hindi"])
if language_select=="Hindi":

    #import file 
    energy_cooking = pd.read_excel('cooking_energy.xlsx',sheet_name='खाना पकाने की ऊर्जा',index_col=(0))
    electricity_tariff_file = pd.read_excel('cooking_energy.xlsx',sheet_name='बिजली दर',index_col=(0))
    stove_file = pd.read_excel('cooking_energy.xlsx',sheet_name='चूल्हे',index_col=(0))

    social_carbon_cost = 86 * 82.32 * 0.001 # Social carbon cost is 86 USD per ton of CO2

    # #____________ Page info________________________________________
    # about_markdown = 'Development Team - Bikash Sahu, Vikas Kumar.' + \
    # 'For further details contact bikash@vasudhaindia.org.' + 
    # 'This analysis is a part of Deep Electrification initiative by Vasudha Foundation with support from SED Fund.'




    # Set the page layout to be responsive
    

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
    # title_trans = translator.translate('Techno Economic Analysis of Cooking Technologies', dest='hi') 
    col2.title('खाना पकाने की प्रौद्योगिकियों का तकनीकी आर्थिक विश्लेषण')

    col2.write('अपनी विशिष्ट खाना पकाने की जरूरतों का चयन करने के लिए इस वेब ऐप का अन्वेषण करें और भारतीय बाजार में उपलब्ध विभिन्न खाना पकाने के समाधानों की व्यापक तुलना की खोज करें।')

    # extracting data from datafile (excel)
    State_list = electricity_tariff_file['राज्य'].tolist()
    energy_source_list = stove_file['ईंधन'].unique().tolist()

    #burners or stoves list
    firewood_stove=[ "पारंपरिक कुक स्टोव (टीसीएस)","बेहतर कुक स्टोव (आईसीएस - प्राकृतिक)","बेहतर कुक स्टोव (आईसीएस - मजबूर)"]
    livestock_stove=[ "पारंपरिक कुक स्टोव (टीसीएस)", "बेहतर कुक स्टोव (आईसीएस - प्राकृतिक)","बेहतर कुक स्टोव (आईसीएस - मजबूर)"]
    lpg_stove=["एलपीजी (2 बर्नर)"]
    png_stove=["पीएनजी (2 बर्नर)"]
    bio_gas_stove=["बायोगैस (2 बर्नर)"]
    grid_electricity_stove=["विद्युत प्रेरण (1 burner)", "विद्युत प्रेरण (2 बर्नर)", "Electric Pressure Cooker"]
    microgrid_electricity_stove=["विद्युत प्रेरण (1 burner)", "विद्युत प्रेरण (2 बर्नर)", "Electric Pressure Cooker"]



    tab1, tab2 = st.tabs(["उपयोगकर्ता का चयन", "अधिक जानकारी"])
    with tab2:

        
        with st.expander('इलेक्ट्रिक इंडक्शन और इसके लाभों के बारे में अधिक जानकारी'):
            st.markdown("""
                * **खाना पकाने का समय कम हो जाता है:**  इंडक्शन कुकटॉप पारंपरिक इलेक्ट्रिक या गैस कुकटॉप की तुलना में बहुत तेजी से गर्म होते हैं। ऐसा इसलिए है क्योंकि गर्मी कुकटॉप के बजाय सीधे पैन में उत्पन्न होती है।
                * **सटीक तापमान नियंत्रण:**  इंडक्शन कुकटॉप सटीक तापमान नियंत्रण प्रदान करते हैं, जो नाजुक व्यंजनों के लिए आदर्श है या जब आपको लंबे समय तक कुछ उबालने की आवश्यकता होती है।
                * **दक्षता:**  इंडक्शन कुकटॉप बहुत कुशल हैं, जिसका अर्थ है कि वे पारंपरिक कुकटॉप की तुलना में कम ऊर्जा का उपयोग करते हैं। यह आपको अपने ऊर्जा बिलों पर पैसे बचा सकता है।
                * **सुरक्षा:**  इंडक्शन कुकटॉप बहुत सुरक्षित हैं। कोई खुली लौ या गर्म सतह नहीं है, इसलिए जलने या आग लगने का खतरा कम है।
                * **आसान सफाई:**  इंडक्शन कुकटॉप को साफ करना बहुत आसान है। कुकटॉप की चिकनी सतह इसे पोंछना आसान बनाती है, और चिंता करने के लिए कोई रिसाव या छींटे नहीं हैं।
                """ )

        st.subheader("भोजन पकाने के लिए ऊर्जा की खपत")
        st.markdown('इलेक्ट्रिक खाना पकाने के लिए भोजन ऊर्जा खपत धारणाएं निम्नलिखित तालिका में प्रदान की गई हैं। कृपया ध्यान दें कि उल्लिखित मूल्यों को 4 से 5 व्यक्तियों वाले घर के लिए माना जाता है। अन्य खाना पकाने के ईंधन के लिए भोजन ऊर्जा खपत का अनुमान नीचे उल्लिखित थर्मल दक्षता के आधार पर लगाया गया है।')
        st.dataframe(energy_cooking.iloc[:,[1,2,3]].round({'समय (मिनट)':0, 'ऊर्जा (kWh)':2}))
        st.markdown('स्रोत:  https://mecs.org.uk/wp-content/uploads/2022/03/India-eCookbook-21-compressed.pdf')
        # rounded_energy_cooking = energy_cooking.iloc[:, [1, 2, 3]].round({'Column1Name': 0, 'Column3Name': 2})

        
        st.subheader("कुकस्टोव विशेषताएं")
        stove_char = {
            'चूल्हा प्रकार': ['पारंपरिक खुदाई चूल्हा','सुधारित चूल्हा (प्राकृतिक)','सुधारित चूल्हा (बलपूर्वक)','बायोगैस (2 बर्नर)',
                            'पीएनजी (2 बर्नर)','"एलपीजी" (2 बर्नर)','इलेक्ट्रिक इंडक्शन (1 बर्नर)','इलेक्ट्रिक इंडक्शन (2 बर्नर)','इंडोर सोलर कुकिंग सॉल्यूशन (1 बर्नर)','इंडोर सोलर कुकिंग सॉल्यूशन (2 बर्नर)'],
            'जीवन (साल)': [1, 4, 4, 10, 10, 10, 10, 10, 10, 10],
            'उष्मीय कुशलता (प्रतिशत)': ['15%', '20%', '30%', '60%', '60%', '60%', '80%', '80%', '80%', '80%'],
            'Capex (INR)': ['0','1,250','2,000','50,000','2,000','1,500','2,000','4,000','40,000','1,00,000'],
            'यूनिट लागत (INR/kWh)': ['1.41','1.34','1.27','1.5','4.77','4.98','बिजली दर के आधार पर','बिजली दर के आधार पर','0','0']
        }
        stove_char_df = pd.DataFrame(stove_char)
        stove_char_df = stove_char_df.set_index('चूल्हा प्रकार')
        st.dataframe(stove_char_df)
        # st.markdown('Source: http://164.100.94.214/national-biomass-cookstoves-programme, https://mnre.gov.in/img/documents/uploads/77e0a45feb0c4ce4974a0429d1e39001.pdf, https://beestarlabel.com/Content/Files/Final_LPG_schedule.pdf, https://beestarlabel.com/Content/Files/Schedule_Induction_hobs.pdf')
        st.markdown('स्रोत: ')
        st.markdown(' http://164.100.94.214/national-biomass-cookstoves-programme')
        st.markdown(' https://mnre.gov.in/img/documents/uploads/77e0a45feb0c4ce4974a0429d1e39001.pdf')
        st.markdown(' https://beestarlabel.com/Content/Files/Final_LPG_schedule.pdf')
        st.markdown(' https://beestarlabel.com/Content/Files/Schedule_Induction_hobs.pdf')



        st.subheader("कार्बन उत्सर्जन कारक")
        carbon_ef = {
            'ईंधन प्रकार': ['बायोमास (कुद्दूकट और पशुगोबर मल)', 'बायोगैस', 'एलपीजी', 'पीएनजी', 'ग्रिड बिजली', 'सोलर पीवी छत'],
            'यूनिट कार्बन उत्सर्जन (किलोग्राम कार्बन डाइऑक्साइड संवादित/किलोवॉट-घंटा)': [0.4, 0.15, 0.23, 0.2, 0.72, 0],
        }

        carbon_ef_df = pd.DataFrame(carbon_ef)
        carbon_ef_df = carbon_ef_df.set_index('ईंधन प्रकार')
        st.dataframe(carbon_ef_df)
        st.markdown('स्रोत: ')
        st.markdown('https://acp.copernicus.org/articles/18/15169/2018/acp-18-15169-2018.pdf')
        st.markdown('https://www.mdpi.com/2073-4433/10/12/729')
        st.markdown('https://cea.nic.in/cdm-co2-baseline-database')
        st.markdown('https://www.sciencedirect.com/science/article/abs/pii/S0301421513010719')

        st.subheader("कार्बन की सामाजिक लागत")
        st.write('सामाजिक कार्बन लागत 86 अमेरिकी डॉलर प्रति टन CO2 मानी गई है। USD से INR रूपांतरण 1 अप्रैल 2023 से 31 अगस्त 2023 तक संदर्भ दरों का औसत है')

        st.markdown('स्रोत: ')
        st.markdown('https://www.rff.org/publications/explainers/social-cost-carbon-101/')
        st.markdown('https://www.downtoearth.org.in/dte-infographics/social_cost_corbon/index.html')
        st.markdown('https://www.rbi.org.in/scripts/ReferenceRateArchive.aspx')

        st.subheader("भारतीय राज्यों की राज्यवार ग्रिड विद्युत टैरिफ")
        el_tariff_rates = pd.DataFrame(electricity_tariff_file.iloc[:,[0,1,2,3,4]].round(2))
        el_tariff_rates = el_tariff_rates.set_index("राज्य")
        st.dataframe(el_tariff_rates)
        st.markdown('स्रोत:  DISCOMs Electricity Tariff Orders of 2021-22 and 2022-23')
        
        st.subheader("दैनिक IHAP")
        ihap = {
        'चूल्हा प्रकार': ["पारंपरिक कुक स्टोव (टीसीएस)","बेहतर कुक स्टोव (आईसीएस - प्राकृतिक)","बेहतर कुक स्टोव (आईसीएस - मजबूर)",
                    'बायोगैस (2 बर्नर)','PNG (2 बर्नर)','"एलपीजी" (2 बर्नर)','विद्युत प्रेरण','Electric Pressure Cooker'],
        'दैनिक IHAP - PM 2.5 (μg/m3)': [1230, 410, 165, 60, 47, 64, 47, 35],
        }
        ihap_df = pd.DataFrame(ihap)
        ihap_df = ihap_df.set_index('चूल्हा प्रकार')
        st.dataframe(ihap_df)
        st.markdown('स्रोत: ')
        st.markdown('https://www.sciencedirect.com/science/article/pii/S0160412018324772')
        st.markdown('https://www.researchgate.net/publication/337429023_In-Field_Emission_Measurements_from_Biogas_and_Liquified_Petroleum_Gas_LPG_Stoves')
        st.markdown('https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-020-09865-1')
        st.markdown('https://www.isid.ac.in/~epu/dispapers/dp22_04.pdf') 
        st.markdown('https://www.jstor.org/stable/resrep21836.8') 
        st.markdown('https://thermopedia.com/content/10255/')

        st.subheader('परिवार की वार्षिक आय')
        income = {
            'क्षेत्र प्रकार': ['ग्रामीण','ग्रामीण','ग्रामीण','शहरी','शहरी','शहरी'],
            'सामाजिक-आर्थिक स्तर': ['निचला','मध्यम','उच्च','निचला','मध्यम','उच्च'],
            'वार्षिक आय (भारतीय रुपये)': ['2,00,000','5,70,000','9,00,000','2,50,000','7,12,500','11,25,000']
        }
        income_df = pd.DataFrame(income)
        income_df = income_df.set_index('क्षेत्र प्रकार')
        st.dataframe(income_df)
        st.markdown('स्रोत:  India Residential Energy Survey (IRES) 2020')




    with tab1:
        #_______________basic settings_________________________________________
        st.subheader("घरेलू रूपरेखा", help = 'उपयोगकर्ता को घरेलू रूपरेखा को पूरा करने के लिए निम्नलिखित विवरण का चयन करना होगा।')
        c1, c2 = st.columns(2)
        with c1: 
            state_select = st.selectbox('राज्य चुनें', State_list, help = 'भारत में उस राज्य का चयन करें जिसके लिए आप खाना पकाने के समाधान की तुलना करना चाहते हैं।')
            with st.container():
                area_select = st.selectbox('क्षेत्र का प्रकार', ('ग्रामीण','शहरी'), help = 'क्षेत्र प्रकार का चयन करें. शहरी क्षेत्र आमतौर पर नगर निगमों, नगर परिषदों या नगर समितियों द्वारा शासित होते हैं, जबकि ग्रामीण क्षेत्र पंचायतों (ग्राम-स्तरीय स्व-शासन निकायों) के अधिकार क्षेत्र में आते हैं।')
            monthly_income = st.number_input('मासिक आय दर्ज करें', min_value=0, max_value=1000000, value=30000, step=1000, help = 'कृपया परिवार की मासिक आय का उल्लेख करें। खाना पकाने के खर्च के हिस्से का अनुमान लगाने के लिए यह आवश्यक है।')
            interest_rate = st.number_input('वार्षिक ब्याज दर', min_value=0, max_value=20, value=5, step=1, help = "कृपया उधारकर्ता द्वारा पेश किए जाने वाले पाकन समाधानों के लिए वार्षिक ब्याज दर शर्तों का उल्लेख करें, जैसे कि बायोगैस और सौर ऊर्जा से चलने वाले कुकस्टोव्स जैसे बड़े आगे के खर्च।")
        annual_income = monthly_income * 12
        with c2:
            with st.container():
                cooking_source_options = energy_source_list
                cooking_source_select = st.multiselect('खाना पकाने के ईंधन का उपयोग', cooking_source_options, default=['ग्रिड बिजली'], help = 'वर्तमान उपयोग किए जाने वाले खाना पकाने के ईंधन का चयन करें।')
                filtered_stoves = stove_file.loc[stove_file['ईंधन'].isin(cooking_source_select), 'स्टोव'].unique().tolist()
                # cookstove_select = st.multiselect('Cookstove Used', filtered_stoves, default=['Electric Induction (1 burner)'], help = 'Select the cookstoves used' + 
                #                                   ' in the household.')
                cookstove_select = st.multiselect('खाना पकाने के लिए का उपयोग किया गया स्टोव', filtered_stoves, help = 'घर में उपयोग किए जाने वाले स्टोव का चयन करें।')  
                lpg_subsidy = st.selectbox('क्या आप एलपीजी सब्सिडी के लिए पात्र हैं?', ("नहीं",'हां'), help = 'यह समझने के लिए आवश्यक है कि क्या आपको घरेलू खाना पकाने के प्रयोजनों के लिए सब्सिडी की आवश्यकता होगी।') 
                loan_tenure = st.selectbox('वर्षों में ऋण अवधि चुनें।', (1,2,3,4,5), help = "इसके लिए उपयुक्त वित्तीय विकल्पों की गणना करने के लिए यह महत्वपूर्ण है, जैसे कि बायोगैस और सौर ऊर्जा से चलने वाले कुकस्टोव्स जैसे बड़े आगे के खर्च।") 

        if area_select=='ग्रामीण':
            if annual_income < 200000:
                category = "BoP"
            elif annual_income < 570000:
                category = "निचला"
            elif annual_income < 900000:
                category = "मध्यम"
            else:
                category = "उच्च"
        else:
            if annual_income < 250000:
                category = "BoP"
            elif annual_income < 712500:
                category = "निचला"
            elif annual_income < 1125000:
                category = "मध्यम"
            else:
                category = "उच्च"

        # Filter the DataFrame based on the selected state
        electricity_tariff = electricity_tariff_file[electricity_tariff_file["राज्य"] == state_select]

        if not electricity_tariff.empty:
            # Select the tariff value from the filtered DataFrame
            electricity_tariff = electricity_tariff.iloc[0][category]
        else:
            electricity_tariff = None
    # Stoves lists
        stove_file_list = stove_file[stove_file["क्षेत्र"] == area_select]
        stove_file_list = stove_file_list[stove_file_list["सामाजिक-आर्थिक"] == category]
        stove_file_list = stove_file_list[stove_file_list["ईंधन"].isin(cooking_source_select)]
        # stove_file_list
        # extracting data from datafile (excel)
        stove_list = stove_file_list['स्टोव'].tolist()

        st.subheader("भोजन रूपरेखा", help='नीचे दिए गए दिन के भोजन के अनुसार अपने सामान्य खाना पकाने के संज्ञा का चयन करें')
        c1, c2, c3,c4 = st.columns(4)  
        with c1:
            st.write('नाश्ता')
            items = ["इडली", "पुरी", "रोटी", "दोसा", "चावल", "दाल", "सब्जी करी", "मांस करी", "सूखी सब्जी", "तला हुआ खाना"]
            # Create a form
            with st.form("my_form"):
                # Create a column for items
                quantity_bf = st.number_input('लोगों की संख्या', value =1, step =1 , format = "%d")
                items_column = st.multiselect("व्यंजन", items)
                # Create a column for the quantity
                quantities = {}
                energy_sources = {}
                for bf_item in items_column:
                    # quantity = st.number_input(f"For no. of people {bf_item}", key=f"bf_{bf_item}", value=1, step=1, format="%d")
                    quantities[bf_item] = quantity_bf
                    energy_source = st.selectbox(f"{bf_item} के लिए ऊर्जा स्रोत", cookstove_select, key=f"bf_{bf_item}_energy")
                    energy_sources[bf_item] = energy_source
                # If the user clicks the submit button, do something
                if st.form_submit_button("जमा करें"):
                    # Create a DataFrame from user input
                    user_response_breakfast_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                    user_response_breakfast_df['स्टोव'] = user_response_breakfast_df['व्यंजन'].map(energy_sources)
                    st.write("User input:")
                    st.dataframe(user_response_breakfast_df)
                user_response_breakfast_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                user_response_breakfast_df['स्टोव'] = user_response_breakfast_df['व्यंजन'].map(energy_sources)

        with c2:
            st.write('दोपहर का भोजन')
            items = ["रोटी", "चावल", "पुरी", "दाल", "सब्जी करी", "मांस करी", "सूखी सब्जी", "तला हुआ खाना"]
            # Create a form
            with st.form("my_form_lunch"):
                # Create a column for items
                quantity_lunch =  st.number_input('लोगों की संख्या', value =1, step =1 , format = "%d")
                items_column = st.multiselect("व्यंजन", items)
                # Create a column for the quantity
                quantities = {}
                energy_sources = {}
                for l_item in items_column:
                    # quantity = st.number_input(f"For no. of people {l_item}", key=f"l_{l_item}", value=1, step=1, format="%d")
                    quantities[l_item] = quantity_lunch
                    energy_source = st.selectbox(f"{l_item} के लिए ऊर्जा स्रोत", cookstove_select, key=f"l_{l_item}_energy")
                    energy_sources[l_item] = energy_source
                # If the user clicks the submit button, do something
                if st.form_submit_button("जमा करें"):
                    # Create a DataFrame from user input
                    user_response_lunch_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                    user_response_lunch_df['स्टोव'] = user_response_lunch_df['व्यंजन'].map(energy_sources)
                    st.write("User input:")
                    st.dataframe(user_response_lunch_df)
                user_response_lunch_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                user_response_lunch_df['स्टोव'] = user_response_lunch_df['व्यंजन'].map(energy_sources)

        with c3:
            st.write('रात का खाना')
            items = ["चावल", "रोटी", "दोसा", "इडली", "पुरी", "दाल", "सब्जी करी", "मांस करी", "सूखी सब्जी", "तला हुआ खाना"]
            # Create a form
            with st.form("my_form_dinner"):
                # Create a column for items
                quantity_dinner =  st.number_input('लोगों की संख्या', value =1, step =1 , format = "%d")
                items_column = st.multiselect("व्यंजन", items)
                # Create a column for the quantity
                quantities = {}
                energy_sources = {}
                for d_item in items_column:
                    # quantity = st.number_input(f"For no. of people {d_item}", key=f"d_{d_item}", value=1, step=1, format="%d")
                    quantities[d_item] = quantity_dinner
                    energy_source = st.selectbox(f"{d_item} के लिए ऊर्जा स्रोत", cookstove_select, key=f"d_{d_item}_energy")
                    energy_sources[d_item] = energy_source
                # If the user clicks the submit button, do something
                if st.form_submit_button("जमा करें"):
                    # Create a DataFrame from user input
                    user_response_dinner_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                    user_response_dinner_df['स्टोव'] = user_response_dinner_df['व्यंजन'].map(energy_sources)
                    st.write("User input:")
                    st.dataframe(user_response_dinner_df)
                user_response_dinner_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                user_response_dinner_df['स्टोव'] = user_response_dinner_df['व्यंजन'].map(energy_sources)

        with c4:
            st.write('हल्का नाश्ता या पेय पदार्थ')
            items = ["दूध", "चाय/कॉफी", "पकोड़ा", "समोसा", "पाव भाजी"]
            # Create a form
            with st.form("my_form_snacks"):
                # Create a column for items
                quantity_snacks =  st.number_input('लोगों की संख्या', value =1, step =1 , format = "%d")
                items_column = st.multiselect("व्यंजन", items)
                # Create a column for the quantity
                quantities = {}
                energy_sources = {}
                for ts_item in items_column:
                    # quantity = st.number_input(f"For no. of people {ts_item}", key=ts_item, value=1, step=1, format="%d")
                    quantities[ts_item] = quantity_snacks
                    energy_source = st.selectbox(f" {ts_item} के लिए ऊर्जा स्रोत",
                                                cookstove_select)
                    energy_sources[ts_item] = energy_source
                # If the user clicks the submit button, do something
                if st.form_submit_button("जमा करें"):
                    # Create a DataFrame from user input
                    user_response_snacks_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                    user_response_snacks_df['स्टोव'] = user_response_snacks_df['व्यंजन'].map(energy_sources)
                    st.write("User input:")
                    st.dataframe(user_response_snacks_df)
                user_response_snacks_df = pd.DataFrame(list(quantities.items()), columns=['व्यंजन', 'मात्रा (लोगों की संख्या)'])
                user_response_snacks_df['स्टोव'] = user_response_snacks_df['व्यंजन'].map(energy_sources)

        user_response_breakfast_df.columns = ['व्यंजन', 'मात्रा (लोगों की संख्या)','स्टोव']
        user_response_lunch_df.columns = ['व्यंजन', 'मात्रा (लोगों की संख्या)','स्टोव']
        user_response_dinner_df.columns = ['व्यंजन', 'मात्रा (लोगों की संख्या)','स्टोव']
        user_response_snacks_df.columns = ['व्यंजन', 'मात्रा (लोगों की संख्या)','स्टोव']


        # # Concatenate the DataFrames vertically
        user_response_df = pd.concat([user_response_breakfast_df, user_response_lunch_df, user_response_dinner_df,user_response_snacks_df], axis=0)


        result_container = st.container()


        #for induction
        df1=pd.merge(stove_file_list,user_response_df,  on=['स्टोव'])



    #################################need to change quantity
        df=pd.merge(energy_cooking, df1,  on=['व्यंजन'])
    ############################## add if else condition for stove selection ###################
    #add fuel condition on df
  


        selection_of_stoves=df['ईंधन'].unique()
        selection_of_stoves= ', '.join(selection_of_stoves)
    ################################
        ############for no of people
        no_of_people=df['मात्रा (लोगों की संख्या)'].tolist()
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
        df["लोगों की संख्या"] = new_people_list
        df["new time"] = new_time_list
        df['कुल मात्रा (ग्राम)'] = df['मात्रा (ग्राम)'] * df['लोगों की संख्या']

        df['कुल ऊर्जा आवश्यक (इलेक्ट्रिक इंडक्शन के लिए)'] = df['ऊर्जा (kWh)'] * df['लोगों की संख्या']
        df['कुल ऊर्जा आवश्यक'] = df['कुल ऊर्जा आवश्यक (इलेक्ट्रिक इंडक्शन के लिए)'] / df['ऊष्मीय दक्षता']
        contains_electricity_df = df[df['ईंधन'].str.contains('ग्रिड बिजली')]
        contains_electricity_df['RS(monthly)'] = contains_electricity_df['कुल ऊर्जा आवश्यक'] * electricity_tariff* 30 #30 days 

        does_not_contain_electricity_dff = df[~df['ईंधन'].str.contains('ग्रिड बिजली')]
        does_not_contain_electricity_dff['RS(monthly)'] = does_not_contain_electricity_dff['कुल ऊर्जा आवश्यक'] * does_not_contain_electricity_dff['इकाई लागत'] * 30     

        df=pd.concat([contains_electricity_df, does_not_contain_electricity_dff], axis=0)
        df['daily time'] = (df['समय (मिनट)'] * df["new time"] * df['time_conversion']) / 60
        df['emissions'] = df['कुल ऊर्जा आवश्यक'] * df['एकक कार्बन उत्सर्जन']
        total_emissions = df['emissions'].sum()
        total_emissions_annual = total_emissions * 365 * 0.9
        total_energy = df['कुल ऊर्जा आवश्यक'].sum()
        present_EF = total_emissions / total_energy
        current_time_daily=df['daily time'].sum()
        df_time = ((df["new time"]*df['समय (मिनट)']).sum())/60 #hours
        total_energy_user = df['कुल ऊर्जा आवश्यक'].sum()
        current_cost = df['RS(monthly)'].sum()
        current_cost_annual = current_cost * 12 
        total_energy_induction = df['कुल ऊर्जा आवश्यक (इलेक्ट्रिक इंडक्शन के लिए)'].sum()

        stove_file1=stove_file[stove_file["क्षेत्र"] == area_select]
        stove_file1=stove_file1[stove_file1["सामाजिक-आर्थिक"] == category]

        #########Grid_Electricity#########
        Grid_electricity_data = stove_file1[stove_file1["ईंधन"] == 'ग्रिड बिजली']

        Grid_electricity_data["Grid electricity_consumption"] = total_energy_induction/Grid_electricity_data['ऊष्मीय दक्षता']
        Grid_electricity_data["Grid electricity_RS"] = Grid_electricity_data["Grid electricity_consumption"]*electricity_tariff * 30 #30 days
        Grid_electricity_cost = Grid_electricity_data["Grid electricity_RS"].mean()
        Grid_electricity_cost_annual = Grid_electricity_cost * 12
        Grid_electricity_consumption_KWH = Grid_electricity_data["Grid electricity_consumption"].mean()

        Grid_electricity_time_conversion = Grid_electricity_data['time_conversion'][0]
        Grid_electricity_time = df_time * Grid_electricity_time_conversion
        Grid_electricity_efficiency = Grid_electricity_data['ऊष्मीय दक्षता'][0]

        Grid_electricity_capex = Grid_electricity_data['कैपेक्स'][1]
        Grid_electricity_emission = Grid_electricity_data['एकक कार्बन उत्सर्जन'][0]
        Grid_electricity_emission_annual = Grid_electricity_emission * Grid_electricity_consumption_KWH * 365 * 0.9
        Grid_electricity_ihap = Grid_electricity_data['दैनिक गणना (PM2.5)'][0]
        Grid_electricity_pbp = (Grid_electricity_capex) / (current_cost_annual - Grid_electricity_cost_annual)
        
        #########Solar Induction#########
        Solar_rooftop_data=stove_file1[stove_file1["ईंधन"] == 'सौर छत']
        Solar_rooftop_data["Solar rooftop_consumption"]=total_energy_induction/Solar_rooftop_data['ऊष्मीय दक्षता']
        Solar_rooftop_data["Solar rooftop_RS"]=Solar_rooftop_data["Solar rooftop_consumption"]*Solar_rooftop_data['इकाई लागत']*30 #30 days
        Solar_rooftop_cost=Solar_rooftop_data["Solar rooftop_RS"][0]
         
        Solar_rooftop_cost_annual = Solar_rooftop_cost * 12
        Solar_rooftop_consumption_kwh = Solar_rooftop_data["Solar rooftop_consumption"][0]
        Solar_rooftop_time_conversion = Solar_rooftop_data['time_conversion'][0]
        Solar_rooftop_time = df_time * Solar_rooftop_time_conversion
        Solar_rooftop_efficiency = Solar_rooftop_data['ऊष्मीय दक्षता'][0]
        Solar_rooftop_capex = Solar_rooftop_data['कैपेक्स'][0]
        Solar_rooftop_capex_token = Solar_rooftop_capex * 0.05
        Solar_rooftop_emission = Solar_rooftop_data['एकक कार्बन उत्सर्जन'][0]
        Solar_rooftop_emission_annual = Solar_rooftop_emission * Solar_rooftop_consumption_kwh * 365 * 0.9
        Solar_rooftop_ihap = Solar_rooftop_data['दैनिक गणना (PM2.5)'][0]
        Solar_rooftop_pbp = Solar_rooftop_capex / (current_cost_annual - Solar_rooftop_cost_annual)

        ### monthly easy financing
        Solar_rooftop_cost_princ = Solar_rooftop_capex - Solar_rooftop_capex_token
        # Calculate monthly interest rate
        monthly_interest_rate = (interest_rate / 100) / 12
        # Calculate total number of monthly payments
        total_payments = loan_tenure * 12
        # Calculate the monthly payment using the formula
        monthly_payment_solar = (Solar_rooftop_cost_princ * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
        
        #########"एलपीजी"#########
        LPG_data=stove_file1[stove_file1["ईंधन"] == "एलपीजी"]

        LPG_data["lpg_consumption"]=total_energy_induction/LPG_data['ऊष्मीय दक्षता']
        LPG_water_heater_eff=LPG_data['ऊष्मीय दक्षता'].mean()  # for water heater
        LPG_data["lpg_RS"]=LPG_data["lpg_consumption"]*LPG_data['इकाई लागत']*30 #30 days
        LPG_cost=LPG_data["lpg_RS"].mean()
        LPG_cost_annual = LPG_cost * 12
        LPG_consumption_kwh=LPG_data["lpg_consumption"].mean()
        LPG_time = df_time * LPG_data["time_conversion"][0]
        LPG_efficiency = LPG_data['ऊष्मीय दक्षता'][0]
        LPG_capex = LPG_data['कैपेक्स'][0]
        LPG_emission = LPG_data['एकक कार्बन उत्सर्जन'][0]
        LPG_emission_annual = LPG_emission * LPG_consumption_kwh * 365 * 0.9
        LPG_ihap = LPG_data['दैनिक गणना (PM2.5)'][0]
        LPG_pbp = LPG_capex / (current_cost_annual - LPG_cost_annual)


        #########PNG#########
        PNG_data=stove_file1[stove_file1["ईंधन"] == 'पीएनजी']
        PNG_data["png_consumption"]=total_energy_induction/PNG_data['ऊष्मीय दक्षता']
        PNG_data["png_RS"]=PNG_data["png_consumption"]*PNG_data['इकाई लागत']*30 #30 days
        PNG_water_heater_eff=PNG_data['ऊष्मीय दक्षता'].mean()# fo water heater
        PNG_cost=PNG_data["png_RS"].mean()
        PNG_cost_annual = PNG_cost * 12
        PNG_CONSUMPTON_KWH=PNG_data["png_consumption"].mean()
        PNG_time = df_time * PNG_data["time_conversion"][0]
        PNG_efficiency = PNG_data['ऊष्मीय दक्षता'][0]
        PNG_capex = PNG_data['कैपेक्स'][0]
        PNG_emission = PNG_data['एकक कार्बन उत्सर्जन'][0]
        PNG_emission_annual = PNG_emission * PNG_CONSUMPTON_KWH * 365 * 0.9
        PNG_ihap = PNG_data['दैनिक गणना (PM2.5)'][0]
        PNG_pbp = PNG_capex / (current_cost_annual - PNG_cost_annual)

        #########Biogas#########
        Biogas_data=stove_file1[stove_file1["ईंधन"] == 'बायोगैस']
        Biogas_data["Biogas_consumption"]=total_energy_induction/Biogas_data['ऊष्मीय दक्षता']
        Biogas_data["Biogas_RS"]=Biogas_data["Biogas_consumption"]*Biogas_data['इकाई लागत']*30 #30 days
        Biogas_water_heater_eff=Biogas_data['ऊष्मीय दक्षता'][0]# for water heater
        Biogas_cost=Biogas_data["Biogas_RS"][0]
        Biogas_cost_annual = Biogas_cost * 12
        Biogas_CONSUMPTION_KWH=Biogas_data["Biogas_consumption"][0]
        Biogas_time = df_time * Biogas_data["time_conversion"][0]
        Biogas_efficiency = Biogas_data['ऊष्मीय दक्षता'][0]
        Biogas_capex = Biogas_data['कैपेक्स'][0]
        Biogas_capex_token = Biogas_capex * 0.05
        Biogas_emission = Biogas_data['एकक कार्बन उत्सर्जन'][0]
        Biogas_emission_annual = Biogas_emission * Biogas_CONSUMPTION_KWH * 365 * 0.9
        Biogas_ihap = Biogas_data['दैनिक गणना (PM2.5)'][0]
        Biogas_pbp = Biogas_capex / (current_cost_annual - Biogas_cost_annual)


        ### monthly easy financing
        Biogas_cost_princ = Biogas_capex - Biogas_capex_token
        # Calculate monthly interest rate
        monthly_interest_rate = (interest_rate / 100) / 12
        # Calculate total number of monthly payments
        total_payments = loan_tenure * 12
        # Calculate the monthly payment using the formula
        biogas_monthly_payment = (Biogas_cost_princ * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
        

        #########Traditional Solid Biomass#########
        Biomass_data=stove_file1[stove_file1["ईंधन"] == 'पारंपरिक ठोस बायोमास']
        Biomass_data["Biomass_consumption"] = total_energy_induction/Biomass_data['ऊष्मीय दक्षता']
        Biomass_data["Biomass_RS"] = Biomass_data["Biomass_consumption"] * Biomass_data['इकाई लागत']*30 #30 days
        # Biomass_water_heater_eff=Biomass_data['ऊष्मीय दक्षता'].mean()# for water heater
        Biomass_cost = Biomass_data["Biomass_RS"][2]
        Biomass_cost_annual = Biomass_cost * 12
        Biomass_consumption_KWH = Biomass_data["Biomass_consumption"][2]
        Biomass_time = df_time * Biomass_data["time_conversion"][2]
        Biomass_efficiency = Biomass_data['ऊष्मीय दक्षता'][2]
        Biomass_capex = Biomass_data['कैपेक्स'][2]
        Biomass_emission = Biomass_data['एकक कार्बन उत्सर्जन'][2]
        Biomass_emission_annual = Biomass_emission * Biomass_consumption_KWH * 365 * 0.9
        Biomass_ihap = Biomass_data['दैनिक गणना (PM2.5)'][2]
        Biomass_pbp = Biomass_capex / (current_cost_annual - Biomass_cost_annual)


        #______________Results SHOWING TO USER______________________
        with result_container:
            change_str2 = lambda v : '+' if v > 0 else '-'


            fuel_list=df['ईंधन'].unique()

            # Check if specific words are in the list
            if 'बायोगैस' in fuel_list and 'सौर छत' in fuel_list:
                current_cost = df['RS(monthly)'].sum()+monthly_payment_solar+biogas_monthly_payment
                #result = "Both 'Solar rooftop' and 'gas' are in the list."
            elif 'सौर छत' in fuel_list:
                current_cost = df['RS(monthly)'].sum()+monthly_payment_solar
                #result = "'Solar rooftop' is in the list, but 'gas' is not."
            elif 'बायोगैस' in fuel_list:
                current_cost = df['RS(monthly)'].sum()+biogas_monthly_payment
                #result = "'gas' is in the list, but 'induction' is not."
            else:
                current_cost = df['RS(monthly)'].sum()
                #result = "Neither 'induction' nor 'gas' are in the list."

            # Print the result
            current_cost_annual = current_cost * 12 

            submit_button = st.button("परिणाम दिखाएँ")

            # Only execute code below if the submit button is clicked
            if submit_button:
                # st.write("Code execution after submit button is clicked.")

                st.subheader('खाना पकाने के लिए कुल परिचालन लागत (INR / माह)', help = 'यह खाना पकाने की ऊर्जा की मांग पर मासिक खर्च की एक सांकेतिक राशि है।')
                c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
                with c1:
                    st.metric('वर्तमान लागत', f"₹{current_cost:,.0f}")
                with c2:
                    dcost = -100*(current_cost - Grid_electricity_cost)/current_cost
                    st.metric('इलेक्ट्रिक इंडक्शन', f"₹{Grid_electricity_cost:,.0f}", 
                    delta=f"{change_str2(dcost)}₹{abs(current_cost - Grid_electricity_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                # with c3:
                #     dcost = -100*(current_cost - Solar_rooftop_cost)/current_cost
                #     st.metric('Indoor Solar Cooking Solution', f"₹{Solar_rooftop_cost:,.0f}", 
                #     delta=f"{change_str2(dcost)}₹{abs(current_cost - Solar_rooftop_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c3:
                    dcost = -100*(current_cost - monthly_payment_solar)/current_cost
                    st.metric('सौर कुकर', f"₹{monthly_payment_solar:,.0f}", 
                    delta=f"{change_str2(dcost)}₹{abs(current_cost - monthly_payment_solar):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c4:
                    dcost = -100*(current_cost - LPG_cost)/current_cost
                    st.metric('एलपीजी', f"₹{LPG_cost:,.0f}", 
                    delta=f"{change_str2(dcost)}₹{abs(current_cost - LPG_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse') 
                with c5:
                    dcost = -100*(current_cost - PNG_cost)/current_cost
                    st.metric('पीएनजी',f"₹{PNG_cost:,.0f}", 
                    delta=f"{change_str2(dcost)} ₹{abs(current_cost - PNG_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c6:
                    dcost = -100*(current_cost - (biogas_monthly_payment + Biogas_cost))/current_cost
                    st.metric('बायोगैस', f"₹{(biogas_monthly_payment + Biogas_cost):,.0f}", 
                    delta=f"{change_str2(dcost)} ₹{abs(current_cost - (biogas_monthly_payment + Biogas_cost)):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c7:
                    dcost = -100*(current_cost - Biomass_cost)/current_cost
                    st.metric('जैवभार', f"₹{Biomass_cost:,.0f}", 
                    delta=f"{change_str2(dcost)} ₹{abs(current_cost - Biomass_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')

                st.markdown('*इनडोर सोलर पाकन समाधान और बायोगैस के मासिक लागत को समाधानों की पूंजी लागत और वित्तीय लागत पर आधारित किया जाता है।*')

                
                st.subheader('वार्षिक कार्बन उत्सर्जन (kgCO2eq/वर्ष)', help = 'यह अनुमानित ऊर्जा खपत के कारण होने वाले कार्बन उत्सर्जन की एक सांकेतिक राशि है।')
                c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
                with c1:
                    st.metric('वर्तमान उत्सर्जन', f"{(total_emissions_annual):,.0f}")
                with c2:
                    st.metric('इलेक्ट्रिक इंडक्शन', f"{Grid_electricity_emission_annual:,.0f}",)
                with c3:
                    st.metric('सौर कुकर', f"{Solar_rooftop_emission_annual:,.0f}",) 
                with c4:
                    st.metric('एलपीजी', f"{LPG_emission_annual:,.0f}",)
                with c5:
                    st.metric('पीएनजी',f"{PNG_emission_annual:,.0f}",)
                with c6:
                    st.metric('बायोगैस',f"{Biogas_emission_annual:,.0f}")
                with c7:
                    st.metric('जैवभार', f"{Biomass_emission_annual:,.0f}",)

                


                # st.header('_Health Impacts_')
                st.subheader('दैनिक इनडोर घरेलू वायु प्रदूषण (आईएचएपी) [पीएम 2.5]', help = 'यह अनुमानित इनडोर वायु प्रदूषण है जो लंबे समय तक संपर्क में रहने पर स्वास्थ्य खतरों का कारण बनता है।')
                c1, c2,c3,c4,c5,c6 = st.columns(6)
                with c1:
                    # st.metric('Electric Induction', f"{Grid_electricity_ihap:,.0f}",)
                    st.metric('इलेक्ट्रिक इंडक्शन', f"{0:,.0f}",)
                with c2:
                    # st.metric('Indoor Solar Cooking Solution', f"{Solar_rooftop_ihap:,.0f}",)
                    st.metric('सौर कुकर', f"{0:,.0f}",)
                with c3:
                    st.metric('एलपीजी', f"{LPG_ihap:,.0f}",)
                with c4:
                    # st.metric('PNG', f"{PNG_ihap:,.0f}",)
                    st.metric('पीएनजी',f"{LPG_ihap:,.0f}",)
                with c5:
                    st.metric('बायोगैस', f"{Biogas_ihap:,.0f}",) 
                with c6:
                    st.metric('जैवभार', f"{Biomass_ihap:,.0f}",)
                
                # st.subheader('Health Hazards')
                st.markdown('डब्ल्यूएचओ के अद्यतन दिशानिर्देशों में कहा गया है कि पीएम 2.5 की वार्षिक औसत सांद्रता 5 μg / m3 से अधिक नहीं होनी चाहिए, जबकि 24 घंटे का औसत एक्सपोजर प्रति वर्ष 3 - 4 दिनों से अधिक 15 μg / m3 से अधिक नहीं होना चाहिए।')



            with st.container():
                # Sample data
                data = {
                    ' यूनिट लागत (INR/kWh)': [f"{(current_cost/total_energy_user)/30:,.2f}", f"{electricity_tariff:,.2f}", f"{0:,.2f}", 6.38, 5.86, f"{1.5:,.2f}",1.32],
                    'खाना पकाने के लिए कुल परिचालन लागत (INR / माह)': [f"{current_cost:,.0f}", f"{Grid_electricity_cost:,.0f}", f"{monthly_payment_solar:,.0f}",
                                                                    f"{LPG_cost:,.0f}", f"{PNG_cost:,.0f}", f"{(biogas_monthly_payment+Biogas_cost):,.0f}", f"{Biomass_cost:,.0f}"],
                    'मासिक आय के साथ खाना पकाने के खर्च का प्रतिशत (%)': [f"{(current_cost/monthly_income):,.2%}", f"{(Grid_electricity_cost/monthly_income):,.2%}", 
                                                                            f"{(Solar_rooftop_cost/monthly_income):,.2%}", f"{(LPG_cost/monthly_income):,.2%}", 
                                                                            f"{(PNG_cost/monthly_income):,.2%}", f"{(Biogas_cost/monthly_income):,.2%}", 
                                                                            f"{(Biomass_cost/monthly_income):,.2%}"],
                    'दैनिक खाना पकाने की अवधि (घंटे / दिन)': [f"{current_time_daily:,.2f}", f"{Grid_electricity_time:,.2f}", f"{Solar_rooftop_time:,.2f}", 
                                                        f"{LPG_time:,.2f}", f"{PNG_time:,.2f}", f"{Biogas_time:,.2f}", f"{Biomass_time:,.2f}"],
                    'खाना पकाने के लिए दैनिक ऊर्जा खपत (kWh / दिन)': [f"{total_energy:,.2f}", f"{Grid_electricity_consumption_KWH:.2f}", f"{Solar_rooftop_consumption_kwh:.2f}", 
                                                                f"{LPG_consumption_kwh:,.2f}",f"{PNG_CONSUMPTON_KWH:.2f}", f"{Biogas_CONSUMPTION_KWH:.2f}", f"{Biomass_consumption_KWH:.2f}"],
                    'तापीय कार्यक्षमता (%)': ['-',f"{Grid_electricity_efficiency:,.0%}", f"{Solar_rooftop_efficiency:,.0%}", f"{LPG_efficiency:,.0%}", 
                                            f"{PNG_efficiency:,.0%}", f"{Biogas_efficiency:,.0%}", f"{Biomass_efficiency:,.0%}"],
                    'खाना पकाने के स्टोव और उपकरण लागत (INR)': ['NA',f"{Grid_electricity_capex:,.0f}", f"{(Solar_rooftop_capex * 0.05):,.0f}", f"{LPG_capex:,.0f}", f"{PNG_capex:,.0f}",
                                                        f"{(Biogas_capex * 0.05):,.0f}",  f"{Biomass_capex:,.0f}"],
                    'इकाई कार्बन उत्सर्जन (kgCO2eq./kWh)' : [f"{present_EF:.2f}", f"{Grid_electricity_emission:.2f}", f"{Solar_rooftop_emission:.2f}", f"{LPG_emission:.2f}", 
                                                            f"{PNG_emission:.2f}", f"{Biogas_emission:.2f}", f"{Biomass_emission:.2f}"],
                    'वार्षिक कार्बन उत्सर्जन (kgCO2eq/वर्ष)' : [f"{total_emissions_annual:.0f}", f"{Grid_electricity_emission_annual:.0f}", f"{Solar_rooftop_emission_annual:.0f}", 
                                                                f"{LPG_emission_annual:.0f}", f"{PNG_emission_annual:.0f}", f"{Biogas_emission_annual:.0f}", f"{Biomass_emission_annual:.0f}"],
                    'सामाजिक कार्बन लागत (INR / वर्ष)' : [f"{(total_emissions_annual * social_carbon_cost):,.0f}",  f"{Grid_electricity_emission_annual * social_carbon_cost:,.0f}",
                                                        f"{Solar_rooftop_emission_annual * social_carbon_cost:,.0f}",  f"{LPG_emission_annual * social_carbon_cost:,.0f}",
                                                            f"{PNG_emission_annual * social_carbon_cost:,.0f}",  f"{Biogas_emission_annual * social_carbon_cost:,.0f}",
                                                                f"{Biomass_emission_annual * social_carbon_cost:,.0f}"],
                    'दैनिक IHAP [PM 2.5] (μg/m3)' : ['NA', f"{Grid_electricity_ihap:,.0f}",  f"{Solar_rooftop_ihap:,.0f}",  f"{LPG_ihap:,.0f}",  f"{PNG_ihap:,.0f}",
                                                    f"{Biogas_ihap:,.0f}",  f"{Biomass_ihap:,.0f}"],

                    'वार्षिक परिचालन बचत (INR)' : ['NA', f"{(current_cost_annual - Grid_electricity_cost_annual):,.0f}",  f"{(current_cost_annual - Solar_rooftop_cost_annual):,.0f}",
                                                    f"{(current_cost_annual - LPG_cost_annual):,.0f}",  f"{(current_cost_annual - PNG_cost_annual):,.0f}",  f"{(current_cost_annual - Biogas_cost_annual):,.0f}",
                                                        f"{(current_cost_annual - Biomass_cost_annual):,.0f}"],
                    # 'Payback period (years)' : ['NA',f"{Grid_electricity_pbp:,.0f}", f"{Solar_rooftop_pbp:,.0f}", f"{LPG_pbp:,.0f}",  f"{PNG_pbp:,.0f}",  f"{Biogas_pbp:,.0f}",
                                                #   f"{Firewood_pbp:,.0f}"],
                    'भुगतान अवधि (वर्ष)': ['NA','NA' if Grid_electricity_pbp > 15 or Grid_electricity_pbp < 0 else f"{Grid_electricity_pbp:,.0f}",
                                    'NA' if Solar_rooftop_pbp > 15 or Solar_rooftop_pbp < 0 else f"{Solar_rooftop_pbp:,.0f}",
                                    'NA' if LPG_pbp > 15 or  LPG_pbp <0 else f"{LPG_pbp:,.0f}",
                                    'NA' if PNG_pbp > 15 or PNG_pbp < 0 else f"{PNG_pbp:,.0f}",
                                    'NA' if Biogas_pbp > 15 or Biogas_pbp < 0 else f"{Biogas_pbp:,.0f}",
                                    'NA' if Biomass_pbp > 15 or Biomass_pbp < 0 else f"{Biomass_pbp:,.0f}"]
                }
                df = pd.DataFrame(data)
                # Available variables for x and y
                available_variables = list(df.columns)
                
                st.subheader("खाना पकाने के मापदंडों का दृष्टि प्रयोग")
                # Select x and y variables
                x_variable =['वर्तमान - '+str(selection_of_stoves),'इलेक्ट्रिक इंडक्शन', 'सौर कुकर', 'एलपीजी', 'पीएनजी','बायोगैस','जैवभार']
                y_variable = st.selectbox('**किसी मापदंड का चयन करें**', available_variables)
                df['cooking stoves']=x_variable
                # Filter DataFrame based on selected x_variable and y_variable

                c1,c2= st.columns([5,3],gap="small")
                    # Generate bar plot using Plotly
                with c1:
                    # colors = ['lightslategray','black','red','blue','green','orange','yellow']
                    # colors[1] = 'crimson'
                    # colors[2]
                    fig = px.bar(df, x='cooking stoves', y=y_variable, 
                                color_discrete_map={'वर्तमान - Selection of Stoves': 'red', 'इलेक्ट्रिक इंडक्शन': 'green',
                                                    'सौर कुकर': 'blue','एलपीजी': 'goldenrod', 'पीएनजी': 'magenta','बायोगैस': 'black','जैवभार': 'indigo'})
                    # color_discrete_sequence= px.colors.sequential.Plasma_r
                    fig.update_layout(xaxis_tickangle = -45) # Rotate x-axis labels by 45 degrees
                    fig.update_traces(hovertemplate = 'Value: %{y}') # Add tooltips for each bar
                    fig.update_layout(xaxis_title = "पाकने की विधि") # Set x-axis label 
                    fig.update_layout(yaxis_title = y_variable) # Set y-axis label
                    st.plotly_chart(fig)
            
                with c2:
                    df_filtered = df[['cooking stoves', y_variable]].copy()
                    df_filtered.rename(columns={'cooking stoves': 'Cooking Method'}, inplace=True)
                    # df_filtered['cooking stoves'] = x_variable
                    df_filtered.reset_index()
                    df_filtered["खाना पकाने की विधि"]=df_filtered["Cooking Method"]
                    df_filtered1=df_filtered.drop('Cooking Method',axis=1)
                    df_filtered = df_filtered.set_index('Cooking Method')
                    df_filtered1 = df_filtered1.set_index('खाना पकाने की विधि')
                    # Display DataFrame as a table
                    st.dataframe(df_filtered1)

                    # Save DataFrame as CSV
                    csv_data = df_filtered1.to_csv(index=True)
                    st.download_button("डेटा डाउनलोड करें", data=csv_data, file_name="filtered_data.csv", mime="text/csv")
                
                st.subheader('टिप्पणियाँ')
                st.markdown('''
- परिणाम तुलना के लिए जूलभण्ड बायोमास चूल्हों के लिए मूल्य संख्या प्रयोजन किए गए अनिवार्य शृंग बायोमास चूल्ह के विकल्पों से संबंधित है।
- इनडोर सोलर पाकन समाधान और बायोगैस के लिए, फ्रंट-एंड कुकस्टोव और उपकरण लागत कुल उपकरण की लागत का 5% है।
- इनडोर सोलर पाकन समाधान और बायोगैस के बाकी राशि को ब्याज दर और कार्यकाल के आधार पर मासिक परिचालन लागत के रूप में दिखाया जाता है।
- ग्रिड आधारित इलेक्ट्रिक इंडक्शन कुकटॉप की परिणाम तुलना में, दो कुकटॉप्स का अनुमान लिया गया है।
- कैपेक्स लागत की धारणा बाजार में उपलब्ध कुकस्टोव विकल्पों के लिए और योजनाओं के माध्यम से उपलब्ध सूचना के मूल्यांकन के आधार पर की गई है।
- सोलर कुकस्टोव की लागत में बैटरी संग्रहण शामिल नहीं है।
- वापसी की अवधि केवल तभी दिखाई जाती है अगर वह 15 वर्षों के नीचे है। वापसी की अवधि 15 साल से अधिक या ऋण की अवधि से नकारात्मक होने पर "NA" का उपयोग किया जाता है।
''')


            # else:
            #     st.write('Refresh Page')

else:

    #import file 
    energy_cooking = pd.read_excel('cooking_energy.xlsx',sheet_name='cooking energy',index_col=(0))
    electricity_tariff_file = pd.read_excel('cooking_energy.xlsx',sheet_name='electricity tariff',index_col=(0))
    stove_file = pd.read_excel('cooking_energy.xlsx',sheet_name='stoves',index_col=(0))

    social_carbon_cost = 86 * 82.32 * 0.001 # Social carbon cost is 86 USD per ton of CO2

    # #____________ Page info________________________________________
    # about_markdown = 'Development Team - Bikash Sahu, Vikas Kumar.' + \
    # 'For further details contact bikash@vasudhaindia.org.' + 
    # 'This analysis is a part of Deep Electrification initiative by Vasudha Foundation with support from SED Fund.'

    about_markdown = '''Development Team - Bikash Sahu, Vikas Kumar.
    For further details contact bikash@vasudhaindia.org.
    This analysis is a part of Deep Electrification initiative by Vasudha Foundation with support from SED Fund.'''



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
    # title_trans = translator.translate('Techno Economic Analysis of Cooking Technologies', dest='hi') 
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


    tab1, tab2 = st.tabs(["User Selection", "Further Information"])
    with tab2:
        ## user guide download
        # with open("user-guide.pdf", "rb") as pdf_file:
        #     PDFbyte = pdf_file.read()
        # st.download_button(label="User Guide",
        #                 data=PDFbyte,
        #                 file_name="user-guide.pdf",
        #                 mime='application/pdf')
        
        # ## methodology download
        # with open("methodology.pdf", "rb") as pdf_file:
        #     PDFbyte = pdf_file.read()
        # st.download_button(label="Methodology",
        #                 data=PDFbyte,
        #                 file_name="methodology.pdf",
        #                 mime='application/pdf')
        
        with st.expander('More about electric induction and its benefits'):
            st.markdown("""
                * **Faster cooking times:** Induction cooktops heat up much faster than traditional electric or gas cooktops. This is because the heat is generated directly in the pan, rather than in the cooktop itself.
                * **Precise temperature control:** Induction cooktops offer precise temperature control, which is ideal for delicate dishes or when you need to simmer something for a long period of time.
                * **Efficiency:** Induction cooktops are very efficient, meaning they use less energy than traditional cooktops. This can save you money on your energy bills.
                * **Safety:** Induction cooktops are very safe. There is no open flame or hot surface, so there is less risk of burns or fire.
                * **Easy cleaning:** Induction cooktops are very easy to clean. The smooth surface of the cooktop makes it easy to wipe down, and there are no spills or splatters to worry about.
                """ )

        st.subheader("Meal Energy Consumption")
        st.markdown('The meal energy consumption assumptions for electric cooking are provided in the following table.' 
                    + ' Please note the values mentioned are considered for a household comprising of 4 to 5 persons.'
                    + ' The meal energy consumption for other cooking fuels have been estimated based on the thermal efficiency mentioned below.')
        st.dataframe(energy_cooking.iloc[:,[1,2,3]].round({'time (min)':0, 'Energy (kWh)':2}))
        st.markdown('Source: https://mecs.org.uk/wp-content/uploads/2022/03/India-eCookbook-21-compressed.pdf')
        # rounded_energy_cooking = energy_cooking.iloc[:, [1, 2, 3]].round({'Column1Name': 0, 'Column3Name': 2})

        
        st.subheader("Cookstove Characteristics")

        stove_char = {
        'Stove Type': ['Traditional cook stove','Improved cook stove (Natural)','Improved cook stove (Forced)','Biogas (2 burner)',
                    'PNG (2 burner)','LPG (2 burner)','Electric Induction (1 burner)','Electric Induction (2 burner)','Indoor Solar Cooking Solution (1 burner)','Indoor Solar Cooking Solution (2 burner)'],
        'Life (years)': [1, 4, 4, 10, 10, 10, 10, 10, 10, 10],
        'Thermal Efficiency (percent)': ['15%', '20%', '30%', '60%', '60%', '60%', '80%', '80%', '80%', '80%'],
        'Capex (INR)': ['0','1,250','2,000','50,000','2,000','1,500','2,000','4,000','40,000','1,00,000'],
        'Unit Cost (INR/kWh)': ['1.41','1.34','1.27','1.5','4.77','4.98','Based on electricity tariff','Based on electricity tariff','0','0']
        }
        stove_char_df = pd.DataFrame(stove_char)
        stove_char_df = stove_char_df.set_index('Stove Type')
        st.dataframe(stove_char_df)
        # st.markdown('Source: http://164.100.94.214/national-biomass-cookstoves-programme, https://mnre.gov.in/img/documents/uploads/77e0a45feb0c4ce4974a0429d1e39001.pdf, https://beestarlabel.com/Content/Files/Final_LPG_schedule.pdf, https://beestarlabel.com/Content/Files/Schedule_Induction_hobs.pdf')
        st.markdown('Sources:')
        st.markdown(' http://164.100.94.214/national-biomass-cookstoves-programme')
        st.markdown(' https://mnre.gov.in/img/documents/uploads/77e0a45feb0c4ce4974a0429d1e39001.pdf')
        st.markdown(' https://beestarlabel.com/Content/Files/Final_LPG_schedule.pdf')
        st.markdown(' https://beestarlabel.com/Content/Files/Schedule_Induction_hobs.pdf')



        st.subheader("Carbon Emission Factors")
        carbon_ef = {
        'Fuel Type': ['Biomass (Firewood & Livestock Waste)','बायोगैस','एलपीजी','PNG','Grid electricity','Solar PV rooftop'],
        'Unit Carbon Emission (kgCO2eq./kWh)': [0.4, 0.15, 0.23, 0.2, 0.72, 0],
        }
        carbon_ef_df = pd.DataFrame(carbon_ef)
        carbon_ef_df = carbon_ef_df.set_index('Fuel Type')
        st.dataframe(carbon_ef_df)
        st.markdown('Sources:')
        st.markdown('https://acp.copernicus.org/articles/18/15169/2018/acp-18-15169-2018.pdf')
        st.markdown('https://www.mdpi.com/2073-4433/10/12/729')
        st.markdown('https://cea.nic.in/cdm-co2-baseline-database')
        st.markdown('https://www.sciencedirect.com/science/article/abs/pii/S0301421513010719')

        st.subheader("Social Cost of Carbon")
        st.write('The Social Carbon Cost assumed is USD 86 per ton of CO2. The USD to INR conversion is the average of reference rates from 1 April 2023 to 31 August 2023.')

        st.markdown('Sources:')
        st.markdown('https://www.rff.org/publications/explainers/social-cost-carbon-101/')
        st.markdown('https://www.downtoearth.org.in/dte-infographics/social_cost_corbon/index.html')
        st.markdown('https://www.rbi.org.in/scripts/ReferenceRateArchive.aspx')

        st.subheader("Statewise Grid Electricity Tariff of Indian States")
        el_tariff_rates = pd.DataFrame(electricity_tariff_file.iloc[:,[0,1,2,3,4]].round(2))
        el_tariff_rates = el_tariff_rates.set_index("State")
        st.dataframe(el_tariff_rates)
        st.markdown('Source: DISCOMs Electricity Tariff Orders of 2021-22 and 2022-23')
        
        st.subheader("Daily IHAP")
        ihap = {
        'Stove Type': ['Traditional cook stove (TCS)','Improved cook stove (ICS - Natural)','Improved cook stove (ICS - Forced)',
                    'Biogas (2 burner)','PNG (2 burner)','LPG (2 burner)','Electric Induction','Electric Pressure Cooker'],
        'Daily IHAP - PM 2.5 (μg/m3)': [1230, 410, 165, 60, 47, 64, 47, 35],
        }
        ihap_df = pd.DataFrame(ihap)
        ihap_df = ihap_df.set_index("Stove Type")
        st.dataframe(ihap_df)
        st.markdown('Sources:')
        st.markdown('https://www.sciencedirect.com/science/article/pii/S0160412018324772')
        st.markdown('https://www.researchgate.net/publication/337429023_In-Field_Emission_Measurements_from_Biogas_and_Liquified_Petroleum_Gas_LPG_Stoves')
        st.markdown('https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-020-09865-1')
        st.markdown('https://www.isid.ac.in/~epu/dispapers/dp22_04.pdf') 
        st.markdown('https://www.jstor.org/stable/resrep21836.8') 
        st.markdown('https://thermopedia.com/content/10255/')
        
        st.subheader('Annual Income of HH')
        income = {
        'Area Type': ['Rural','Rural','Rural','Urban','Urban','Urban'],
        'Socio-economic status': ['Lower','Middle','Higher','Lower','Middle','Higher'],
        'Annual Income (INR)': ['₹ 2,00,000','₹ 5,70,000','₹ 9,00,000','₹ 2,50,000','₹ 7,12,500','₹ 11,25,000']
        }
        income_df = pd.DataFrame(income)
        income_df = income_df.set_index('Area Type')
        st.dataframe(income_df)
        st.markdown('Source: India Residential Energy Survey (IRES) 2020')

        # st.subheader('References')

        # data = [
        # "https://mecs.org.uk/wp-content/uploads/2022/03/India-eCookbook-21-compressed.pdf",
        # "http://164.100.94.214/national-biomass-cookstoves-programme",
        # "https://mnre.gov.in/img/documents/uploads/77e0a45feb0c4ce4974a0429d1e39001.pdf",
        # "https://beestarlabel.com/Content/Files/Final_LPG_schedule.pdf",
        # "https://beestarlabel.com/Content/Files/Schedule_Induction_hobs.pdf",
        # "https://acp.copernicus.org/articles/18/15169/2018/acp-18-15169-2018.pdf",
        # "https://www.mdpi.com/2073-4433/10/12/729",
        # "https://cea.nic.in/cdm-co2-baseline-database",
        # "https://www.sciencedirect.com/science/article/abs/pii/S0301421513010719",
        # "https://www.sciencedirect.com/science/article/pii/S0160412018324772",
        # "https://www.researchgate.net/publication/337429023_In-Field_Emission_Measurements_from_Biogas_and_Liquified_Petroleum_Gas_LPG_Stoves",
        # "https://bmcpublichealth.biomedcentral.com/articles/10.1186/s12889-020-09865-1",
        # "https://www.isid.ac.in/~epu/dispapers/dp22_04.pdf",
        # "https://www.jstor.org/stable/resrep21836.8",
        # "https://thermopedia.com/content/10255/",
        # "DISCOMs Electricity Tariff Orders of 2021-22 and 2022-23",
        # "https://www.rff.org/publications/explainers/social-cost-carbon-101/",
        # "https://www.downtoearth.org.in/dte-infographics/social_cost_corbon/index.html",
        # "India Residential Energy Survey (IRES) 2020"
        # ]

        # def is_url(s):
        #     return s.startswith("http://") or s.startswith("https://")

        # markdown_text = ""
        # for i, item in enumerate(data, 1):
        #     if is_url(item):
        #         markdown_text += f"{i}. [{item}]({item})\n"
        #     else:
        #         markdown_text += f"{i}. {item}\n"

        # st.markdown(markdown_text)


    with tab1:
        #_______________basic settings_________________________________________
        st.subheader("Household Profile", help = 'The user has to select the following details to complete the household profile.')
        c1, c2 = st.columns(2)
        with c1: 
            state_select = st.selectbox('Select State', State_list, help = 'Select the state in India for which you want to compare the cooking solutions.')
            with st.container():
                area_select = st.selectbox('Area Type', ('Urban', 'Rural'), help = 'Select the area type. Urban areas are usually governed by Municipal Corporations,' +
                                        ' Municipal Councils, or Town Committees, while rural areas fall under the jurisdiction of' +
                                        ' Panchayats (village-level self-governance bodies).')
            monthly_income = st.number_input('Enter Monthly Income', min_value=0, max_value=1000000, value=30000, step=1000, help = "Please mention the Household's" + 
                                            ' gross monthly income. This is required for estimating the share of cooking expenses.')
            interest_rate = st.number_input('Enter Annual Interest Rate', min_value=0, max_value=20, value=5, step=1, help = 'Please mention the annual interest' 
                                            + ' rate terms offered by the financier for cooking solutions with significant upfront expenses, such as biogas and solar-powered cookstoves.')
        annual_income = monthly_income * 12
        with c2:
            with st.container():
                cooking_source_options = energy_source_list
                cooking_source_select = st.multiselect('Cooking Fuel Used', cooking_source_options, default=['Grid electricity'], help = 'Select the cooking fuels' +
                                                        ' presently used in the household.')
                filtered_stoves = stove_file.loc[stove_file['Fuel'].isin(cooking_source_select), 'stoves'].unique().tolist()
                # cookstove_select = st.multiselect('Cookstove Used', filtered_stoves, default=['Electric Induction (1 burner)'], help = 'Select the cookstoves used' + 
                #                                   ' in the household.')
                cookstove_select = st.multiselect('Cookstove Used', filtered_stoves, help = 'Select the cookstoves used' + 
                                                ' in the household.')  
                lpg_subsidy = st.selectbox('Are you eligible for an LPG subsidy?', ('No','Yes'), help = 'This is required to understand if you would be requiring' + 
                                        ' subsidy for household cooking purposes.') 
                loan_tenure = st.selectbox('Choose the loan duration in years', (1,2,3,4,5), help = 'This is crucial for calculating affordable financing options' +
                                        ' for cooking solutions with significant upfront expenses, such as biogas and solar-powered cookstoves.') 

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

        st.subheader("Meal Profile", help='Select your usual cooking pattern according to meal of the day below.')
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
        Solar_rooftop_cost=Solar_rooftop_data["Solar rooftop_RS"][0]
        
    
        
        Solar_rooftop_cost_annual = Solar_rooftop_cost * 12
        Solar_rooftop_consumption_kwh = Solar_rooftop_data["Solar rooftop_consumption"][0]
        Solar_rooftop_time_conversion = Solar_rooftop_data['time_conversion'][0]
        Solar_rooftop_time = df_time * Solar_rooftop_time_conversion
        Solar_rooftop_efficiency = Solar_rooftop_data['Thermal Efficiency'][0]
        Solar_rooftop_capex = Solar_rooftop_data['Capex'][0]
        Solar_rooftop_capex_token = Solar_rooftop_capex * 0.05
        Solar_rooftop_emission = Solar_rooftop_data['Unit carbon emission'][0]
        Solar_rooftop_emission_annual = Solar_rooftop_emission * Solar_rooftop_consumption_kwh * 365 * 0.9
        Solar_rooftop_ihap = Solar_rooftop_data['Daily IHAP (PM2.5)'][0]
        Solar_rooftop_pbp = Solar_rooftop_capex / (current_cost_annual - Solar_rooftop_cost_annual)

        ### monthly easy financing
        Solar_rooftop_cost_princ = Solar_rooftop_capex - Solar_rooftop_capex_token
        # Calculate monthly interest rate
        monthly_interest_rate = (interest_rate / 100) / 12
        # Calculate total number of monthly payments
        total_payments = loan_tenure * 12
        # Calculate the monthly payment using the formula
        monthly_payment_solar = (Solar_rooftop_cost_princ * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
        
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
        Biogas_water_heater_eff=Biogas_data['Thermal Efficiency'][0]# for water heater
        Biogas_cost=Biogas_data["Biogas_RS"][0]
        Biogas_cost_annual = Biogas_cost * 12
        Biogas_CONSUMPTION_KWH=Biogas_data["Biogas_consumption"][0]
        Biogas_time = df_time * Biogas_data["time_conversion"][0]
        Biogas_efficiency = Biogas_data['Thermal Efficiency'][0]
        Biogas_capex = Biogas_data['Capex'][0]
        Biogas_capex_token = Biogas_capex * 0.05
        Biogas_emission = Biogas_data['Unit carbon emission'][0]
        Biogas_emission_annual = Biogas_emission * Biogas_CONSUMPTION_KWH * 365 * 0.9
        Biogas_ihap = Biogas_data['Daily IHAP (PM2.5)'][0]
        Biogas_pbp = Biogas_capex / (current_cost_annual - Biogas_cost_annual)


        ### monthly easy financing
        Biogas_cost_princ = Biogas_capex - Biogas_capex_token
        # Calculate monthly interest rate
        monthly_interest_rate = (interest_rate / 100) / 12
        # Calculate total number of monthly payments
        total_payments = loan_tenure * 12
        # Calculate the monthly payment using the formula
        biogas_monthly_payment = (Biogas_cost_princ * monthly_interest_rate * (1 + monthly_interest_rate) ** total_payments) / ((1 + monthly_interest_rate) ** total_payments - 1)
        

        #########Traditional Solid Biomass#########
        Biomass_data=stove_file1[stove_file1["Fuel"] == 'Traditional Solid Biomass']
        Biomass_data["Biomass_consumption"] = total_energy_induction/Biomass_data['Thermal Efficiency']
        Biomass_data["Biomass_RS"] = Biomass_data["Biomass_consumption"] * Biomass_data['Unit cost']*30 #30 days
        # Biomass_water_heater_eff=Biomass_data['Thermal Efficiency'].mean()# for water heater
        Biomass_cost = Biomass_data["Biomass_RS"][2]
        Biomass_cost_annual = Biomass_cost * 12
        Biomass_consumption_KWH = Biomass_data["Biomass_consumption"][2]
        Biomass_time = df_time * Biomass_data["time_conversion"][2]
        Biomass_efficiency = Biomass_data['Thermal Efficiency'][2]
        Biomass_capex = Biomass_data['Capex'][2]
        Biomass_emission = Biomass_data['Unit carbon emission'][2]
        Biomass_emission_annual = Biomass_emission * Biomass_consumption_KWH * 365 * 0.9
        Biomass_ihap = Biomass_data['Daily IHAP (PM2.5)'][2]
        Biomass_pbp = Biomass_capex / (current_cost_annual - Biomass_cost_annual)

        #########Fire Wood#########
        # Fire_Wood_data=stove_file1[stove_file1["Fuel"] == 'Firewood']
        # Fire_Wood_data["Fire_Wood_consumption"]=total_energy_induction/Fire_Wood_data['Thermal Efficiency']
        # Fire_Wood_data["Fire_Wood_RS"]=Fire_Wood_data["Fire_Wood_consumption"]*Fire_Wood_data['Unit cost']*30 #30 days
        # Fire_wood_water_heater_eff=Fire_Wood_data['Thermal Efficiency'].mean()# for water heater
        # Fire_Wood_cost=Fire_Wood_data["Fire_Wood_RS"].mean()
        # Fire_Wood_cost_annual = Fire_Wood_cost * 12
        # Fire_Wood_consumption_KWH=Fire_Wood_data["Fire_Wood_consumption"].mean()
        # Firewood_time = df_time * Fire_Wood_data["time_conversion"][0]
        # Firewood_efficiency = Fire_Wood_data['Thermal Efficiency'].mean()
        # Firewood_capex = Fire_Wood_data['Capex'].mean()
        # Firewood_emission = Fire_Wood_data['Unit carbon emission'][0]
        # Firewood_emission_annual = Firewood_emission * Fire_Wood_consumption_KWH * 365 * 0.9
        # Firewood_ihap = Fire_Wood_data['Daily IHAP (PM2.5)'][0]
        # Firewood_pbp = Firewood_capex / (current_cost_annual - Fire_Wood_cost_annual)

        #########Livestock Waste#########
        # Livestock_Waste_data=stove_file1[stove_file1["Fuel"] == 'Livestock Waste']
        # Livestock_Waste_data["Livestock Waste_consumption"]=total_energy_induction/Livestock_Waste_data['Thermal Efficiency']
        # Livestock_Waste_data["Livestock Waste_RS"]=Livestock_Waste_data["Livestock Waste_consumption"]*Livestock_Waste_data['Unit cost']*30 #30 days
        # Livestock_Waste_cost=Livestock_Waste_data["Livestock Waste_RS"].mean()
        # Livestock_Waste_cost_annual = Livestock_Waste_cost * 12
        # Livestock_Waste_consumption_KWH=Livestock_Waste_data["Livestock Waste_consumption"].mean()
        # Livestock_Waste_time = df_time * Livestock_Waste_data["time_conversion"][0]
        # Livestock_Waste_efficiency = Livestock_Waste_data['Thermal Efficiency'][0]
        # Livestock_capex = Livestock_Waste_data['Capex'].mean()
        # Livestock_emission = Livestock_Waste_data['Unit carbon emission'][0]
        # Livestock_emission_annual = Livestock_emission * Livestock_Waste_consumption_KWH * 365 * 0.9
        # Livestock_ihap = Livestock_Waste_data['Daily IHAP (PM2.5)'][0]
        # Livestock_pbp = Livestock_capex / (current_cost_annual - Livestock_Waste_cost_annual)

        ############average of firewood and livestocks#########
        # firewood_livestock_cost_average=(Livestock_Waste_cost+Fire_Wood_cost)/2
        # firewood_livestock_time = (Firewood_time+ Livestock_Waste_time)/2
        # firewood_livestock_efficiency = (Firewood_efficiency + Livestock_Waste_efficiency)/2
        # firewood_livestock_capex = (Firewood_capex + Livestock_capex)/2
        # firewood_livestock_emission = (Firewood_emission + Livestock_emission)/2
        # firewood_livestock_emission_annual = (Firewood_emission_annual + Livestock_emission_annual)/2
        # firewood_livestock_ihap = (Firewood_ihap + Livestock_ihap) / 2
        # firewood_livestock_pbp = (Firewood_pbp + Livestock_pbp) / 2

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
            # Check if 'specific_column' contains 'induction' or 'gas'
            fuel_list=df['Fuel'].unique()

            # Check if specific words are in the list
            if 'Biogas' in fuel_list and 'Solar rooftop' in fuel_list:
                current_cost = df['RS(monthly)'].sum()+monthly_payment_solar+biogas_monthly_payment
                #result = "Both 'Solar rooftop' and 'gas' are in the list."
            elif 'Solar rooftop' in fuel_list:
                current_cost = df['RS(monthly)'].sum()+monthly_payment_solar
                #result = "'Solar rooftop' is in the list, but 'gas' is not."
            elif 'Biogas' in fuel_list:
                current_cost = df['RS(monthly)'].sum()+biogas_monthly_payment
                #result = "'gas' is in the list, but 'induction' is not."
            else:
                current_cost = df['RS(monthly)'].sum()
                #result = "Neither 'induction' nor 'gas' are in the list."

            # Print the result
            current_cost_annual = current_cost * 12 

            submit_button = st.button("Show Results")

            # Only execute code below if the submit button is clicked
            if submit_button:
                # st.write("Code execution after submit button is clicked.")

                st.subheader('Total operating cost for cooking (INR/month)', help = 'This is an indicative amount of monthly expenses on cooking energy demand.')
                c1, c2, c3,c4,c5,c6,c7 = st.columns(7)
                with c1:
                    st.metric('Present Cost', f"₹{current_cost:,.0f}")
                with c2:
                    dcost = -100*(current_cost - Grid_electricity_cost)/current_cost
                    st.metric('Electric Induction', f"₹{Grid_electricity_cost:,.0f}", 
                    delta=f"{change_str2(dcost)}₹{abs(current_cost - Grid_electricity_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                # with c3:
                #     dcost = -100*(current_cost - Solar_rooftop_cost)/current_cost
                #     st.metric('Indoor Solar Cooking Solution', f"₹{Solar_rooftop_cost:,.0f}", 
                #     delta=f"{change_str2(dcost)}₹{abs(current_cost - Solar_rooftop_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c3:
                    dcost = -100*(current_cost - monthly_payment_solar)/current_cost
                    st.metric('Indoor Solar Cooking Solution', f"₹{monthly_payment_solar:,.0f}", 
                    delta=f"{change_str2(dcost)}₹{abs(current_cost - monthly_payment_solar):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c4:
                    dcost = -100*(current_cost - LPG_cost)/current_cost
                    st.metric('LPG', f"₹{LPG_cost:,.0f}", 
                    delta=f"{change_str2(dcost)}₹{abs(current_cost - LPG_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse') 
                with c5:
                    dcost = -100*(current_cost - PNG_cost)/current_cost
                    st.metric('PNG', f"₹{PNG_cost:,.0f}", 
                    delta=f"{change_str2(dcost)} ₹{abs(current_cost - PNG_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c6:
                    dcost = -100*(current_cost - (biogas_monthly_payment + Biogas_cost))/current_cost
                    st.metric('Biogas', f"₹{(biogas_monthly_payment + Biogas_cost):,.0f}", 
                    delta=f"{change_str2(dcost)} ₹{abs(current_cost - (biogas_monthly_payment + Biogas_cost)):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')
                with c7:
                    dcost = -100*(current_cost - Biomass_cost)/current_cost
                    st.metric('Biomass', f"₹{Biomass_cost:,.0f}", 
                    delta=f"{change_str2(dcost)} ₹{abs(current_cost - Biomass_cost):,.0f} ({change_str2(dcost)} {abs(dcost):.0f}%)", delta_color='inverse')

                st.markdown('*The monthly cost for indoor solar cooking solution and biogas is based on the capital cost and financing cost of the solutions.*')

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
                
                st.subheader('Annual carbon emission (kgCO2eq./year)', help = 'This is an indicative amount of the carbon emissions caused due' 
                            + ' to the estimated energy consumption.')
                c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
                with c1:
                    st.metric('Present Emissions', f"{(total_emissions_annual):,.0f}")
                with c2:
                    st.metric('Electric Induction', f"{Grid_electricity_emission_annual:,.0f}",)
                with c3:
                    st.metric('Indoor Solar Cooking Solution', f"{Solar_rooftop_emission_annual:,.0f}",) 
                with c4:
                    st.metric('LPG', f"{LPG_emission_annual:,.0f}",)
                with c5:
                    st.metric('PNG', f"{PNG_emission_annual:,.0f}",)
                with c6:
                    st.metric('Biogas',f"{Biogas_emission_annual:,.0f}")
                with c7:
                    st.metric('Biomass', f"{Biomass_emission_annual:,.0f}",)

                
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
                st.subheader('Daily Indoor Household Air Pollution (IHAP) [PM 2.5] (μg/m3)', help = 'This is the estimated indoor air pollution' 
                            + ' which causes health hazards on prolonged exposure.')
                c1, c2,c3,c4,c5,c6 = st.columns(6)
                with c1:
                    # st.metric('Electric Induction', f"{Grid_electricity_ihap:,.0f}",)
                    st.metric('Electric Induction', f"{0:,.0f}",)
                with c2:
                    # st.metric('Indoor Solar Cooking Solution', f"{Solar_rooftop_ihap:,.0f}",)
                    st.metric('Indoor Solar Cooking Solution', f"{0:,.0f}",)
                with c3:
                    st.metric('LPG', f"{LPG_ihap:,.0f}",)
                with c4:
                    # st.metric('PNG', f"{PNG_ihap:,.0f}",)
                    st.metric('PNG', f"{LPG_ihap:,.0f}",)
                with c5:
                    st.metric('Biogas', f"{Biogas_ihap:,.0f}",) 
                with c6:
                    st.metric('Biomass', f"{Biomass_ihap:,.0f}",)
                
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
                    'Unit cost (INR/kWh)': [f"{(current_cost/total_energy_user)/30:,.2f}", f"{electricity_tariff:,.2f}", f"{0:,.2f}", 6.38, 5.86, f"{1.5:,.2f}",1.32],
                    'Total operating cost for cooking (INR/month)': [f"{current_cost:,.0f}", f"{Grid_electricity_cost:,.0f}", f"{monthly_payment_solar:,.0f}",
                                                                    f"{LPG_cost:,.0f}", f"{PNG_cost:,.0f}", f"{(biogas_monthly_payment+Biogas_cost):,.0f}", f"{Biomass_cost:,.0f}"],
                    'Percentage of cooking expenses with monthly income (%)': [f"{(current_cost/monthly_income):,.2%}", f"{(Grid_electricity_cost/monthly_income):,.2%}", 
                                                                            f"{(Solar_rooftop_cost/monthly_income):,.2%}", f"{(LPG_cost/monthly_income):,.2%}", 
                                                                            f"{(PNG_cost/monthly_income):,.2%}", f"{(Biogas_cost/monthly_income):,.2%}", 
                                                                            f"{(Biomass_cost/monthly_income):,.2%}"],
                    'Daily cooking duration (hours/day)': [f"{current_time_daily:,.2f}", f"{Grid_electricity_time:,.2f}", f"{Solar_rooftop_time:,.2f}", 
                                                        f"{LPG_time:,.2f}", f"{PNG_time:,.2f}", f"{Biogas_time:,.2f}", f"{Biomass_time:,.2f}"],
                    'Daily energy consumption for cooking (kWh/day)': [f"{total_energy:,.2f}", f"{Grid_electricity_consumption_KWH:.2f}", f"{Solar_rooftop_consumption_kwh:.2f}", 
                                                                f"{LPG_consumption_kwh:,.2f}",f"{PNG_CONSUMPTON_KWH:.2f}", f"{Biogas_CONSUMPTION_KWH:.2f}", f"{Biomass_consumption_KWH:.2f}"],
                    'Thermal efficiency (%)': ['-',f"{Grid_electricity_efficiency:,.0%}", f"{Solar_rooftop_efficiency:,.0%}", f"{LPG_efficiency:,.0%}", 
                                            f"{PNG_efficiency:,.0%}", f"{Biogas_efficiency:,.0%}", f"{Biomass_efficiency:,.0%}"],
                    'Cookstove and equipment cost (INR)': ['NA',f"{Grid_electricity_capex:,.0f}", f"{(Solar_rooftop_capex * 0.05):,.0f}", f"{LPG_capex:,.0f}", f"{PNG_capex:,.0f}",
                                                        f"{(Biogas_capex * 0.05):,.0f}",  f"{Biomass_capex:,.0f}"],
                    'Unit carbon emission (kgCO2eq./kWh)' : [f"{present_EF:.2f}", f"{Grid_electricity_emission:.2f}", f"{Solar_rooftop_emission:.2f}", f"{LPG_emission:.2f}", 
                                                            f"{PNG_emission:.2f}", f"{Biogas_emission:.2f}", f"{Biomass_emission:.2f}"],
                    'Annual carbon emission (kgCO2eq./year)' : [f"{total_emissions_annual:.0f}", f"{Grid_electricity_emission_annual:.0f}", f"{Solar_rooftop_emission_annual:.0f}", 
                                                                f"{LPG_emission_annual:.0f}", f"{PNG_emission_annual:.0f}", f"{Biogas_emission_annual:.0f}", f"{Biomass_emission_annual:.0f}"],
                    'Social carbon cost (INR/year)' : [f"{(total_emissions_annual * social_carbon_cost):,.0f}",  f"{Grid_electricity_emission_annual * social_carbon_cost:,.0f}",
                                                        f"{Solar_rooftop_emission_annual * social_carbon_cost:,.0f}",  f"{LPG_emission_annual * social_carbon_cost:,.0f}",
                                                            f"{PNG_emission_annual * social_carbon_cost:,.0f}",  f"{Biogas_emission_annual * social_carbon_cost:,.0f}",
                                                                f"{Biomass_emission_annual * social_carbon_cost:,.0f}"],
                    'Daily IHAP [PM 2.5] (μg/m3)' : ['NA', f"{Grid_electricity_ihap:,.0f}",  f"{Solar_rooftop_ihap:,.0f}",  f"{LPG_ihap:,.0f}",  f"{PNG_ihap:,.0f}",
                                                    f"{Biogas_ihap:,.0f}",  f"{Biomass_ihap:,.0f}"],

                    'Annual opex savings (INR)' : ['NA', f"{(current_cost_annual - Grid_electricity_cost_annual):,.0f}",  f"{(current_cost_annual - Solar_rooftop_cost_annual):,.0f}",
                                                    f"{(current_cost_annual - LPG_cost_annual):,.0f}",  f"{(current_cost_annual - PNG_cost_annual):,.0f}",  f"{(current_cost_annual - Biogas_cost_annual):,.0f}",
                                                        f"{(current_cost_annual - Biomass_cost_annual):,.0f}"],
                    # 'Payback period (years)' : ['NA',f"{Grid_electricity_pbp:,.0f}", f"{Solar_rooftop_pbp:,.0f}", f"{LPG_pbp:,.0f}",  f"{PNG_pbp:,.0f}",  f"{Biogas_pbp:,.0f}",
                                                #   f"{Firewood_pbp:,.0f}"],
                    'Payback period (years)': ['NA','NA' if Grid_electricity_pbp > 15 or Grid_electricity_pbp < 0 else f"{Grid_electricity_pbp:,.0f}",
                                    'NA' if Solar_rooftop_pbp > 15 or Solar_rooftop_pbp < 0 else f"{Solar_rooftop_pbp:,.0f}",
                                    'NA' if LPG_pbp > 15 or  LPG_pbp <0 else f"{LPG_pbp:,.0f}",
                                    'NA' if PNG_pbp > 15 or PNG_pbp < 0 else f"{PNG_pbp:,.0f}",
                                    'NA' if Biogas_pbp > 15 or Biogas_pbp < 0 else f"{Biogas_pbp:,.0f}",
                                    'NA' if Biomass_pbp > 15 or Biomass_pbp < 0 else f"{Biomass_pbp:,.0f}"]
                }
                df = pd.DataFrame(data)

                # Available variables for x and y
                available_variables = list(df.columns)
                
                st.subheader('Visualisation of cooking parameters')
                # Select x and y variables
                x_variable =['Present - '+str(selection_of_stoves),'Electric Induction', 'Indoor Solar Cooking Solution', 'LPG', 'PNG', 'Biogas','Biomass']
                y_variable = st.selectbox('**Select a parameter**', available_variables)
                df['cooking stoves']=x_variable
                # Filter DataFrame based on selected x_variable and y_variable

                c1,c2= st.columns([5,3],gap="small")
                    # Generate bar plot using Plotly
                with c1:
                    # colors = ['lightslategray','black','red','blue','green','orange','yellow']
                    # colors[1] = 'crimson'
                    # colors[2]
                    fig = px.bar(df, x='cooking stoves', y=y_variable, 
                                color_discrete_map={'Present - Selection of Stoves': 'red', 'Electric Induction': 'green',
                                                    'Indoor Solar Cooking Solution': 'blue','LPG': 'goldenrod', 'PNG': 'magenta','Biogas': 'black','Firewood': 'indigo'})
                    # color_discrete_sequence= px.colors.sequential.Plasma_r
                    fig.update_layout(xaxis_tickangle = -45) # Rotate x-axis labels by 45 degrees
                    fig.update_traces(hovertemplate = 'Value: %{y}') # Add tooltips for each bar
                    fig.update_layout(xaxis_title = 'Cooking Method') # Set x-axis label 
                    fig.update_layout(yaxis_title = y_variable) # Set y-axis label
                    st.plotly_chart(fig)
            
                with c2:
                    df_filtered = df[['cooking stoves', y_variable]].copy()
                    df_filtered.rename(columns={'cooking stoves': 'Cooking Method'}, inplace=True)
                    # df_filtered['cooking stoves'] = x_variable
                    df_filtered.reset_index()
                    df_filtered = df_filtered.set_index('Cooking Method')
                    # Display DataFrame as a table
                    st.dataframe(df_filtered)

                    # Save DataFrame as CSV
                    csv_data = df_filtered.to_csv(index=True)
                    st.download_button("Download CSV", data=csv_data, file_name="filtered_data.csv", mime="text/csv")
                
                st.subheader('Notes')
                st.markdown('''
                - The values for biomass stoves in the result comparison pertains to forced draft biomass stove variants.
                - For indoor solar cooking solution and biogas, the upfront cookstove and equipment cost is 5% of the total device cost.
                - The rest of the amount for indoor solar cooking soluton and biogas is shown as monthly operating cost based on the interest rate and tenure. 
                - In the results comparison of grid based electric induction cooktops, two cooktops are assumed.
                - Capex cost is assumed based on secondary research of available cookstove options in the market and through schemes.
                - Cost of solar cookstove does not include battery storage.
                - Payback period is shown only if it is below 15 years. "NA" is used for payback periods above 15 years or negative payback periods.
                ''')


            # else:
            #     st.write('Refresh Page')
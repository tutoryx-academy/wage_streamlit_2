import pandas as pd
import streamlit as st
import re

def clean_rate(rate:str)->float:

    regex_pattern = r"[^\d.]+"
    rate_str = re.sub(regex_pattern,"",str(rate))
    return float(rate_str)

def get_currency(rate:str)->str:

    regex_pattern = r"[^\d.]+"
    rate_str = re.findall(regex_pattern,rate)
    return rate_str[0].strip()

def currency_rates(df):
    currency_dictionary = dict(zip(df['currency'],df['rate']))
    return currency_dictionary

def calculate_wage(hours:float, rate:float)->float:

    if hours <= 40:
        wage = rate * hours
    else:
        wage = (hours - 40) * 1.5 * rate + 40 * rate
    return wage

st.title('Calculate Wage Application')

uploaded_file_hours = st.file_uploader('Upload Hours-Rate file!', type=['csv'])
uploaded_file_rates = st.file_uploader('Upload Currency rates to Lek file!', type=['csv'])

if uploaded_file_hours is None or uploaded_file_rates is None:
    st.warning('Please upload csv files to calculate the wage!')
else:
    df = pd.read_csv(uploaded_file_hours)
    df_rate = pd.read_csv(uploaded_file_rates)

    if 'Rate' not in df.columns or 'Hours' not in df.columns:
        st.error("Please rename your columns to correct format 'Rate' and 'Hours' not other")
    else:
        df['Rate_float'] = df['Rate'].apply(clean_rate)
        df['Wage'] = df.apply(lambda x: calculate_wage(x['Hours'],x['Rate_float']), axis=1)
        df['existing_rate']=df['Rate'].apply(get_currency)
        currency_dictionary = currency_rates(df_rate)
        df['leke_rate']=df['existing_rate'].map(currency_dictionary)
        df['Wage_leke'] = df['Wage']*df['leke_rate']
        #TODO: Drop unnecesary columns
        st.dataframe(df)
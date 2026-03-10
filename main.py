#Import libraries
import pandas as pd
import numpy as np

#Import functions
from data_cleaning.customers_cleaning import clean_customers_data

#Import files
customers = pd.read_csv('Data/customers.csv')

#Cleaning files
customers_clean = clean_customers_data(
    date_cols=['birth_date', 'registration_date'],
    category_cols=['gender', 'loyalty_status', 'country']
)
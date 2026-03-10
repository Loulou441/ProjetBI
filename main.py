#Import libraries
import pandas as pd
import numpy as np

#Import functions
from data_cleaning.customers_cleaning import clean_customers_data
from data_cleaning.stores_cleaning import clean_stores_data

#Import files
customers = pd.read_csv('Data/customers.csv')
stores = pd.read_csv('Data/stores.csv')

#Cleaning files
customers_clean = clean_customers_data(customers)
stores_clean = clean_stores_data(stores)

#Saving files
customers_clean.to_csv('customers_clean.csv', index=False)
stores_clean.to_csv('stores_clean.csv', index=False)

#Import libraries
import pandas as pd
import numpy as np

#Import functions
from data_cleaning.customers_cleaning import clean_customers_data
from data_cleaning.stores_cleaning import clean_stores_data
from data_cleaning.suppliers_cleaning import clean_suppliers_data


#Import files
customers = pd.read_csv('Data/customers.csv')
stores = pd.read_csv('Data/stores.csv')
suppliers = pd.read_csv('Data/suppliers.csv')

#Cleaning files
customers_clean = clean_customers_data(customers)
stores_clean = clean_stores_data(stores)
suppliers_clean = clean_suppliers_data(suppliers)

#Saving files
customers_clean.to_csv('customers_clean.csv', index=False)
stores_clean.to_csv('stores_clean.csv', index=False)
suppliers_clean.to_csv('suppliers_clean.csv', index=False)

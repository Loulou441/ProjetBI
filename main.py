#Import libraries
import pandas as pd
import numpy as np

#Import functions
from data_cleaning.customers_cleaning import clean_customers_data
from data_cleaning.stores_cleaning import clean_stores_data
from data_cleaning.suppliers_cleaning import clean_suppliers_data
from data_transforming.bi_customers import fact_table_customers

#Import files
customers = pd.read_csv('Data/customers.csv')
stores = pd.read_csv('Data/stores.csv')
suppliers = pd.read_csv('Data/suppliers.csv')
transactions = pd.read_csv('data_cleaning/transactions_silver.csv')

#Cleaning files
customers_clean = clean_customers_data(customers)
stores_clean = clean_stores_data(stores)
suppliers_clean = clean_suppliers_data(suppliers)

#Saving files
customers_clean.to_csv('data_cleaning/customers_clean.csv', index=False)
stores_clean.to_csv('data_cleaning/stores_clean.csv', index=False)
suppliers_clean.to_csv('data_cleaning/suppliers_clean.csv', index=False)

#Calcul des KPIs
fact_table_customers = fact_table_customers(customers_clean, stores_clean, transactions)
fact_table_customers.to_csv('fact_customer_table.csv', index=False)
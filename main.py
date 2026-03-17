#Import libraries
import pandas as pd
import numpy as np

#Import functions
from data_cleaning.customers_cleaning import clean_customers_data
from data_cleaning.stores_cleaning import clean_stores_data
from data_cleaning.suppliers_cleaning import clean_suppliers_data
from data_cleaning.transaction_cleaning import clean_transactions_data
from data_cleaning.products_cleaning import clean_products_data
from data_cleaning.marketing_cleaning import clean_marketing_data
from data_cleaning.accounting_cleaning import clean_accounting_data
from data_transforming.bi_customers import fact_table_customers

#Import files
customers = pd.read_csv('Data/customers.csv')
stores = pd.read_csv('Data/stores.csv')
suppliers = pd.read_csv('Data/suppliers.csv')
transactions = pd.read_csv('Data/transactions.csv')
products = pd.read_csv('Data/products.csv')
marketing = pd.read_csv('Data/marketing.csv')
accounting = pd.read_csv('Data/accounting.csv')

#Cleaning files
customers_clean = clean_customers_data(customers)
stores_clean = clean_stores_data(stores)
suppliers_clean = clean_suppliers_data(suppliers)
transactions_clean = clean_transactions_data(transactions)
products_clean = clean_products_data(products)
marketing_clean = clean_marketing_data(marketing)
accounting_clean = clean_accounting_data(accounting)

#Saving files
customers_clean.to_csv('data_cleaning/data_cleaned/customers_clean.csv', index=False)
stores_clean.to_csv('data_cleaning/data_cleaned/stores_clean.csv', index=False)
suppliers_clean.to_csv('data_cleaning/data_cleaned/suppliers_clean.csv', index=False)
transactions_clean.to_csv('data_cleaning/data_cleaned/transactions_clean.csv', index=False)
products_clean.to_csv('data_cleaning/data_cleaned/products_clean.csv', index=False)
marketing_clean.to_csv('data_cleaning/data_cleaned/marketing_clean.csv', index=False)
accounting_clean.to_csv('data_cleaning/data_cleaned/accounting_clean.csv', index=False)

#Calcul des KPIs
fact_table_customers = fact_table_customers(customers_clean, stores_clean, transactions)
fact_table_customers.to_csv('fact_customer_table.csv', index=False)
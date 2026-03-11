import pandas as pd

def fact_table_customers(customers, stores, transactions):

    customers = customers[customers['country'] != 'Inconnu']
    customers = customers[customers['loyalty_status'] != 'Inconnu']
    customers = customers.rename(columns={'country': 'country_customer'})

    stores = stores[stores['country'] != 'Inconnu']
    stores = stores.rename(columns={'country': 'country_store'})


    clv_analysis = transactions.groupby(["customer_id","store_id"]).agg(
    total_CA=("total_price", "sum"),
    nb_transactions=("transaction_id", "count"),
    panier_moyen=("total_price", "mean")
    ).reset_index()

    #Calcul sur les magasins
    #Le CA par surface
    stores['CA_per_m2'] = stores['annual_revenue'] / stores['surface_sqm']
    #La fréquence par magasin
    frequency_store = transactions.groupby("store_id")["transaction_id"].count().reset_index()

    #Jointures
    stores = pd.merge(
        frequency_store, 
        stores, 
        on='store_id', 
        how='inner'
    )

    fact_table = pd.merge(
        clv_analysis[['customer_id','store_id','total_CA', 'nb_transactions','panier_moyen']], 
        customers[['customer_id', 'loyalty_status', 'country_customer']], 
        on='customer_id', 
        how='inner'
    )

    fact_table = pd.merge(
        fact_table, 
        stores[['store_id', 'annual_revenue', 'country_store', 'district_type', 'CA_per_m2']], 
        on='store_id', 
        how='inner'
    )

    return fact_table
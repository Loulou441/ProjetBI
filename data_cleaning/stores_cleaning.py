import pandas as pd
import numpy as np

def clean_stores_data(df):
    initial_len = len(df)
    
    # --- AUDIT AVANT NETTOYAGE ---
    bad_ids = len(df[df['store_id'] == 'BADID'])
    bad_warehouses = (len(df[df['warehouse_id'] == 'ENT_UNKNOWN']) + len(df[df['warehouse_id'] == 'BADID']))
    bad_revenue = len(df[df['annual_revenue'] <= 0])
    bad_surface = len(df[df['surface_sqm'] <= 0])
    bad_address = df['address'].isna().sum()
    bruit = ['Narnia', 'inconnu', 'extra', 'X', 'UNKNOWN']
    nb_bruit = df['country'].isin(bruit).sum()  
    bad_dates = len(df[pd.to_datetime(df['opening_date'], errors='coerce') > pd.Timestamp.now()])

    print(f"📊 RAPPORT D'AUDIT : Stores")
    print(f"❌ Identifiants Customers ID : {bad_ids} ({(bad_ids/initial_len):.1%})")
    print(f"❌ Identifiants WAREHOUSE : {bad_warehouses} ({(bad_warehouses/initial_len):.1%})")
    print(f"💰 Revenus négatifs ou nuls : {bad_revenue} ({(bad_revenue/initial_len):.1%})")
    print(f"📏 Surfaces négatives ou nulles : {bad_surface} ({(bad_surface/initial_len):.1%})")
    print(f"📏 Adresses vides : {bad_address} ({(bad_address/initial_len):.1%})")
    print(f"🎭 Valeurs fantaisistes dans Pays : {nb_bruit} ({(nb_bruit/initial_len):.1%})")
    print(f"📅 Ouvertures dans le futur (2099) : {bad_dates} ({(bad_dates/initial_len):.1%})")

    # --- NETTOYAGE ---
    # 1. On garde uniquement les IDs valides
    df_clean = df[df['store_id'] != 'BADID'].copy()
    df_clean = df_clean[df['warehouse_id'] != 'BADID'].copy()
    df_clean = df_clean[df['warehouse_id'] != 'ENT_UNKNOWN'].copy()

    # 2. On garde uniquement les valeurs numériques cohérentes
    df_clean = df_clean[df_clean['annual_revenue'] > 0]
    df_clean = df_clean[df_clean['surface_sqm'] > 0]
    
    # 3. Correction des dates
    df_clean['opening_date'] = pd.to_datetime(df_clean['opening_date'], errors='coerce')
    df_clean = df_clean[df_clean['opening_date'] <= pd.Timestamp.now()]
    
    # 4. Harmonisation des pays et types de quartier
    garbage = ['Narnia', 'N/A', 'inconnu', 'UNKNOWN', 'extra']
    for col in ['country', 'district_type', 'property_status']:
        df_clean[col] = df_clean[col].replace(garbage, 'Inconnu').fillna('Inconnu')

    print("-" * 30)
    print(f"✅ Nettoyage terminé : {len(df_clean)} magasins valides sur {initial_len} soit {(len(df_clean)/initial_len):.1%}")
    return df_clean
import pandas as pd
import numpy as np

def clean_transactions_data(df):
    # 1. Chargement
    total_initial = len(df)
    id_cols = ['transaction_id', 'ticket_id', 'customer_id', 'product_id', 'store_id']
    cat_cols=['sales_channel']

    print(f"--- Rapport d'Audit pour Transaction ---")
    
    # 2. Compte des BADID
    for i in id_cols:
        nb_badid = (df[i] == 'BADID').sum() + (df[i].str.endswith('UNKNOWN', na=False)).sum() 
        print(f"❌ Identifiants corrompus (BADID et UNKNOWN) dans '{i}' : {nb_badid} ({(nb_badid/total_initial):.1%})")

    # 3. Audit des valeurs négatives
    nb_quantity = (df['quantity'] < 0).sum()
    print(f"🎭 Valeurs négatives dans 'quantity' : {nb_quantity} ({(nb_quantity/total_initial):.1%})")

    # 4. Audit des valeurs fantaisistes
    bruit = ['Narnia', 'inconnu', 'extra', 'X', 'UNKNOWN']
    for col in cat_cols:
        nb_bruit = df[col].isin(bruit).sum()
        print(f"🎭 Valeurs fantaisistes dans '{col}' : {nb_bruit} ({(nb_bruit/total_initial):.1%})")

    # --- NETTOYAGE EFFECTIF ---
    # On filtre les IDs
    df_clean = df
    for i in id_cols:
        df_clean = df_clean[df_clean[i] != 'BADID']
        df_clean = df_clean[~df_clean[i].str.endswith('UNKNOWN', na=False)]
        
    # On nettoie les catégories
    for col in cat_cols:
        df_clean[col] = df_clean[col].replace(bruit, np.nan).fillna('Inconnu')

    #On nettoie les quantités
    df_clean = df_clean[df_clean['quantity'] > 0]
    
    print("-" * 30)
    print(f"✅ Nettoyage fini : {len(df_clean)} lignes valides sur {total_initial} soit {(len(df_clean)/total_initial):.1%}")
    
    return df_clean
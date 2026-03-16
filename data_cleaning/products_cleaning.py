import pandas as pd
import numpy as np

def clean_products_data(df):
    # 1. Chargement
    total_initial = len(df)
    id_cols = ['product_id', 'supplier_id']
    cat_cols=['category', 'manufacturing_origin']
    weight_cols = ['volume_l', 'weight_kg']

    print(f"--- Rapport d'Audit pour Products ---")
    
    # 2. Compte des BADID
    for col in id_cols:
        nb_badid = (df[col] == 'BADID').sum() + (df[col].str.endswith('UNKNOWN', na=False)).sum() 
        print(f"❌ Identifiants corrompus dans '{col}' : {nb_badid} ({(nb_badid/total_initial):.1%})")

    # 3. Audit des valeurs nulles
    for col in weight_cols:
        nb_weight_nul = (df[col] == 0).sum()
        print(f"🎭 Valeurs nulle dans '{col}' : {nb_weight_nul} ({(nb_weight_nul/total_initial):.1%})")

    # 4. Audit des valeurs fantaisistes
    bruit = ['Narnia', 'inconnu', 'extra', 'X', 'UNKNOWN']
    for col in cat_cols:
        nb_bruit = df[col].isin(bruit).sum()
        print(f"🎭 Valeurs fantaisistes dans '{col}' : {nb_bruit} ({(nb_bruit/total_initial):.1%})")

    # 5. Nombre de produits sans nom
    nb_bad_name = (df['product_name'].isnull()).sum()
    print(f"❌ Valeurs nulles dans 'product name': {nb_bad_name} ({(nb_bad_name/total_initial):.1%})")

    # --- NETTOYAGE EFFECTIF ---
    # On filtre les IDs
    df_clean = df
    for col in id_cols:
        df_clean = df_clean[df_clean[col] != 'BADID']
        df_clean = df_clean[~df_clean[col].str.endswith('UNKNOWN', na=False)]
        
    # On nettoie les catégories
    for col in cat_cols:
        df_clean[col] = df_clean[col].replace(bruit, np.nan).fillna('Inconnu')

    #On nettoie les quantités
    for col in weight_cols:
        df_clean = df_clean[df_clean[col] > 0]

    #On fait les cols sans nom
    df_clean = df_clean[~df_clean['product_name'].isnull()]
    
    print("-" * 30)
    print(f"✅ Nettoyage fini : {len(df_clean)} lignes valides sur {total_initial} soit {(len(df_clean)/total_initial):.1%}")
    
    return df_clean
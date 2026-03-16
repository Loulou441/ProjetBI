import pandas as pd
import numpy as np

def clean_marketing_data(df):
    # 1. Chargement
    total_initial = len(df)
    id_cols = ['marketing_id', 'campaign_group_id', 'product_id']
    cat_cols=['promotion_type', 'target_customer_type']
    date_cols = ['promotion_date']
    euro_cols = ['budget','actual_cost']

    print(f"--- Rapport d'Audit pour Marketing ---")
    
    # 2. Compte des BADID
    for col in id_cols:
        nb_badid = (df[col] == 'BADID').sum() + (df[col].str.endswith('UNKNOWN', na=False)).sum() 
        print(f"❌ Identifiants corrompus dans '{col}' : {nb_badid} ({(nb_badid/total_initial):.1%})")

    # 3. Audit des dates aberrantes
    aujourdhui = pd.Timestamp.now()
    stats_dates = {}

    for col in date_cols:
        temp_series = pd.to_datetime(df[col], errors='coerce')
        nb_futur = (temp_series > aujourdhui).sum()
        nb_invalide = temp_series.isna().sum() - df[col].isna().sum()
        stats_dates[col] = nb_futur + nb_invalide
        print(f"📅 Dates aberrantes dans '{col}' : {stats_dates[col]} ({(stats_dates[col]/total_initial):.1%})")

    # 4. Audit des valeurs fantaisistes
    bruit = ['Narnia', 'inconnu', 'extra', 'X', 'UNKNOWN']
    for col in cat_cols:
        nb_bruit = df[col].isin(bruit).sum()
        print(f"🎭 Valeurs fantaisistes dans '{col}' : {nb_bruit} ({(nb_bruit/total_initial):.1%})")

    # 5. Budget positif
    for col in euro_cols:
        nb_budget = (df[col] <= 0).sum() + (df[col].isna()).sum()
        print(f"❌ Valeurs négatives ou nulle dans '{col}': {nb_budget} ({(nb_budget/total_initial):.1%})")

    # --- NETTOYAGE EFFECTIF ---
    # On filtre les IDs
    df_clean = df
    for col in id_cols:
        df_clean = df_clean[df_clean[col] != 'BADID']
        df_clean = df_clean[~df_clean[col].str.endswith('UNKNOWN', na=False)]
        
    # On nettoie les catégories
    for col in cat_cols:
        df_clean[col] = df_clean[col].replace(bruit, np.nan).fillna('Inconnu')

    #On nettoie les dates
    for col in date_cols:
        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        df_clean = df_clean[df_clean[col] <= aujourdhui]
    
    #On nettoie les budget
    for col in euro_cols:
        df_clean = df_clean[df_clean[col] > 0]

    print("-" * 30)
    print(f"✅ Nettoyage fini : {len(df_clean)} lignes valides sur {total_initial} soit {(len(df_clean)/total_initial):.1%}")
    
    return df_clean
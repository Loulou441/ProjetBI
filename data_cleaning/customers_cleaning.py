import pandas as pd
import numpy as np

def clean_customers_data(df):
    # 1. Chargement
    total_initial = len(df)
    date_cols=['birth_date', 'registration_date'] # Liste de colonnes
    cat_cols=['gender', 'loyalty_status', 'country', 'acquisition_source']
    dedup_col='email'

    print(f"--- Rapport d'Audit pour Customers ---")
    
    # 2. Compte des BADID
    nb_badid = (df['customer_id'] == 'BADID').sum()
    print(f"❌ Identifiants corrompus (BADID) : {nb_badid} ({(nb_badid/total_initial):.1%})")
    
    # 3. Audit des dates (Correction du bug 'assemble mappings')
    aujourdhui = pd.Timestamp.now()
    stats_dates = {}
    
    for col in date_cols:
        # On force l'accès en "Série" (un seul crochet) pour éviter le bug
        temp_series = pd.to_datetime(df[col], errors='coerce')
        nb_futur = (temp_series > aujourdhui).sum()
        nb_invalide = temp_series.isna().sum() - df[col].isna().sum()
        stats_dates[col] = nb_futur + nb_invalide
        print(f"📅 Dates aberrantes dans '{col}' : {stats_dates[col]} ({(stats_dates[col]/total_initial):.1%})")

    # 4. Audit des valeurs "Fantaisistes"
    bruit = ['Narnia', 'inconnu', 'extra', 'X', 'UNKNOWN']
    for col in cat_cols:
        nb_bruit = df[col].isin(bruit).sum()
        print(f"🎭 Valeurs fantaisistes dans '{col}' : {nb_bruit} ({(nb_bruit/total_initial):.1%})")

    # 5. Audit des doublons
    nb_doublons = df.duplicated(subset=[dedup_col]).sum()
    print(f"👯 Doublons détectés sur '{dedup_col}' : {nb_doublons} ({(nb_doublons/total_initial):.1%})")

    # --- NETTOYAGE EFFECTIF ---
    # On filtre les IDs
    df_clean = df[df['customer_id'] != 'BADID'].copy()
    
    # On nettoie les dates
    for col in date_cols:
        df_clean[col] = pd.to_datetime(df_clean[col], errors='coerce')
        df_clean = df_clean[df_clean[col] <= aujourdhui]
        
    # On nettoie les catégories
    for col in cat_cols:
        if col == 'loyalty_status':
            df_clean[col] = df_clean[col].replace(np.nan, '1')
            df_clean[col] = df_clean[col].replace(bruit, np.nan).fillna('Inconnu')
            df_clean[col] = df_clean[col].replace('1', np.nan)
        else:
            df_clean[col] = df_clean[col].replace(bruit, np.nan).fillna('Inconnu')
        
    # On supprime les doublons
    df_clean = df_clean.drop_duplicates(subset=[dedup_col])
    
    print("-" * 30)
    print(f"✅ Nettoyage fini : {len(df_clean)} lignes valides sur {total_initial} soit {(len(df_clean)/total_initial):.1%}")
    
    return df_clean
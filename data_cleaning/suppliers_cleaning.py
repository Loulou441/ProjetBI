import pandas as pd
import numpy as np

def clean_suppliers_data(df):
    total_rows = len(df)
    
    print(f"📊 RAPPORT D'AUDIT : Suppliers")

    # --- ÉTAPE A : AUDIT AVEC POURCENTAGES ---
    bad_ids = (df['supplier_id'] == 'BADID').sum()
    bad_scores = ((df['reliability_score'] < 0) | (df['reliability_score'] > 1)).sum()
    bad_lead_time = (df['lead_time_days'] <= 0).sum()
    garbage_country = df['country'].isin(['inconnu', 'N/A', 'UNKNOWN']).sum()

    print(f"❌ Identifiants BADID        : {bad_ids} ({bad_ids/total_rows:.2%})")
    print(f"📉 Scores fiabilité invalides : {bad_scores} ({bad_scores/total_rows:.2%})")
    print(f"🕒 Délais livraison négatifs  : {bad_lead_time} ({bad_lead_time/total_rows:.2%})")
    print(f"🌍 Pays non identifiés       : {garbage_country} ({garbage_country/total_rows:.2%})")

    # --- ÉTAPE B : NETTOYAGE DES ERREURS ---
    # 1. On garde les IDs valides
    df_clean = df[df['supplier_id'] != 'BADID'].copy()

    # 2. On redresse les scores de fiabilité (on cape entre 0 et 1)
    df_clean['reliability_score'] = df_clean['reliability_score'].clip(0, 1)

    # 3. On corrige les délais de livraison (si <= 0, on met la moyenne du fichier)
    avg_lead_time = df_clean[df_clean['lead_time_days'] > 0]['lead_time_days'].mean()
    df_clean.loc[df_clean['lead_time_days'] <= 0, 'lead_time_days'] = avg_lead_time

    # 4. Harmonisation des catégories
    garbage = ['inconnu', 'N/A', 'UNKNOWN', 'extra', 'X']
    cat_cols = ['country', 'contract_type', 'specialization']
    for col in cat_cols:
        df_clean[col] = df_clean[col].replace(garbage, 'À déterminer').fillna('À déterminer')

    # --- ÉTAPE C : IMPACT CO2 ---
    # Si le CO2 est manquant, on met 0 (impact neutre par défaut pour ne pas fausser les calculs)
    df_clean['co2_modifier_per_kg'] = df_clean['co2_modifier_per_kg'].fillna(0)

    print("-" * 45)
    print(f"✅ Nettoyage terminé : {len(df_clean)} fournisseurs exploitables soit {(len(df_clean)/total_rows):.1%}.")
    
    return df_clean
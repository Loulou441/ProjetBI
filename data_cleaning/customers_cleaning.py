import pandas as pd
import numpy as np

def clean_customers_data(date_cols=None, category_cols=None):
    """
    Nettoie un DataFrame retail : supprime les BADID, corrige les dates 
    et élimine les valeurs fantaisistes.
    """
    # 1. Chargement
    initial_count = len(df)
    
    # 2. Suppression des identifiants corrompus
    df = df[df['customer_id'] != 'BADID']
    
    # 3. Traitement des dates (si spécifiées)
    if date_cols:
        for col in date_cols:
            df[col] = pd.to_datetime(df[col], errors='coerce')
        
        # Filtre : pas de dates dans le futur (seuil à aujourd'hui)
        aujourdhui = pd.Timestamp.now()
        for col in date_cols:
            df = df[df[col] <= aujourdhui]
            
        # Logique spécifique : Inscription après Naissance (si les deux existent)
        if 'registration_date' in df.columns and 'birth_date' in df.columns:
            df = df[df['registration_date'] >= df['birth_date']]

    # 4. Nettoyage des catégories "polluées" (si spécifiées)
    if category_cols:
        garbage_values = ['Narnia', 'inconnu', 'extra', 'X', 'UNKNOWN', 'N/A']
        for col in category_cols:
            df[col] = df[col].replace(garbage_values, np.nan)

    final_count = len(df)
    print(f"Lignes supprimées : {initial_count - final_count}")
    print(f"Lignes exploitables restantes : {final_count}\n")
    
    return df
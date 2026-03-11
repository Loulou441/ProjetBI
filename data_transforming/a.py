import pandas as pd

def commercial_performance(customers, stores, transactions):
    # --- KPI 1 : Chiffre d'Affaires au m² (CA/m2) ---
    # Ce ratio permet de comparer l'efficacité réelle des surfaces de vente.
    stores['CA_per_m2'] = stores['annual_revenue'] / stores['surface_sqm']

    # --- KPI 2 : Taux de Pénétration par Pays ---
    # On calcule combien de clients uniques on a par pays par rapport au CA total dans ce pays.
    # Note : Dans une vraie étude, on diviserait par la population totale du pays. 
    # Ici, on mesure la "densité de clients" par million d'euros de CA.
    customers_2 = customers[customers['country'] != 'Inconnu']
    stores = stores[stores['country'] != 'Inconnu']
    penetration = customers_2['country'].value_counts().to_frame('client_count')
    ca_par_pays = stores.groupby('country')['annual_revenue'].sum()

    penetration_stats = penetration.join(ca_par_pays)
    penetration_stats['penetration_ratio'] = (penetration_stats['client_count'] / penetration_stats['annual_revenue']) * 1_000_000

    # --- KPI 3 : Part du CA par Segment de Fidélité ---
    # On ne garde que les colonnes nécessaires pour optimiser la mémoire.
    customers_3 = customers[customers['loyalty_status'] != 'Inconnu']
    df_final = pd.merge(
        transactions[['customer_id', 'total_price']], 
        customers_3[['customer_id', 'loyalty_status', 'country']], 
        on='customer_id', 
        how='inner'
    )

    # Calcul du CA par Segment
    ca_per_segment = df_final.groupby('loyalty_status')['total_price'].agg(['sum', 'count', 'mean'])
    ca_per_segment.columns = ['Total_CA', 'Nombre_Transactions', 'Panier_Moyen']

    # Calcul des Parts de Marché Internes (%)
    total_ca_global = ca_per_segment['Total_CA'].sum()
    ca_per_segment['Part_CA_Pct'] = (ca_per_segment['Total_CA'] / total_ca_global) * 100

    # Tri pour la présentation
    ca_per_segment = ca_per_segment.sort_values(by='Part_CA_Pct', ascending=False)

    # --- KPI 4 : Répartition des Segments de Fidélité par Pays ---
    # On crée un tableau croisé (pivot table) : Pays en lignes, Segments en colonnes
    customers_4 = customers[customers['loyalty_status'] != 'Inconnu']
    customers_4 = customers_4[customers_4['country'] != 'Inconnu']
    loyalty_by_country = pd.crosstab(customers_4['country'], customers_4['loyalty_status'])

    # On transforme en pourcentages pour pouvoir comparer les pays entre eux 
    # (car la France a beaucoup plus de clients en volume que le Portugal, par exemple)
    loyalty_pct_by_country = loyalty_by_country.div(loyalty_by_country.sum(axis=1), axis=0) * 100

    # --- AFFICHAGE DES RÉSULTATS ---
    print("🚀 ANALYSE DE PERFORMANCE COMMERCIALE")
    print("-" * 50)

    print("\n1. Top 5 des Pays et par district par CA/m² moyen :")
    print(stores.groupby(['country', 'district_type'])['CA_per_m2'].mean().sort_values(ascending=False))

    print("\n2. Densité de clients (nb clients pour 1M€ de CA) :")
    print(penetration_stats['penetration_ratio'].sort_values(ascending=False))

    print("\n3. Part estimée du CA par Segment de Fidélité (%) :")
    print(ca_per_segment.round(2))

    print("\n4. Répartition des segments de fidélité par pays(%)")
    print("-" * 60)
    print(loyalty_pct_by_country.round(2))
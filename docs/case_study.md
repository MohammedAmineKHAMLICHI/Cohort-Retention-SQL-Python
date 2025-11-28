# Étude de cas - Rétention e-commerce synthétique

## 🧭 Problématique
- Marque direct-to-consumer avec ~600 clients par trimestre et churn rapide.
- Question métier : à quel moment les cohortes décrochent-elles et quels leviers stabilisent la rétention M+1 / M+3 ?

## 🛠️ Méthode
1. **Données**  
   - Simulation contrôlée via `GenerationConfig` pour répartir les cohortes sur 2023-2024.  
   - Deux sources brutes : `users.csv` et `orders.csv` (dates + montants).
2. **Mesures**  
   - Python : `build_retention` (pandas) calcule taille de cohorte et % actif M+0..M+7.  
   - SQL : `sql/queries.sql` reproduit le KPI avec `retention_pct`.  
   - Pytest + DuckDB garantissent la parité SQL == Python sur des données représentatives.
3. **Visuels & insights**  
   - `notebooks/02_retention.ipynb` génère la heatmap.  
   - CLI (`src/retention.py`) imprime des phrases d’insight après chaque exécution.

## 📈 Résultats clés (seed 42, 600 utilisateurs)
| KPI | Valeur |
| --- | --- |
| Rétention moyenne M+1 | **23,6 %** |
| Rétention moyenne M+3 | **7,4 %** |
| Meilleure cohorte | **Juillet 2023 - 45,8 % à M+1** |
| Taille médiane de cohorte | 24 clients |
| AOV | **51 EUR** |

Au-delà de M+6, la rétention médiane tombe à 0 %, ce qui suggère des actions de réactivation.

## 🚀 Recommandations
1. **Réactivation rapide (J+7 / J+30)**  
   Nourrir la relation pour faire progresser M+1 de 23 % vers 30 % (offres progressives + éducation produit).
2. **Répliquer les meilleures cohortes**  
   Analyser le mix d’acquisition de juillet 2023 (créatif, canal, offre) et le rejouer sur les cohortes à venir.
3. **Parcours VIP / P90**  
   Créer un segment premium avec avantages exclusifs pour conserver au moins 10 % de clients actifs à M+3.

## 🔭 Pistes futures
- Connecter le pipeline à un entrepôt réel (BigQuery, Snowflake, DuckDB) ou un projet dbt.
- Ajouter un tableau de bord Streamlit / Power BI alimenté par `outputs/retention.csv`.
- Planifier un reporting automatique (GitHub Actions sur cron + export Slack/Teams).

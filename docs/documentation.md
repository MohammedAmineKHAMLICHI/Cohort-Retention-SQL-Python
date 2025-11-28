# Documentation - Cohort Retention Project

## 📚 Dictionnaire de données
- `users.csv` : `user_id`, `signup_date`.
- `orders.csv` : `order_id`, `user_id`, `order_date`, `amount`.
- `outputs/retention.csv` : `cohort_month`, `cohort_size`, colonnes `0..7` pour les taux de rétention (un mois relatif par colonne).

## 🧭 Méthode analytique
1. Cohorte = mois du premier achat (`MIN(order_date)` par `user_id`).
2. `month_index` = nombre de mois entre `order_month` et `cohort_month`.
3. Rétention = `active_users(M+i) / cohort_size`, arrondie à 0,1.
4. Insights = statistiques descriptives (moyenne M+1, horizon le plus lointain, décroissance).

## ✅ Contrôles qualité automatisés
- Validation d’entrée (`src/retention.py`) : colonnes requises, dates valides, dataset non vide.
- Suite Pytest :
  - scénario multi-mois avec churn,
  - aller-retour CLI,
  - parité SQL via DuckDB.
- GitHub Actions (Python 3.11) : flake8 + pytest à chaque push/PR.

## 🎛️ Règles d’acceptation
- `cohort_size` > 0 pour chaque cohorte conservée.
- `retention[0]` à 100 % (ou `NaN` si aucune activité en mois 0).
- `month_index` sans saut (incrément de 1), sinon la cohorte est filtrée avant visualisation.

## 🚀 Pistes d’action métier
- Relances automatisées à J+7 / J+30 pour sécuriser la rétention M+1.
- Offres tactiques en M+2/M+3 pour les cohortes faibles.
- Parcours VIP (P90) afin de limiter la chute entre M+1 et M+3.

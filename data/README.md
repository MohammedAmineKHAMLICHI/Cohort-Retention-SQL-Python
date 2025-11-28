# 📊 Données du projet

## 🎯 Résumé
Ce répertoire stocke les jeux de données générés pour l’analyse de rétention. Les fichiers sont régénérés localement et ignorés par git.

## 🔑 Fichiers
- `users.csv` : journal d’inscriptions synthétique (`user_id`, `signup_date`).
- `orders.csv` : commandes e-commerce synthétiques (`order_id`, `user_id`, `order_date`, `amount`).

## ⚙️ Régénération
```bash
python src/generate_data.py
```
ou, après `make install` :
```bash
make data
```
Les deux commandes recréent les CSV de manière déterministe via `GenerationConfig` (seed 42, 600 utilisateurs, fenêtre janv. 2023 à déc. 2024). Supprimer les fichiers existants pour modifier les paramètres.

## ℹ️ Notes d’usage
- La CLI (`src/retention.py`) lit `orders.csv` dans ce dossier par défaut. L’option `--input` permet de cibler un autre chemin.
- Jeux de données 100 % synthétiques, partageables sans enjeu de confidentialité.

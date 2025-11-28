# Cohort Retention - Mini-projet SQL + Python
[![CI](https://github.com/MohammedAmineKHAMLICHI/Cohort-Retention-SQL-Python/actions/workflows/ci.yml/badge.svg)](https://github.com/MohammedAmineKHAMLICHI/Cohort-Retention-SQL-Python/actions/workflows/ci.yml)

Auteur : Mohammed Amine KHAMLICHI
LinkedIn : https://www.linkedin.com/in/mohammedaminekhamlichi/

## 🎯 Résumé du projet
Analyse de rétention par cohorte sur un jeu de données e-commerce synthétique. Le projet compare une implémentation Python (pandas) et SQL (DuckDB), automatise les tests de parité et fournit des visualisations ainsi qu’une CLI pour produire des matrices de rétention.

## 🧭 Contexte et objectif
Contexte analytique orienté marketing produit. Objectif principal : générer des données synthétiques, calculer des matrices de rétention par cohorte, vérifier la cohérence entre pipelines SQL et Python, puis exposer les résultats sous forme de CSV et de heatmap.

## 🔑 Fonctionnalités principales
- Génération déterministe des données (`users.csv`, `orders.csv`) avec `src/generate_data.py`.
- Construction de tables de rétention et extraction d’insights via `src/retention.py`.
- Pipeline SQL équivalent dans `sql/schema.sql` et `sql/queries.sql` (DuckDB).
- Notebooks d’analyse (EDA et heatmap).
- Suite de tests pytest couvrant CLI et parité SQL/Python.
- Workflow CI GitHub Actions pour lint et tests.

## 🛠️ Stack technique
- Python 3.11
- pandas, numpy, duckdb, matplotlib
- Pytest, flake8
- Makefile pour les raccourcis de build

## ⚙️ Installation
1. Cloner le dépôt.
2. Créer un environnement virtuel : `python -m venv .venv` (ou `python3` selon l’OS).
3. Activer l’environnement : `.\.venv\Scripts\Activate.ps1` (Windows) ou `source .venv/bin/activate` (macOS/Linux).
4. Mettre pip à jour : `python -m pip install --upgrade pip`.
5. Installer les dépendances : `pip install -r requirements.txt` (ou `make install`).

## 🚀 Utilisation
- Régénérer les données : `python src/generate_data.py` ou `make data`.
- Calculer la rétention et les insights :  
  `python src/retention.py --input data/orders.csv --output outputs/retention.csv --insights 5`  
  Raccourci : `make retention`.
- Lancer Jupyter Lab pour les notebooks : `python -m jupyter lab` ou `make notebook`.

## 🗂️ Structure du dépôt
- `src/` : `generate_data.py`, `retention.py`
- `sql/` : schéma et requêtes de rétention (DuckDB)
- `notebooks/` : EDA et heatmap de rétention
- `docs/` : documentation et case study
- `data/` : CSV générés (ignorés par git)
- `outputs/` : exports de rétention (ignorés)
- `tests/` : tests pytest incluant checks DuckDB
- `.github/workflows/ci.yml` : CI (flake8 + pytest)
- `Makefile` : raccourcis d’installation et de run

## ✅ Tests
- Lint : `flake8`
- Tests unitaires et d’intégration : `pytest -q`
- CI : workflow GitHub Actions `ci.yml` (Python 3.11)

## 🌟 Compétences mises en avant
- Génération et manipulation de jeux de données synthétiques
- Analyse de rétention et calculs par cohorte
- Parité entre pipelines SQL et Python
- Automatisation de tests et CI GitHub Actions
- Visualisation de données (matplotlib, notebooks)

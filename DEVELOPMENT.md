# Guide de Développement

Ce document est destiné aux développeurs souhaitant modifier le code source, personnaliser l'apparence ou comprendre l'architecture du Dashboard.

## 🛠️ Stack Technique

* **Backend** : Python 3.12, Django 5.2.
* **Frontend** :
    * **HTML5/CSS3** : Structure.
    * **Tailwind CSS** : Framework utilitaire (chargé localement ou via CDN pour le développement rapide).
    * **HTMX** : Pour les interactions dynamiques (AJAX, édition inline).
    * **SortableJS** : Pour le Drag & Drop.
* **Base de données** : SQLite (par défaut), compatible PostgreSQL.

---

## ⚙️ Installation (Environnement de Dév)

### 1. Pré-requis
* Python 3.12+
* Git

### 2. Setup du projet
```bash
# Cloner le dépôt
git clone [https://github.com/cocolombo/dashboard.git](https://github.com/cocolombo/dashboard.git)
cd dashboard

# Créer l'environnement virtuel
python -m venv .venv

# Activer l'environnement
# Linux/Mac :
source .venv/bin/activate
# Windows :
# .venv\Scripts\activate

# Installer les dépendances
pip install django
# (Ajoutez ici : pip install -r requirements.txt si vous en avez créé un)

# Migrer la base de données
python manage.py migrate

# (Optionnel) Peupler la base avec des données de test
# python manage.py seed_db
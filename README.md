# Django Personal Dashboard

Un tableau de bord (Dashboard) personnel, auto-hébergé et interactif, inspiré de services comme Start.me. Il permet de gérer ses signets, de les organiser par catégories (widgets) et par pages (onglets), le tout avec une interface Drag & Drop fluide.

## 🚀 Fonctionnalités

* **Organisation Hiérarchique** : Pages (Onglets) > Widgets (Catégories) > Liens.
* **Drag & Drop Complet** :
    * Déplacez les liens au sein d'une catégorie.
    * Déplacez les liens d'une catégorie à une autre.
    * Réorganisez l'ordre des catégories sur la page.
* **Gestion Facile** :
    * Créer, Renommer, Supprimer des Pages.
    * Ajouter, Supprimer des Liens directement depuis l'interface.
    * Menu contextuel (clic-droit) pour déplacer des éléments entre les pages.
* **Interface Moderne** : Mode sombre (Dark Mode) utilisant Tailwind CSS.
* **Barre de recherche** : Recherche Google intégrée.
* **Persistance** : Base de données SQLite (par défaut) ou PostgreSQL.

## 🛠️ Stack Technique

* **Backend** : Python 3.12, Django 5.2.
* **Frontend** : HTML5, Tailwind CSS (via CDN ou local), HTMX (pour les interactions AJAX), SortableJS (pour le Drag & Drop).
* **Base de données** : SQLite (développement), compatible PostgreSQL.

## ⚙️ Installation & Démarrage

### 1. Pré-requis
Assurez-vous d'avoir Python 3.12 installé.

### 2. Cloner et Configurer
```bash
# Cloner le projet (ou copier les fichiers)
cd votre-dossier-projet

# Créer un environnement virtuel
python -m venv .venv
source .venv/bin/activate  # Sur Linux/Mac
# .venv\Scripts\activate   # Sur Windows

# Installer les dépendances
pip install django


### Structure du Projet
 - startme/ : Configuration principale Django (settings.py, urls.py).
 - dashboard/ : L'application principale.
   - models.py : Définition des données (Page, Widget, Link).
   - views.py : Logique métier (affichage, APIs de mise à jour).
   - templates/dashboard/index.html : Le frontend unique de l'application.
   - management/commands/ : Scripts utilitaires (import, seed).
- static/ : Fichiers JS/CSS locaux (Tailwind, HTMX, SortableJS).

### Utilisation
 - Ajouter un lien : Cliquez sur le + à droite du titre d'une catégorie.
 - Déplacer un élément : Cliquez et glissez un lien ou un titre de catégorie.
 - Menu Contextuel : Faites un clic-droit sur un lien ou un titre de catégorie pour voir les options de déplacement vers d'autres pages.
 - Gérer les pages : Utilisez les boutons +, ✎ (renommer) et 🗑 (supprimer) dans la barre de navigation supérieure.

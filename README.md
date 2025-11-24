# Django Personal Dashboard

Un tableau de bord (Dashboard) personnel, auto-hébergé et interactif, inspiré de services comme Start.me. Il permet de gérer ses signets, de les organiser par catégories (widgets) et par pages (onglets), avec une interface moderne et fluide entièrement pilotable à la souris.

## 🚀 Fonctionnalités

### Organisation
* **Structure Hiérarchique** : Pages (Onglets) > Widgets (Catégories) > Liens.
* **Barre de Recherche** : Recherche Google intégrée directement dans le dashboard.

### Drag & Drop (Glisser-Déposer)
* **Liens** : Déplacez les liens d'une catégorie à une autre ou réorganisez-les au sein d'une liste.
* **Catégories** : Réorganisez l'ordre des catégories sur la page par simple glisser-déposer via l'en-tête.
* **Persistance** : Toutes les modifications de position sont sauvegardées instantanément en base de données.

### Gestion Complète
* **Pages** :
    * **Créer** : Bouton `+` dans la barre d'onglets.
    * **Renommer/Supprimer** : Boutons `✎` et `🗑` disponibles pour la page active (avec fenêtres de confirmation).
* **Catégories (Widgets)** :
    * **Ajouter** : Bouton `+ Catégorie` situé à côté de la barre de recherche.
    * **Supprimer** : Icône `🗑` dans l'en-tête du widget (avec fenêtre de confirmation sécurisée).
    * **Déplacer** : Icône `➜` pour envoyer une catégorie entière vers une autre page.
* **Liens** :
    * **Ajouter** : Bouton `+` dans chaque catégorie pour ouvrir le formulaire d'ajout rapide.
    * **Supprimer** : Croix `×` au survol de chaque lien.

### Interface (UI/UX)
* **Design** : Mode sombre (Dark Mode) utilisant Tailwind CSS.
* **Interactivité** : Fenêtres modales (Popups) pour toutes les actions importantes (création, suppression), remplaçant les alertes natives du navigateur pour une meilleure expérience.

## 🛠️ Stack Technique

* **Backend** : Python 3.12, Django 5.2.
* **Frontend** :
    * **HTML5/CSS3** : Structure et mise en page.
    * **Tailwind CSS** : Framework CSS utilitaire (via CDN ou fichiers locaux).
    * **HTMX** : Pour les interactions AJAX légères.
    * **SortableJS** : Pour la gestion fluide du Drag & Drop.
* **Base de données** : SQLite (par défaut, zéro config), compatible PostgreSQL.

## ⚙️ Installation & Démarrage

### 1. Pré-requis
Assurez-vous d'avoir **Python 3.12** installé sur votre machine.

### 2. Installation
```bash
# Cloner le projet
git clone [https://github.com/cocolombo/dashboard.git](https://github.com/cocolombo/dashboard.git)
cd dashboard

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

### Guide d'utilisation rapide
 - Ajouter un lien : Cliquez sur le petit + vert à droite du titre d'une catégorie.
 - Déplacer une catégorie : Cliquez et maintenez le clic sur le titre (en orange) d'une boîte pour la déplacer.
 - Envoyer vers une autre page : Cliquez sur la flèche ➜ dans l'en-tête d'une catégorie pour la transférer vers un autre onglet.
 - Supprimer : Utilisez les icônes corbeille 🗑. Une fenêtre vous demandera toujours confirmation avant la suppression définitive d'une page ou d'une catégorie.



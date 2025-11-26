# Django Personal Dashboard

Un tableau de bord (Dashboard) personnel, auto-hébergé et interactif, inspiré de services comme Start.me. Il permet de gérer ses signets, de les organiser par catégories (widgets) et par pages (onglets), avec une interface moderne et fluide entièrement pilotable à la souris.

## 🚀 Fonctionnalités

### Organisation
* **Structure Hiérarchique** : Pages (Onglets) > Widgets (Catégories) > Liens.
* **Barre de Recherche** : Recherche Google intégrée directement dans le dashboard.
* **Page "Infos" Spéciale** : Si une page est nommée **"Infos"**, elle affiche automatiquement :
    * Météo locale (via wttr.in).
    * Horloge numérique en temps réel.
    * Liste de suivi des marchés financiers (via TradingView).

### Drag & Drop (Glisser-Déposer)
* **Liens** : Déplacez les liens d'une catégorie à une autre ou réorganisez-les au sein d'une liste.
* **Catégories** : Réorganisez l'ordre des catégories sur la page par simple glisser-déposer via l'en-tête.
* **Persistance** : Toutes les modifications de position sont sauvegardées instantanément en base de données.

### Gestion Complète
* **Pages** :
    * **Créer** : Bouton `+` dans la barre d'onglets.
    * **Renommer/Supprimer** : Boutons `✎` et `🗑` disponibles pour la page active (avec fenêtres de confirmation).
* **Catégories (Widgets)** :
    * **Ajouter** : Bouton bleu `+ Catégorie` situé à côté de la barre de recherche.
    * **Supprimer** : Icône `🗑` dans l'en-tête du widget (avec fenêtre de confirmation sécurisée).
    * **Déplacer** : Icône `➜` pour envoyer une catégorie entière vers une autre page.
* **Liens** :
    * **Ajouter** : Bouton `+` dans chaque catégorie pour ouvrir le formulaire d'ajout rapide.
    * **Supprimer** : Croix `×` au survol de chaque lien.

### Interface (UI/UX)
* **Design** : Mode sombre (Dark Mode) utilisant Tailwind CSS.
* **Interactivité** : Fenêtres modales (Popups) pour toutes les actions importantes, remplaçant les alertes natives du navigateur pour une expérience fluide.

## 🛠️ Stack Technique

* **Backend** : Python 3.12, Django 5.2.
* **Frontend** :
    * **HTML5/CSS3** : Structure et mise en page.
    * **Tailwind CSS** : Framework CSS utilitaire (fichiers locaux pour support hors-ligne/Firefox).
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

### Personnalisation (Guide Rapide)
 - Le design est géré via Tailwind CSS directement dans dashboard/templates/dashboard/index.html. Voici les lignes clés à modifier pour ajuster l'apparence.
 - 1. Changer la largeur des colonnes (Catégories)
 -- Cherchez la ligne contenant id="widget-grid". Modifiez la classe lg:grid-cols-4 :
 -- Plus large : lg:grid-cols-3 (3 colonnes par ligne)
 -- Plus petit : lg:grid-cols-5 (5 colonnes par ligne)
 -- Mobile : grid-cols-1 (1 colonne par défaut sur petit écran)
 - 2. Changer les couleurs (Thème)
 --  Fond de la page : Dans la balise <body>, changez bg-gray-900.
 -- Fond des boîtes : Cherchez et remplacez partout bg-gray-800.
 -- Titres (Orange) : Cherchez text-orange-400 et remplacez par text-blue-400, text-green-400, etc.

 - 3. Espacement des liens (Densité)
 -- Dans la liste des liens (<ul class="sortable-list ...">) :
 -- Écart vertical : Modifiez space-y-0.5 (0.5 = très serré, 2 = aéré).
 -- Hauteur de ligne : Dans les balises <li>, modifiez py-1 (padding vertical).

 - 4. Modifier les données Bourse (Tickers)
 -- Le widget Bourse est un script TradingView intégré dans la section "Infos". Pour changer les actions affichées :

Ouvrez index.html.
Cherchez le bloc ``.
Dans le script JSON, modifiez la liste "symbols".
Format : { "s": "MARCHE:SYMBOLE", "d": "Nom affiché" }
Exemple : { "s": "NASDAQ:AAPL", "d": "Apple" }


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


### Progression
20251126 14:50 Édition Inline
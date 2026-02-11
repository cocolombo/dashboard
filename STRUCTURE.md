dashboard/
├── startme/               # Configuration principale Django (settings, urls)
├── dashboard/             # Application principale
│   ├── models.py          # Modèles de données (Page, Widget, Link)
│   ├── views.py           # Logique métier et endpoints HTMX
│   ├── urls.py            # Routes de l'application
│   ├── templates/
│   │   ├── dashboard/
│   │   │   └── index.html # LE fichier frontend principal (Monolithique)
│   │   └── partials/      # Fragments HTML pour HTMX (Formulaires, Items)
│   └── management/        # Commandes personnalisées (ex: seed_db)
├── static/                # Fichiers statiques (JS, CSS, Images)
│   ├── js/                # htmx.js, sortable.js, tailwind.js
│   └── css/
├── db.sqlite3             # Base de données locale
└── manage.py              # Point d'entrée Django



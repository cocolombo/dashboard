#!/bin/bash

# 1. Se déplacer dans le dossier du projet
cd /media/120gb/python/startme
# 2. Activer l'environnement virtuel
source venv/bin/activate

# 3. Lancer le serveur sur le port 8888 (comme PyCharm) en arrière-plan
# Le "&" à la fin permet de continuer le script
python manage.py runserver 8888 &

# 4. Attendre quelques secondes que le serveur soit prêt
sleep 5

# 5. Ouvrir le navigateur
xdg-open http://127.0.0.1:8888

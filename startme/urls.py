
from django.contrib import admin
from django.urls import path, include  # <--- Notez l'ajout de 'include' ici

urlpatterns = [
    path('admin/', admin.site.urls),
    # Cette ligne dit : "Pour la page d'accueil (vide), va chercher les URLs du dashboard"
    path('', include('dashboard.urls')), 
]
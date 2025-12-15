from django.contrib import admin
from .models import Page, Widget, Link

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Page.
    """
    # Affiche les champs 'name', 'slug', et 'order' dans la liste des pages.
    list_display = ('name', 'slug', 'order')

    # Pré-remplit automatiquement le champ 'slug' à partir du champ 'name' lors de la création.
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Widget.
    """
    # Affiche les champs 'title', 'page', et 'order' dans la liste des widgets.
    list_display = ('title', 'page', 'order')

    # Ajoute un filtre sur le côté pour trier les widgets par page.
    list_filter = ('page',)

@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    """
    Configuration de l'interface d'administration pour le modèle Link.
    """
    # Affiche les champs 'title', 'url', 'widget', et 'order' dans la liste des liens.
    list_display = ('title', 'url', 'widget', 'order')

    # Ajoute des filtres pour trier les liens par page (via le widget) et par widget.
    list_filter = ('widget__page', 'widget')

### Mes modèles

from django.db import models

class Page(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name

class Widget(models.Model):
    title = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='widgets')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.title

class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    icon_url = models.URLField(blank=True, null=True)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='links')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title


### Les routes
from django.urls import path
from . import views

urlpatterns = [
    # Navigation principale
    path('', views.index, name='index_root'),
    path('page/create/', views.create_page, name='create_page'),
    path('page/rename/<int:page_id>/', views.rename_page, name='rename_page'),
    path('page/delete/<int:page_id>/', views.delete_page, name='delete_page'),
    path('widget/move/<int:widget_id>/', views.move_widget_to_page, name='move_widget'),
    path('widget/delete/<int:widget_id>/', views.delete_widget, name='delete_widget'),
    path('widget/add/<int:page_id>/', views.add_widget, name='add_widget'),
    path('widget/<int:pk>/rename/', views.rename_widget, name='rename_widget'),
    path('link/<int:pk>/edit/', views.edit_link, name='edit_link'),



    # --- API (Pour le Javascript) ---
    path('api/update-order/', views.update_link_order, name='update_order'),
    path('api/move-link/<int:link_id>/', views.move_link_to_page, name='move_link'),

    # --- Actions manuelles (Boutons) ---
    # 1. Route pour ajouter un lien dans un widget spécifique
    path('link/add/<int:widget_id>/', views.add_link, name='add_link'),

    # 2. Route pour supprimer un lien spécifique
    path('link/delete/<int:link_id>/', views.delete_link, name='delete_link'),
    path('api/update-widget-order/', views.update_widget_order, name='update_widget_order'),

    path('page/<slug:slug>/', views.index, name='index'),

]

### Les règles UI
Tailwind, HTMX, Dark mode


État actuel : Le drag & drop et l'édition inline fonctionnent. Je veux maintenant travailler sur..."


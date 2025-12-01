Voici le contexte de mon projet actuel.

Contexte Technique du Projet Dashboard

1. Stack Technique

    Backend : Python 3.12, Django 5.2.
    Frontend : HTML5, Tailwind CSS (Local), HTMX (AJAX), SortableJS.
    Base de données : SQLite.
    Système : psutil pour le monitoring serveur.
    Design : Dark Mode par défaut.

2. Models (dashboard/models.py)

Structure hiérarchique : Page > Widget > Link.

Class Page: name, slug, order Class Widget: title, page(FK), order Class Link: title, url, icon_url, widget(FK), order

3. URLs (dashboard/urls.py)

Inclut les routes classiques (CRUD) et les APIs HTMX.
    path('', views.index, name='index_root')
    path('page/<slug:slug>/', views.index, name='index')
    path('page/create/', views.create_page, name='create_page')
    path('page/rename/<int:page_id>/', views.rename_page, name='rename_page')
    path('page/delete/<int:page_id>/', views.delete_page, name='delete_page')
    path('widget/add/<int:page_id>/', views.add_widget, name='add_widget')
    path('widget/delete/<int:widget_id>/', views.delete_widget, name='delete_widget')
    path('widget/move/<int:widget_id>/', views.move_widget_to_page, name='move_widget')
    path('widget/<int:pk>/rename/', views.rename_widget, name='rename_widget')
    path('widget/<int:widget_id>/toggle/', views.toggle_widget_collapse, name='toggle_widget_collapse'),
    path('link/add/<int:widget_id>/', views.add_link, name='add_link')
    path('link/delete/<int:link_id>/', views.delete_link, name='delete_link')
    path('link/<int:pk>/edit/', views.edit_link, name='edit_link')
    path('api/update-order/', views.update_link_order, name='update_order')
    path('api/update-widget-order/', views.update_widget_order, name='update_widget_order')
    path('api/move-link/<int:link_id>/', views.move_link_to_page, name='move_link')
    path('api/system-monitor/', views.system_monitor, name='system_monitor')

4. Les modèles

class Page(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

class Widget(models.Model):
    title = models.CharField(max_length=100)
    page = models.ForeignKey(Page, on_delete=models.CASCADE, related_name='widgets')
    order = models.IntegerField(default=0)
    is_collapsed = models.BooleanField(default=False) 

    class Meta:
        ordering = ['order']

class Link(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField()
    icon_url = models.URLField(blank=True, null=True)
    widget = models.ForeignKey(Widget, on_delete=models.CASCADE, related_name='links')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']


5. Règles UI & Frontend

    Templates : Un seul template principal index.html situé dans startme/templates/dashboard/.
    Partials : Les fragments HTML pour HTMX sont dans startme/templates/partials/.

    Interactions :

        Drag & Drop : SortableJS, sauvegarde via API fetch.
        Édition : Inline via HTMX (hx-swap="outerHTML").
        Mode Zen : Bouton JS pur + classe CSS .zen-mode.
        Widgets Spéciaux : Météo (API JS), Calendrier (JS Frontend), Bourse (Iframe), Système (HTMX Polling 5s).
        
        
from django.urls import path
from . import views

urlpatterns = [
    # Navigation principale
    path('', views.index, name='index_root'),
    path('page/create/', views.create_page, name='create_page'),
    path('page/rename/<int:page_id>/', views.rename_page, name='rename_page'),
    path('page/delete/<int:page_id>/', views.delete_page, name='delete_page'),
    path('widget/move/<int:widget_id>/', views.move_widget_to_page, name='move_widget'),


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

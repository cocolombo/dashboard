from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from .models import Page, Widget, Link

def index(request, slug=None):
    """
    Affiche la page principale du tableau de bord (Dashboard).

    Cette vue gère l'affichage des onglets (Pages) et du contenu de la page active
    (Widgets et Liens).

    Args:
        request (HttpRequest): L'objet de requête HTTP.
        slug (str, optional): Le slug de la page à afficher.
                              Si None, la première page disponible est affichée.

    Returns:
        HttpResponse: La page HTML rendue avec le contexte (pages, active_page).
    """
    pages = Page.objects.all()
    if not slug:
        active_page = pages.first()
    else:
        active_page = get_object_or_404(Page, slug=slug)

    context = {
        'pages': pages,
        'active_page': active_page,
    }
    return render(request, 'dashboard/index.html', context)


@csrf_exempt
@require_POST
def update_link_order(request):
    """
    API pour mettre à jour l'ordre et le parent des liens via Drag & Drop.

    Appelée par SortableJS lorsqu'un lien est déplacé. Elle gère deux cas :
    1. Réorganisation au sein du même widget.
    2. Déplacement d'un lien vers un autre widget.

    Args:
        request (HttpRequest): Requête POST contenant :
            - widget_id (str): L'ID du widget de destination.
            - link (list): Liste ordonnée des IDs des liens dans ce widget.

    Returns:
        HttpResponse: Statut 200 si succès.
    """
    # 1. On récupère l'ID du widget dans lequel le lien a atterri
    widget_id = request.POST.get('widget_id')

    # 2. On récupère la liste des liens dans leur nouvel ordre
    link_ids = request.POST.getlist('link')

    # Si on a un widget_id (donc un déplacement ou réarrangement)
    if widget_id:
        target_widget = get_object_or_404(Widget, id=widget_id)

        for index, link_id in enumerate(link_ids):
            try:
                link = Link.objects.get(id=link_id)

                # On change le parent du lien pour le nouveau widget
                link.widget = target_widget

                # On met à jour sa position
                link.order = index
                link.save()
            except Link.DoesNotExist:
                continue

    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def update_widget_order(request):
    """
    API pour mettre à jour l'ordre des widgets (catégories) sur une page.

    Appelée par SortableJS lors du déplacement d'un bloc widget entier.

    Args:
        request (HttpRequest): Requête POST contenant :
            - widget (list): Liste ordonnée des IDs des widgets.

    Returns:
        HttpResponse: Statut 200 si succès.
    """
    widget_ids = request.POST.getlist('widget')

    for index, widget_id in enumerate(widget_ids):
        try:
            widget = get_object_or_404(Widget, id=widget_id)
            widget.order = index
            widget.save()
        except:
            continue

    return HttpResponse(status=200)


@csrf_exempt
@require_POST
def move_link_to_page(request, link_id):
    """
    API pour déplacer un lien vers une autre page via le menu contextuel.

    Le lien est déplacé vers le premier widget disponible de la page cible.

    Args:
        request (HttpRequest): Requête POST contenant 'target_page_id'.
        link_id (int): L'ID du lien à déplacer.

    Returns:
        HttpResponse: Statut 200 si succès, 400 si aucun widget cible trouvé.
    """
    link = get_object_or_404(Link, id=link_id)
    target_page_id = request.POST.get('target_page_id')
    target_page = get_object_or_404(Page, id=target_page_id)

    # On déplace vers le premier widget de la page cible par défaut
    target_widget = target_page.widgets.first()

    if target_widget:
        link.widget = target_widget
        link.save()
        return HttpResponse(status=200)
    return HttpResponse(status=400)


@require_POST
def add_link(request, widget_id):
    """
    Ajoute un nouveau lien dans un widget spécifique.

    Args:
        request (HttpRequest): Requête POST contenant 'title' et 'url'.
        widget_id (int): L'ID du widget parent.

    Returns:
        HttpResponseRedirect: Redirige vers la page précédente (HTTP_REFERER).
    """
    widget = get_object_or_404(Widget, id=widget_id)
    title = request.POST.get('title')
    url = request.POST.get('url')

    # On crée le lien à la fin de la liste (order=999 pour être sûr qu'il est dernier)
    if title and url:
        Link.objects.create(title=title, url=url, widget=widget, order=999)

    # On recharge la page précédente
    return redirect(request.META.get('HTTP_REFERER', '/'))


def delete_link(request, link_id):
    """
    Supprime un lien spécifique.

    Args:
        request (HttpRequest): L'objet de requête.
        link_id (int): L'ID du lien à supprimer.

    Returns:
        HttpResponseRedirect: Redirige vers la page précédente.
    """
    link = get_object_or_404(Link, id=link_id)
    link.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def create_page(request):
    """
    Crée une nouvelle page (onglet) dans le tableau de bord.

    Gère la création automatique d'un slug unique basé sur le nom.

    Args:
        request (HttpRequest): Requête POST contenant 'name'.

    Returns:
        HttpResponseRedirect: Redirige vers la nouvelle page créée.
    """
    name = request.POST.get('name')
    if name:
        # On génère un slug unique (ex: "Ma Page" -> "ma-page")
        base_slug = slugify(name)
        slug = base_slug
        counter = 1

        # Gestion des doublons de slug
        while Page.objects.filter(slug=slug).exists():
            slug = f"{base_slug}-{counter}"
            counter += 1

        # On crée la page (à la fin de la liste par défaut)
        Page.objects.create(name=name, slug=slug, order=999)

        # On redirige immédiatement vers la nouvelle page
        return redirect('index', slug=slug)

    return redirect('index_root')


@require_POST
def rename_page(request, page_id):
    """
    Renomme une page existante.

    Met à jour le nom et régénère le slug pour garder l'URL cohérente.

    Args:
        request (HttpRequest): Requête POST contenant le nouveau 'name'.
        page_id (int): L'ID de la page à modifier.

    Returns:
        HttpResponseRedirect: Redirige vers la page avec son nouveau slug.
    """
    page = get_object_or_404(Page, id=page_id)
    new_name = request.POST.get('name')

    if new_name:
        page.name = new_name
        # Mise à jour du slug
        page.slug = slugify(new_name)
        page.save()
        return redirect('index', slug=page.slug)

    return redirect('index', slug=page.slug)


def delete_page(request, page_id):
    """
    Supprime une page complète et tout son contenu (widgets/liens).

    Args:
        request (HttpRequest): L'objet de requête.
        page_id (int): L'ID de la page à supprimer.

    Returns:
        HttpResponseRedirect: Redirige vers la racine (index_root).
    """
    page = get_object_or_404(Page, id=page_id)
    page.delete()
    return redirect('index_root')


@require_POST
def move_widget_to_page(request, widget_id):
    """
    Déplace un widget (catégorie) entier vers une autre page.

    Args:
        request (HttpRequest): Requête POST contenant 'target_page_id'.
        widget_id (int): L'ID du widget à déplacer.

    Returns:
        HttpResponseRedirect: Redirige vers la page d'origine (HTTP_REFERER).
    """
    widget = get_object_or_404(Widget, id=widget_id)
    target_page_id = request.POST.get('target_page_id')

    if target_page_id:
        target_page = get_object_or_404(Page, id=target_page_id)
        widget.page = target_page
        # On place le widget à la fin de la nouvelle page
        widget.order = 999
        widget.save()

    # On recharge la page actuelle pour voir le widget disparaître
    return redirect(request.META.get('HTTP_REFERER', '/'))


# dashboard/views.py

def delete_widget(request, widget_id):
    widget = get_object_or_404(Widget, id=widget_id)
    widget.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


# dashboard/views.py

@require_POST
def add_widget(request, page_id):
    page = get_object_or_404(Page, id=page_id)
    title = request.POST.get('title')

    if title:
        # On crée le widget à la fin de la liste
        Widget.objects.create(title=title, page=page, order=999)

    # On recharge la page courante
    return redirect('index', slug=page.slug)

def rename_widget(request, pk):
    widget = get_object_or_404(Widget, pk=pk)

    # 1. Si on reçoit du POST, c'est que l'utilisateur a validé le formulaire
    if request.method == "POST":
        new_title = request.POST.get('title')
        if new_title:
            widget.title = new_title
            widget.save()
        # On renvoie le template d'affichage (le HTML normal)
        return render(request, 'partials/widget_title.html', {'widget': widget})

    # 2. Si on reçoit du GET, c'est que l'utilisateur a cliqué pour éditer
    # On renvoie le formulaire d'édition
    return render(request, 'partials/widget_title_form.html', {'widget': widget})


# views.py
def edit_link(request, pk):
    link = get_object_or_404(Link, pk=pk)

    if request.method == "POST":
        link.title = request.POST.get('title')
        link.url = request.POST.get('url')
        # On peut aussi relancer la récupération du favicon si l'URL change
        link.save()
        return render(request, 'partials/link_item.html', {'link': link})

    return render(request, 'partials/link_form.html', {'link': link})











from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils.text import slugify
from .models import Page, Widget, Link
import psutil
import subprocess
import os

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


def delete_widget(request, widget_id):
    """
    Supprime un widget (catégorie) et tous les liens ou notes qu'il contient.

    Args:
        request (HttpRequest): L'objet de requête.
        widget_id (int): L'ID du widget à supprimer.

    Returns:
        HttpResponseRedirect: Redirige vers la page précédente.
    """
    widget = get_object_or_404(Widget, id=widget_id)
    widget.delete()
    return redirect(request.META.get('HTTP_REFERER', '/'))


@require_POST
def add_widget(request, page_id):
    """
    Ajoute une nouvelle catégorie (Widget) sur une page spécifique.

    Prend en compte le type de widget sélectionné (Liste ou Bloc-notes).

    Args:
        request (HttpRequest): Requête POST contenant 'title' et 'widget_type'.
        page_id (int): L'ID de la page parente.

    Returns:
        HttpResponseRedirect: Redirige vers la page active (index).
    """
    page = get_object_or_404(Page, id=page_id)
    title = request.POST.get('title')
    # C'est la ligne magique qui manquait :
    # On récupère le choix fait dans la modale (ou 'list' par défaut)
    w_type = request.POST.get('widget_type', 'list')

    if title:
        Widget.objects.create(
            title=title,
            page=page,
            order=999,
            widget_type=w_type  # On enregistre le type en base de données
        )

    return redirect('index', slug=page.slug)


def rename_widget(request, pk):
    """
    Gère l'affichage et la mise à jour du titre d'un widget (Mode édition In-Line).

    Utilisé par HTMX.
    - GET : Renvoie le formulaire d'édition du titre.
    - POST : Met à jour le titre et renvoie le titre affiché (HTML).

    Args:
        request (HttpRequest): L'objet de requête.
        pk (int): La clé primaire (ID) du widget.

    Returns:
        HttpResponse: Le fragment HTML (Partial) correspondant à l'état (formulaire ou titre).
    """
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


def edit_link(request, pk):
    """
    Gère l'édition d'un lien (Titre et URL) en mode 'In-Place'.

    Utilisé par HTMX.
    - GET : Renvoie le formulaire d'édition à la place du lien.
    - POST : Sauvegarde les modifications et renvoie l'élément lien standard.

    Args:
        request (HttpRequest): L'objet de requête.
        pk (int): La clé primaire (ID) du lien.

    Returns:
        HttpResponse: Le fragment HTML (Partial) mis à jour.
    """
    link = get_object_or_404(Link, pk=pk)

    if request.method == "POST":
        # Sauvegarde
        link.title = request.POST.get('title')
        link.url = request.POST.get('url')
        link.save()
        # On renvoie l'item normal mis à jour
        return render(request, 'partials/link_item.html', {'link': link})

    # Si GET, on renvoie le formulaire d'édition
    return render(request, 'partials/link_form.html', {'link': link})


# dashboard/views.py

def get_gpu_stats():
    """Récupère VRAM et Température via nvidia-smi sans librairie tierce."""
    try:
        # On demande : température, mémoire utilisée, mémoire totale
        cmd = "nvidia-smi --query-gpu=temperature.gpu,memory.used,memory.total --format=csv,noheader,nounits"
        output = subprocess.check_output(cmd.split(), encoding='utf-8')
        temp, used, total = map(int, output.strip().split(', '))
        return {
            'temp': temp,
            'used': used,
            'total': total,
            'percent': round((used / total) * 100, 1)
        }
    except Exception:
        return None  # Pas de GPU Nvidia ou erreur driver


def system_monitor(request):
    """
    Récupère les métriques du système (CPU, GPU, RAM, Disque) pour le widget de monitoring.

    Cette vue est appelée périodiquement par HTMX (Polling).

    Args:
        request (HttpRequest): L'objet de requête.

    Returns:
        HttpResponse: Le fragment HTML (Partial) avec les jauges et valeurs mises à jour.
    """
    # 1. CPU & RAM (Existant)
    cpu = psutil.cpu_percent(interval=None)
    ram = psutil.virtual_memory()

    # 2. DISQUES (CONFIGURATION À ADAPTER ICI)
    # Remplacez les chemins par VOS points de montage (ceux trouvés avec df -h)
    disks_to_check = [
        {'name': 'Système', 'path': '/'},
        {'name': 'Data 3TB', 'path': '/media/nimzo/3tb'},  # <--- Mettez votre chemin ici
        {'name': 'Fast 120GB', 'path': '/media/120gb'},  # <--- Mettez votre chemin ici
    ]

    disks_info = []
    for d in disks_to_check:
        try:
            usage = psutil.disk_usage(d['path'])
            disks_info.append({
                'name': d['name'],
                'percent': usage.percent,
                'free_gb': round(usage.free / (1024 ** 3), 0),
                'total_gb': round(usage.total / (1024 ** 3), 0)
            })
        except FileNotFoundError:
            # Si le disque n'est pas monté, on l'ignore ou on met 0
            continue

    # 3. GPU
    gpu = get_gpu_stats()

    context = {
        'cpu_usage': cpu,
        'ram_percent': ram.percent,
        'ram_used_gb': round(ram.used / (1024 ** 3), 1),
        'ram_total_gb': round(ram.total / (1024 ** 3), 1),
        'disks': disks_info,  # On envoie la liste des disques
        'gpu': gpu,
    }
    return render(request, 'partials/system_monitor.html', context)







@require_POST
def save_note_content(request, widget_id):
    """
    Sauvegarde automatiquement le contenu textuel d'un widget 'Bloc-notes'.

    Déclenché par HTMX lors de la frappe ou de la perte de focus.

    Args:
        request (HttpRequest): Requête POST contenant 'content'.
        widget_id (int): L'ID du widget.

    Returns:
        HttpResponse: Statut 200 OK (pas de rendu HTML nécessaire).
    """
    widget = get_object_or_404(Widget, id=widget_id)
    # On récupère le contenu envoyé par le champ texte
    new_content = request.POST.get('content', '')
    widget.content = new_content
    widget.save()
    # On ne renvoie rien (ou un petit statut 200 OK), HTMX n'a pas besoin de redessiner
    return HttpResponse(status=200)


def open_local_file(request, link_id):
    """
    Ouvre un fichier ou dossier local sur le serveur (l'ordinateur de l'utilisateur).

    Utilise la commande système `xdg-open` pour contourner les restrictions de sécurité
    des navigateurs concernant les liens `file://`.

    Args:
        request (HttpRequest): L'objet de requête.
        link_id (int): L'ID du lien contenant le chemin local.

    Returns:
        HttpResponse:
            - 204 (No Content) si succès (l'action est faite côté système).
            - 404 si le fichier n'existe pas sur le disque.
    """
    link = get_object_or_404(Link, id=link_id)
    path = link.url.strip()

    # Nettoyage si l'utilisateur a copié "file://"
    if path.startswith('file://'):
        path = path[7:]

    if os.path.exists(path):
        # xdg-open est la commande magique d'Ubuntu pour ouvrir n'importe quoi
        # avec le programme par défaut
        subprocess.Popen(['xdg-open', path], start_new_session=True)
        return HttpResponse(status=204) # 204 = Succès, ne fais rien sur la page
    else:
        print(f"Erreur: Fichier introuvable -> {path}")
        return HttpResponse(status=404)


@csrf_exempt
@require_POST
def update_page_order(request):
    """
    API pour réorganiser les pages (onglets) via Drag & Drop.
    """
    page_ids = request.POST.getlist('page')

    for index, page_id in enumerate(page_ids):
        try:
            page = get_object_or_404(Page, id=page_id)
            page.order = index
            page.save()
        except:
            continue

    return HttpResponse(status=200)
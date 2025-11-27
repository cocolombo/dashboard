### Personnalisation (Guide CSS & UI)
Le design est géré via Tailwind CSS. La majorité des modifications se font directement dans dashboard/templates/dashboard/index.html.

1. Grille et Disposition (Colonnes)
Pour changer le nombre de catégories affichées par ligne :

Fichier : index.html
Chercher : id="widget-grid"
Modifier : La classe lg:grid-cols-4
lg:grid-cols-3 : Plus large (3 colonnes)
lg:grid-cols-5 : Plus compact (5 colonnes)
grid-cols-1 : Mobile (1 colonne)

2. Thème et Couleurs
Fond global : Balise <body>, classe bg-gray-900.
Fond des Widgets : Cherchez bg-gray-800 et remplacez par une autre nuance (ex: bg-slate-800).

Titres (Couleur d'accent) : Cherchez text-orange-400. Remplacez par :
Bleu : text-blue-400
Vert : text-green-400
Violet : text-purple-400

3. Densité (Espacement des liens)
Pour rendre la liste des liens plus compacte ou plus aérée :
Fichier : templates/partials/link_item.html (ou dans la boucle <ul> de index.html)

Modifier :
space-y-0 ou space-y-1 sur le conteneur <ul>.
py-1 (padding vertical) sur les éléments <li>.

### Configuration des Widgets Spéciau

Widget Bourse (TradingView)
Le widget financier dans l'onglet "Infos" est un script externe injecté.
Fichier : index.html (Section "Infos")
Modification : Cherchez le script JSON dans la balise <script ... embed-widget-market-overview.js">.

Format :
JSON
{
  "symbols": [
    { "s": "NASDAQ:AAPL", "d": "Apple" },
    { "s": "FOREXCOM:SPXUSD", "d": "S&P 500" },
    { "s": "BITSTAMP:BTCUSD", "d": "Bitcoin" }
  ]
}
Widget Météo (Open-Meteo)
Fichier : index.html (Script JS en bas de page)
Variable : const weatherAPI = "..."
Modification : Changez latitude et longitude dans l'URL pour votre ville.

// Exemple pour Paris
const weatherAPI = "[https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522](https://api.open-meteo.com/v1/forecast?latitude=48.8566&longitude=2.3522)&...";


## Personnalisation (Guide Rapide)
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

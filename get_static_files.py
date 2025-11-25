import os
import urllib.request

# Configuration
FILES = {
    "htmx.js": "https://unpkg.com/htmx.org@1.9.6/dist/htmx.min.js",
    "sortable.js": "https://cdnjs.cloudflare.com/ajax/libs/Sortable/1.14.0/Sortable.min.js",
    "tailwind.js": "https://cdn.tailwindcss.com"
}

# Dossier cible
TARGET_DIR = os.path.join("static", "js")


def download_files():
    # 1. Créer le dossier s'il n'existe pas
    if not os.path.exists(TARGET_DIR):
        os.makedirs(TARGET_DIR)
        print(f"📁 Dossier créé : {TARGET_DIR}")

    # 2. Télécharger chaque fichier
    for filename, url in FILES.items():
        file_path = os.path.join(TARGET_DIR, filename)
        print(f"⬇️  Téléchargement de {filename}...")

        try:
            # On utilise un User-Agent pour ne pas être bloqué par les sites
            req = urllib.request.Request(
                url,
                data=None,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response, open(file_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"✅ {filename} sauvegardé avec succès.")
        except Exception as e:
            print(f"❌ Erreur sur {filename}: {e}")


if __name__ == "__main__":
    download_files()

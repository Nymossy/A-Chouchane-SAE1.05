import os
import markdown

def enregistrer_resultats_markdown(visites_sources, visites_destinations, file_path, nombre_trames):
    """
    Enregistre les résultats pertinents dans un fichier Markdown.
    
    :param visites_sources: Dictionnaire des visites des sources
    :param visites_destinations: Dictionnaire des visites des destinations
    :param file_path: Chemin du fichier Markdown
    :param nombre_trames: Nombre total de trames
    """
    with open(file_path, 'w', encoding='utf-8') as mdfile:
        mdfile.write("#  Analyse du tcpdump :\n\n")
        
        # Afficher le nombre de trames
        mdfile.write(f"## Nombre de trames : {nombre_trames}\n\n")
        
        # Afficher les sources avec leur nombre de requêtes par ordre croissant
        mdfile.write("## Requêtes des sources (par ordre croissant)\n")
        for source, count in sorted(visites_sources.items(), key=lambda item: item[1]):
            mdfile.write(f"- **{source}** : {count} requêtes\n")
        
        
        # Afficher l'activité suspecte
        mdfile.write("\n## Activité suspecte\n")
        if "190-0-175-100.gba.solunet.com.ar" in visites_sources:
            mdfile.write(f"- **190-0-175-100.gba.solunet.com.ar** : {visites_sources['190-0-175-100.gba.solunet.com.ar']} requêtes\n")
        if "BP-Linux8" in visites_sources:
            mdfile.write(f"- **BP-Linux8** : {visites_sources['BP-Linux8']} requêtes\n")

def convertir_markdown_en_html(contenu_markdown):
    """
    Convertit le contenu Markdown en HTML.
    
    :param contenu_markdown: Texte du fichier Markdown
    :return: Texte HTML
    """
    return markdown.markdown(contenu_markdown)

def enregistrer_html(contenu_html, file_path):
    """
    Enregistre le contenu HTML dans un fichier.
    
    :param contenu_html: Texte HTML
    :param file_path: Chemin du fichier HTML
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(contenu_html)

def creer_page_html_depuis_markdown(markdown_file_path, html_file_path):
    """
    Crée une page HTML à partir d'un fichier Markdown.
    
    :param markdown_file_path: Chemin du fichier Markdown
    :param html_file_path: Chemin du fichier HTML
    """
    contenu_markdown = lire_fichier_markdown(markdown_file_path)
    contenu_html = convertir_markdown_en_html(contenu_markdown)
    enregistrer_html(contenu_html, html_file_path)

def lire_fichier_markdown(file_path):
    """
    Lit le contenu d'un fichier Markdown et retourne le texte sous forme de chaîne.
    
    :param file_path: Le chemin du fichier Markdown
    :return: Texte du fichier Markdown
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            contenu = file.read()
        return contenu
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{file_path}' n'a pas été trouvé.")
        return ""
    except IOError:
        print(f"Erreur: Impossible de lire le fichier '{file_path}'.")
        return ""

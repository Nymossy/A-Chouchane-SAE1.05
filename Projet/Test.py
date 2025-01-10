# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:00:00 2024

Programme pour traiter le fichier texte "Fichier texte à traiter.txt"
"""

import re
import os

def lire_fichier(file_path):
    """
    Lit le contenu d'un fichier texte et retourne les lignes sous forme de liste.
    
    :param file_path: Le chemin du fichier texte
    :return: Liste des lignes du fichier
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lignes = file.readlines()
        return [ligne.strip() for ligne in lignes]
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{file_path}' n'a pas été trouvé.")
        return []
    except IOError:
        print(f"Erreur: Impossible de lire le fichier '{file_path}'.")
        return []

def extraire_informations(lignes):
    """
    Extrait les informations spécifiques des lignes du fichier texte.
    
    :param lignes: Liste des lignes à traiter
    :return: Liste des dictionnaires des informations extraites
    """
    informations = []
    
    ip_pattern = re.compile(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b')
    machine_name_pattern = re.compile(r'\b(?:[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)\b')
    url_pattern = re.compile(r'\b(?:[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+\.[a-zA-Z0-9-_]+)\b')
    
    for ligne in lignes:
        if ligne.startswith("11:42"):
            info = {
                'nom_machine': None,
                'adresse_ip': None,
                'adresse_site_web': None
            }
            
            if machine_name_match := machine_name_pattern.search(ligne):
                info['nom_machine'] = machine_name_match.group()
            if ip_match := ip_pattern.search(ligne):
                info['adresse_ip'] = ip_match.group()
            if url_match := url_pattern.search(ligne):
                info['adresse_site_web'] = url_match.group()
            
            informations.append(info)
    
    return informations

def main():
    # Afficher le répertoire de travail actuel
    print("Répertoire de travail actuel :", os.getcwd())

    # Définir le chemin du fichier texte
    file_path = "Projet/tcpdump.txt"  # Utiliser un chemin relatif
    
    # Lire le fichier et obtenir les lignes
    lignes = lire_fichier(file_path)
    
    # Extraire les informations des lignes lues
    informations = extraire_informations(lignes)
    
    # Afficher les informations extraites
    print("Informations extraites :")
    for info in informations:
        print(info)

# Point d'entrée du programme
if __name__ == "__main__":
    main()
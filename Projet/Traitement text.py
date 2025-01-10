# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:00:00 2024

Programme pour traiter le fichier texte "Fichier texte à traiter.txt"
"""

import re
import os
import csv
from collections import defaultdict

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

def compter_acces(informations):
    """
    Compte le nombre de fois qu'une même adresse IP accède à un même site web et le nombre de fois qu'un site web est visité.
    
    :param informations: Liste des dictionnaires des informations extraites
    :return: Dictionnaire avec les adresses IP et les sites web et leur nombre d'accès, et le nombre de visites par site web
    """
    acces = defaultdict(int)
    visites_site_web = defaultdict(int)
    
    for info in informations:
        if info['adresse_ip'] and info['adresse_site_web']:
            key = (info['adresse_ip'], info['adresse_site_web'])
            acces[key] += 1
        if info['adresse_site_web']:
            visites_site_web[info['adresse_site_web']] += 1
    
    return acces, visites_site_web

def enregistrer_informations_csv(informations, file_path):
    """
    Enregistre les informations extraites dans un fichier CSV.
    
    :param informations: Liste des dictionnaires des informations extraites
    :param file_path: Chemin du fichier CSV
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['nom_machine', 'adresse_ip', 'adresse_site_web']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for info in informations:
            writer.writerow(info)

def main():
    # Afficher le répertoire de travail actuel
    print("Répertoire de travail actuel :", os.getcwd())

    # Définir le chemin du fichier texte
    file_path = "Projet/tcpdump.txt"  # Utiliser un chemin relatif
    
    # Lire le fichier et obtenir les lignes
    lignes = lire_fichier(file_path)
    
    # Extraire les informations des lignes lues
    informations = extraire_informations(lignes)
    
    # Enregistrer les informations extraites dans un fichier CSV
    csv_file_path = "Projet/informations_extraites.csv"
    enregistrer_informations_csv(informations, csv_file_path)
    
    # Compter les accès des adresses IP aux sites web et les visites par site web
    acces, visites_site_web = compter_acces(informations)
    
    # Afficher les informations extraites
    print("Informations extraites :")
    for info in informations:
        print(info)
    
    # Afficher tous les accès des adresses IP aux sites web
    print("\nTous les accès des adresses IP aux sites web :")
    for (ip, site), count in acces.items():
        print(f"{ip} accède à {site} : {count} fois")
    
    # Afficher le nombre de visites par site web
    print("\nNombre de visites par site web :")
    for site, count in visites_site_web.items():
        print(f"{site} : {count} visites")
    
    # Afficher les accès des adresses IP aux sites web avec un nombre supérieur ou égal à 50
    print("\nAccès des adresses IP aux sites web (50 fois ou plus) :")
    for (ip, site), count in sorted(acces.items(), key=lambda item: item[1]):
        if count >= 50:
            print(f"{ip} accède à {site} : {count} fois")
    
    # Afficher les sites web visités 50 fois ou plus, sans adresse IP associée
    print("\nSites web visités (50 fois ou plus, sans adresse IP associée) :")
    for site, count in sorted(visites_site_web.items(), key=lambda item: item[1]):
        if count >= 50 and not any(ip == site for ip, _ in acces.keys()):
            print(f"{site} : {count} visites")

# Point d'entrée du programme
if __name__ == "__main__":
    main()
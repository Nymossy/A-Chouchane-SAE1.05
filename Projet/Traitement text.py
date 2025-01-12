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

def filtrer_lignes(lignes):
    """
    Filtre les lignes qui commencent soit par "11:42", soit qui ne commencent pas par "0x".
    
    :param lignes: Liste des lignes à filtrer
    :return: Liste des lignes filtrées
    """
    lignes_filtrees = [ligne for ligne in lignes if ligne.startswith("11:42") or not ligne.startswith("0x")]
    return lignes_filtrees

def ecrire_fichier(file_path, lignes):
    """
    Écrit les lignes filtrées dans un nouveau fichier texte.
    
    :param file_path: Chemin du fichier texte
    :param lignes: Liste des lignes à écrire
    """
    with open(file_path, 'w', encoding='utf-8') as file:
        for ligne in lignes:
            file.write(ligne + '\n')

def extraire_informations(lignes):
    """
    Extrait les informations de source et de destination des lignes du fichier texte.
    
    :param lignes: Liste des lignes à traiter
    :return: Liste des dictionnaires des informations extraites
    """
    informations = []
    
    pattern = re.compile(r'IP\s+([^\s>]+)\s+>\s+([^\s:]+)')
    
    for ligne in lignes:
        if match := pattern.search(ligne):
            info = {
                'source': match.group(1),
                'destination': match.group(2)
            }
            informations.append(info)
    
    return informations

def enregistrer_informations_csv(informations, file_path):
    """
    Enregistre les informations extraites dans un fichier CSV.
    
    :param informations: Liste des dictionnaires des informations extraites
    :param file_path: Chemin du fichier CSV
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source', 'destination']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for info in informations:
            writer.writerow(info)

def normaliser_nom_machine(nom):
    """
    Normalise le nom de la machine pour regrouper les occurrences de "BP-Linux8", "par", et "190-0-175-100.gba.solunet.com.ar".
    
    :param nom: Le nom de la machine
    :return: Le nom normalisé de la machine
    """
    if nom.startswith("BP-Linux8"):
        return "BP-Linux8"
    if nom.startswith("par"):
        return "par.1e100"
    if nom.startswith("190-0-175-100.gba.solunet.com.ar"):
        return "190-0-175-100.gba.solunet.com.ar"
    return nom

def compter_visites(informations):
    """
    Compte combien de fois une source et une destination sont visitées.
    
    :param informations: Liste des dictionnaires des informations extraites
    :return: Deux dictionnaires avec les sources et les destinations et leur nombre de visites
    """
    visites_sources = defaultdict(int)
    visites_destinations = defaultdict(int)
    
    for info in informations:
        source = normaliser_nom_machine(info['source'])
        destination = normaliser_nom_machine(info['destination'])
        visites_sources[source] += 1
        visites_destinations[destination] += 1
    
    return visites_sources, visites_destinations

def enregistrer_visites_csv(visites_sources, visites_destinations, file_path):
    """
    Enregistre les visites des sources et des destinations dans un fichier CSV.
    
    :param visites_sources: Dictionnaire des visites des sources
    :param visites_destinations: Dictionnaire des visites des destinations
    :param file_path: Chemin du fichier CSV
    """
    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['source', 'nombre_requete_source', 'destination', 'nombre_visites_destination']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        
        # Écrire les sources et leurs visites
        for source, count in visites_sources.items():
            writer.writerow({'source': source, 'nombre_requete_source': count})
        
        # Écrire les destinations et leurs visites
        for destination, count in visites_destinations.items():
            writer.writerow({'destination': destination, 'nombre_visites_destination': count})

def main():
    # Afficher le répertoire de travail actuel
    print("Répertoire de travail actuel :", os.getcwd())

    # Définir le chemin du fichier texte
    file_path = "Projet/tcpdump.txt"  # Utiliser un chemin relatif
    
    # Lire le fichier et obtenir les lignes
    lignes = lire_fichier(file_path)
    
    # Filtrer les lignes et écrire dans un nouveau fichier texte
    lignes_filtrees = filtrer_lignes(lignes)
    resume_file_path = "Projet/tcpdump_resume.txt"
    ecrire_fichier(resume_file_path, lignes_filtrees)
    
    # Lire le fichier résumé et obtenir les lignes
    lignes_resume = lire_fichier(resume_file_path)
    
    # Extraire les informations des lignes filtrées
    informations = extraire_informations(lignes_resume)
    
    # Enregistrer les informations extraites dans un fichier CSV
    csv_file_path = "Projet/informations_extraites.csv"
    enregistrer_informations_csv(informations, csv_file_path)
    
    # Compter les visites des sources et des destinations
    visites_sources, visites_destinations = compter_visites(informations)
    
    # Afficher les visites des sources par ordre croissant, avec 100 visites ou plus
    print("\nRequêtes des sources (100 ou plus) :")
    for source, count in sorted(visites_sources.items(), key=lambda item: item[1]):
        if count >= 100:
            print(f"{source} : {count} requêtes")
    
    # Afficher les visites des destinations par ordre croissant, avec 100 visites ou plus
    print("\nVisites des destinations (100 visites ou plus) :")
    for destination, count in sorted(visites_destinations.items(), key=lambda item: item[1]):
        if count >= 100:
            print(f"{destination} : {count} visites")
    
    # Enregistrer les visites des sources et des destinations dans un fichier CSV
    visites_csv_file_path = "Projet/nombre_requetes.csv"
    enregistrer_visites_csv(visites_sources, visites_destinations, visites_csv_file_path)

# Point d'entrée du programme
if __name__ == "__main__":
    main()
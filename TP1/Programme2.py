# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 11:11:35 2024

@author: aciac
"""
import re

def tab(file_path):
    """
    Fonction pour lire un fichier ICS ligne par ligne et stocker chaque ligne dans un tableau.

    :param file_path: Le chemin du fichier .ics
    :return: Liste contenant les lignes du fichier.
    """
    lines = []  # Initialisation de la liste pour stocker les lignes
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Lire le fichier ligne par ligne et ajouter chaque ligne à la liste
            for line in file:
                lines.append(line.strip())  # Ajouter la ligne après suppression des espaces et retours à la ligne
    except FileNotFoundError:
        print(f"Erreur: Le fichier '{file_path}' n'a pas été trouvé.")
    except IOError:
        print(f"Erreur: Impossible d'ouvrir le fichier '{file_path}'.")

    return lines

def parse_event(lines):
    """
    Analyse les lignes d'un fichier ICS pour extraire les informations d'un événement unique.

    :param lines: Liste des lignes représentant un événement ICS
    :return: Chaîne formatée selon les spécifications ou "vide" pour les champs manquants.
    """
    # Dictionnaire pour stocker les données d'événement
    event_data = {
        "UID": "vide",
        "DTSTART": "vide",
        "DTEND": "vide",
        "SUMMARY": "vide",
        "LOCATION": "vide",
        "DESCRIPTION": "vide"
    }

    # Parcourir les lignes pour extraire les informations pertinentes
    for line in lines:
        if line.startswith("UID:"):
            event_data["UID"] = line.split("UID:")[1]
        elif line.startswith("DTSTART:"):
            event_data["DTSTART"] = line.split("DTSTART:")[1]
        elif line.startswith("DTEND:"):
            event_data["DTEND"] = line.split("DTEND:")[1]
        elif line.startswith("SUMMARY:"):
            event_data["SUMMARY"] = line.split("SUMMARY:")[1]
        elif line.startswith("LOCATION:"):
            event_data["LOCATION"] = line.split("LOCATION:")[1]
        elif line.startswith("DESCRIPTION:"):
            event_data["DESCRIPTION"] = line.split("DESCRIPTION:")[1]

    # Transformer DTSTART et DTEND pour extraire la date et l'heure
    start_match = re.match(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})", event_data["DTSTART"])
    end_match = re.match(r"(\d{4})(\d{2})(\d{2})T(\d{2})(\d{2})", event_data["DTEND"])

    if start_match and end_match:
        start_date = f"{start_match.group(3)}-{start_match.group(2)}-{start_match.group(1)}"
        start_time = f"{start_match.group(4)}:{start_match.group(5)}"
        end_time = f"{end_match.group(4)}:{end_match.group(5)}"
    else:
        start_date, start_time, end_time = "vide", "vide", "vide"

    # Calculer la durée de l'événement
    try:
        start_hour, start_minute = map(int, start_time.split(":"))
        end_hour, end_minute = map(int, end_time.split(":"))
        duration_hours = end_hour - start_hour
        duration_minutes = end_minute - start_minute
        if duration_minutes < 0:
            duration_hours -= 1
            duration_minutes += 60
        duration = f"{duration_hours:02}:{duration_minutes:02}"
    except ValueError:
        duration = "vide"

    # Extraire les détails de la description
    session_match = re.search(r"RT1-(S\d)", event_data["DESCRIPTION"])
    teacher_match = re.findall(r"([A-Z]+ [A-Z]+)", event_data["DESCRIPTION"])

    session = session_match.group(1) if session_match else "vide"
    teachers = "|".join(teacher_match) if teacher_match else "vide"

    # Construire la chaîne formatée selon le format demandé
    formatted_output = (
        f"{event_data['UID']};"
        f"{start_date};"
        f"{start_time};"
        f"{duration};"
        f"CM;{event_data['SUMMARY']};"
        f"{event_data['LOCATION'].replace(' ', '|') if event_data['LOCATION'] != 'vide' else 'vide'};"
        f"{teachers};"
        f"{session}"
    )

    return formatted_output

def parse_ics(file_path):
    """
    Analyse un fichier ICS contenant plusieurs événements et retourne un tableau de pseudo-CSV.

    :param file_path: Le chemin du fichier ICS
    :return: Liste de chaînes de caractères formatées
    """
    lines = tab(file_path)
    events = []
    current_event = []

    for line in lines:
        if line == "BEGIN:VEVENT":
            current_event = []  # Démarrer un nouvel événement
        elif line == "END:VEVENT":
            # Ajouter l'événement analysé à la liste
            events.append(parse_event(current_event))
            current_event = []
        else:
            current_event.append(line)

    return events

def main():
    # Définir le chemin du fichier .ics
    file_path = "ADE_RT1_Septembre2023_Decembre2023.ics"  # Exemple de fichier

    # Analyser le fichier ICS pour obtenir le tableau des événements
    tableau = parse_ics(file_path)

    # Afficher chaque événement formaté
    print("\nTableau des événements :")
    for evenement in tableau:
        print(evenement)

# Point d'entrée du programme
if __name__ == "__main__":
    main()


# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 10:48:29 2024

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

def parse_ics(lines):
    """
    Analyse les lignes d'un fichier ICS pour extraire les informations nécessaires.

    :param lines: Liste des lignes du fichier ICS
    :return: Chaîne formatée selon les spécifications.
    """
    # Dictionnaire pour stocker les données d'événement
    event_data = {
        "UID": "",
        "DTSTART": "",
        "DTEND": "",
        "SUMMARY": "",
        "LOCATION": "",
        "DESCRIPTION": ""
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
        raise ValueError("Le format de DTSTART ou DTEND est invalide.")

    # Calculer la durée de l'événement
    start_hour, start_minute = map(int, start_time.split(":"))
    end_hour, end_minute = map(int, end_time.split(":"))
    duration_hours = end_hour - start_hour
    duration_minutes = end_minute - start_minute
    if duration_minutes < 0:
        duration_hours -= 1
        duration_minutes += 60
    duration = f"{duration_hours:02}:{duration_minutes:02}"

    # Extraire les détails de la description
    session_match = re.search(r"RT1-(S\d)", event_data["DESCRIPTION"])
    teacher_match = re.findall(r"([A-Z]+ [A-Z]+)", event_data["DESCRIPTION"])

    session = session_match.group(1) if session_match else ""
    teachers = "|".join(teacher_match) if teacher_match else ""

    # Construire la chaîne formatée selon le format demandé
    formatted_output = (
        f"{event_data['UID']};"
        f"{start_date};"
        f"{start_time};"
        f"{duration};"
        f"CM;{event_data['SUMMARY']};"
        f"{event_data['LOCATION'].replace(' ', '|')};"
        f"{teachers};"
        f"{session}"
    )

    return formatted_output

def main():
    # Définir le chemin du fichier .ics
    file_path = "evenementSAE_15.ics"

    # Lire le fichier et obtenir les lignes dans un tableau
    lignes = tab(file_path)

    # Vérifier si des lignes ont été récupérées
    if lignes:
        print("Les lignes du fichier .ics sont :")
        for i, ligne in enumerate(lignes, 1):
            print(f"Ligne {i}: {ligne}")

        # Analyser les lignes et afficher le résultat formaté
        print("\nSortie formatée :")
        print(parse_ics(lignes))
    else:
        print("Aucune ligne lue du fichier.")

# Point d'entrée du programme
if __name__ == "__main__":
    main()

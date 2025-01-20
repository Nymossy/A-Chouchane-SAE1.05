# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 12:00:00 2024

Programme pour traiter le fichier texte "Fichier texte à traiter.txt"
"""

import re
import markdown
import matplotlib.pyplot as plt
import os

# Définition des patterns
Ip_pattern = re.compile(r'IP (\S+)')
Ip_pattern4 = re.compile(r'IP (\S+)')
IP_pattern3 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
IP_pattern5 = re.compile(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}')
port_pattern = re.compile(r'\.\d+$')

def convertir_markdown_en_html(contenu_markdown):
    """
    Convertit le contenu Markdown en HTML.
    
    :param contenu_markdown: Texte du fichier Markdown
    :return: Texte HTML
    """
    return markdown.markdown(contenu_markdown)

def enregistrer_html(contenu_html, file_path):
    with open(file_path, "w", encoding="utf-8") as fichier:
        fichier.write(contenu_html)

def generer_markdown(nombre_trames, visites_sources, visites_destinations, fichier_markdown):
    with open(fichier_markdown, "w", encoding="utf-8") as mdfile:
        mdfile.write("# Analyse du tcpdump :\n\n")
        
        # Afficher le nombre de trames
        mdfile.write(f"## Nombre de trames : {nombre_trames}\n\n")
        
        # Afficher les requêtes des sources par ordre croissant
        mdfile.write("## Requêtes des sources (par ordre croissant)\n")
        for source, count in sorted(visites_sources.items(), key=lambda item: item[1]):
            mdfile.write(f"- **{source}** : {count} requêtes\n")
        mdfile.write("\n")
        
        # Afficher les visites des destinations par ordre croissant
        mdfile.write("## Visites des destinations (par ordre croissant)\n")
        for destination, count in sorted(visites_destinations.items(), key=lambda item: item[1]):
            mdfile.write(f"- **{destination}** : {count} visites\n")
        mdfile.write("\n")
        
        # Afficher l'activité suspecte
        mdfile.write("## Activité suspecte\n")
        if "190-0-175-100.gba.solunet.com.ar" in visites_sources:
            mdfile.write(f"- **190-0-175-100.gba.solunet.com.ar** : {visites_sources['190-0-175-100.gba.solunet.com.ar']} requêtes\n")
        if "BP-Linux8" in visites_sources:
            mdfile.write(f"- **BP-Linux8** : {visites_sources['BP-Linux8']} requêtes\n")

def Analyser(log_contents):
    with open(log_contents, "r") as f:
        http = https = domaine = ssh = icmp = icmp_req = icmp_rep = ipa = flags_connexion = flags_SynAcK = flags_deco = flags_push = flags_nokonnexion = compteur = 0
        suspect = {}
        occurence = {} 
        allip = {}

        for line in f:
            if '.domain' in line:
                domaine += 1
            if 'ssh' in line:
                ssh += 1
            if 'https' in line:
                https += 1
            if 'http' in line:
                http += 1
            if 'ICMP echo request' in line:
                icmp_req += 1
            if 'ICMP echo reply' in line:
                icmp_rep += 1
            if '192.168' in line:
                ipa += 1
            if 'Flags [S]' in line:
                flags_connexion += 1
            if 'Flags [S.]' in line:
                flags_SynAcK += 1
            if 'Flags [F.]' in line:
                flags_deco += 1
            if 'Flags [P.]' in line:
                flags_push += 1
            if 'Flags [.]' in line:
                flags_nokonnexion += 1

            for ip2 in Ip_pattern4.findall(line):
                clean_ip2 = port_pattern.sub('', ip2)
                if clean_ip2 not in allip:
                    allip[clean_ip2] = 1
                else:
                    allip[clean_ip2] += 1

            for ip2 in IP_pattern5.findall(line):
                clean_ip2 = port_pattern.sub('', ip2)
                if clean_ip2 not in allip:
                    allip[clean_ip2] = 1
                else:
                    allip[clean_ip2] += 1

            for ip in Ip_pattern.findall(line):
                clean_ip = port_pattern.sub('', ip)
                compteur += 1
                if clean_ip not in occurence and 'https' not in clean_ip:
                    occurence[clean_ip] = 1
                elif clean_ip in occurence and 'https' not in clean_ip:
                    occurence[clean_ip] += 1

            for ip in IP_pattern3.findall(line):
                clean_ip = port_pattern.sub('', ip)
                if clean_ip not in occurence and 'https' not in clean_ip:
                    occurence[clean_ip] = 1
                elif clean_ip in occurence and 'https' not in clean_ip:
                    occurence[clean_ip] += 1

    moyenne = sum(occurence.values()) / len(occurence)
    suspect = {cle: valeur for cle, valeur in occurence.items() if valeur > moyenne}

    http_final = http - https
    icmp = icmp_req + icmp_rep

    return http, https, http_final, domaine, ssh, icmp, icmp_req, icmp_rep, compteur, suspect, allip, flags_connexion, flags_SynAcK, flags_deco, flags_push, flags_nokonnexion

def filtrer_lignes_interessantes(fichier_source, fichier_destination):
    mots_cles = ["http", "https", "ssh", "ICMP", "Flags"]
    with open(fichier_source, "r") as source, open(fichier_destination, "w") as destination:
        for line in source:
            if any(mot in line for mot in mots_cles):
                destination.write(line)

def main():
    # Spécifiez le chemin du fichier à analyser directement dans le code
    fichier = "Projet/tcpdump_old.txt"
    fichier_resume = "Projet/tcpdump_resume.txt"
    
    # Filtrer les lignes intéressantes et les écrire dans tcpdump_resume.txt
    filtrer_lignes_interessantes(fichier, fichier_resume)
    
    http, https, http_final, domaine, ssh, icmp, icmp_req, icmp_rep, compteur, suspect, addresse, flags_connexion, flags_SynAcK, flags_deco, flags_push, flags_nokonnexion = Analyser(fichier_resume)

    pseudo_csv_content = "IP;Nombre de requêtes\n"
    for ip, count in addresse.items():
        pseudo_csv_content += f"{ip};{count}\n"

    os.makedirs("Projet", exist_ok=True)
    with open("Projet/adresses_extraites.csv", "w") as csv_file:
        csv_file.write(pseudo_csv_content)

    cles = list(suspect.keys())
    valeurs = list(suspect.values())

    # Assurez-vous que le répertoire Projet existe
    os.makedirs("Projet", exist_ok=True)
    
    colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral', 'red', 'blue', 'yellow']
    plt.figure(figsize=(10, 7))
    plt.pie(valeurs, labels=cles, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
    plt.axis('equal')
    plt.savefig('Projet/Activité-suspect.png', transparent=True)

    markdown_text = f'''
# ___Résultats Brut analyse du trafic___

___Nombre de trames :___ {compteur}

## ___adresses IP :___
''' + '\n'.join(f'- {ip} : {addresses} requêtes' for ip, addresses in addresse.items()) + f'''

## ___Activité Suspecte :___
''' + '\n'.join(f'- {ip} : {occurrences} requêtes' for ip, occurrences in suspect.items()) + f'''

<img src="Activité-suspect.png" class="merge" />
## ___Protocol + Stats :___ 
- SSH: {ssh}
- HTTP: {http_final}
- HTTPS: {https}
- DNS: {domaine}
- ICMP: {icmp}
- ICMP Requests: {icmp_req}
- ICMP Replies: {icmp_rep}

## ___Flags :___
- Connexion Demande: {flags_connexion}
- SynAcK: {flags_SynAcK}
- Déconnexion: {flags_deco}
- Push: {flags_push}
- No Connexion: {flags_nokonnexion}
'''

    # Écrire le texte Markdown dans un fichier
    with open("Projet/compte_rendu.md", "w") as md_file:
        md_file.write(markdown_text)

    # Convertir le texte Markdown en HTML
    html_output = markdown.markdown(markdown_text)

    # Écrire le contenu HTML dans un fichier
    with open("Projet/compte_rendu.html", "w") as file:
        file.write(html_output)

    print("Done.")

# Point d'entrée du programme
if __name__ == "__main__":
    main()
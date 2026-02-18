import json
import os

# contient tout les fichier dont l'extention et bien .json
liste_valid_files = []

# Nom de ton dossier
dossier = 'analayse_data'

# verifie si le fichier est corompu ou non en tantant de l'ouvrire
def json_corupt_or_not(chemin_fichier):
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            json.load(f) # On essaie de charger le contenu
        return True
    except (json.JSONDecodeError, IOError, UnicodeDecodeError):
        # Si une erreur survient (mauvais format, fichier vide, caractères bizarres)
        return False

# On vérifie d'abord si le dossier existe pour éviter une erreur
if os.path.exists(dossier):
    fichiers = os.listdir(dossier)
    
    allisjson = True
    
    for nom in fichiers:
        print(nom)
        chemin_complet = os.path.join(dossier, nom)
        
        # On ne vérifie que les fichiers (on ignore les sous-dossiers éventuels)
        if os.path.isfile(chemin_complet):
            if not nom.lower().endswith('.json'):
                print(f"⚠️ Alerte : Le fichier '{nom}' n'est pas un JSON !")
                allisjson = False
            else:
                print(f"✅ {nom} est valide.")
                # cette condition verifie si le fichier et lisible ou non grace a une fonction
                if json_corupt_or_not(chemin_complet):
                    # ajoute a la liste des fichier qui son valide pour la suite
                    liste_valid_files.append(chemin_complet)
                else:
                    print(f"Erreur : Le fichier '{nom}' est imposible a ouvrire.")
    
    if allisjson:
        print("\nParfait ! Tous les fichiers sont des JSON.")
else:
    print(f"Erreur : Le dossier '{dossier}' n'existe pas.")


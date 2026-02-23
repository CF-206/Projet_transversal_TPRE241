import json
import os

# chemain vers ce script
script_path = os.path.dirname(__file__)

# chemain vers le dossier ou se trouve les json a analyser
dossier = os.path.abspath(os.path.join(script_path,'..', 'analayse_data'))

jsonvlaide = []

# Charger le fichier de référence une seule fois au début
chemin_ref = os.path.join(dossier, 'ref.json')
with open(chemin_ref, 'r', encoding='utf-8') as f:
    reference_json = json.load(f)

def validate(ref, data, path=""):
    errors = []
    cles_a_ignorer = ["raw", "class", "value", "timestamp"]

    for key, rule in ref.items():

        # Si la clé est dans la liste, on passe au prochain tour de boucle
        if key in cles_a_ignorer:
            continue
        current_path = f"{path}.{key}" if path else key
        
        # si une clée est manquante par rapport au json de réfèrence
        if key not in data:
            errors.append(f"MANQUANT : {current_path}")
            continue
        
        val = data[key]
        
        if isinstance(rule, list) and isinstance(val, list):
            if len(rule) > 0 and isinstance(rule[0], dict):
                for i, item in enumerate(val):
                    errors.extend(validate(rule[0], item, f"{current_path}[{i}]"))
            
            elif len(rule) == 2 and all(isinstance(i, (int, float)) for i in rule):
                if not (rule[0] <= val <= rule[1]):
                    errors.append(f"RANGE : {current_path} ({val}) hors limites {rule}")
        
        elif isinstance(rule, dict) and isinstance(val, dict):
            errors.extend(validate(rule, val, current_path))
        
        elif isinstance(rule, str) and rule.endswith(('_', '-')):
            if not str(val).startswith(rule):
                errors.append(f"FORMAT : {current_path} ({val}) doit commencer par '{rule}'")
        
        else:
            if val != rule and not isinstance(rule, list):
                errors.append(f"VALEUR : {current_path} ({val}) != attendu ({rule})")
    
    for key in data:
        if key not in ref and key not in cles_a_ignorer:
            current_path = f"{path}.{key}" if path else key
            errors.append(f"INCONNU : La clé '{current_path}' n'est pas dans la référence")
    return errors
    
if os.path.exists(dossier):
    fichiers = os.listdir(dossier) 
    for nom in fichiers:
        chemin_complet = os.path.join(dossier, nom)
        
        # On ignore le fichier de référence lui-même
        if nom == "ref.json":
            continue

        if os.path.isfile(chemin_complet):
            
            if nom.lower().endswith('.json'):
                print(f"\n--- Analyse de {nom} ---")
                
                # On essaie de lire le contenu
                try:
                    with open(chemin_complet, 'r', encoding='utf-8') as f:
                        data_a_tester = json.load(f)
                    
                    # si le json est vlaide, on lance la validation
                    rapport_erreurs = validate(reference_json, data_a_tester)

                    if not rapport_erreurs:
                        print(f"{nom} est parfaitement conforme.")
                        jsonvlaide.append(chemin_complet)
                    else:
                        print(f"{nom} présente des erreurs :")
                        for err in rapport_erreurs:
                            print(f"    - {err}")
                except (json.JSONDecodeError, IOError):
                    print(f"Erreur : Le fichier '{nom}' est corrompu.")
            else:
                print(f"Alerte : '{nom}' n'est pas un fichier JSON, ignoré.")
else:
    print(f"Erreur : Le dossier '{dossier}' n'existe pas.")

print(jsonvlaide)
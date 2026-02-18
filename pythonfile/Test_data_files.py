# import json
# import os

# def charger_et_analyser_donnees():

#     script_path = os.path.dirname(__file__)
    
#     chemin_dossier = os.path.abspath(os.path.join(script_path,'..', 'datas\projects_data\set_3'))
    
#     liste_valid_json_data_files = []
#     liste_invalid_json_data_files = []
#     tous_les_blocs = [] # Pour stocker les données d'analyse

#     fichiers = [f for f in os.listdir(chemin_dossier) if f.endswith('.json')]
#     index = 0

#     while index < len(fichiers):
#         nom_fichier = fichiers[index]
#         chemin_complet = os.path.join(chemin_dossier, nom_fichier)
        
#         try:
#             with open(chemin_complet, 'r', encoding='utf-8') as f:
#                 data = json.load(f)
            
#             # 1. VERIFICATION DE LA STRUCTURE (Le Contrat) [cite: 58, 59]
#             if all(k in data for k in ("run_info", "execution_trace", "link_data")):
#                 # Extraction des infos de base
#                 run_id = data["run_info"].get("run_id")
                
#                 # 2. INGESTION DES TRACES [cite: 95, 98]
#                 for trace in data["execution_trace"]:
#                     trace['run_id'] = run_id  # On lie la trace au Run pour l'analyse
#                     tous_les_blocs.append(trace)
                
#                 liste_valid_json_data_files.append(chemin_complet)
#                 print(f"{nom_fichier} : Valide")
#             else:
#                 liste_invalid_json_data_files.append(chemin_complet)
#                 print(f"{nom_fichier} : Invalide (Structure incomplète)")
                
#         except Exception as e:
#             liste_invalid_json_data_files.append(chemin_complet)
#             print(f"{nom_fichier} : Invalide (Erreur lecture : {e})") [cite: 57, 99]
            
#         index += 1

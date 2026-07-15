# Projet

Prototype de traitement automatisé des demandes RH.

# Architecture imposée

- Interface Streamlit
- ChromaDB avec embeddings multilingues remplaçables
- Classifieur unique pour le sujet et la sensibilité
- Validation humaine obligatoire
- Contrôle des droits d’accès aux documents
- Escalade si la demande est sensible, incomplète ou incertaine
- Pas de recherche hybride
- Pas de module de traduction

# Règles de travail

- Réaliser le changement minimal nécessaire.
- Ne jamais utiliser de données RH réelles dans les tests.
- Exécuter les tests après chaque modification.
- Indiquer ce qui fonctionne, ce qui est simulé et ce qui manque.
- Ne jamais déclarer une fonctionnalité terminée sans vérification.

# Commandes

- Installation : `pip install -r requirements.txt`
- Tests : `pytest -q`
- Application : `streamlit run app.py`

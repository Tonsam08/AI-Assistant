# Prototype d’assistant RH

Prototype démontrable du parcours principal : classification, détection de sensibilité, contrôle d’accès documentaire, recherche de politiques et préparation d’une réponse soumise à validation humaine.

Toutes les données fournies sont fictives.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell : .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Lancement

```bash
streamlit run app.py
```

## Tests

```bash
pytest -q
```

## Scénarios de démonstration

- Réponse normale : `Comment déposer une demande de congés et partir en vacances ?`
- Demande sensible : `Je veux signaler un harcèlement.`
- Demande incomplète : `J’ai une question.`
- Contrôle d’accès : choisir `employees`, puis demander une correction de paie.

## Réel dans ce prototype

- interface Streamlit ;
- classifieur unique sujet/sensibilité, déterministe et testable ;
- filtrage des politiques par pays et groupe avant la recherche ;
- recherche ChromaDB lorsqu’elle est disponible ;
- réponse avec sources et validation humaine obligatoire ;
- escalade des demandes sensibles, inconnues ou sans source fiable ;
- tests automatisés du parcours principal.

## Simulé ou provisoire

- les politiques sont fictives et chargées depuis un fichier JSON ;
- les embeddings sont locaux et déterministes, pas un modèle multilingue de production ;
- la réponse est assemblée depuis des extraits, sans LLM ;
- l’identité et les groupes de l’utilisateur sont sélectionnés dans l’interface ;
- aucune connexion SharePoint, Outlook ou Claude ;
- la validation humaine est représentée par un statut, sans file de traitement persistante.

## Prochaine intégration minimale

Remplacer successivement les composants provisoires sans changer le workflow :

1. fournisseur d’identité et groupes réels ;
2. synchronisation SharePoint ;
3. embeddings multilingues validés ;
4. génération contrôlée avec citations ;
5. file de validation RH et journal d’audit.

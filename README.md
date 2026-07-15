# Prototype d’assistant RH

Prototype démontrable du parcours principal : nettoyage d’e-mails, classification, routage structuré, contrôle d’accès documentaire, RAG multilingue avec ChromaDB, génération OpenAI citée, audit et validation humaine.

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

Le premier lancement télécharge le modèle d'embeddings multilingue local. Pour activer la génération IA, copier `.env.example` vers `.env`, puis fournir `OPENAI_API_KEY` dans l'environnement. Aucun secret ne doit être commité.

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
- Mail Scrubber MIME/HTML et inventaire des pièces jointes ;
- classifieur unique sujet/sensibilité sur embeddings locaux, déterministe et testable ;
- routeur produisant une décision JSON et une liste fermée d’outils ;
- filtrage des politiques par pays et groupe avant la recherche ;
- découpage des politiques en passages chevauchants et index ChromaDB persistant ;
- embeddings multilingues locaux (`paraphrase-multilingual-MiniLM-L12-v2`) ;
- filtrage pays/groupes avant la recherche, seuil de pertinence et limitation de la redondance ;
- génération via l'API OpenAI Responses, citations contrôlées et passages réellement utilisés affichés dans l'interface ;
- réponse de secours locale et validation humaine obligatoire ;
- escalade des demandes sensibles, inconnues ou sans source fiable ;
- tests automatisés du parcours principal.
- journal d’audit SQLite et adaptateurs simulés Outlook/Jira.

## Simulé ou provisoire

- les politiques sont fictives et chargées depuis un fichier JSON ;
- l'appel OpenAI n'est actif que si une clé est fournie et si chaque politique porte `external_ai_allowed: true` ;
- les politiques sensibles ou non approuvées ne quittent jamais l'application ;
- l’identité et les groupes de l’utilisateur sont sélectionnés dans l’interface ;
- le connecteur SharePoint Graph est un contrat non configuré ; Outlook et Jira sont simulés ;
- la validation humaine est représentée par un statut, sans file de traitement persistante.

## Prochaine intégration minimale

Remplacer successivement les composants provisoires sans changer le workflow :

1. fournisseur d’identité et groupes réels ;
2. synchronisation SharePoint ;
3. validation sécurité/DPO du modèle et de l'usage OpenAI ;
4. jeu d'évaluation métier multilingue avec seuils mesurés ;
5. file de validation RH persistante.

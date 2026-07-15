# Runbook

## Installation

```bash
python -m venv .venv
pip install -r requirements.txt
```

## Vérification

```bash
pytest -q
python -m compileall -q hr_assistant app.py
```

## Lancement

```bash
streamlit run app.py
```

## Incident

- ChromaDB indisponible : l’application utilise le moteur local de secours.
- Aucune politique pertinente : escalade humaine.
- Demande sensible : aucune recherche et escalade humaine.
- SharePoint/Outlook/Jira non configuré : utiliser les adaptateurs simulés.

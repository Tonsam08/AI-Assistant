# Démonstration en 5 minutes

1. Lancer `streamlit run app.py`.
2. Demander : `Comment déposer une demande de congés et partir en vacances ?`.
3. Montrer la catégorie, le score, la route structurée, les sources et le trace ID.
4. Demander : `Je veux signaler un harcèlement.` et montrer l’escalade sans recherche.
5. Demander : `J’ai une question.` et montrer la demande d’informations.
6. Choisir un autre pays ou groupe et montrer que les politiques non autorisées ne sont pas recherchées.

Préciser que SharePoint, Outlook et Jira sont simulés ou non configurés.

## Mode de secours pour une présentation hors ligne

Si le modèle multilingue n'a pas pu être téléchargé avant la présentation, définir
`EMBEDDING_BACKEND=lexical` dans `.env`, puis relancer Streamlit. Les parcours de
démonstration restent opérationnels avec les données fictives et l'interface indique
clairement que le moteur lexical de secours est utilisé.

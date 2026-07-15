# Architecture du prototype

Le flux suit les décisions validées :

1. Le Mail Scrubber transforme un e-mail brut en demande propre.
2. Un classifieur unique détermine le sujet, la sensibilité et la confiance.
3. Le routeur produit une décision structurée et une liste fermée d’outils autorisés.
4. Les politiques sont filtrées par pays et groupes avant toute recherche.
5. ChromaDB recherche uniquement dans le périmètre documentaire autorisé.
6. Le générateur local prépare une réponse citée ou une demande d’informations.
7. Toutes les sorties restent en attente de validation humaine en phase 1.
8. L’AuditStore conserve la décision et son statut.

## Connecteurs

- SharePoint : interface et adaptateur Graph non configuré.
- Outlook : boîte simulée tant que Graph API n’est pas disponible.
- Jira : passerelle simulée tant qu’aucune instance n’est disponible.

Les connecteurs réels devront être injectés sans modifier le workflow métier.

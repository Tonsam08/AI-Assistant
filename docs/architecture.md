# Architecture du prototype

Le flux suit les décisions validées :

1. Le Mail Scrubber transforme un e-mail brut en demande propre.
2. Un classifieur unique détermine le sujet, la sensibilité et la confiance.
3. Le routeur produit une décision structurée et une liste fermée d’outils autorisés.
4. Les politiques sont filtrées par pays et groupes avant toute recherche.
5. Les politiques sont découpées en passages stables puis vectorisées localement avec un modèle multilingue.
6. ChromaDB recherche uniquement dans le périmètre documentaire autorisé, applique un seuil de similarité et limite les doublons par politique.
7. Seuls les passages retenus, non sensibles et explicitement autorisés sont transmis au générateur OpenAI.
8. Le générateur utilise l'API Responses sans stockage, doit citer chaque affirmation avec `[S1]`, et sa sortie est rejetée si les citations sont absentes ou invalides.
9. L'interface montre mot pour mot les passages utilisés pour produire le brouillon.
10. Toutes les sorties restent en attente de validation humaine en phase 1.
11. L’AuditStore conserve la décision et son statut.

## Frontière de confidentialité

Les embeddings sont calculés localement. La demande est expurgée des e-mails et numéros de téléphone avant l'appel OpenAI. Une politique réelle est exclue de la génération externe par défaut (`external_ai_allowed: false`) ; son propriétaire doit autoriser explicitement cet usage. Les demandes sensibles sont escaladées avant la recherche et la génération.

## Connecteurs

- SharePoint : interface et adaptateur Graph non configuré.
- Outlook : boîte simulée tant que Graph API n’est pas disponible.
- Jira : passerelle simulée tant qu’aucune instance n’est disponible.

Les connecteurs réels devront être injectés sans modifier le workflow métier.

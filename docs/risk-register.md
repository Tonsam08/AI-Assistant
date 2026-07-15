# Risques et critères d'évaluation

## Registre des risques

| Risque | Impact | Réponse retenue |
|---|---|---|
| Absence d'accès à Outlook Graph | Impossible de lire une boîte réelle | Utiliser un adaptateur simulé et documenter le contrat d'intégration |
| Absence d'accès à SharePoint Graph / ChromaDB | Impossible de synchroniser ou d'indexer les policies réelles automatiquement | Travailler sur des données fictives ou des extraits explicitement autorisés ; conserver le connecteur comme interface |
| Policies internes confidentielles | Risque de divulgation ou d'usage non autorisé par une IA externe | Ne pas transmettre les policies à une IA externe sans cadre approuvé ; prévoir environnement maîtrisé, anonymisation si nécessaire et validation humaine |
| Droits d'accès insuffisants | Réponse basée sur une policy d'un autre pays ou périmètre | Filtrer les documents selon pays et groupes avant la recherche |
| Demande RH sensible | Réponse automatique inadaptée ou risquée | Escalade humaine immédiate, sans suite automatique |
| Peu d'exemples pour le classifieur | Confiance insuffisante pour un usage production | Présenter le résultat comme une preuve de faisabilité et conserver l'escalade lorsque la confiance est faible |
| Policies hétérogènes et multilingues | Recherche moins pertinente ou contenu difficile à exploiter | Utiliser des embeddings multilingues ; appliquer la template aux nouvelles policies et mettre à jour les anciennes au fil de l'eau |

## Critères d'évaluation du prototype

Le prototype est considéré utile s'il permet de démontrer que :

- une demande est orientée vers une réponse, une demande de précisions ou une escalade ;
- une demande sensible est escaladée ;
- une policy non autorisée n'est pas utilisée ;
- la réponse proposée conserve le passage source retenu ;
- les limites liées aux accès internes sont explicites.

Ces critères évaluent le fonctionnement et les garde-fous du prototype ; ils ne constituent pas une validation de production.

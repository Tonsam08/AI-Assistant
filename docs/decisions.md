# Décisions

- Validation humaine obligatoire pour toutes les réponses en phase 1.
- Escalade immédiate des demandes sensibles.
- Un seul classifieur fournit sujet, sensibilité et confiance.
- Recherche par embeddings uniquement, sans recherche hybride ni TF-IDF.
- Pas de traduction : les embeddings doivent couvrir les langues attendues.
- Filtrage d’accès avant l’indexation ou la recherche.
- Pas d’API externe sur du contenu sensible sans protection approuvée.
- Les intégrations indisponibles sont simulées derrière des contrats explicites.

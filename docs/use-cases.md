# Scénarios d'utilisation

## Cas 1 — Demande RH répondue à partir d'une policy

Un salarié formule une demande sur une procédure couverte par une policy accessible dans son périmètre.

Le système nettoie la demande, la classe, vérifie l'absence de sensibilité, filtre les documents autorisés puis recherche les passages pertinents. Il prépare une réponse et affiche le passage retenu. La réponse reste soumise à validation RH en phase 1.

## Cas 2 — Information manquante

La demande concerne une procédure connue, mais la policy exige une information absente du message.

Le système ne déduit pas l'information. Il prépare une demande de précisions, qui doit être validée par les RH avant envoi.

## Cas 3 — Demande sensible

La demande est identifiée comme sensible.

Le système arrête le traitement automatisé et escalade le cas vers les RH. Aucune recherche documentaire ni réponse automatique n'est produite.

## Cas 4 — Document hors périmètre

La policy potentiellement pertinente n'est pas accessible au demandeur selon son pays ou ses groupes.

Le document est exclu avant la recherche. Le système ne l'utilise pas pour répondre et le cas est orienté vers une revue humaine si nécessaire.

## Hors périmètre du prototype

La lecture d'une boîte Outlook réelle, la synchronisation automatique de SharePoint, l'envoi d'e-mails et la création de tickets Jira réels dépendent d'accès non encore disponibles.

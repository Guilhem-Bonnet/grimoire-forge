# Statut E2E - RUN-20260414-000430

## Statut

Aucune suite end-to-end navigateur dediee n'a ete executee pour ce candidat.

## Ce que couvre ce run a la place

- `npm run cockpit:verify` regenere le runtime views report et le build web du cockpit, puis verifie que les entrypoints generes existent.
- Le lot cible runtime surfaces valide les read models Game UI et Observability sur la meme verite runtime.
- Le candidat V5 courant dispose donc d'une preuve release et d'une preuve d'integration ciblee, mais pas d'une campagne complete d'interaction navigateur.

## Impact sur la decision release

Cela reste une limite connue et l'une des raisons pour lesquelles le verdict global de release V5 reste `NO-GO`, meme si le pack de preuves lui-meme est maintenant complet.

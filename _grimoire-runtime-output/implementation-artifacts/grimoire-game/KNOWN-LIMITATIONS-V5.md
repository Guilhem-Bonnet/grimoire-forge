# Known Limitations V5 - Agent OS + Game UI

## Objet

Lister explicitement les limites connues de la V5 resserree pour eviter les faux positifs de maturite.

## Limitations runtime

- Le write-path est limite a un sous-ensemble borne de cles de configuration.
- Le control plane live global reste partiel et non generalise a toutes les mutations metier.
- Les extensions write hors budget sont refusees par design (fail-closed).

## Limitations produit

- La surface cockpit finale n est pas encore complete pour tous les scenarios operateur.
- Certaines interactions restent plus rapides via transcript brut que via la surface board.
- Le mode spectateur partageable est encore en phase d industrialisation.

## Limitations qualite

- Les suites e2e navigateur ne couvrent pas encore la totalite des scenarios canoniques V5.
- Les checks perf et securite dedies existent dans l evidence pack structurel, mais la couverture de campagne reste a etendre.

## Limitations release

- La release discipline est active sur la chaine runtime TypeScript.
- Le passage release V5 global reste bloque tant que G-V5-01 a G-V5-04 ne sont pas fermes.

## References

- [GO-NO-GO-V5.md](GO-NO-GO-V5.md)
- [MATRICE-validation-V5.md](MATRICE-validation-V5.md)
- [RISK-REGISTER-V5.md](RISK-REGISTER-V5.md)
- [RELEASE-NOTES-V5.md](RELEASE-NOTES-V5.md)

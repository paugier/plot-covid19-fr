# Plot covid-19 France

Ce dépot contient du code permettant de visualiser les données en rapport avec
l'épidémie de COVID-19 en France. On se concentre pour l'instant sur la reprise
de l'épidémie quelques mois après la sortie du confinement (à partir d'août
2020, donc).

## Comment visualiser les figures?

Attention : Malheureusement, il y a un bug avec Firefox! On peut utiliser à la
place Chromium ou Chrome.

- Pour visualiser les figures sans le code (avec Voilà), cliquez sur ce bouton
: [![Binder
Voila](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/paugier/plot-covid19/master?urlpath=%2Fvoila%2Frender%2Fplot_covid19.ipynb)

- Pour visualiser le code et les figures et potentiellement modifier le code
(avec Jupyter Notebook), cliquez sur ce bouton :
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/paugier/plot-covid19/master?filepath=plot_covid19.ipynb)

## A propos des données utilisées

### Données Système d’Informations de DEPistage (SI-DEP)

https://www.data.gouv.fr/fr/datasets/donnees-relatives-aux-resultats-des-tests-virologiques-covid-19/

- Départements :
https://www.data.gouv.fr/fr/datasets/r/406c6a23-e283-4300-9484-54e78c8ae675
(`sp-pos-quot-dep-*-19h15.csv`)

- France :
https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c
(`sp-pos-quot-fra-*-19h15.csv`)

### Données hospitalières

https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/

- Variations à hospital :
https://www.data.gouv.fr/fr/datasets/r/6fadff46-9efd-4c53-942a-54aca783c30c
(`donnees-hospitalieres-nouveaux-covid19-*-19h00.csv`)

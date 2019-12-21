# Cryptocurrencies trading


# TODO
### Faire un modèle de marché plus proche de la réalité. 
* *Done* : Notamment, les buying fees et les selling fees peuvent être différents.
* *Done* : Baser l'algorithme sur les prix de vente et les prix d'achat, non pas seulement les prix d'achat.
* *WiP* : Faire un modèle de marché dans lequel on puisse évaluer à tout instant combien de XBT on peut acheter pour une quantité fixe d'EUR.

### Changement de langage de programmation
Le traîtement en Python est assez lent.

* *Scala* : intéressant pour faire le feature engineering mais après
    * Si la partie Modèle est prise en charge par Python, fournir les résultats à Python en temps réel ?
    * Si le modèle de machine learning est en Scala, lequel choisir sachant qu'il n'y a pas beaucoup de libs.
* *Kotlin* : langage intéressant à apprendre en soi, mais idem : comment faire les modèles de machine learning ?
    * TensorFlow semble avoir une API proche de celle des versions < 1.4
* *Julia* : contient tout ce qu'il faut en termes de bibliothèques, mais :
    * Le développement est lent car la stacktrace est difficile à comprendre.
    * Il n'y a pas de bons outils de refactoring aujourd'hui.
* *Cython* : semble être un bon compromis
    * Dispense d'avoir à tout recoder from scratch
    * Bugs avec Jupyter
    * Demande une seconde passe de compilation, ce qui néecessite de la configuration
* *Numba* : meilleur choix à ce jour.
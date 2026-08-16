Un projet comporte d'innombrables fichiers source, qui sont placés dans plusieurs répertoires selon leur type, leur fonction et leur module. Le Makefile définit une série de règles pour spécifier quels fichiers doivent être compilés en premier, quels fichiers doivent être compilés ensuite, quels fichiers doivent être recompilés, et même pour effectuer des opérations fonctionnelles plus complexes.

### Relation entre Make et Makefile

`make` est un outil de commande qui interprète les instructions contenues dans le Makefile.
Le fichier Makefile décrit l'ordre de compilation et les règles de compilation de tous les fichiers du projet.
Lors de son exécution, `make` lit les règles du fichier Makefile.

### Règles de nommage du Makefile

`Makefile` ou `makefile`, on utilise généralement `Makefile`.
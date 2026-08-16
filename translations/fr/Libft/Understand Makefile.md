Un projet comporte d'innombrables fichiers sources, classés par type, fonction et module dans plusieurs répertoires. Le Makefile définit une série de règles pour spécifier quels fichiers doivent être compilés en premier, lesquels en second, lesquels doivent être recompilés, ou même pour effectuer des opérations fonctionnelles plus complexes.

### Relation entre Make et Makefile

make est un outil de commande qui interprète les instructions d'un Makefile.
Le fichier Makefile décrit l'ordre de compilation et les règles de compilation de tous les fichiers du projet.
Lors de son exécution, make lit les règles du fichier Makefile, mais le Makefile doit être écrit par vous-même.

### Règles de nommage du Makefile

Le fichier est généralement nommé Makefile ou makefile.



### PS: Informations complémentaires

#### `gcc (g++) <options> <sourcefile>`
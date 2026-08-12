`strrchr` parcourt une chaîne de caractères C à la recherche de la dernière occurrence du caractère `c`, et renvoie un pointeur vers cette position ; si le caractère n'est pas trouvé, elle renvoie `NULL`.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Son rôle est de rechercher de gauche à droite, mais en renvoyant la dernière occurrence du caractère.

L'implémentation spécifique peut soit parcourir la chaîne de gauche à droite, soit de droite à gauche :

1. Une approche classique de gauche à droite consiste à : parcourir la chaîne depuis le début, et à chaque fois que le caractère cible est trouvé, mettre à jour la position de la dernière occurrence. Au lieu de retourner dès la première trouvaille, on écrase la position précédente à chaque nouvelle découverte.
	Avantages de cette méthode :
		- Pas besoin de calculer la longueur de la chaîne au préalable.
		- Permet de traiter le caractère '\0' en même temps.
		- Logique très stable.

2. Une autre méthode intuitive consiste à chercher de droite à gauche, en partant du dernier caractère et en remontant vers le début.
	Avantages :
		- La logique correspond parfaitement au nom `strrchr`.
		- Dès qu'une occurrence est trouvée, on peut retourner directement, car il s'agit de la dernière.
	Inconvénients :
		- Nécessite généralement de calculer la longueur au préalable.
		- Si l'on appelle `ft_strlen` soi-même, cela ajoute un parcours supplémentaire.

#### 2. Différence entre `strrchr` et `strchr`

Par exemple : la lettre 'o' apparaît 2 fois dans "hello world"

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr` : recherche le caractère de gauche à droite et renvoie la première occurrence.
 - `strrchr` : recherche de gauche à droite, mais renvoie la dernière occurrence.

#### 3. Valeur de retour de `strrchr`

Le type de la valeur de retour est `char *`, qui renvoie l'adresse du caractère trouvé, ou NULL si le caractère n'est pas trouvé.

Une caractéristique importante de `strrchr` est qu'il recherche également '\0', c'est-à-dire qu'il peut renvoyer l'adresse du terminateur de chaîne '\0'.
Par conséquent, lors du parcours de la chaîne, il ne faut pas oublier de vérifier '\0'.

#### 4. Le cas d'utilisation courant de `strrchr` est « l'obtention de l'extension de fichier »

Exemple 1 : `strrchr` est très couramment utilisé lors du traitement de chemins de fichiers et de noms de fichiers.

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

Le pointeur de résultat p pointe vers le `.txt` de document.txt, donc :

```c
printf("%s\n", p); // .txt
```

Exemple 2 : Examinons un autre exemple de chemin, où l'on souhaite trouver le dernier `/` :

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

p pointe vers le dernier `/` de la chaîne "/Users/lee/project/main.c", donc :

```c
printf("%s\n", p + 1);
```

On obtient `/main.c`, p + 1 pointe vers `main.c`, c'est pourquoi on voit souvent l'écriture suivante :

```c
char *filename = strrchr(path, '/');

if (filename)
    filename++;
```
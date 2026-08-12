`strrchr` parcourt une chaîne de caractères C pour trouver la dernière occurrence du caractère `c` et renvoie un pointeur vers cette position ; s'il n'est pas trouvé, il renvoie `NULL`.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Son rôle est de rechercher de gauche à droite, mais en renvoyant la dernière occurrence du caractère.

L'implémentation spécifique peut soit scanner la chaîne de gauche à droite, soit de droite à gauche :

1. Une approche typique consistant à rechercher le caractère de gauche à droite est la suivante : parcourir la chaîne depuis le début, et chaque fois que le caractère cible est trouvé, mettre à jour la position de la dernière occurrence. Au lieu de retourner dès qu'il est trouvé, on écrase la position précédente à chaque fois qu'on le trouve.
	Les avantages de cette méthode sont :
		- Il n'est pas nécessaire de calculer d'abord la longueur de la chaîne.
		- Il peut traiter '\0' au passage.
		- La logique est très stable.

2. Une autre méthode intuitive consiste à chercher de droite à gauche, en partant du dernier caractère et en reculant.

	L'avantage est :
		- La logique correspond très bien au nom `strrchr`.
		- Dès qu'il est trouvé la première fois, on peut retourner directement, car c'est la dernière occurrence.
		
	Les inconvénients sont :
		- Il est généralement nécessaire de calculer d'abord la longueur.
		- Si l'on appelle `ft_strlen` soi-même, cela entraîne un parcours supplémentaire.

#### 2. Différence entre `strrchr` et `strchr`

Par exemple : la lettre o apparaît 2 fois dans "hello world".

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr` : recherche le caractère de gauche à droite et renvoie la première occurrence.
 - `strrchr` : recherche de gauche à droite, mais renvoie la dernière occurrence.

#### 3. Valeur de retour de `strrchr`

Le type de la valeur de retour est `char *`. Il renvoie l'adresse du caractère trouvé, ou NULL si le caractère n'est pas trouvé.

Une caractéristique importante de `strrchr` est qu'il recherche également '\0', c'est-à-dire qu'il renverra l'adresse du terminateur de chaîne '\0'.
Par conséquent, il ne faut pas oublier de vérifier '\0' lors du parcours de la chaîne.

#### 4. Le cas d'utilisation courant de `strrchr` est l'« obtention de l'extension de fichier »

Exemple 1 : `strrchr` est très couramment utilisé lors du traitement de chemins de fichiers et de noms de fichiers.

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

Le pointeur de résultat p pointe vers le `.txt` de document.txt, donc :

```c
printf("%s\n", p); // .txt
```

Exemple 2 : Regardons un autre exemple de chemin, si nous voulons trouver le dernier `/`, nous pouvons faire :

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

p pointe vers le dernier `/` de la chaîne "/Users/lee/project/main.c", alors :

```c
printf("%s\n", p + 1);
```

En obtenant `/main.c`, p + 1 pointe vers `main.c`, c'est pourquoi on voit souvent l'écriture suivante :

```c
char *filename = strrchr(path, '/');

if (filename)
    filename++;
```
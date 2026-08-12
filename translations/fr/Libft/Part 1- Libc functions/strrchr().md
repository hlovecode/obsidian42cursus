strrchr recherche la dernière occurrence d'un caractère dans une chaîne.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Son rôle est de rechercher de gauche à droite, mais de renvoyer la dernière occurrence du caractère.

L'implémentation spécifique peut soit parcourir la chaîne de l'avant vers l'arrière, soit de l'arrière vers l'avant :
1. Une approche classique de recherche de l'avant vers l'arrière consiste à : parcourir la chaîne depuis le début et, à chaque fois que le caractère cible est trouvé, mettre à jour la position de la dernière occurrence. Au lieu de faire un return dès la première trouvaille, on écrase la position précédente à chaque fois qu'on le trouve. 
	Avantages de cette méthode :
		- Pas besoin de calculer la longueur de la chaîne au préalable
		- Permet de traiter '\0' au passage
		- Approche très stable

2. Une autre méthode intuitive consiste à chercher de l'arrière vers l'avant, en partant du dernier caractère pour remonter.
	Ses avantages sont :
		- La logique correspond parfaitement au nom `strrchr`
		- Dès qu'on trouve la première occurrence, on peut retourner directement, car c'est la dernière
	Ses inconvénients sont :
		- Nécessite généralement de calculer la longueur au préalable
		- Si l'on appelle soi-même `ft_strlen`, cela ajoute un parcours supplémentaire

#### 2. Différence entre `strrchr` et `strchr`

Par exemple : la lettre o apparaît 2 fois dans « hello world »

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr` : recherche le caractère de gauche à droite et renvoie la première occurrence du caractère.
 - `strrchr` : recherche de gauche à droite, mais renvoie la dernière occurrence.

#### 3. Valeur de retour de `strrchr`

Le type de la valeur de retour est `char *`. Il renvoie l'adresse du caractère trouvé, ou NULL si le caractère n'est pas trouvé.

Une caractéristique importante de `strrchr` est qu'il recherche également '\0', c'est-à-dire qu'il peut renvoyer l'adresse du caractère de fin de chaîne '\0'.

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

Exemple 2 : Regardons un autre exemple de chemin. Si nous voulons trouver le dernier `/`, nous pouvons faire :

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

p pointe vers le dernier `/` de la chaîne « /Users/lee/project/main.c », alors :

```c
printf("%s\n", p + 1);
```

On obtient `/main.c`, p + 1 pointe vers `main.c`, c'est pourquoi on voit souvent l'écriture suivante :

```c
char *filename = strrchr(path, '/');

if (filename)
    filename++;
```
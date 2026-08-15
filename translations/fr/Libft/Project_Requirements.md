Implémenter certaines fonctions en langage C, telles que la ré-implémentation de la libc, en créant un makefile et en exécutant la commande `make` pour générer une bibliothèque statique publique `libft.a`.
<font color="red">C'est la bibliothèque de base de tout le Common Core.</font>
###### Groupe 1 : Caractères
```c
ft_isalpha

ft_isdigit

ft_isalnum

ft_isascii

ft_isprint
```
###### Groupe 2 : Manipulation de mémoire
```c
memset

bzero

memcpy

memmove

memcmp

memchr
```
###### Groupe 3 : Fonctions de chaînes de caractères
```c
strlen

strlcpy

strlcat

strchr

strrchr

strncmp

strnstr

strdup
```
###### Groupe 4 : Conversion de caractères
```c
toupper

tolower
```
###### Groupe 5 : Conversion de nombres
```c
atoi
```
###### Groupe 6 : Mémoire dynamique
```c
calloc // 不同系统，行为可能不同
strdup
```
###### Groupe 7 : Nouvelles fonctions demandées
```c
ft_substr
ft_strjoin
ft_strtrim
ft_split
ft_itoa
ft_strmapi
ft_striteri
ft_putchar_fd
ft_putstr_fd
ft_putendl_fd
ft_putnbr_fd
```
###### Groupe 8 : Fonctions de listes chaînées (Linked List)
| Fonction            | Fonctionnalité             |
| ----------------- | -------------------- |
| `ft_lstnew`       | Créer un nouveau nœud            |
| `ft_lstadd_front` | Insertion en tête          |
| `ft_lstsize`      | Compter le nombre de nœuds   |
| `ft_lstlast`      | Obtenir le dernier nœud      |
| `ft_lstadd_back`  | Insertion en queue         |
| `ft_lstdelone`    | Supprimer un nœud          |
| `ft_lstclear`     | Supprimer toute la liste     |
| `ft_lstiter`      | Parcourir la liste et exécuter une fonction sur chaque nœud |
| `ft_lstmap`       | Transformer le contenu de chaque nœud pour générer une nouvelle liste |

### 1. Technical considerations Exigences techniques

1 **Interdiction d'utiliser des variables globales**

Étant donné que Libft est une bibliothèque publique, elle doit toujours donner le même résultat pour la même entrée -> toujours la même sortie.
S'il y a des variables globales, leur modification entraînera une modification du résultat final.

2 **Les fonctions auxiliaires (Helper Functions) doivent être static**

Par exemple : 
```c
ft_split()
```
qui nécessite
```c
int count_words()
void copy_word()
free_all()
```
Ces fonctions ne doivent pas être exposées aux autres et doivent être écrites ainsi :
```c
static int count_words()
static void copy_word()
static free_all()
```
Car `static` signifie <font color="red">utilisable uniquement dans ce fichier</font> et ne pollue pas toute la bibliothèque.

3 **Tous les fichiers doivent être placés dans le répertoire racine, comme suit :**

```
libft/

Makefile

libft.h

ft_strlen.c
ft_memcpy.c
...
```
Tout est placé directement à la racine.

4 **Il est interdit de soumettre des fichiers superflus**

Par exemple :
```c
test.c
old.c
abc.c
```
Si le Makefile ne les utilise pas du tout, ne les soumettez pas.

5 **Tous les fichiers .c doivent :**

```bash
-Wall
-Wextra
-Werror
```
Compiler sans avertissements (warnings).

6 **L'utilisation de la commande `ar` est obligatoire**

`ar` est l'abréviation de archive. C'est un outil sous les systèmes Unix/Linux/macOS utilisé pour empaqueter plusieurs fichiers objets (`.o`) dans un fichier d'archive.
Les objets principaux du travail de `ar` sont `.o`


L'utilisation la plus typique dans un projet C est de passer de plusieurs fichiers `.o` -> `ar` -> une bibliothèque statique `.a`.
Par exemple pour Libft :
```c
ft_strlen.o
ft_memset.o
ft_memcpy.o
ft_isalpha.o
ft_atoi.o
ft_split.o
...
```
Via :
```bash
</> Bash
ar
```
Pour obtenir finalement :
```bash
libft.a
```
Par conséquent :
```bash
.c
 ↓ gcc/cc
.o
 ↓ ar
.a
```
Cette chaîne est très importante.

`libft.a` n'est pas une bibliothèque en cours d'exécution, c'est en fait un fichier d'archive contenant de nombreux fichiers `.o`, ce qui peut se comprendre grossièrement par :
```c
libft.a
│
├── ft_strlen.o
├── ft_memset.o
├── ft_memcpy.o
├── ft_isalpha.o
├── ft_isdigit.o
├── ft_strdup.o
├── ft_split.o
├── ft_itoa.o
└── ...
```

Par conséquent, ce que fait `ar` consiste essentiellement à organiser et empaqueter de nombreux fichiers objets dans un fichier de bibliothèque statique.
> Comprendre la commande
> ```bash
>	ar rcs libft.a *.o
> ```
> `ar` : appelle l'outil d'archivage
> `rcs` :
>	- `r` = replace (remplacer) : ajoute les fichiers `.o` spécifiés à l'archive. Si un membre du même nom existe déjà dans l'archive, il est remplacé ; sinon, il est créé.
>	- `c` = create (créer) : crée l'archive si elle n'existe pas.
>	- `s` : crée un index de symboles (symbol index) pour l'archive.

La commande :
```bash
</> Bash
ar rcs libft.a *.o
```
est la manière la plus typique de créer une bibliothèque statique, qui peut être comprise comme :
```bash
ar
│
├── r → 把 .o 加进去 / 替换旧版本
├── c → 必要时创建 .a
└── s → 建立符号索引
```

| Outil         | Rôle principal       |
| ------------ | -------------- |
| `cc` / `gcc` | Compiler le C       |
| `ar`         | Créer/Gérer l'archive |
| linker       | Lier les fichiers objets/bibliothèques pour former le programme final |

Le projet exige explicitement d'utiliser `ar` pour créer `libft.a`, et interdit l'utilisation de `libtool`

7 **libft.a doit se trouver à la racine**

`libft.a` se trouve juste à côté de `Makefile`.

### 2. README Requirements

`README.md` fait partie du projet et il est obligatoire de le fournir à la racine du dépôt.

`README` doit contenir au minimum les éléments suivants :

1 **La première ligne doit être en italique et son contenu doit être exactement :**
```
*This activity has been created as part of the 42 curriculum by <login>.*
```
En cas de travail d'équipe, plusieurs logins peuvent être écrits à la suite.

2 **Description (Présentation du projet), expliquant :**
- Ce qu'est Libft
- Les objectifs du projet
- Le contenu principal implémenté

3 **Instructions (Instructions d'utilisation)**, telles que :
- La compilation, par exemple `make`
- La génération de `libft.a`
- L'utilisation de cette bibliothèque statique dans d'autres projets

4 **Resources (Références)**
Lister les documents consultés pendant l'apprentissage, par exemple :
- La documentation de la bibliothèque standard C (pages man)
- Des tutoriels
- Des articles techniques, etc.
De plus, il est obligatoire d'expliquer **l'utilisation de l'IA dans le projet**, par exemple si elle a été utilisée pour l'explication de concepts, la relecture de code ou le débogage, tout en précisant quelles parties ont été réalisées par vous-même.

5 **Présentation détaillée de la bibliothèque créée**
Fournir une description détaillée de la bibliothèque `libft` elle-même, par exemple :
- Les catégories de fonctions incluses
- L'utilité de chaque catégorie de fonctions
- Le rôle de cette bibliothèque dans les projets 42 ultérieurs
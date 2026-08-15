Implémenter certaines fonctions en langage C, telles que la réimplémentation de la libc, en créant un makefile et en exécutant la commande make pour générer une bibliothèque statique publique `libft.a`.
<font color="red">C'est la bibliothèque de base de tout le Tronc Commun (Common Core).</font>
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
###### Groupe 6 : Allocation dynamique
```c
calloc // 不同系统，行为可能不同
strdup
```
###### Groupe 7 : Nouvelles fonctions requises
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
| Fonction            | Fonctionnalité         |
| ----------------- | -------------------- |
| `ft_lstnew`       | Créer un nouveau nœud     |
| `ft_lstadd_front` | Insertion en tête      |
| `ft_lstsize`      | Compter le nombre de nœuds   |
| `ft_lstlast`      | Obtenir le dernier nœud      |
| `ft_lstadd_back`  | Insertion en queue     |
| `ft_lstdelone`    | Supprimer un nœud          |
| `ft_lstclear`     | Supprimer toute la liste     |
| `ft_lstiter`      | Parcourir la liste et exécuter une fonction sur chaque nœud |
| `ft_lstmap`       | Transformer le contenu de chaque nœud pour générer une nouvelle liste |

### 1. Technical considerations Exigences techniques

1 **Interdiction d'utiliser des variables globales**

Étant donné que Libft est une bibliothèque publique, elle doit toujours donner la même sortie pour la même entrée -> Entrée identique = Sortie identique.
S'il y a des variables globales, la modification de l'une d'elles entraînera des changements dans le résultat final.

2 **Les fonctions d'assistance (Helper Functions) doivent être static**

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
Parce que static signifie <font color="red">utilisable uniquement dans ce fichier</font>, ce qui évite de polluer l'ensemble de la bibliothèque.

3 **Tous les fichiers doivent être placés à la racine, comme suit :**

```
libft/

Makefile

libft.h

ft_strlen.c
ft_memcpy.c
...
```
Tous directement à la racine.

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
Être compilables sans avertissements (Warning).

6 **L'utilisation de la commande ar est obligatoire**

ar est l'abréviation d'archive. C'est un outil présent dans les systèmes Unix/Linux/macOS, utilisé pour regrouper plusieurs fichiers objets (`.o`) dans un fichier archive.
Les principaux objets de travail de ar sont `.o`


Dans un projet C, l'utilisation la plus typique est de passer de plusieurs fichiers .o -> ar -> à une bibliothèque statique .a.
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
Cette chaîne est extrêmement importante.

`libft.a` n'est pas une bibliothèque en cours d'exécution, c'est en réalité un fichier d'archive contenant de nombreux fichiers `.o`, que l'on peut approximativement comprendre comme :
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

Par conséquent, ce que fait `ar`, par essence, c'est d'organiser et de regrouper de nombreux fichiers objets en un seul fichier de bibliothèque statique.
> Comprendre la commande
> ```bash
>	ar rcs libft.a *.o
> ```
> ar : Appel de l'outil d'archivage
> rcs :
>	- r = replace (remplacer) : Ajoute les fichiers `.o` spécifiés à l'archive. Si un membre portant le même nom existe déjà dans l'archive, il est remplacé ; s'il n'existe pas, il est créé.
>	- c = create (créer) : Crée l'archive si elle n'existe pas.
>	- s : Crée un index de symboles (symbol index) pour l'archive.

La commande :
```bash
</> Bash
ar rcs libft.a *.o
```
est la manière la plus typique de créer une bibliothèque statique, ce qui peut se comprendre comme :
```bash
ar
│
├── r → 把 .o 加进去 / 替换旧版本
├── c → 必要时创建 .a
└── s → 建立符号索引
```

| Outil          | Rôle principal       |
| ------------ | -------------- |
| `cc` / `gcc` | Compiler le C        |
| `ar`         | Créer/gérer l'archive |
| linker       | Lier les fichiers objets/bibliothèques pour former le programme final |

Le projet exige explicitement d'utiliser `ar` pour créer `libft.a`, et interdit l'utilisation de `libtool`

7 **libft.a doit se trouver à la racine**

`libft.a` se trouve juste à côté de `Makefile`.

### 2. README Requirements

`README.md` fait partie intégrante du projet et sa présence à la racine du dépôt est obligatoire.

`README` doit contenir au minimum les éléments suivants :

1 **La première ligne doit être en italique et son contenu doit être exactement :**

```
*This activity has been created as part of the 42 curriculum by <login>.*
```
En cas de travail en groupe, plusieurs identifiants (login) peuvent être écrits à la suite.

2 **Description : présentation du projet, expliquant :**

- Ce qu'est Libft
- Les objectifs du projet
- Le contenu principal mis en œuvre

3 **Instructions : mode d'emploi**, par exemple :

- La compilation, par exemple make
- La génération de `libft.a`
- L'utilisation de cette bibliothèque statique dans d'autres projets

4 **Resources (Références)**

Lister les documents consultés pendant l'apprentissage, par exemple :
- La documentation de la bibliothèque standard C (pages man)
- Des tutoriels
- Des articles techniques, etc.
De plus, il est obligatoire d'expliquer **l'utilisation de l'IA dans le projet**, par exemple si elle a été utilisée pour l'explication de concepts, la revue de code ou le débogage, tout en précisant quelles parties ont été réalisées par vous-même.

5 **Présentation détaillée de la bibliothèque créée**

Fournir une description détaillée de la bibliothèque `libft` elle-même, par exemple :
- Les catégories de fonctions incluses
- L'utilité de chaque type de fonction
- Le rôle de cette bibliothèque dans les projets 42 ultérieurs
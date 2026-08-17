C'est ici qu'il faut vraiment maîtriser le projet `Libft`.

Un Makefile typique :
```Makefile
NAME = libft.a

CC = cc
CFLAGS = -Wall -Wextra -Werror

SRCS = ft_strlen.c \
       ft_memset.c \
       ft_memcpy.c

OBJS = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all
```
Ici :
```Makefile
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```
s'occupe de :
```Makefile
.c -> .o
```
tandis que :
```Makefile
$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)
```
s'occupe de :
```Makefile
.o → libft.a
```
Par conséquent, toute la logique du Makefile :
```Makefile
                cc
.c ─────────────────────→ .o
                            │
                            │
                            │ ar rcs
                            ↓
                         libft.a
```

`ar` traite principalement les membres `archive`, c'est-à-dire `.o`, et le code source C `.c` doit d'abord être compilé par `cc`, ce qui donne donc :
```bash
.c
 ↓ cc
.o
 ↓ ar
.a
```
et non :
```bash
.c
 ↓ ar
.a
```

`ar` est un programme qui permet de maintenir des fichiers de bibliothèque en ajoutant, supprimant et extrayant des fichiers. On utilise généralement `ar` pour créer et gérer les bibliothèques d'objets utilisées par l'éditeur de liens.

#### Retenez 4 commandes :

1 Compiler un fichier `.c` :
```bash
cc -Wall -Wextra -Werror -c ft_strlen.c
```
pour obtenir :
```bash
ft_strlen.o
```

2 Créer une bibliothèque statique :
```bash
ar rcs libft.a ft_strlen.o
```
pour obtenir :
```bash
libft.a
```

`libft.a` est la bibliothèque statique créée à l'aide de l'outil `ar`.

`ar` n'est pas un compilateur en soi, il ne compile pas `.c` en code machine, son rôle est d'empaqueter et d'archiver des fichiers `.o` déjà compilés en `libft.a`, où `.a` indique qu'il s'agit d'un fichier archive.

`ar` traite des fichiers objets / membres d'archive tels que `.o`, et n'est pas responsable de la compilation du code source C en code objet.

3 Afficher le contenu d'une bibliothèque statique :
```bash
ar -t libft.a
```
pour obtenir :
```bash
ft_strlen.o
...
```

4 Supprimer la bibliothèque statique :
```bash
rm -f libft.a
```

#### Relier tout le processus de Libft

On peut comprendre `Libft` comme :
```bash
              你的 C 源代码
                     │
                     │ cc -c
                     ↓
              ┌──────────────┐
              │   .o 文件     │
              ├──────────────┤
              │ ft_strlen.o  │
              │ ft_memset.o  │
              │ ft_memcpy.o  │
              │ ft_split.o   │
              │ ft_itoa.o    │
              │ ...          │
              └──────┬───────┘
                     │
                     │ ar rcs
                     ↓
              ┌──────────────┐
              │   libft.a    │
              │ Static       │
              │ Library      │
              └──────┬───────┘
                     │
                     │ linker
                     ↓
              ┌──────────────┐
              │ 你的程序      │
              │ main.c       │
              └──────────────┘
```

**`cc` compile `.c` en `.o` ; `ar` regroupe plusieurs `.o` dans la bibliothèque statique `.a` ; enfin, l'éditeur de liens extrait le code nécessaire du `.a` pour générer l'exécutable.**
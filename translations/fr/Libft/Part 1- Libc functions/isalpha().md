`isalpha()` est l'une des fonctions de classification de caractères les plus utilisées de la **bibliothèque standard C (<ctype.h>)**, utilisée pour **déterminer si un caractère est une lettre alphabétique (a ~ z / A ~ Z).**
Les lettres sont déterminées selon la table ASCII, il s'agit donc des plages 65 ~ 90 et 97 ~ 122.

1. **Prototype**
```c
#include <ctype.h>

int isalpha(int c);
```
Valeur de retour :
- Différente de 0 (généralement 1, mais la norme n'impose pas que ce soit 1) s'il s'agit d'une lettre
- 0 si ce n'est pas une lettre
Par exemple :
```c
isalpha('A');   // true
isalpha('z');   // true
isalpha('3');   // false
isalpha('$');   // false
```

<font color="red"> isalpha() vérifie simplement s'il s'agit de 65 ~ 90 ou 97 ~ 122. </font>

2. **Pourquoi le paramètre de la fonction est-il un int ? Car :**
- Un char subit une promotion automatique
	Par exemple :
	```c
	char c = 'a';
	isalpha(c);
	```
	En réalité, lors de l'appel, le char est automatiquement promu en int, c'est pourquoi la bibliothèque standard utilise directement int c

- On peut également passer `EOF`
`EOF` signifie End of File (Fin de fichier), c'est-à-dire la fin d'un fichier ou d'une entrée.
En langage C, `EOF` est une valeur entière spéciale qui indique qu'il n'y a plus de caractères à lire, ou qu'une erreur de lecture s'est produite. Ce n'est pas un caractère ordinaire ; dans les systèmes, la valeur de `EOF` est généralement `-1`, mais attention, la norme C garantit seulement que `EOF` est une valeur int négative, sans exiger qu'elle soit nécessairement `-1`.

==Remarque== :
`EOF` n'appartient pas aux caractères ASCII, c'est une valeur de retour spéciale utilisée par la bibliothèque standard C pour indiquer « qu'il n'y a plus d'entrée ». Il faut le comprendre ainsi :
```txt
字符 → 实际读到的数据

EOF → 没有数据可以继续读
```

int peut contenir à la fois des valeurs de caractères et EOF, tandis qu'un char ne peut pas nécessairement distinguer correctement un caractère ordinaire de EOF. C'est pourquoi le paramètre de la fonction dans la bibliothèque standard utilise int c, ce qui constitue une conception très importante du langage C.

==Remarque== :
`EOF` et `\0` sont totalement différents !
- EOF n'est pas un terminateur de chaîne, il indique que le flux d'entrée ou le fichier n'a plus de contenu à lire, informant le programme que la lecture du fichier est terminée.
- \0 est un véritable caractère dont la valeur ASCII = 0, principalement utilisé pour marquer la fin d'une chaîne de caractères en C.

Comprendre EOF dans le contexte global du système d'entrée C :
```txt
                 C 输入流
                    │
                    ▼
              getchar()
              /       \
             /         \
       正常读取        读取结束/错误
          │                 │
          ▼                 ▼
       字符的 int           EOF
          │
          ▼
      isalpha(c)
      isdigit(c)
      isspace(c)
      ...
```
Par exemple :
```c
int c;

while ((c = getchar()) != EOF)
{
    if (isalpha(c))
        printf("letter\n");
}
```

**EOF n'est pas un caractère, mais une valeur de retour entière négative spéciale utilisée par les fonctions d'entrée en C pour indiquer « qu'il n'y a plus de caractères à lire (ou qu'une erreur de lecture s'est produite). »**

[[isalnum()]]
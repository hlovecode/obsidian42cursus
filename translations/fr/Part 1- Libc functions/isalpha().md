`isalpha()` est l'une des fonctions de classification de caractères les plus couramment utilisées dans la **bibliothèque standard C (<ctype.h>)**, utilisée pour **déterminer si un caractère est une lettre anglaise (a ~ z / A ~ Z).**
Les lettres sont déterminées en fonction de la table ASCII, soit de 65 à 90 et de 97 à 122. 

1. **Prototype**
```c
#include <ctype.h>

int isalpha(int c);
```
Valeur de retour :
- Non nulle (généralement 1, mais la norme ne l'exige pas) si c'est une lettre
- 0 si ce n'est pas une lettre
Par exemple :
```c
isalpha('A');   // true
isalpha('z');   // true
isalpha('3');   // false
isalpha('$');   // false
```

<font color="red"> isalpha() vérifie simplement s'il est compris entre 65 ~ 90 ou 97 ~ 122. </font>

2. **Pourquoi le paramètre de la fonction est-il un int ? Parce que :**
- char subit une promotion automatique
	Par exemple :
	```c
	char c = 'a';
	isalpha(c);
	```
	En réalité, lors de l'appel, le char est automatiquement converti en int, c'est pourquoi la bibliothèque standard utilise directement int c.

- Il est également possible de passer `EOF`
`EOF` signifie End of File (Fin de fichier), c'est-à-dire la fin d'un fichier ou d'une saisie.
En langage C, `EOF` est une valeur de drapeau entière spéciale, utilisée pour indiquer qu'il n'y a plus de caractères à lire ou qu'une erreur de lecture s'est produite. Ce n'est pas un caractère ordinaire ; généralement, dans les systèmes, la valeur de `EOF` est `-1`, mais notez que la norme C garantit seulement que `EOF` est une valeur int négative, sans exiger qu'elle soit nécessairement `-1`.

==Remarque== :
`EOF` n'appartient pas aux caractères ASCII, c'est une valeur de retour spéciale utilisée par la bibliothèque standard C pour indiquer "qu'il n'y a plus d'entrées". Il faut le comprendre ainsi :
```txt
字符 → 实际读到的数据

EOF → 没有数据可以继续读
```

int peut contenir à la fois des valeurs de caractères et EOF, tandis que char ne peut pas nécessairement distinguer correctement un caractère ordinaire de EOF. Par conséquent, la bibliothèque standard utilise int c pour le paramètre de la fonction, ce qui est une conception très importante du langage C.

==Remarque== :
`EOF` et `\0` sont complètement différents !
- EOF n'est pas un terminateur de chaîne, il indique que le flux d'entrée / le fichier n'a plus de contenu à lire, informant le programme que la lecture du fichier est terminée.
- \0 est un véritable caractère, dont la valeur ASCII est = 0, principalement utilisé pour marquer la fin d'une chaîne de caractères en C.

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

**EOF n'est pas un caractère, mais une valeur de retour entière négative spéciale utilisée par les fonctions d'entrée C pour indiquer "qu'il n'y a plus de caractères à lire (ou qu'une erreur de lecture s'est produite)".**

[[isalnum()]]
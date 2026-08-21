strdup() a un rôle très direct : il duplique une chaîne de caractères et alloue dynamiquement de la mémoire pour la copie.
On peut le comprendre comme `string duplicate`

#### 1. Prototype

```c
char *strdup(const char *s);
```

Par exemple :

```c
char *copy;

copy = strdup("Hello");
```

Après l'exécution des 2 lignes de code ci-dessus, on peut considérer qu'un nouveau "Hello" est créé.

Chaîne de caractères d'origine :

"Hello\0"
   ↑
   s

`strdup()`
   ├── Calcule la longueur de la chaîne
   ├── Alloue une nouvelle mémoire
   └── Y copie "Hello\0"
          ↓
Nouvelle mémoire dynamique :

┌────┬────┬────┬────┬────┬────┐
│ H  │ e  │ l  │ l  │ o  │ \0 │
└────┴────┴────┴────┴────┴────┘
  ↑
 copy

copy pointe vers un nouveau bloc mémoire

**strdup renvoie finalement l'adresse de début de la chaîne nouvellement dupliquée.**
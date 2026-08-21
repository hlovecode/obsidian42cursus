Le rôle de strdup() est très direct : il duplique une chaîne de caractères et alloue dynamiquement de la mémoire pour la chaîne copiée.

#### 1. Prototype

```c
char *strdup(const char *s);
```

Par exemple :

```c
char *copy;

copy = strdup("Hello");
```

Après l'exécution des 2 lignes de code ci-dessus, on peut comprendre cela ainsi :

La chaîne d'origine :

"Hello\0"
   ↑
   s

`strdup()`
   ├── Calcule la longueur de la chaîne
   ├── Alloue de la mémoire
   └── Y copie "Hello\0"
          ↓

La nouvelle mémoire dynamique :

┌────┬────┬────┬────┬────┬────┐
│ H  │ e  │ l  │ l  │ o  │ \0 │
└────┴────┴────┴────┴────┴────┘
  ↑
 copy
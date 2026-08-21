strdup() a un rôle très direct : il duplique une chaîne de caractères et alloue dynamiquement de la mémoire pour la copie.
On peut l'assimiler à `string duplicate`

`strdup` est présent sur de nombreux systèmes Unix / POSIX, mais ce n'est pas une fonction définie par la norme ISO C ; elle fait partie des interfaces courantes de l'environnement Unix / POSIX. 

#### 1. Prototype

```c
char *strdup(const char *s);
```

Par exemple :

```c
char *copy;

copy = strdup("Hello");
```

Après l'exécution de ces 2 lignes de code, on peut considérer qu'un nouveau "Hello" est créé.

La chaîne d'origine :

"Hello\0"

   ↑
   s

`strdup()`

   ├── Calcule la longueur de la chaîne
   ├── Alloue de la nouvelle mémoire
   └── Y copie "Hello\0"
          ↓
La nouvelle mémoire dynamique :

┌────┬────┬────┬────┬────┬────┐
  
  │ H  │ e  │ l  │ l  │ o  │ \0 │
  
└────┴────┴────┴────┴────┴────┘
  ↑
 copy

copy pointe vers un nouveau bloc mémoire

**strdup renvoie finalement l'adresse de début de la chaîne nouvellement dupliquée et ne modifie pas la chaîne d'origine**

`strdup` = « Allocation d'espace + Copie de chaîne »

#### 2. `strdup` vs `strcpy`

`strcpy` : copie la chaîne src dans un espace mémoire dest déjà existant.

`strdup` : alloue lui-même une nouvelle mémoire, puis y copie src.

|               | strcpy   | strdup  |
| ------------- | -------- | ------- |
| Copie la chaîne      | Oui      | Oui     |
| Alloue une nouvelle mémoire | Non      | Oui     |
| dest doit-il exister au préalable | Oui | Non     |
| Valeur de retour | char \*  | char \* |
| Nécessite free après utilisation | Dépend de dest | Oui |
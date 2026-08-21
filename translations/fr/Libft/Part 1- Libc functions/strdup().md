Le rôle de `string duplicate` est très direct : il duplique une chaîne de caractères et alloue dynamiquement de la mémoire pour la chaîne copiée.
On peut le voir comme `strdup`.

```c
char *strdup(const char *s);
``` est présent sur de nombreux systèmes Unix / POSIX, mais ce n'est pas une fonction définie par la norme ISO C ; elle fait partie des interfaces courantes de l'environnement Unix / POSIX. 

#### 1. Prototype

```c
char *copy;

copy = strdup("Hello");
```

Par exemple :

`strdup()`

Après l'exécution de ces 2 lignes de code, on peut considérer qu'un nouveau "Hello" est créé,

La chaîne d'origine s : "Hello\0"

`strdup`

   ├── Calculer la longueur de la chaîne
   ├── Allouer de la nouvelle mémoire
   └── Y copier "Hello\0"
   
          ↓
Nouvelle mémoire dynamique :

┌────┬────┬────┬────┬────┬────┐
  
  │ H  │ e  │ l  │ l  │ o  │ \0 │
  
└────┴────┴────┴────┴────┴────┘
  ↑
 copy

copy pointe vers un nouveau bloc mémoire

**strdup retourne finalement l'adresse de début de la nouvelle chaîne dupliquée et ne modifie pas la chaîne d'origine**

`strdup` = « Allocation d'espace + Copie de chaîne »

#### 2. `strcpy` vs `strcpy`

`strdup` : Copie la chaîne de src dans la mémoire de dest qui existe déjà.

___PROTECTED_10___ : Alloue lui-même une nouvelle mémoire, puis y copie src.

|               | strcpy   | strdup  |
| ------------- | -------- | ------- |
| Copie la chaîne       | Oui      | Oui     |
| Alloue une nouvelle mémoire       | Non      | Oui     |
| dest doit-il exister à l'avance | Oui      | Non     |
| Valeur de retour           | char \*  | char \* |
| Nécessite un free après utilisation  | Dépend de dest | Oui      |
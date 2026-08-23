Le rôle de `string duplicate` est très direct : il copie une chaîne de caractères et alloue dynamiquement de la mémoire pour la chaîne copiée.
On peut le voir comme `strdup`.

```c
char *strdup(const char *s);
``` est présent sur de nombreux systèmes Unix / POSIX, mais ce n'est pas une fonction définie par la norme ISO C ; elle appartient aux interfaces courantes des environnements Unix / POSIX.

#### 1. Prototype

```c
char *copy;

copy = strdup("Hello");
```

Par exemple :

`strdup()`

Après l'exécution de ces 2 lignes de code, on peut considérer qu'un nouveau "Hello" est créé.

Chaîne originale s : "Hello\0"

`strdup`

   ├── Calcule la longueur de la chaîne
   
   ├── Alloue une nouvelle mémoire
   
   └── Y copie "Hello\0"
   
          ↓
Nouvelle mémoire dynamique :

┌────┬────┬────┬────┬────┬────┐
  
  │ H  │ e  │ l  │ l  │ o  │ \0 │
  
└────┴────┬────┬────┬────┬────┘
  ↑
 copy

copy pointe vers un nouveau bloc mémoire.

**`strdup` renvoie finalement l'adresse de début de la nouvelle chaîne copiée et ne modifie pas la chaîne d'origine.**

`strcpy` = « Allocation d'espace + Copie de chaîne »

#### 2. `strcpy` vs `strdup`

___PROTECTED_10___ : Copie la chaîne de src dans la mémoire de dest qui existe déjà.

___PROTECTED_11___ : Alloue elle-même une nouvelle mémoire, puis y copie src.

|               | strcpy   | strdup  |
| ------------- | -------- | ------- |
| Copie la chaîne       | Oui      | Oui     |
| Alloue une nouvelle mémoire       | Non      | Oui     |
| dest doit-il exister au préalable | Oui      | Non     |
| Valeur de retour           | char \*  | char \* |
| Nécessite un free après utilisation  | Dépend de dest | Oui      |
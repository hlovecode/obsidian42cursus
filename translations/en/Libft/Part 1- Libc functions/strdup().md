The function of `strdup()` is very straightforward: it duplicates a string and dynamically allocates memory for the duplicated string.

#### 1. Prototype

```c
char *strdup(const char *s);
```

For example:

```c
char *copy;

copy = strdup("Hello");
```

After executing the 2 lines of code above, it can be understood as:

Original string:

"Hello\0"
   ↑
   s

`strdup()`
   ├── Calculate string length
   ├── Allocate new memory
   └── Copy "Hello\0" into it
          ↓

New dynamic memory:

┌────┬────┬────┬────┬────┬────┐
│ H  │ e  │ l  │ l  │ o  │ \0 │
└────┴────┴────┴────┴────┴────┘
  ↑
 copy
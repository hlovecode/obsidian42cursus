The function of `strdup()` is very straightforward: it duplicates a string and dynamically allocates memory for the duplicated string.
It can be understood as `string duplicate`

#### 1. Prototype

```c
char *strdup(const char *s);
```

For example:

```c
char *copy;

copy = strdup("Hello");
```

After executing the above 2 lines of code, it can be understood as creating a new "Hello",

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

`copy` points to a block of new memory.

**`strdup` ultimately returns the starting address of the newly duplicated string.**
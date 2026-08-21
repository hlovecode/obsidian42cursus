The function of `strdup()` is very straightforward: it duplicates a string and dynamically allocates memory for the copied string.
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

copy points to a piece of new memory

**`strdup` ultimately returns the starting address of the newly copied string and does not modify the original string.**

#### 2. `strdup` vs `strcpy`

`strcpy`: Copies the string from src into an already existing dest memory buffer.

`strdup`: Allocates new memory by itself, and then copies src into it.

|               | strcpy   | strdup  |
| ------------- | -------- | ------- |
| Copies string        | Yes      | Yes     |
| Allocates new memory | No       | Yes     |
| Does dest need to exist beforehand | Yes | No |
| Return value  | char \*  | char \* |
| Requires free after use | Depends on dest | Yes |
The function of `strdup()` is very straightforward: it duplicates a string and dynamically allocates memory for the copied string.
It can be understood as `string duplicate`

`strdup` is available on many Unix / POSIX systems, but it is not a function defined by the ISO C standard; it belongs to common interfaces in the Unix / POSIX environment.

#### 1. Prototype

```c
char *strdup(const char *s);
```

For example:

```c
char *copy;

copy = strdup("Hello");
```

After the above 2 lines of code are executed, it can be understood as creating a new "Hello",

Original string s: "Hello\0"

`strdup()`

   ├── Calculate string length
   
   ├── Allocate new memory
   
   └── Copy "Hello\0" into it
   
⬇`
		
New dynamic memory:

┌────┬────┬────┬────┬────┬────┐
  
  │ H  │ e  │ l  │ l  │ o  │ \0 │
  
└────┴────┴────┴────┴────┴────┘
  ↑
 copy

copy points to a new block of memory

**strdup ultimately returns the starting address of the newly copied string, and does not modify the original string**

`strdup` = "Allocate space + Copy string"

#### 2. `strdup` vs `strcpy`

`strcpy`: Copies the string from src into the already existing dest memory

`strdup`: Allocates new memory by itself, and then copies src into it

|               | strcpy   | strdup  |
| ------------- | -------- | ------- |
| Copies string       | Yes      | Yes     |
| Allocates new memory       | No       | Yes     |
| Does dest need to exist in advance | Yes      | No      |
| Return value           | char \*  | char \* |
| Requires free after use  | Depends on dest | Yes      |

translation in french is ok or not ?
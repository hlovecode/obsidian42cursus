strrchr finds the last occurrence of a character in a string.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Its function is to search from left to right, but return the position of the last occurrence of the character.
The specific implementation can scan the string either from front to back, or from back to front.

#### 2. Difference between `strrchr` and `strchr`

For example: the letter 'o' appears 2 times in "hello world"

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr`: Searches for the character from left to right, and returns the position of the first occurrence.
 - `strrchr`: Searches from left to right, but returns the position of the last occurrence.

#### 3. Return value of `strrchr`

The return type is `char *`, which returns the address of the found character, or NULL if the character is not found.

An important feature of `strrchr` is that it will search for '\0', meaning it will return the address of the string termination character '\0'.

#### 4. A common scenario for `strrchr` is "getting the file extension"

Example 1: `strrchr` is very common when processing file paths and file names

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

The resulting pointer p points to the `.txt` of document.txt, so:

```c
printf("%s\n", p); // .txt
```

Example 2: Let's look at another path example. If we want to find the last `/`, we can do:

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

p points to the last `/` of the string "/Users/lee/project/main.c", then:

```c
printf("%s\n", p + 1);
```

Gives `main.c`
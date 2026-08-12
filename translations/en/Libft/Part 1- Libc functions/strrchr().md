`strrchr` iterates through a C string, searches for the last occurrence of the character `c`, and returns a pointer to that position; if not found, it returns `NULL`.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Its function is to search from left to right, but return the position of the last occurrence of the character.

The specific implementation can either scan the string from front to back, or from back to front:
1. A typical approach for finding characters from front to back is: traverse starting from the beginning of the string, and update the position of the last occurrence every time the target character is found. Instead of returning immediately upon the first find, overwrite the previous position every time it is found.
	Advantages of this method:
		- No need to calculate the string length in advance
		- Can handle '\0' along the way
		- Very robust logic

2. Another intuitive method is to search from back to front, scanning backwards starting from the last character.
	Advantages:
		- The logic closely matches the name `strrchr`
		- Can return immediately upon finding the first match, because it is the last occurrence
	Disadvantages:
		- Usually requires calculating the length first
		- If calling `ft_strlen` yourself, it incurs an extra traversal

#### 2. Differences between `strrchr` and `strchr`

For example: the letter 'o' appears 2 times in "hello world"

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr`: Searches for a character from left to right, returning the position of its first occurrence.
 - `strrchr`: Searches from left to right, but returns the position of the last occurrence.

#### 3. Return value of `strrchr`

The return type is `char *`. It returns the address of the found character, or NULL if the character is not found.

An important characteristic of `strrchr` is that it will search for '\0', meaning it can return the address of the string terminator '\0'. Therefore, you must remember to check for '\0' when scanning the string.

#### 4. Common use case of `strrchr`: "Getting the file extension"

Example 1: `strrchr` is very common when processing file paths and file names.

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

The resulting pointer p points to the `.txt` of document.txt, so:

```c
printf("%s\n", p); // .txt
```

Example 2: Looking at another path example, if we want to find the last `/`, we can do:

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

If p points to the last `/` of the string "/Users/lee/project/main.c", then:

```c
printf("%s\n", p + 1);
```

We get `/main.c`, and p + 1 points to `main.c`, which is why you often see the following idiom:

```c
char *filename = strrchr(path, '/');

if (filename)
    filename++;
```
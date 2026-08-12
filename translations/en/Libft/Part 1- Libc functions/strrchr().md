strrchr finds the last occurrence of a character in a string.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Its function is to search from left to right, but return the position of the last occurrence of the character.

The concrete implementation can either scan the string from front to back, or from back to front:
1. A typical approach for searching from front to back is: iterate starting from the beginning of the string, and update the position of the last occurrence every time the target character is found. Instead of returning upon the first find, it overwrites the previous position on every match.
	Advantages of this method:
		- No need to calculate the string length in advance
		- Can handle '\0' naturally
		- Highly stable logic

2. Another intuitive method is to search from back to front, scanning backwards starting from the last character.
	Advantages:
		- The logic closely matches the name `strrchr`
		- Can return immediately upon the first find, as it is guaranteed to be the last occurrence
	Disadvantages:
		- Usually requires calculating the length first
		- If calling `ft_strlen` internally, it results in an extra traversal

#### 2. Difference between `strrchr` and `strchr`

For example, the letter 'o' appears twice in "hello world"

```c 
char *str = "hello world";

strchr(str, 'o'); // return first occurrence, o in hello

strrchr(str, 'o'); // return last occurrence, o in world
```
 
 - `strchr`: Searches for the character from left to right and returns the address of its first occurrence.
 - `strrchr`: Searches from left to right, but returns the address of its last occurrence.

#### 3. Return value of `strrchr`

The return type is `char *`. It returns the address of the found character, or NULL if the character is not found.

An important feature of `strrchr` is that it searches for '\0', meaning it can return the address of the string terminator '\0'.

#### 4. Common use case of `strrchr`: "getting the file extension"

Example 1: `strrchr` is very common when processing file paths and filenames.

```c
char *filename = "document.txt";

char *p = strrchr(filename, '.');
```

The resulting pointer p points to the `.txt` of document.txt, therefore:

```c
printf("%s\n", p); // .txt
```

Example 2: Let's look at another path example. If we want to find the last `/`, we can do:

```c
char *path = "/Users/lee/project/main.c";

char *p = strrchr(path, '/');
```

If p points to the last `/` of the string "/Users/lee/project/main.c", then:

```c
printf("%s\n", p + 1);
```

gives `/main.c`, and p + 1 points to `main.c`, which is why you often see the following idiom:

```c
char *filename = strrchr(path, '/');

if (filename)
    filename++;
```
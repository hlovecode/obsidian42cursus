#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Its function is very simple: it calculates the number of characters in a string, excluding the terminating `'\0`. 

#### 2. Why is '\0' not counted?

Strings in C are not an independent data type; they are actually a sequence of `char`s. 
The purpose of '\0' is to tell C that the string ends here. 
If the logical length of the string is 5, the actual character array space occupied is 6.

```c
#include <string.h>

size_t strlen(const char *s);
``` only reads the string and will not modify its contents.
The function parameter must point to a valid C string terminated by '\0'.

`strlen()` is an empty string, which is actually just '\0', and the function returns 0.
Note: An empty string is not devoid of memory, but rather contains a '\0'.

```c
char *str = NULL;
strlen(str);
``` is illegal and results in undefined behavior, because ```c
#include <string.h>

size_t strlen(const char *s);
``` will attempt to access a string that has no valid backing. Therefore, do not write:
```c
char *str = NULL;
strlen(str);
```
Nor should you use ```c
#include <string.h>

size_t strlen(const char *s);
``` to check whether `str` is `NULL`. Do not write:
```c
if (strlen(str) == 0) 来判断 str == NULL
```
The correct way is:
```c
if (str == NULL)
{
	/* NULL */
	...
}
else if (strlen(str) == 0)
{
	/* empty string */
	...
}
```

#### 3. The `size_t` Type

It is an unsigned integer type `unsigned int` or `unsigned long`, declared and defined by `<stddef.h>`. It is the safest type to use for any integer data object serving as an array index, as you do not need to worry that a small array will evolve into a very large array as the program changes.

When using `size_t`, index arithmetic will never overflow. In a program, `size_t` should be used for all places where arithmetic operations are performed on array indices or addresses. The downside is that negative values cannot be used. 

`size_t` is an unsigned integer type defined by the C standard, specifically used to represent:
- Object sizes
- Array sizes
- Memory sizes
- Byte counts


## GitHub Actions Test

This is a GitHub Actions automated translation test.
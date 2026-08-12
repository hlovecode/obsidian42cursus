#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Its function is very simple: it calculates the number of characters in a string, excluding the terminating `'\0`. 

#### 2. Why is '\0' not counted?

Strings in C are not an independent data type; they are actually a sequence of `char`. 
The purpose of '\0' is to tell C that the string ends here. 
If the logical length of the string is 5, the actual character array space occupied is 6.

strlen() only reads the string and does not modify its contents.
The function argument must point to a valid C string terminated by '\0'.

strlen("") is an empty string, which is actually just '\0', and the function returns 0.
Note: An empty string does not mean it has no memory; rather, it contains a '\0'.

strlen(NULL) is illegal and results in undefined behavior, because strlen will attempt to access a memory location that has no valid string at all. Therefore, do not write:

```c
char *str = NULL;
strlen(str);
```
Also, do not use strlen to check whether `str` is NULL. Do not write:
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

It is an unsigned integer type `unsigned int` or `unsigned long`, declared and defined by `<stddef.h>`. It is the safest type to use for any integer data objects used as array indices, eliminating the worry that small arrays might evolve into very large arrays as the program changes.

When using `size_t`, index arithmetic will never overflow. In a program, all places performing arithmetic operations on array indices or addresses should use the `size_t` type. The downside is that negative values cannot be used. 

`size_t` is an unsigned integer type defined by the C standard, specifically used to represent:
- Object size
- Array size
- Memory size
- Byte count
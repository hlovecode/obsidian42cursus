#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Its function is very simple: it calculates the number of characters in a string, excluding the terminating `'\0`. 

#### 2. Why is '\0' not counted?

Strings in C are not an independent data type; they are actually a sequence of ___chars___. 
The purpose of ___'\0'___ is to tell C where the string ends. 
If the logical length of a string is 5, the actual space occupied in the character array is 6.

`strlen()` only reads the string and does not modify its contents.
The function parameter must point to a valid C string terminated by ___'\0'___.

___strlen("")___ is an empty string, which is actually just ___'\0'___, and the function returns 0.
Note: An empty string is not without memory; rather, it contains a ___'\0'___.

___strlen(NULL)___ is illegal and results in undefined behavior, because ___strlen___ will attempt to access a memory address that has no valid string. Therefore, do not write:
```c
char *str = NULL;
strlen(str);
```
Nor should you use ___strlen___ to check whether ___str___ is NULL; do not write:
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

#### 3. The type size_t

It is an unsigned integer type, `unsigned int` or `unsigned long`, declared and defined in `<stddef.h>`. It is the safest type to use for any integer data object representing an array subscript, as you don't have to worry about small arrays growing into very large ones as the program evolves.

When using `size_t`, subscript arithmetic will never overflow. In a program, `size_t` should be used for all arithmetic operations involving array subscripts or addresses. The disadvantage is that negative values cannot be used. 

`size_t` is an unsigned integer type defined by the C standard, specifically used to represent:
- Object size
- Array size
- Memory size
- Byte count
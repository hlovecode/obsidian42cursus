#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Its function is very simple: it calculates the number of characters in a string, excluding the terminating `'\0`.

#### 2. Why is '\0' not counted?

Strings in C are not an independent data type; they are actually a sequence of `char`s.
The role of '\0' is to tell C that the string ends here.
If the logical length of a string is 5, the actual storage space occupied in the character array is 6.

`strlen()` only reads the string; it does not modify the string contents.
The function parameter must point to a valid C string terminated by '\0'.

`strlen("")` is an empty string, which is actually just '\0', and the function returns 0.
Note: An empty string is not devoid of memory; rather, it contains a '\0'.

`strlen(NULL)` is illegal and results in undefined behavior, because `strlen` will attempt to access a memory address that does not contain a valid string. Therefore, do not write:

```c
char *str = NULL;
strlen(str);
```
Nor should you use `strlen` to check whether `str` is `NULL`. Do not write:
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

It is an unsigned integer type, either `unsigned int` or `unsigned long`, declared and defined by `<stddef.h>`. It is the safest type to use for any integer data object acting as an array subscript, as there is no need to worry about small arrays evolving into very large ones as the program changes.

When using `size_t`, subscript arithmetic will never overflow. Throughout a program, `size_t` should be used for all arithmetic operations on array subscripts or addresses. Its drawback is that negative values cannot be used.

`size_t` is an unsigned integer type defined by the C standard, specifically used to represent:

- Object sizes
- Array sizes
- Memory sizes
- Byte counts
#### 1. Prototype

```c
#include <string.h>

size_t strlen(const char *s);
```
Its function is very simple: it calculates the number of characters in a string, excluding the terminating `'\0`.

#### 2. Why is '\0' not counted?

Strings in C are not an independent data type; they are actually just a sequence of `char`s.
The purpose of '\0' is to tell C that the string ends here.
If the logical length of a string is 5, the character array actually occupies 6 spaces in memory.

`strlen()` only reads the string and will not modify its contents.
The function parameter must point to a valid C string terminated by '\0'.

`strlen("")` is an empty string, which is actually just '\0', and the function returns 0.
Note: An empty string does not mean it has no memory; rather, it contains a '\0'.

`strlen(NULL)` is illegal and results in undefined behavior, because `strlen` will attempt to access a memory address that does not contain a valid string. Therefore, do not write:
```c
char *str = NULL;
strlen(str);
```
Nor should you use `strlen` to check whether `str` is `NULL`. Do not write:
```c
if (strlen(str) == 0) 来判断 str == NULL
```
Instead, the correct way is:
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

#### 3. The `size_t` type

It is an unsigned integer type `unsigned int` or `unsigned long`, declared and defined by `<stddef.h>`. It is the safest type to use for any integer data object used as an array subscript, ensuring you don't have to worry about small arrays growing into very large ones as the program evolves.

When using `size_t`, subscript arithmetic will never overflow. In a program, `size_t` should be used anywhere arithmetic operations are performed on array subscripts or memory addresses. The downside is that it cannot hold negative values.

`size_t` is an unsigned integer type defined by the C standard, specifically designed to represent:
- Object sizes
- Array sizes
- Memory sizes
- Byte counts


## GitHub Actions Test

This is a GitHub Actions automated translation test.
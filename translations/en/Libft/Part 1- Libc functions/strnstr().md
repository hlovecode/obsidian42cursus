`strnstr` is used to find the first occurrence of the string `needle` within the first len characters of the string `haystack`.

#### 1. Prototype

```c
#include <string.h>

char	*strnstr(const char *haystack, const char *needle, size_t len);
```

Parameters:

- haystack: The string to be searched
- needle: The string to search for, i.e., the substring
- len: The maximum number of characters allowed to be searched within the first len characters of haystack; this controls how many characters are allowed to be searched in haystack

Return Value:

A pointer to the first occurrence of needle in haystack. If not found, returns NULL. If needle is an empty string, returns haystack.

#### 2. `strnstr` Core Logic

1. Is needle an empty string? If so, return haystack.
2. Search for potential starting points within the first len characters of haystack.
3. For each potential starting point: check if needle matches completely.
4. Is the match successful? If so, return the current position.
5. Have all possibilities been checked? If so, [return NULL].

#### 3. Comparison with Similar Functions

| Function | Search Object | Limits Search Range? |
| --- | --- | --- |
| `strstr` | Substring in a string | No |
| `strnstr` | Substring in a string | Yes |
| `strchr` | Single character | No |
| `strrchr` | Last occurrence of a single character | No |
| `strncmp` | Compare two strings | Yes |
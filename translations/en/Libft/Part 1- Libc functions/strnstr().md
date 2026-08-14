`strnstr` is used to find the first occurrence of the string `needle` within the first `len` characters of the string `haystack`.

#### 1. Prototype

```c
#include <string.h>

char	*strnstr(const char *haystack, const char *needle, size_t len);
```

Parameters:

- haystack: The string to be searched
- needle: The string to search for, i.e., the substring
- len: The maximum number of allowed characters to search within the first `len` characters of `haystack`, controlling how many characters are allowed to be searched in `haystack`

Return value:

A pointer to the first occurrence of `needle` in `haystack`. If not found, returns `NULL`. If `needle` is an empty string, returns `haystack`.

#### 2. `strnstr` Core Logic

1. Is `needle` an empty string? If so, return `haystack`.
2. Search for possible starting points within the first `len` characters of `haystack`.
3. For each possible starting point: check if `needle` matches completely.
4. Is the match successful? If so, return the current position.
5. Have all possibilities been checked? If so, return `NULL`.

`strnstr`: Searches for the first complete occurrence of `needle` within the first `len` characters of `haystack`; returns a pointer if found, returns `NULL` if not found, and returns `haystack` if `needle` is an empty string.

#### 3. Comparison with Similar Functions

| Function | Search Target | Range-limited Search |
| --- | --- | --- |
| `strstr` | Substring within a string | No |
| `strnstr` | Substring within a string | Yes |
| `strchr` | Single character | No |
| `strrchr` | Last occurrence of a single character | No |
| `strncmp` | Compare two strings | Yes |

- `strchr`: Find a character
- `strstr`: Find a string
- `strnstr`: Find a string within a limited length
- `strncmp`: Compare the first `n` characters of two strings
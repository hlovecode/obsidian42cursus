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

#### 2. Comparison with Similar Functions

| Function | Search Object | Limits Search Range? |
| --------- | ---------- | -------- |
| `strstr`  | Substring in a string  | No      |
| `strnstr` | Substring in a string  | Yes       |
| `strchr`  | Single character       | No      |
| `strrchr` | Last occurrence of a single character | No      |
| `strncmp` | Compare two strings    | Yes       |
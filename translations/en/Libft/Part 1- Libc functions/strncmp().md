`strncmp` compares at most the first `n` characters.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Its function is to compare `s1` and `s2` byte by byte from the beginning, up to a maximum of `n` characters; it can stop upon encountering the first differing character or `\0`. If all characters within the comparison range are identical, it returns `0`; otherwise, it returns a negative or positive value based on the relative magnitude of the first differing character.

Return value:

|Comparison Result|Return Value|
|---|---|
|The first `n` characters of `s1` are identical to `s2`|`0`|
|`s1` is less than `s2`|`< 0`|
|`s1` is greater than `s2`|`> 0`|
Note: Do not rely on specific returns of -1 or 1; the standard only guarantees < 0, = 0, or > 0.

#### 2. Differences between `strncmp` and `strcmp`

`strcmp` compares the entire string, whereas `strncmp` compares at most the first n characters.

|          | strcmp     | strncmp    |
| -------- | ---------- | ---------- |
| Header file | <string.h> | <string.h> |
| Compare strings | yes        | yes        |
| Number of arguments | 2          | 3          |
| Limit comparison length | no         | yes        |
| Max characters to compare | Unlimited | n characters |
| Returns 0 | Equal      | First n characters are equal |

#### 3. Application of `strncmp`

This function is very suitable for determining string prefixes.

For example: determine whether "quit_now" starts with quit

```c
if (strncmp(command, "quit", 4) == 0)
{
	...
}
```

The 3 most crucial points about `strncmp`:

- n is the "maximum number of characters to compare", not necessarily having to compare n characters
- Stops upon encountering the 1st differing character
- The return value only depends on the sign; do not rely on specific numbers:

```c
if (strncmp(s1, s2, n) < 0)

if (strncmp(s1, s2, n) == 0)

if (strncmp(s1, s2, n) > 0)
```

Do not write:

```c
if (strncmp(s1, s2, n) == -1)
```

Because the standard does not guarantee it will always return -1.

The essence of `strncmp` is:

- Within a window of at most `n`, find the first differing character between `s1` and `s2`
- Compare if found; return 0 if not found
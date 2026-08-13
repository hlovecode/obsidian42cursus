`strncmp` compares at most the first `n` characters.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Its function is to compare `s1` and `s2` byte by byte from the beginning, up to a maximum of `n` characters. It stops upon encountering the first differing character or `\0`. If all characters within the comparison range are identical, it returns `0`; otherwise, it returns a negative or positive value based on the relational magnitude of the first differing character.

Return value:

|Comparison Result|Return Value|
|---|---|
|The first `n` characters of `s1` are identical to `s2`|`0`|
|`s1` is less than `s2`|`< 0`|
|`s1` is greater than `s2`|`> 0`|
Note: Do not rely specifically on returning -1 or 1; the standard only guarantees < 0, = 0, or > 0.
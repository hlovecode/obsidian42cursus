`strncmp` compares at most the first `n` characters.

#### 1. Prototype

```c
#include <string.h>

int strncmp(const char *s1, const char *s2, size_t n);
```

Its function is to compare `s1` and `s2` byte by byte from the beginning, up to a maximum of `n` characters. It can stop when the first differing character or `\0` is encountered. If all characters within the comparison range are identical, it returns `0`; otherwise, it returns a negative or positive value based on the relative size of the first differing character.
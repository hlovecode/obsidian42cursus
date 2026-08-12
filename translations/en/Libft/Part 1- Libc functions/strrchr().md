strrchr finds the last occurrence of a character in a string.

#### 1. Prototype

```c
#include <string.h>

char *strrchr(const char *s, int c);
```

Its function is to search from left to right, but return the position of the last occurrence of the character.
The specific implementation can scan the string either from front to back, or from back to front.

#### 2. `strrchr` and `strchr`
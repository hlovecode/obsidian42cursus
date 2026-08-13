`memcmp` compares the contents of the first `n` bytes of two memory blocks, rather than comparing strings.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Its function is to compare the first `n` bytes of the two memory regions starting from `s1` and `s2` respectively.

Return value:

|Comparison Result|`memcmp` Return Value|
|---|---|
|The two memory blocks are identical|`0`|
|The first differing byte in `s1` is **less than** the corresponding byte in `s2`|Less than `0`|
|The first differing byte in `s1` is **greater than** the corresponding byte in `s2`|Greater than `0`|

The C standard only guarantees the sign of the return value (positive, negative, or zero), not the exact magnitude. Therefore, you should make one of the following checks instead of assuming a specific value:

```c
if (memcmp(s1, s2, n) > 0)

if (memcmp(s1, s2, n) == 0)

if (memcmp(s1, s2, n) < 0)
```
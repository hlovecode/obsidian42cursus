`memcmp` compares the contents of the first `n` bytes of two memory blocks, rather than comparing strings.
It treats memory as a sequence of bytes and compares them byte by byte.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Its purpose is to compare the first `n` bytes of the two memory areas starting at `s1` and `s2` respectively, meaning it compares at most that many bytes.

Return value:

|Comparison Result|`memcmp` Return Value|
|---|---|
|The two memory blocks are completely identical|`0`|
|The first differing byte in `s1` is **less than** the corresponding byte in `s2`|Less than `0`|
|The first differing byte in `s1` is **greater than** the corresponding byte in `s2`|Greater than `0`|

The C standard only guarantees the sign of the return value (positive, negative, or zero), not the exact magnitude. In other words, you should make one of the following checks rather than checking for `memcmp(s1, s2, n) == -1`, because the C standard does not mandate returning -1:

```c
if (memcmp(s1, s2, n) > 0)

if (memcmp(s1, s2, n) == 0)

if (memcmp(s1, s2, n) < 0)
```

#### 2. `memcmp` compares bytes

Example:

```c
char a[] = "abc";
char b[] = "abd";
```

Memory can actually be understood as:

```c
a:

address
 ↓
+----+----+----+----+
| a  | b  | c  | \0 |
+----+----+----+----+
 97   98   99    0
 
 
 b:
 
+----+----+----+----+
| a  | b  | d  | \0 |
+----+----+----+----+
 97   98  100    0

```

Executing `memcmp(a, b, 3);` actually compares:

```c
first byte: 97 == 97

second byte: 98 == 98

third byte: 99 != 100

```

Since 99 < 100, therefore `memcmp(a, b, 3) < 0`

#### 3. `memcmp` vs `memcpy` vs `memmove`

| Function  | What it does                       |
| --------- | ---------------------------------- |
| `memset`  | Sets a memory block to a specific byte |
| `memcpy`  | Copies a memory block to another   |
| `memmove` | Safely moves/copies possibly overlapping memory |
| `memchr`  | Searches for a byte in memory      |
| `memcmp`  | Compares two memory blocks         |
| `strlen`  | Calculates string length           |
| `strcmp`  | Compares strings                   |
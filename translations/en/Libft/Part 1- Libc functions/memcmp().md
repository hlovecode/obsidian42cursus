`memcmp` compares the contents of the first `n` bytes of two memory blocks, rather than comparing strings.
It treats memory as a stream of bytes and compares them byte by byte.

#### 1. Prototype

```c
#include <string.h>

int memcmp(const void *s1, const void *s2, size_n);
```

Its function is to compare the first `n` bytes of the two memory regions starting at `s1` and `s2` respectively, meaning it compares at most that many bytes.

Return value:

|Comparison Result|`memcmp` Return Value|
|---|---|
|The two memory blocks are completely identical|`0`|
|The first differing byte in `s1` is **less than** the corresponding byte in `s2`|Less than `0`|
|The first differing byte in `s1` is **greater than** the corresponding byte in `s2`|Greater than `0`|

The C standard only guarantees the sign of the return value and zero, without guaranteeing the specific returned amount. This means you should make one of the following checks rather than `memcmp(s1, s2, n) == -1`, because the C standard does not mandate returning -1:

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

#### 3. `s1` vs `memcpy` vs `memmove`

| Function | What it does |
| --------- | --------------- |
| `memset` | Sets a memory block to a specific byte |
| `memcpy` | Copies one memory block to another |
| `memmove` | Safely moves/copies memory that may overlap |
| `memchr` | Locates a specific byte in memory |
| `memcmp` | Compares two memory blocks |
The common feature of this group of functions is that they treat data as raw bytes rather than interpreting it as "strings".

#### 4. `memcmp` vs `strcmp`

| Comparison Item | `memcmp` | `strcmp` |
| ------------------- | ------------------------------------------------------- | --------------------------------------------- |
| **Function Prototype** | `int memcmp(const void *s1, const void *s2, size_t n);` | `int strcmp(const char *s1, const char *s2);` |
| **Purpose** | Compares the first `n` **bytes** of two memory blocks | Compares two **strings** |
| **Requires `n`?** | **Yes**, `n` specifies how many bytes to compare | **No** |
| **Requires `\0`?** | **No** | **Yes, strings must be terminated by `\0`** |
| **When it stops** | After comparing `\0` bytes, or upon encountering the first differing byte | Upon encountering the first differing character, or upon encountering `\0` |
| **Comparison Object** | Arbitrary memory data | C strings |
| **Can compare binary data?** | **Yes** | **Not suitable** |
| **Treats `\0` as a special terminator?** | **No**, `\0` is just an ordinary byte | **Yes**, `\0` indicates the end of the string |
| **Returns `0` when** | The first `n` bytes are all identical | The two strings have identical content |
| **Returns `< 0` when** | In the first differing byte, `s1` is less than `s2` | In the first differing character, `s1` is less than `s2` |
| **Returns `> 0` when** | In the first differing byte, `s1` is greater than `s2` | In the first differing character, `s1` is greater than `s2` |
| **Typical Use Case** | Comparing arrays, raw memory in structures, binary data, etc. | Comparing strings such as usernames, words, and sentences |
| **Example** | `memcmp(a, b, 10)` | `strcmp("abc", "abd")` |

`memcmp` compares "a specified number of memory bytes", while `strcmp` compares "strings terminated by `\0`"
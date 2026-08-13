`memchr` searches for a specific byte within the first `n` bytes of a memory block, and it does not care about `'\0'`.
`memchr` searches for a byte, not a character. It's just that when searching for a normal ASCII string, a character usually occupies exactly one byte, making it look like it's searching for a character.
This function only reads memory and does not modify it.

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

Its function is to inspect the first `n` bytes starting from the memory area `s`, looking for the first byte whose value equals `(unsigned char)c`.

Return value:

- If found, returns a pointer to this byte.
- If not found, returns NULL.

#### 2. `memchir` can handle data without '\0'

One of the biggest differences between `memchr` and other string functions is that it can handle data without '\0'. It does not need '\0' to determine the end position; it relies solely on n.

`memchr` essentially checks byte by byte and can handle arbitrary memory.

#### 3.  `memchir`  vs  `strchr` 

|Feature|`strchr`|`memchr`|
|---|---|---|
|Header|`<string.h>`|`<string.h>`|
|Search Object|C string|Memory area|
|Requires `'\0'`|Yes|No|
|Stops upon encountering `'\0'`|Yes|No|
|Search Range|Up to `'\0'`|First `n` bytes|
|`n` Parameter|No|Yes|
|Can search binary data|Unsuitable|Very suitable|
|Return Value|`char *`|`void *`|
|Not Found|`NULL`|`NULL`|

- `strchr` : Searches for a character in a string
- `memchr` : Searches for a byte in memory

#### 4. Implementation concept of `memchr`

1. Cast s to unsigned char *
2. Check from i = 0 while i < n
3. Check if s\[i] equals (unsigned char)c:
	- If equal, return `&s[i]`
	- If not equal, i++
	- If the loop finishes and it's still not equal, return NULL

`memchr(s, c, n)` starts from `s`, treats the memory as a string of bytes, strictly checks the first `n` bytes, and looks for the first byte equal to `(unsigned char)c`; if found, it returns its address, and if not found, it returns `NULL`.
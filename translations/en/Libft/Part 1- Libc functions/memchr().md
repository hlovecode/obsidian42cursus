`memchr` Searches for a specific byte in the first `n` bytes of a block of memory, and it does not care about `'\0'`.
`memchr` Searches for a byte (byte) rather than a character. It is just that when searching for ordinary ASCII strings, a character usually occupies exactly one byte, so it appears to be searching for characters.
This function only reads memory and does not modify it.

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

Its function is to start from the memory area `s`, check the first `n` bytes, and look for the first byte whose value equals `(unsigned char)c`. 

Return value:

- If found, returns a pointer to this byte
- If not found, returns NULL

#### 2. `memchir` can handle data without '\0'

One of the biggest differences between `memchr` and other string functions is that it can handle data without '\0'. It does not need '\0' to determine the end position; it relies solely on n.
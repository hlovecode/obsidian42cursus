`memchr` Searches for a specific byte within the first `n` bytes of a block of memory; it does not care about `'\0'`.
`memchr` Searches for the byte `btye`, not a character. It just happens that when searching for a regular ASCII string, a character typically occupies exactly one byte, making it look like it is searching for a character.
This function only reads memory and does not modify it. 

#### 1. Prototype

```c
<string.h>

void *memchr(const void *s, int c, size_t n);
```

Its function is to start from the memory area `s`, check the first `n` bytes, and look for the first byte whose value is equal to `(unsigned char)c`. 

Return value:

- If found, returns a pointer to this byte
- If not found, returns NULL

#### 2. `memchr` Can handle data without '\0'

One of the biggest differences between `memchr` and other string functions is that it can handle data without '\0'. It does not need '\0' to determine the end position; it relies solely on `n`. 

`memchr` essentially checks byte by byte, and it can handle arbitrary memory.

#### 3.  `memchr`  vs  `strchr` 

|Feature|`strchr`|`memchr`|
|---|---|---|
|Library|`<string.h>`|`<string.h>`|
|Search Target|C string|Memory area|
|Requires `'\0'`|Yes|No|
|Stops when encountering `'\0'`|Yes|No|
|Search Range|Up to `'\0'`|First `n` bytes|
|`n` Parameter|None|Yes|
|Can search binary data|Unsuitable|Very suitable|
|Return Value|`char *`|`void *`|
|Not found|`NULL`|`NULL`|

- `strchr` : Searches for a character in a string
- `memchr` : Searches for a byte in memory

#### 4. Implementation concept of `memchr`

1. Cast `s` to `unsigned char *`
2. Start checking from `i = 0` while `i < n`
3. Check if `s[i]` is equal to `(unsigned char)c`:
	- If equal, return `&s[i]`
	- If not equal, `i++`
	- If the loop finishes and it is still not equal, return `NULL`

`memchr(s, c, n)` starts from `s`, treats the memory as a sequence of bytes, strictly checks the first `n` bytes, and looks for the first byte equal to `(unsigned char)c`. If found, it returns its address; if not found, it returns `NULL`.
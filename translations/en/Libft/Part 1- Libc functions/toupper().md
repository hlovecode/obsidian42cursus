If a lowercase English letter `'a'` through `'z'` is passed in, convert it to the corresponding uppercase letter `'A'` through `'Z'`; otherwise, return it unchanged.

#### 1. Prototype

```c
#include <ctype.h>

int toupper(int c);
```
`toupper()` accepts an `int`, and returns an `int`

#### 2. Why is the return type int?

Character functions in `ctype.h` typically require the parameter to be able to represent:
1. An `unsigned char` value
2. Or the special value `EOF`, where `EOF` is generally defined as a negative `int` value
Therefore, int is used to pass characters.

[[tolower()]]
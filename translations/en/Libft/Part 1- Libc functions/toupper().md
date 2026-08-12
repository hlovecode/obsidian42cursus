<<<<<<< HEAD
If the passed character is a lowercase English letter `'a'` through `'z'`, convert it to the corresponding uppercase letter `'A'` through `'Z'`; otherwise, return it unchanged.

#### 1.  Prototype
=======
If a lowercase English letter `'a'` through `'z'` is passed in, convert it to the corresponding uppercase letter `'A'` through `'Z'`; otherwise, return it unchanged.

#### 1. Prototype
>>>>>>> origin/main

```c
#include <ctype.h>

int toupper(int c);
```
<<<<<<< HEAD
`toupper()` accepts `int` and also returns `int`

#### 2. Why is the return type int?

Character functions in `ctype.h` typically require parameters that can represent:
1. A `unsigned char` value
=======
`toupper()` accepts an `int`, and returns an `int`

#### 2. Why is the return type int?

Character functions in `ctype.h` typically require the parameter to be able to represent:
1. An `unsigned char` value
>>>>>>> origin/main
2. Or the special value `EOF`, where `EOF` is generally defined as a negative `int` value
Therefore, int is used to pass characters.

[[tolower()]]
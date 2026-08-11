`isalpha()` is one of the most commonly used character classification functions in the **C Standard Library (`<ctype.h>`)**, used to **determine whether a character is an English letter (a ~ z / A ~ Z).**
Letters are determined based on the ASCII table, specifically 65 ~ 90 and 97 ~ 122.

1. **Prototype**
```c
#include <ctype.h>

int isalpha(int c);
```
Return value:
- Non-zero (usually 1, though the standard does not require it to be 1) if it is a letter
- 0 if it is not a letter
For example:
```c
isalpha('A');   // true
isalpha('z');   // true
isalpha('3');   // false
isalpha('$');   // false
```

<font color="red"> isalpha() simply checks for 65 ~ 90 or 97 ~ 122. </font>

2. **Why is the function parameter `int`? Because:**
- `char` undergoes integer promotion
	For example:
	```c
	char c = 'a';
	isalpha(c);
	```
	In actual calls, `char` is automatically promoted to `int`, which is why the standard library directly uses `int c`.

- It can also accept `EOF`
`EOF` stands for End of File, meaning the end of a file or input.
In C, `EOF` is a special integer flag value used to indicate that there are no more characters to read, or that a read error has occurred. It is not an ordinary character; typically in systems, the value of `EOF` is `-1`, but note that the C standard only guarantees that `EOF` is a negative `int` value, and does not require it to be specifically `-1`.

==Note==:
`EOF` is not an ASCII character; it is a special return value used by the C standard library to indicate "no more input." It should be understood as:
```txt
字符 → 实际读到的数据

EOF → 没有数据可以继续读
```

`int` can accommodate both character values and `EOF`, whereas `char` may not be able to correctly distinguish a regular character from `EOF`. Therefore, the C standard library uses `int c` as the function parameter, which is a very important design choice in C.

==Note==:
`EOF` and `\0` are completely different!
- `EOF` is not a string terminator; it indicates that the input stream/file has no more content to read, telling the program that the file has been fully read.
- `\0` is an actual character with an ASCII value of 0, primarily used to mark the end of C-style strings.

Understanding `EOF` within the context of the overall C input system:
```txt
                 C 输入流
                    │
                    ▼
              getchar()
              /       \
             /         \
       正常读取        读取结束/错误
          │                 │
          ▼                 ▼
       字符的 int           EOF
          │
          ▼
      isalpha(c)
      isdigit(c)
      isspace(c)
      ...
```
For example:
```c
int c;

while ((c = getchar()) != EOF)
{
    if (isalpha(c))
        printf("letter\n");
}
```

**`EOF` is not a character, but a special negative integer return value used by C input functions to indicate "no more characters can be read (or a read error occurred)."**

[[isalnum()]]
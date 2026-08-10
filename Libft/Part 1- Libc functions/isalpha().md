`isalpha()` 是 **C 标准库（<ctype.h>）** 中最常用的字符分类函数之一，用于**判断一个字符是否是英文字母(a ~ z / A ~ Z).**
字母是根据ASCII表来判断的, 因此就是 65 ~ 90 以及 97 ~ 122. 

1. **Prototype**
```c
#include <ctype.h>

int isalpha(int c);
```
返回值：
- 非0 (通常为1，但标准没有规定必须是1) 则是字母
- 0 则不是字母
例如：
```c
isalpha('A');   // true
isalpha('z');   // true
isalpha('3');   // false
isalpha('$');   // false
```

<font color="red"> isalpha() 就是检查 65 ~ 90 或者 97 ~ 122. </font>

2. **为什么函数参数是int ? 因为：**
- char 会自动提升
	例如：
	```c
	char c = 'a';
	isalpha(c);
	```
	实际上调用时，char 会自动提升为int，因此标准库直接写int c

- 还可以传 `EOF`
`EOF` 是 End of File, 即文件结束或输入结束.
在C语言中，`EOF` 是一个特殊的整型标志值，用来表示已经没有更多字符可以读取了，或者读取发生了错误. 它不是一个普通字符，通常在系统中，`EOF` 的值是 `-1`，但注意C 标准只保证 `EOF` 是一个负的int 值，不要求一定是`-1`.

==注意==：
`EOF` 不属于 ASCII字符，它是 C 标准库用来表示 “没有更多输入了" 的一种特殊返回值. 应该把它理解成：
```txt
字符 → 实际读到的数据

EOF → 没有数据可以继续读
```

int 同时容纳字符值和EOF, 而 char 未必可以正确区分某个普通字符和EOF，因此函数参数C标准库采用int c，这是一个非常重要的C语言设计.

==注意==：
`EOF` 和 `\0` 完全不同！
- EOF 不是字符串结束符，表示输入流/文件已经没有更多内容可以读取, 告诉程序文件已经读完了
- \0 是一个真正的字符，其ASCII 值 = 0, 主要用于标记C字符串结束

把EOF放到整个C输入体系里理解：
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
例如：
```c
int c;

while ((c = getchar()) != EOF)
{
    if (isalpha(c))
        printf("letter\n");
}
```

**EOF 不是一个字符，而是 C 输入函数用来表示“没有更多字符可读取（或发生读取错误）”的特殊负整数返回值.**

[[isalnum()]]
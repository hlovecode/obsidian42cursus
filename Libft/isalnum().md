`isalnum()` 是 C 标准库 `<ctype.h>` 中非常基础、也非常常用的**字符分类函数**, 用来判断一个字符是不是字母或数字.

#### 1. Prototype

```c
#include <ctype.h>

int isalnum(int c);
```
它判断：
```txt
A-Z
a-z
0-9
```
- 如果是字母或数字，则返回非0
- 如果不是，则返回0

**`isalnum` 和 `isalpha`, `isdigit` 的关系**：
```txt
isalnum 判断是不是字母或数字
   │
   ├── isalpha 只判断是不是字母
   │     └── A-Z / a-z
   │
   └── isdigit 只判断是不是数字
         └── 0-9
```

#### 2. isalnum 不判断下划线_，也不判断负数

```c
isalnum('_') // 不是字母和数字，返回0
isalnum(-100); // 错误
```
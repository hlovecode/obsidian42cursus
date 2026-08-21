strdup() 的作用非常直接，复制一个字符串，并为复制出来的字符串动态分配内存
可以理解为 `string duplicate`

`strdup` 在很多 Unix / POSIX 系统上都有，但它不是 ISO C 标准定义的函数，它属于 Unix / POSIX 环境中常见的接口. 

#### 1. Prototype

```c
char *strdup(const char *s);
```

例如：

```c
char *copy;

copy = strdup("Hello");
```

上面2行代码执行之后，可以理解为创建一个新的 "Hello",

原来的字符串 s："Hello\0"

`strdup()`

   ├── 计算字符串长度
   ├── 申请新的内存
   └── 把 "Hello\0" 复制进去
   
          ↓
新的动态内存：

┌────┬────┬────┬────┬────┬────┐
  
  │ H  │ e  │ l  │ l  │ o  │ \0 │
  
└────┴────┴────┴────┴────┴────┘
  ↑
 copy

copy 指向的是一块新的内存

**strdup 最终返回新复制出来的字符串的起始地址，不会修改原字符串**

`strdup` = “申请空间 + 复制字符串”

#### 2. `strdup` vs `strcpy`

`strcpy`: 把 src 的字符串复制到已经存在的 dest 内存中

`strdup`：是自己申请新的内存，然后把 src 复制进去

|               | strcpy   | strdup  |
| ------------- | -------- | ------- |
| 是否复制字符串       | Yes      | Yes     |
| 是否申请新内存       | No       | Yes     |
| dest 是否需要提前存在 | Yes      | No      |
| 返回值           | char \*  | char \* |
| 使用后是否需要 free  | 取决于 dest | 需要      |

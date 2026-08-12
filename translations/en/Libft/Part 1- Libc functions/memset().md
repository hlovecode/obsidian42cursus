`memset` is a very important **memory operation function** in C, which directly modifies every byte in a block of memory.

#### 1. Prototype

```c
#include <string.h>

void	*memset(void *s, int c, size_t n);
```
Its effect can be simply understood as setting the consecutive n bytes starting from s to the lower 8 bits of c. 
The lower 8 bits are the rightmost 8 bits in the binary representation of an integer. The reason memset takes these 8 bits is that it ultimately writes a byte (with a value range of 0 ~ 255), and 1 byte = 8 bits. 
(ps: 1 bit has only 2 states: 0 and 1)

The 3 parameters of the function:
```txt
             memset
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      s         c        n
      │         │        │
      ↓         ↓        ↓
   起始地址    要设置的   设置多少
               字节值     个字节
```
Returns the starting address s of the modified memory region, of type `void *`, which is a generic memory address. 

`memset` modifies n bytes starting from a certain address. When n == 0, it means modifying 0 bytes, modifying nothing, which can be understood as doing nothing. 
Note that n is the number of bytes, not the number of elements. 

`memset(s, c, n)` means: starting from address `s`, write the lower 8 bits of `c` to `n` consecutive bytes, and return `s`. The "lower 8 bits" are the rightmost 8 bits in the binary representation of an integer; the reason `memset` ultimately uses this part is that it converts `c` into an `unsigned char` and then repeatedly writes it to memory in units of one byte.

#### 2. Understanding Function Parameters

1. The 1st parameter `void *s`
Represents the starting address of the memory region to be operated on. `void *` is because memset does not care what type you pass in; it operates on bytes, not C types like char, int, double, etc.
For example:
```c
char str[10];
int tab[10];
double values[10];
```
Both are acceptable:
```c
memset(str, ...);
memset(tab, ...);
memset(values, ...);
```

2. The 2nd parameter `int c`
Sets n bytes to the converted unsigned char value of c. 
For example:
```c
char str[5];

memset(str, 'A', 5);
```
ASCII value of 'A': 'A' = 65 = 0x41
So 65 converted to hexadecimal is 0x41, and each byte becomes 41 41 41 41 41, which is A A A A A.

3. The 3rd parameter `size_t n`
Represents how many bytes to modify.
For example:
```c
char str[10];

memset(str, 'A', 3);
```
Means:
```txt
第 0 个字节 → A
第 1 个字节 → A
第 2 个字节 → A
```
A total of 3 bytes.

PS: Usually an int is 4 bytes.

#### 3. Most Common Uses of memset

1. Zeroing out an array
```c
int tab[100];

memset(tab, 0, sizeof(tab));
```

2. Initializing a struct
```c
struct person
{
	char	name[50];
	int		age;
};

memset(&p, 0, sizeof(p)); // 把整个结构体占用的字节设置为0
```

3. Clearing a character array
```c
char buffer[1024];

memset(buffer, 0, sizeof(buffer));
```
Result:
```c
buffer[0] = '\0'
buffer[1] = '\0'
buffer[2] = '\0'
...
```

4. Setting a block of memory to a specific byte
```c
char buffer[10];

memset(buffer, 'X', 10);
```
Yields:
```txt
X X X X X X X X X X
```

```txt
① s 是起始地址
        ↓
② 转成 unsigned char *
        ↓
③ i 从 0 开始
        ↓
④ 每次修改 1 byte
        ↓
⑤ 修改 n 次
        ↓
⑥ 返回原来的 s
```

```c
memset(tab, 1, sizeof(tab));

不是把tab中的每个元素设为1，而是把tab占用的每一个byte都设为0x01
```

#### 4. Understanding Function Operations

```txt
                 memset
                    │
                    ↓
             操作 memory
                    │
                    ↓
               按 byte 操作
                    │
                    ↓
             1 byte = 8 bits
                    │
                    ↓
        一个 byte 只有 8 个 bit
                    │
                    ↓
         c 转换成 unsigned char
                    │
                    ↓
            得到一个 byte
                    │
                    ↓
              低 8 位
            
    低8位并不是memset随便选择的，而是因为它最终一次写入的单位就是1个byte, 而这个byte
    在常见平台上是8 bits
```

Example: Understanding the following 2 lines of code
```c
char str[4];

memset(str, 0x12345678, 4);
```
Understanding it in 4 steps:
Step 1: The 2nd parameter c is 0x12345678.
Step 2: Convert to unsigned char, keeping only 1 byte: 0x78.
Step 3: The 3rd parameter n = 4, requiring 4 bytes to be written.
```c
byte 0
byte 1
byte 2
byte 3
```
Step 4: Write all of them as 0x78.
```c
┌──────┬──────┬──────┬──────┐
│ 0x78 │ 0x78 │ 0x78 │ 0x78 │
└──────┴──────┴──────┴──────┘
```
This is `memset(str, 0x12345678, 4);`.

PS: Understanding the notation 0x78
0x -> Tells the compiler that the following number 78 is represented in hexadecimal; the 0x notation is a convention in the C language.
	Understand `0x` as: "The following number is represented in hexadecimal."
78 -> The part that actually represents the value is 78.

[[bzero()]]
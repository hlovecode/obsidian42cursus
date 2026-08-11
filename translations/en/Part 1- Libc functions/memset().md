`memset` is a very important **memory operation function** in the C language, which directly modifies every byte in a block of memory.

#### 1. Prototype

```c
#include <string.h>

void	*memset(void *s, int c, size_t n);
```
Its effect can be simply understood as setting ```txt
             memset
                │
       ┌────────┼────────┐
       ↓        ↓        ↓
      s         c        n
      │         │        │
      ↓         ↓        ↓
   起始地址    要设置的   设置多少
               字节值     个字节
``` consecutive bytes starting from `void *` to the lower 8 bits of `memset`. 
The lower 8 bits refer to the rightmost 8 bits in the binary representation of an integer. The reason `memset(s, c, n)` takes these 8 bits is that it ultimately writes a byte (with a value range of 0 to 255), and 1 byte = 8 bits. 
(ps: 1 bit has only 2 states: 0 and 1)

The three parameters of the function:
`s`
Returns the starting address `n` of the modified memory region, whose type is `c`, a generic memory address. 

`s` modifies `memset` bytes starting from a certain address. When `c`, it means modifying 0 bytes, changing nothing, which can be understood as doing nothing. 
Note that `unsigned char` is the number of bytes, not the number of elements. 

`void *s` means: starting from address `void *`, write ```c
char str[10];
int tab[10];
double values[10];
``` consecutive bytes as the lower 8 bits of ```c
memset(str, ...);
memset(tab, ...);
memset(values, ...);
```, and return `int c`. The "lower 8 bits" are the rightmost 8 bits in the binary representation of an integer; the reason ```c
char str[5];

memset(str, 'A', 5);
``` ultimately uses this part is that it converts `size_t n` into an ```c
char str[10];

memset(str, 'A', 3);
```, and then repeatedly writes it to memory in units of one byte.

#### 2. Understanding Function Parameters

1. The 1st parameter ```txt
第 0 个字节 → A
第 1 个字节 → A
第 2 个字节 → A
```
Represents the starting address of the memory region to be operated on. ```c
int tab[100];

memset(tab, 0, sizeof(tab));
``` is used because ```c
struct person
{
	char	name[50];
	int		age;
};

memset(&p, 0, sizeof(p)); // 把整个结构体占用的字节设置为0
``` does not care what type you pass in; it operates on bytes, not C types like ```c
char buffer[1024];

memset(buffer, 0, sizeof(buffer));
```, ```c
buffer[0] = '\0'
buffer[1] = '\0'
buffer[2] = '\0'
...
```, ```c
char buffer[10];

memset(buffer, 'X', 10);
```, etc.
For example:
```txt
X X X X X X X X X X
```
Both are acceptable:
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

2. The 2nd parameter ```c
memset(tab, 1, sizeof(tab));

不是把tab中的每个元素设为1，而是把tab占用的每一个byte都设为0x01
```
Sets ```txt
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
``` bytes to the converted ```c
char str[4];

memset(str, 0x12345678, 4);
``` value of ```c
byte 0
byte 1
byte 2
byte 3
```. 
For example:
```c
┌──────┬──────┬──────┬──────┐
│ 0x78 │ 0x78 │ 0x78 │ 0x78 │
└──────┴──────┴──────┴──────┘
```
ASCII value of 'A': 'A' = 65 = 0x41
Therefore, 65 converted to hexadecimal is 0x41, and every byte becomes 41 41 41 41 41, which is A A A A A.

3. The 3rd parameter `memset(str, 0x12345678, 4);`
Represents how many bytes to modify.
For example:
`0x`
Means:
___PROTECTED_36___
A total of 3 bytes.

PS: Usually an ___PROTECTED_37___ is 4 bytes.

#### 3. Most Common Uses of memset

1. Zeroing out an array
___PROTECTED_38___

2. Initializing a struct
___PROTECTED_39___

3. Clearing a character array
___PROTECTED_40___
Result:
___PROTECTED_41___

4. Setting a block of memory to a specific byte
___PROTECTED_42___
Result:
___PROTECTED_43___

___PROTECTED_44___

___PROTECTED_45___

#### 4. Understanding Function Operations

___PROTECTED_46___

Example: Understanding the following 2 lines of code
___PROTECTED_47___
Understanding this is divided into 4 steps:
Step 1: The 2nd parameter ___PROTECTED_48___ is ___PROTECTED_49___.
Step 2: Convert to ___PROTECTED_50___, keeping only 1 byte: ___PROTECTED_51___.
Step 3: The 3rd parameter ___PROTECTED_52___, needs to write 4 bytes.
___PROTECTED_53___
Step 4: Write all bytes as ___PROTECTED_54___.
___PROTECTED_55___
This is what ___PROTECTED_56___ does.

PS: Understanding the notation ___PROTECTED_57___
___PROTECTED_58___ -> Tells the compiler that the following number ___PROTECTED_59___ is represented in hexadecimal; the ___PROTECTED_60___ notation is a convention in the C language.
	Understand ___PROTECTED_61___ as: "The following number is represented in hexadecimal."
___PROTECTED_62___ -> The part that actually represents the numerical value is ___PROTECTED_63___.

[[bzero()]]
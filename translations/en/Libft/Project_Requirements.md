Implement some functions in C, such as re-implementing libc, by creating a makefile and executing the make command to generate a static public library `libft.a`.
<font color="red">This is the foundational library for the entire Common Core.</font>
###### Group 1 Character checks:
```c
ft_isalpha

ft_isdigit

ft_isalnum

ft_isascii

ft_isprint
```
###### Group 2 Memory operations
```c
memset

bzero

memcpy

memmove

memcmp

memchr
```
###### Group 3 String functions
```c
strlen

strlcpy

strlcat

strchr

strrchr

strncmp

strnstr

strdup
```
###### Group 4 Character conversion
```c
toupper

tolower
```
###### Group 5 Number conversion
```c
atoi
```
###### Group 6 Dynamic memory
```c
calloc // 不同系统，行为可能不同
strdup
```
###### Group 7 Mandatory new functions
```c
ft_substr
ft_strjoin
ft_strtrim
ft_split
ft_itoa
ft_strmapi
ft_striteri
ft_putchar_fd
ft_putstr_fd
ft_putendl_fd
ft_putnbr_fd
```
###### Group 8 Linked List functions
| Function                | Description                   |
| ----------------- | -------------------- |
| `ft_lstnew`       | Create a new node                |
| `ft_lstadd_front` | Insert at the beginning                   |
| `ft_lstsize`      | Count the number of nodes               |
| `ft_lstlast`      | Get the last node             |
| `ft_lstadd_back`  | Insert at the end                   |
| `ft_lstdelone`    | Delete a node               |
| `ft_lstclear`     | Delete the entire list               |
| `ft_lstiter`      | Traverse the list and execute a function on each node       |
| `ft_lstmap`       | Transform the content of each node to create a new list |

### 1. Technical considerations Technical Requirements

1 **Global variables are prohibited**

Because Libft is a public library, it should always produce the same output for the same input.
If there are global variables, modifying them will cause the final result to change.

2 **Helper functions must be static**

For example: 
```c
ft_split()
```
Inside which you need:
```c
int count_words()
void copy_word()
free_all()
```
These functions should not be exposed to others and should be written as:
```c
static int count_words()
static void copy_word()
static free_all()
```
Because static means <font color="red">it can only be used within the current file</font> and will not pollute the entire library.

3 **All files must be placed in the root directory, as follows:**

```
libft/

Makefile

libft.h

ft_strlen.c
ft_memcpy.c
...
```
Everything must be placed directly in the root directory.

4 **Submitting unused files is not allowed**

For example:
```c
test.c
old.c
abc.c
```
If the Makefile does not use them at all, do not submit them.

5 **All .c files must:**

```bash
-Wall
-Wextra
-Werror
```
Be able to compile without warnings.

6 **Must use the ar command**

ar is short for archive, a tool in Unix/Linux/macOS systems used to pack multiple object files (`.o`) into an archive file.
The main objects of ar are `.o`


The most typical use case in C projects is multiple .o files -> ar -> a single .a static library.
For example, Libft:
```c
ft_strlen.o
ft_memset.o
ft_memcpy.o
ft_isalpha.o
ft_atoi.o
ft_split.o
...
```
Through:
```bash
</> Bash
ar
```
Ultimately resulting in:
```bash
libft.a
```
Therefore:
```bash
.c
 ↓ gcc/cc
.o
 ↓ ar
.a
```
This chain is extremely important.

`libft.a` is not a running library; it is actually an archive file containing many `.o` files, which can be roughly understood as:
```c
libft.a
│
├── ft_strlen.o
├── ft_memset.o
├── ft_memcpy.o
├── ft_isalpha.o
├── ft_isdigit.o
├── ft_strdup.o
├── ft_split.o
├── ft_itoa.o
└── ...
```

Therefore, what `ar` does is essentially organizing and packing many object files into a static library file.
> Understanding the command
> ```bash
>	ar rcs libft.a *.o
> ```
> ar: Invoke the archive tool
> rcs:
>	- r = replace Add the specified `.o` files to the archive. If a member with the same name already exists in the archive, replace it; if it does not exist, create it.
>	- c = create Create the archive if it does not exist.
>	- s Create a symbol index for the archive

The command:
```bash
</> Bash
ar rcs libft.a *.o
```
is the most typical way to create a static library, which can be understood as:
```bash
ar
│
├── r → 把 .o 加进去 / 替换旧版本
├── c → 必要时创建 .a
└── s → 建立符号索引
```

| Tool           | Main Role           |
| ------------ | -------------- |
| `cc` / `gcc` | Compile C           |
| `ar`         | Create/manage archives  |
| linker       | Link object files/libraries into the final program |

The project explicitly requires using `ar` to create `libft.a`, and prohibits using `libtool`

7 **libft.a must be located in the root directory**

`libft.a` is right next to `Makefile`.

### 2. README Requirements

`README.md` is part of the project and is required to be present in the repository root directory.

`README` should at least contain the following contents:

1 **The first line must be in italics, and the content must be strictly:**

```
*This activity has been created as part of the 42 curriculum by <login>.*
```
If working in a group, multiple logins can be listed sequentially.

2 **Description of the project, explaining:**

- What Libft is
- Project goals
- Main implementations

3 **Instructions for use**, such as:

- Compilation, e.g., make
- Generating `libft.a`
- Using the static library in other projects

4 **Resources (Reference materials)**

List the reference materials used during the learning process, such as:
- C standard library documentation (man pages)
- Tutorials
- Technical articles, etc.
In addition, it must also state **how AI was used in the project**, such as for concept explanation, code review, or debugging, while specifying which parts were completed by yourself.

5 **Detailed introduction to the created library**

Provide a detailed description of the `libft` library itself, such as:
- What categories of functions are included
- The purpose of each category of functions
- The role of this library in subsequent 42 projects
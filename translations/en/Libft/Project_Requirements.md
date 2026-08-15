Implement several functions in C, such as re-implementing libc, by creating a Makefile and executing the `make` command to generate a static public library `libft.a`.
<font color="red">This is the foundational library for the entire Common Core.</font>
###### Group 1: Character Classification
```c
ft_isalpha

ft_isdigit

ft_isalnum

ft_isascii

ft_isprint
```
###### Group 2: Memory Operations
```c
memset

bzero

memcpy

memmove

memcmp

memchr
```
###### Group 3: String Functions
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
###### Group 4: Character Conversion
```c
toupper

tolower
```
###### Group 5: Number Conversion
```c
atoi
```
###### Group 6: Dynamic Memory
```c
calloc // 不同系统，行为可能不同
strdup
```
###### Group 7: Additional Functions
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
###### Group 8: Linked List Functions
| Function          | Description                |
| ----------------- | -------------------- |
| `ft_lstnew`       | Creates a new node                |
| `ft_lstadd_front` | Adds a node at the beginning |
| `ft_lstsize`      | Counts the number of nodes               |
| `ft_lstlast`      | Gets the last node             |
| `ft_lstadd_back`  | Adds a node at the end |
| `ft_lstdelone`    | Deletes a node               |
| `ft_lstclear`     | Deletes the entire list               |
| `ft_lstiter`      | Iterates the list and applies a function to each node       |
| `ft_lstmap`       | Applies a function to each node's content to create a new list |

### 1. Technical considerations Technical Requirements

1 **Global variables are strictly prohibited**

Since Libft is a public library, same input -> always same output.
If global variables are used, modifying them will cause the final result to change.

2 **Helper Functions must be static**

For example: 
```c
ft_split()
```
needs
```c
int count_words()
void copy_word()
free_all()
```
These functions should not be exposed externally and should be written as:
```c
static int count_words()
static void copy_word()
static free_all()
```
Because `static` means <font color="red">it can only be used within the current file</font>, preventing pollution of the entire library.

3 **All files must be placed in the root directory, as follows:**

```
libft/

Makefile

libft.h

ft_strlen.c
ft_memcpy.c
...
```
Everything goes directly into the root directory.

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
Compile without warnings.

6 **The `ar` command must be used**

`ar` stands for archive, a utility in Unix/Linux/macOS systems used to bundle multiple object files (`.o`) into an archive file.
The primary targets of `ar` are `.o`


The most typical usage in C projects is multiple `.o` files -> `ar` -> a `.a` static library.
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

Therefore, what `ar` does is essentially organizing and packaging many object files into a static library file.
> Understanding the command
> ```bash
>	ar rcs libft.a *.o
> ```
> `ar`: Invokes the archive utility
> `rcs`:
>	- `r` = replace: Inserts the specified `.o` files into the archive. If a member with the same name already exists in the archive, it is replaced; if it does not exist, it is created.
>	- `c` = create: Creates the archive if it does not exist.
>	- `s`: Creates a symbol index for the archive.

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

| Tool           | Primary Role           |
| ------------ | -------------- |
| `cc` / `gcc` | Compiles C           |
| `ar`         | Creates/manages archives  |
| linker       | Links object files/libraries into the final program |

The project explicitly requires using `ar` to create `libft.a`, and prohibits using `libtool`

7 **`libft.a` must be located in the root directory**

`libft.a` is right next to `Makefile`.

### 2. README Requirements

`README.md` is part of the project and must be provided in the root directory of the repository.

`README` should at least contain the following contents:

1 **The first line must be in italics, with the fixed content:**
```
*This activity has been created as part of the 42 curriculum by <login>.*
```
If working in a team, multiple logins can be listed sequentially.

2 **Description, explaining:**
- What Libft is
- Project objectives
- Main implementations

3 **Instructions**, such as:
- Compilation, e.g., `make`
- Generating `libft.a`
- Using the static library in other projects

4 **Resources**
List the references used during the learning process, such as:
- C standard library documentation (man pages)
- Tutorials
- Technical articles, etc.
Additionally, you must state **the use of AI in the project**, such as for concept explanation, code review, or debugging, while specifying which parts were done by yourself.

5 **Detailed introduction of the created library**
Provide a detailed description of the `libft` library itself, such as:
- What categories of functions are included
- The purpose of each category of function
- The role of this library in subsequent 42 projects
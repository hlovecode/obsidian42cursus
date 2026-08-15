Implement some functions in C, such as re-implementing libc, by creating a Makefile and executing the `make` command to generate a static public library `libft.a`.
<font color="red">This is the foundational library of the entire Common Core.</font>
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
###### Group 7: Required New Functions to Write Yourself
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
| `ft_lstnew`       | Create a new node                |
| `ft_lstadd_front` | Insert at the beginning    |
| `ft_lstsize`      | Count the number of nodes               |
| `ft_lstlast`      | Get the last node             |
| `ft_lstadd_back`  | Insert at the end          |
| `ft_lstdelone`    | Delete a node               |
| `ft_lstclear`     | Delete the entire list               |
| `ft_lstiter`      | Iterate through the list and execute a function on each node       |
| `ft_lstmap`       | Transform the content of each node to generate a new list |

### 1. Technical considerations Technical Requirements

1. **Global variables are strictly prohibited**

Because Libft is a public library, it should follow: same input -> always same output.
If global variables exist, modifying them will cause the final result to change.

2. **Helper Functions must be static**

For example: 
```c
ft_split()
```
which requires
```c
int count_words()
void copy_word()
free_all()
```
These functions must not be exposed to others and should be written as:
```c
static int count_words()
static void copy_word()
static free_all()
```
Because `static` means <font color="red">it can only be used within the current file</font> and will not pollute the entire library.

3. **All files must be placed in the root directory, as follows:**

```
libft/

Makefile

libft.h

ft_strlen.c
ft_memcpy.c
...
```
All files must be placed directly in the root directory.

4. **Submitting unused files is not allowed**

For example:
```c
test.c
old.c
abc.c
```
If the Makefile does not use them at all, do not submit them.

5. **All .c files must:**

```bash
-Wall
-Wextra
-Werror
```
be able to compile without warnings.

6. **Must use the `ar` command**
`ar` stands for archiver and is a tool in Unix/Linux/macOS systems used to bundle multiple object files (`.o`) into an archive file.
The primary working objects of `ar` are `.o`

The most typical usage in a C project is multiple `.o` files -> `ar` -> a `.a` static library.
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

Therefore, what `ar` does is essentially organizing/bundling many object files into a static library file.
> Understanding the command
> ```bash
>	ar rcs libft.a *.o
> ```
> `ar`: invoke the archiver tool
> `rcs`:
>	- `r` = replace: Insert the specified `.o` files into the archive. If a member with the same name already exists in the archive, replace it; if it does not exist, create it.
>	- `c` = create: Create the archive if it does not already exist.
>	- `s` = Create an archive symbol index.

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

| Tool           | Main Purpose       |
| ------------ | -------------- |
| `cc` / `gcc` | Compile C           |
| `ar`         | Create/manage archives  |
| linker       | Link object files/libraries into the final program |

The project explicitly requires using `ar` to create `libft.a`; using `libtool` is prohibited.

7. **`libft.a` must be located in the root directory**

`libft.a` is right next to `Makefile`.

### 2. README Requirements

`README.md` is part of the project and is required to be present in the root directory of the repository.

`README` should at least contain the following contents:
1. **The first line must be in italics, with the fixed content:**
```
*This activity has been created as part of the 42 curriculum by <login>.*
```
If working in a team, multiple logins can be listed sequentially.

2. **Description of the project, explaining:**
- What Libft is
- Project goals
- Main implemented contents

3. **Instructions for use**, such as:
- Compilation, e.g., `make`
- Generating `libft.a`
- Using the static library in other projects

4. **Resources (References)**
List the references used during the learning process, such as:
- C standard library documentation (man pages)
- Tutorials
- Technical articles, etc.
In addition, you must also explain **the use of AI in the project**, such as for conceptual explanations, code review, or debugging, while specifying which parts were completed by yourself.

5. **Detailed introduction to the created library**
Provide a detailed explanation of the `libft` library itself, such as:
- What categories of functions are included
- The purpose of each category of functions
- The role of this library in subsequent 42 projects
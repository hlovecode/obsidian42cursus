This is where the `Libft` project really needs to be mastered.

A typical Makefile:
```Makefile
NAME = libft.a

CC = cc
CFLAGS = -Wall -Wextra -Werror

SRCS = ft_strlen.c \
       ft_memset.c \
       ft_memcpy.c

OBJS = $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all
```
Here:
```Makefile
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```
is responsible for:
```Makefile
.c -> .o
```
While:
```Makefile
$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)
```
is responsible for:
```Makefile
.o → libft.a
```
So the overall logic of the Makefile:
```Makefile
                cc
.c ─────────────────────→ .o
                            │
                            │
                            │ ar rcs
                            ↓
                         libft.a
```

`ar` mainly deals with `archive` members, which are `.o`, and the C source code `.c` needs to go through `cc` compilation first, so it should be:
```bash
.c
 ↓ cc
.o
 ↓ ar
.a
```
Instead of:
```bash
.c
 ↓ ar
.a
```

`ar` is a program that maintains library files by adding, deleting, and extracting files from them. Typically, `ar` is used to create and manage object library files used by the linker.

#### Remember 4 commands:

1 Compile a `.c` file:
```bash
cc -Wall -Wextra -Werror -c ft_strlen.c
```
Yielding:
```bash
ft_strlen.o
```

2 Create a static library:
```bash
ar rcs libft.a ft_strlen.o
```
Yielding:
```bash
libft.a
```

`libft.a` is a static library created using the `ar` tool. 

`ar` itself is not a compiler; it does not compile `.c` into machine code. Its function is to package and archive already compiled `.o` files into a `libft.a`, where `.a` indicates that this is an archive file. 

What `ar` processes are object files/archive members like `.o`, rather than being responsible for compiling C source code into object code. 

3 View the contents of the static library:
```bash
ar -t libft.a
```
Yielding:
```bash
ft_strlen.o
...
```

4 Delete the static library:
```bash
rm -f libft.a
```

#### Connecting the Entire Libft Workflow

You can understand `Libft` as:
```bash
              你的 C 源代码
                     │
                     │ cc -c
                     ↓
              ┌──────────────┐
              │   .o 文件     │
              ├──────────────┤
              │ ft_strlen.o  │
              │ ft_memset.o  │
              │ ft_memcpy.o  │
              │ ft_split.o   │
              │ ft_itoa.o    │
              │ ...          │
              └──────┬───────┘
                     │
                     │ ar rcs
                     ↓
              ┌──────────────┐
              │   libft.a    │
              │ Static       │
              │ Library      │
              └──────┬───────┘
                     │
                     │ linker
                     ↓
              ┌──────────────┐
              │ 你的程序      │
              │ main.c       │
              └──────────────┘
```

**`cc` compiles `.c` into `.o`; `ar` organizes multiple `.o` into the `.a` static library; finally, the linker extracts the code needed by the program from `.a` to generate the executable file.**
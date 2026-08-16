This is where you truly need to master the `Libft` project.

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
Therefore, the entire logic of the Makefile is:
```Makefile
                cc
.c ─────────────────────→ .o
                            │
                            │
                            │ ar rcs
                            ↓
                         libft.a
```

`ar` mainly deals with `archive` members, which are `.o`, and the C source code `.c` needs to be compiled by `cc` first, so the order should be:
```bash
.c
 ↓ cc
.o
 ↓ ar
.a
```
instead of:
```bash
.c
 ↓ ar
.a
```

`ar` is a program that maintains library archives by adding, deleting, and extracting files. Typically, `ar` is used to create and manage object libraries used by the linker.

#### Remember 4 commands:

1. Compile a `.c` file:
```bash
cc -Wall -Wextra -Werror -c ft_strlen.c
```
To get:
```bash
ft_strlen.o
```

2. Create a static library:
```bash
ar rcs libft.a ft_strlen.o
```
To get:
```bash
libft.a
```

3. View the contents of a static library:
```bash
ar -t libft.a
```
To get:
```bash
ft_strlen.o
...
```

4. Delete a static library:
```bash
rm -f libft.a
```

#### Connecting the entire Libft workflow

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

**`cc` compiles `.c` into `.o`; `ar` organizes multiple `.o` into a `.a` static library; ultimately, the linker extracts the code required by the program from `.a` to generate the executable file.**
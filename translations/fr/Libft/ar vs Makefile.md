这是 `Libft` 项目真正要掌握的地方.

典型的Makefile:
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
这里：
```Makefile
%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@
```
负责：
```Makefile
.c -> .o
```
而：
```Makefile
$(NAME): $(OBJS)
	ar rcs $(NAME) $(OBJS)
```
负责：
```Makefile
.o → libft.a
```
所以 Makefile 的整个逻辑：
```Makefile
                cc
.c ─────────────────────→ .o
                            │
                            │
                            │ ar rcs
                            ↓
                         libft.a
```

`ar` 主要处理的的是 `archive` 成员，也就是 `.o` ，而C源代码`.c` 需要首先经过 `cc` 编译，所以应该是：
```bash
.c
 ↓ cc
.o
 ↓ ar
.a
```
而不是：
```bash
.c
 ↓ ar
.a
```

ar 是一个程序，可以通过从文件中增加、删除和析取文件来维护库文件. 通常使用 ar 是为了创建和管理连接程序使用的目标库文件.

#### 记住4个命令：

1 编译一个 `.c` 文件：
```bash
cc -Wall -Wextra -Werror -c ft_strlen.c
```
得到：
```bash
ft_strlen.o
```

2 创建静态库：
```bash
ar rcs libft.a ft_strlen.o
```
得到：
```bash
libft.a
```

`libft.a` 是使用 ar 工具创建出来的静态库. 

ar 本身不是编译器，它不会把 `.c` 编译成机器代码，它的作用是把已经编译好的 `.o` 文件打包归档成 `libft.a`,  `.a` 表示这是一个 archive 文件. 

ar 要处理的是 `.o` 这种目标文件/归档成员，而不是负责把C源代码编译成目标代码. 

3 查看静态库里面有什么：
```bash
ar -t libft.a
```
得到：
```bash
ft_strlen.o
...
```

4 删除静态库
```bash
rm -f libft.a
```

#### 把整个 Libft 流程串起来

可以把 `Libft` 理解成：
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

**`cc` 把 `.c` 编译成 `.o`；`ar` 把多个 `.o` 组织成 `.a` 静态库；最终链接器从 `.a` 中提取程序需要的代码，生成可执行文件.**
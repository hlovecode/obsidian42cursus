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

### 总结

##### 变量定义如下：

| 内容                               | 类型  | 作用            | 具体解释                            |
| -------------------------------- | --- | ------------- | ------------------------------- |
| `NAME = libft.a`                 | 变量  | 定义最终生成的静态库名称  | 最终生成的文件叫 `libft.a`              |
| `CC = gcc`                       | 变量  | 指定 C 编译器      | 使用 GCC 编译 `.c` 文件               |
| `CFLAGS = -Wall -Wextra -Werror` | 变量  | 指定编译选项        | 开启常见警告，并将警告视为错误                 |
| `SRCS = ...`                     | 变量  | 列出所有源文件       | 告诉 Make 哪些 `.c` 文件需要参与编译        |
| `OBJS = $(SRCS:.c=.o)`           | 变量  | 根据源文件生成目标文件列表 | 将 `SRCS` 中所有 `.c` 后缀替换为 `.o`    |
| `AR = ar`                        | 变量  | 指定静态库归档工具     | 使用 `ar` 将 `.o` 文件打包成 `.a` 文件    |
| `ARFLAGS = rcs`                  | 变量  | 指定归档选项        | `r` 添加或替换成员，`c` 创建归档，`s` 建立符号索引 |

特别注意：

```
OBJS = $(SRCS:.c=.o)
```
这是 Make 的变量替换语法，不是执行 shell 命令，也不会立即创建 `.o` 文件。它只生成文件名列表.

##### 构建和编译规则如下：

| 规则                                 | 类型     | 作用                 | 具体解释                                     |
| ---------------------------------- | ------ | ------------------ | ---------------------------------------- |
| `all: $(NAME)`                     | 普通目标规则 | 默认构建目标             | 执行 `make` 时，Make 会尝试生成 `libft.a`         |
| `%.o: %.c libft.h`                 | 模式规则   | 定义 `.c` 如何编译成 `.o` | `%` 表示匹配相同的文件名部分；同时依赖 `.c` 文件和 `libft.h` |
| `$(CC) $(CFLAGS) -c $< -o $@`      | 命令     | 执行实际编译             | 将当前 `.c` 文件编译成对应的 `.o` 文件                |
| `$(NAME): $(OBJS)`                 | 普通目标规则 | 定义静态库的依赖关系         | 创建 `libft.a` 之前，必须先准备好所有 `.o` 文件         |
| `$(AR) $(ARFLAGS) $(NAME) $(OBJS)` | 命令     | 创建静态库              | 将所有 `.o` 文件打包到 `libft.a` 中               |

**重点：模式规则中的三个符号**

```
%.o: %.c libft.h
	$(CC) $(CFLAGS) -c $< -o $@
```

|符号|名称|含义|举例|
|---|---|---|---|
|`%`|通配匹配符|匹配文件名中相同的部分|`ft_atoi`|
|`$<`|第一个依赖文件|当前规则的第一个 prerequisite|`ft_atoi.c`|
|`$@`|当前目标文件|当前正在生成的目标|`ft_atoi.o`|

例如，当 Make 需要生成 `ft_atoi.o` 时：
```
gcc -Wall -Wextra -Werror -c ft_atoi.c -o ft_atoi.o
```

当需要生成 `ft_strlen.o` 时：
```
gcc -Wall -Wextra -Werror -c ft_strlen.c -o ft_strlen.o
```

Make 会针对每个需要更新的 `.o` 文件分别执行命令

##### 清理规则如下：

|规则|类型|作用|具体解释|
|---|---|---|---|
|`clean:`|普通目标规则|删除所有 `.o` 文件|通过 `rm -f $(OBJS)` 删除目标文件|
|`rm -f $(OBJS)`|命令|实际执行删除|`-f` 表示不提示，文件不存在也不报错|
|`fclean: clean`|带依赖的目标规则|完全清理项目|先执行 `clean`，再执行自己的删除命令|
|`rm -f $(NAME)`|命令|删除静态库|删除 `libft.a`|
|`re: fclean all`|带依赖的目标规则|完整重新构建|先执行 `fclean`，再执行 `all`，重新编译并创建静态库|

**三个命令的区别：**

|Terminal 命令|删除 `.o`|删除 `.a`|重新编译|
|---|---|---|---|
|`make clean`|是|否|否|
|`make fclean`|是|是|否|
|`make re`|是|是|是|

##### 伪目标声明如下：

```
.PHONY: all clean fclean re
```

| 内容       | 作用     | 为什么需要                         |
| -------- | ------ | ----------------------------- |
| `.PHONY` | 声明伪目标  | 告诉 Make 这些名称代表操作，而不是实际文件      |
| `all`    | 默认构建操作 | 即使目录中存在名为 `all` 的文件，也仍然执行目标规则 |
| `clean`  | 清理操作   | 避免同名文件阻止清理                    |
| `fclean` | 完全清理操作 | 避免同名文件阻止完全清理                  |
| `re`     | 重新构建操作 | 避免同名文件阻止重新构建                  |

### 整个 Makefile 的执行关系

- **执行make** 

`all` 依赖 `libft.a` -->  `libft.a` 依赖全部 .o 文件 -->  `%.o: %.c libft.h` 按需编译每个 .c 文件 -->  `ar rcs` 将所有 .o 文件打包成 libft.a

- **执行 make re**

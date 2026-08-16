一个工程中的源文件不计其数，其按类型、功能、模块分别放在若干个目录中，Makefile 定义了一系列的规则来指定哪些文件需要先编译，哪些文件需要后编译，哪些文件需要重新编译，甚至于进行更复杂的功能操作.

### Make 与 Makefile 的关系

make 是一个命令工具，它解释了 Makefile 中的指令.
在 Makefile 文件中描述了整个工程所有文件的编译顺序、编译规则.
make 执行的时候，去读取 Makefile 文件中的规则，但 Makefile 需要自己写.

### Makefile 命名规则

Makefile 或 makefile 一般使用 Makefile



### PS: 补充 信息

#### `gcc (g++) <options> <sourcefile>`


`strnstr` 用于在字符串 `haystack` 的前 len 个字符范围内，寻找字符串 `needle` 第一次出现的位置

#### 1. Prototype

```c
#include <string.h>

char	*strnstr(const char *haystack, const char *needle, size_t len);
```

参数：

- haystack: 被搜索的字符串
- needle: 要寻找的字符串，也就是子字符串
- len: 最多允许在 haystack 的前 len 个字符范围内进行搜索，控制的是在 haystack 中允许搜索多少个字符

返回值：

指向 haystack 中第1次出现 needle 的位置的指针，如果没有找到，则返回 NULL，如果 needle 是空字符串，就返回 haystack

#### 2. `strnstr` 核心逻辑

1. needle 是不是空字符串？如果是，返回 haystack
2. 在 haystack 的前 len 个字符中寻找可能的起点
3. 每一个可能的起点：检查 needle 是否完整匹配
4. 匹配成功吗？如果是，返回当前位置
5. 有没有全部检查完？如果是，返回 NULL

`strnstr`:  在 `haystack` 的前 `len` 个字符范围内，寻找 `needle` 第一次完整出现的位置；找到就返回指针，找不到返回 `NULL`，如果 `needle` 是空字符串则返回 `haystack`

#### 3. 对比类似函数

| 函数        | 搜索对象       | 是否限制搜索范围 |
| --------- | ---------- | -------- |
| `strstr`  | 字符串中的子字符串  | 不限制      |
| `strnstr` | 字符串中的子字符串  | 限制       |
| `strchr`  | 单个字符       | 不限制      |
| `strrchr` | 单个字符最后一次出现 | 不限制      |
| `strncmp` | 比较两个字符串    | 限制       |

- `strchr`: 找到一个字符
- `strstr`
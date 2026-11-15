
#### 1.  ft_lstnew

```c
t_list *ft_lstnew(void *content)
```

作用：在堆内存中申请一个新的节点，初始化节点的2个成员，然后返回这个节点的地址

| 参数      | 类型      | 含义             | 返回值                |
| ------- | ------- | -------------- | ------------------ |
| content | void \* | 准备存放在新节点中的数据地址 | 1. 内存申请成功，返回新节点的地址 |
|         |         |                | 2. 内存申请失败，返回NULL   |

#### 2.  ft_lstadd_front

```c
void ft_lstadd_front(t_list **lst, t_list *new)
```

作用：把新节点连接到原来第1个节点的前面，并更新链表头指针


|     |     |
| --- | --- |
|     |     |


#### 3. ft_lstsize

```c
int ft_lstsize(t_list *lst)
```

作用：使用指针遍历整个链表，并统计节点数量

| 参数  | 类型        | 含义           |
| --- | --------- | ------------ |
| lst | t_list \* | 指向链表第1个节点的指针 |
返回值：返回链表中节点的总数量

注意：该函数只负责统计节点数量，不会修改链表，也不会修改节点里面的数据

#### 4. ft_lstlast

```c
t_list *ft_lstlast(t_list *lst)
```

作用：通过一级指针遍历链表，并返回最后一个节点的地址

| 参数  | 类型        | 含义           | 返回值                  |
| --- | --------- | ------------ | -------------------- |
| lst | t_list \* | 指向链表第1个节点的指针 | 1. 链表为空，返回NULL       |
|     |           |              | 2. 链表不为空，返回最后一个节点的地址 |

#### 5. ft_lstadd_back

```c
void ft_lstadd_back(t_list **lst, t_list *new)
```

作用：将一个已经创建好的新节点，添加到单链表的末尾

| 参数  | 类型        | 含义            |
| --- | --------- | ------------- |
| lst | t_list ** | 指向链表头指针的指针    |
| new | t_list ** | 准备添加到链表末尾的新节点 |
该函数没有返回值

**函数的任务：**

- 如果链表为空，让 `new` 成为第一个节点

- 如果链表不为空，找到最后一个节点

- 将最后一个节点的 `next` 指向 `new`
#### 6. ft_lstdelone

```c
void ft_lstdelone(t_list *lst, void (*del)(void *))
```

#### 7. ft_lstclear

```c
void ft_lstclear(t_list **lst, void (*del)(void *))
```

#### 8. ft_lstiter

```c
void ft_lstiter(t_list *lst, void(*f)(void *))
```

#### 9. ft_lstmap

```c
t_list *ft_lstmap(t_list *lst, void *(*f)(void *))
```



#### 1.  ft_lstnew

```c
t_list *ft_lstnew(void *content)
```

#### 2.  ft_lstadd_front

```c
void ft_lstadd_front(t_list **lst, t_list *new)
```

#### 3. ft_lstsize

```c
int ft_lstsize(t_list *lst)
```


#### 4. ft_lstlast

```c
t_list *ft_lstlast(t_list *lst)
```

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


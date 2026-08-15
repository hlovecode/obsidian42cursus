#### 1.  `ft_lstnew`

```c
t_list *ft_lstnew(void *content)
```

#### 2.  `ft_lstadd_front`

```c
void ft_lstadd_front(t_list **lst, t_list *new)
```

#### 3. `ft_lstsize`

```c
int ft_lstsize(t_list *lst)
```

#### 4. `ft_lstlast`

```c
t_list *ft_lstlast(t_list *lst)
```

#### 5. `ft_lstadd_back`

```c
void ft_lstadd_back(t_list **lst, t_list *new)
```

#### 6. `ft_lstdelone`

```c
void ft_lstdelone(t_list *lst, void (*del)(void *))
```

#### 7. `ft_lstclear`

```c
void ft_lstclear(t_list **lst, void (*del)(void *))
```

#### 8. `ft_lstiter`

```c
void ft_lstiter(t_list *lst, void(*f)(void *))
```

#### 9. `ft_lstmap`

```c
t_list *ft_lstmap(t_list *lst, void *(*f)(void *))
```
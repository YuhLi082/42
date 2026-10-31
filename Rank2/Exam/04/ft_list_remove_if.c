/*Assignment name  : ft_list_remove_if
Expected files   : ft_list_remove_if.c
Allowed functions: free
--------------------------------------------------------------------------------

Write a function called ft_list_remove_if that removes from the
passed list any element the data of which is "equal" to the reference data.

It will be declared as follows :

void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)());

cmp takes two void* and returns 0 when both parameters are equal.

You have to use the ft_list.h file, which will contain:

$>cat ft_list.h
typedef struct      s_list
{
    struct s_list   *next;
    void            *data;
}                   t_list;
$>*/


void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
{
    t_list *temp;
    t_list *cur;

    while(*begin_list && cmp((*begin_list)->data, data_ref)==0)
    {
        temp = *begin_list;
        *begin_list = (*begin_list)->next;
        free(temp);
    }
    if(!*begin_list)
        return ;
    cur = *begin_list;
    while(cur->next)
    {
        if(cmp(cur->next->data, data_ref)== 0)
        {
            temp = cur->next;
            cur->next = cur->next->next;
            free(temp);
        }
        else
            cur = cur->next;   
    }
}





























void ft_list_remove_if(t_list **begin_list, void *data_ref, int (*cmp)())
{
    t_list *current;
    t_list *tmp;

    while(*begin_list && cmp((*begin_list -> data), data_ref) == 0)
    {
        tmp = *begin_list;
        *begin_list = (*begin_list) -> next;
        free(tmp);
    }
    if(!*begin_list)
        return ;
    curr = *begin_list;
    while(curr->next)
    {
        if (cmp(curr->next->data, data_ref) == 0)
		{
            tmp = curr->next;
			curr->next = curr->next->next;
			free(tmp);
        }
        else
            curr = curr -> next;
    }
}



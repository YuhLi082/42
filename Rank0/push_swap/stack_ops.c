/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sa.c                                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/08 16:19:26 by yuhli             #+#    #+#             */
/*   Updated: 2025/12/08 16:19:26 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	swap(t_stack *stack)
{
	t_node	*first;
	t_node	*second;

	if (!stack || stack -> size < 2)
		return ;
	first = stack->top;
	second = first->next;
	first->next = second->next;
	if (second->next != NULL)
		second->next->prev = first;
	second -> prev = NULL;
	second -> next = first;
	first -> prev = second;
	stack -> top = second;
	if (stack -> size == 2)
		stack -> bottom = first;
}

void	push(t_stack *src, t_stack *dst)
{
	t_node	*node;

	if (!src || !dst || src -> size < 1)
		return ;
	node = src -> top;
	src -> top = node -> next;
	if (src -> top != NULL)
		src -> top -> prev = NULL;
	else
		src -> bottom = NULL;
	src -> size--;
	node -> next = dst -> top;
	if (dst -> top != NULL)
		dst -> top -> prev = node;
	else
		dst -> bottom = node;
	node -> prev = NULL;
	dst -> top = node;
	dst -> size++;
}

void	rotate(t_stack *stack)
{
	t_node	*node;

	if (!stack || stack -> size < 2)
		return ;
	node = stack -> top;
	stack -> top = node -> next;
	stack -> top -> prev = NULL;
	node -> next = NULL;
	node -> prev = stack -> bottom;
	if (stack->bottom)
		stack -> bottom -> next = node;
	stack->bottom = node;
}

void	reverse_rotate(t_stack *stack)
{
	t_node	*node;

	if (!stack || stack -> size < 2)
		return ;
	node = stack -> bottom;
	stack -> bottom = node -> prev;
	if (stack -> bottom != NULL)
		stack -> bottom -> next = NULL;
	node -> prev = NULL;
	node -> next = stack -> top;
	if (stack->top)
		stack->top->prev = node;
	stack -> top = node;
}

void	error_exit(t_stack *a, t_stack *b)
{
	write(2, "Error\n", 6);
	if (a)
		free_stack(a);
	if (b)
		free_stack(b);
	exit (1);
}

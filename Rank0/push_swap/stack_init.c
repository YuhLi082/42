/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_init.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/13 19:05:37 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 16:25:43 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_stack	*new_stack(void)
{
	t_stack	*stack;

	stack = (t_stack *)malloc(sizeof(t_stack));
	if (!stack)
		return (NULL);
	stack -> top = NULL;
	stack -> bottom = NULL;
	stack -> size = 0;
	return (stack);
}

t_node	*new_node(int value)
{
	t_node	*node;

	node = (t_node *)malloc(sizeof(t_node));
	if (!node)
		return (NULL);
	node -> value = value;
	node -> index = 0;
	node -> next = NULL;
	node -> prev = NULL;
	return (node);
}

void	add_to_top(t_stack *stack, t_node *node)
{
	if (!stack || !node)
		return ;
	node -> prev = NULL;
	node -> next = stack -> top;
	if (stack -> top)
		stack -> top -> prev = node;
	else
		stack -> bottom = node;
	stack -> top = node;
	stack -> size++;
}

void	free_stack(t_stack *stack)
{
	t_node	*current;
	t_node	*next;

	if (!stack)
		return ;
	current = stack -> top;
	while (current)
	{
		next = current -> next;
		free(current);
		current = next;
	}
	free(stack);
}

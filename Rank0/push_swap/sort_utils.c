/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_utils.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/27 20:26:33 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 16:22:05 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_sorted(t_stack *stack)
{
	t_node	*node;

	if (!stack || stack -> size < 2)
		return (1);
	node = stack -> top;
	while (node && node -> next)
	{
		if (node -> value > node -> next ->value)
			return (0);
		node = node ->next;
	}
	return (1);
}

void	final_rotate_a(t_stack *a)
{
	int	size;
	int	pos;

	pos = get_min_index(a);
	size = a -> size;
	if (pos < size / 2)
	{
		while (pos-- > 0)
			ra(a);
	}
	else
	{
		pos = size - pos;
		while (pos-- > 0)
			rra(a);
	}
}

int	index_stack(t_stack *stack)
{
	t_node	*current;
	t_node	*runner;
	int		count;

	if (!stack || !stack->top)
		return (0);
	current = stack->top;
	while (current)
	{
		count = 0;
		runner = stack->top;
		while (runner)
		{
			if (runner->value < current->value)
				count++;
			runner = runner->next;
		}
		current->index = count;
		current = current->next;
	}
	return (1);
}

int	get_min_index(t_stack *stack)
{
	t_node	*current;
	int		index;
	int		min_position;
	int		position;

	if (!stack || !stack -> top)
		return (-1);
	current = stack -> top;
	index = current -> index;
	min_position = 0;
	position = 0;
	while (current)
	{
		if (current -> index < index)
		{
			min_position = position;
			index = current -> index;
		}
		current = current -> next;
		position++;
	}
	return (min_position);
}

int	get_max_index(t_stack *stack)
{
	t_node	*current;
	int		max_val;
	int		max_pos;
	int		pos;

	if (!stack || !stack->top)
		return (-1);
	current = stack->top;
	max_val = current->index;
	max_pos = 0;
	pos = 0;
	while (current)
	{
		if (current->index > max_val)
		{
			max_val = current->index;
			max_pos = pos;
		}
		current = current->next;
		pos++;
	}
	return (max_pos);
}

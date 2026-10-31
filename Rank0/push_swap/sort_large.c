/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_large.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/01 22:12:55 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 15:19:37 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	push_rotate_b(t_stack *a, t_stack *b, int *range)
{
	pb(a, b);
	if (b->size > 1)
		rb(b);
	(*range)++;
}

void	push_max_to_a(t_stack *a, t_stack *b)
{
	int	max_pos;
	int	dist;

	while (b->size > 0)
	{
		max_pos = get_max_index(b);
		if (max_pos <= b->size / 2)
		{
			while (max_pos-- > 0)
				rb(b);
		}
		else
		{
			dist = b->size - max_pos;
			while (dist-- > 0)
				rrb(b);
		}
		pa(a, b);
	}
}

int	get_chunk_size(int size)
{
	if (size <= 100)
		return (18);
	else
		return (25);
}

void	sort_large(t_stack *a, t_stack *b)
{
	int	chunk_size;
	int	range;

	chunk_size = get_chunk_size(a->size);
	range = 0;
	while (a->size > 0)
	{
		if (a->top->index <= range)
			push_rotate_b(a, b, &range);
		else if (a->top->index <= range + chunk_size)
		{
			pb(a, b);
			range++;
		}
		else
			ra(a);
	}
	push_max_to_a(a, b);
	final_rotate_a(a);
}

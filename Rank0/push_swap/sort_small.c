/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   sort_small.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/28 15:51:52 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 16:25:34 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	sort_stack(t_stack *a, t_stack *b)
{
	int	size;

	if (!a || is_sorted(a))
		return ;
	size = a -> size;
	if (size == 2)
		sort_two(a);
	else if (size == 3)
		sort_three(a);
	else if (size <= 5)
		sort_small(a, b);
	else
		sort_large(a, b);
}

void	sort_two(t_stack *a)
{
	if (!a || a -> size != 2)
		return ;
	if (a -> top -> value > a -> top -> next ->value)
		sa(a);
}

void	sort_three(t_stack *a)
{
	int	first;
	int	second;
	int	third;

	if (!a || a -> size != 3)
		return ;
	first = a -> top -> value;
	second = a -> top -> next-> value;
	third = a -> top -> next-> next -> value;
	if (first < second && second > third && first < third)
	{
		sa(a);
		ra(a);
	}
	else if (first > second && second < third && first < third)
		sa(a);
	else if (first < second && second > third && first > third)
		rra(a);
	else if (first > second && second > third && first > third)
	{
		sa(a);
		rra(a);
	}
	else if (first > second && second < third && first > third)
		ra(a);
}

void	push_min_to_b(t_stack *a, t_stack *b)
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
	pb(a, b);
}

void	sort_small(t_stack *a, t_stack *b)
{
	int	push_count;

	if (!a || !b || a->size <= 3 || a->size > 5)
		return ;
	push_count = 0;
	while (a->size > 3 && push_count < 2)
	{
		push_min_to_b(a, b);
		push_count++;
	}
	if (a -> size == 3)
		sort_three(a);
	else if (a -> size == 2)
		sort_two(a);
	while (b -> size > 0)
		pa(a, b);
}

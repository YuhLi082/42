/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/14 17:15:46 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/02 23:26:10 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	is_space(char c)
{
	return (c == ' ' || (c >= 9 && c <= 13));
}

int	is_digit(char c)
{
	return (c >= '0' && c <= '9');
}

int	check_num(char *str)
{
	int		i;
	long	num;

	if (!str || str[0] == '\0')
		return (0);
	i = 0;
	while (is_space(str[i]))
		i++;
	if (str[i] == '-' || str[i] == '+')
	{
		if (!is_digit(str[i + 1]))
			return (0);
		i++;
	}
	while (str[i])
	{
		if (!is_digit(str[i]))
			return (0);
		i++;
	}
	num = ft_atol(str);
	if (num < INT_MIN || num > INT_MAX)
		return (0);
	return (1);
}

int	is_duplicated(t_stack *stack)
{
	t_node	*node;
	t_node	*next_node;

	node = stack -> top;
	while (node)
	{
		next_node = node -> next;
		while (next_node)
		{
			if (node -> value == next_node -> value)
				return (1);
			next_node = next_node -> next;
		}
		node = node -> next;
	}
	return (0);
}

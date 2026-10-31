/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/03 15:52:39 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 15:54:21 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	process_numbers_array(t_stack *stack, char **numbers)
{
	int		i;
	long	value;
	t_node	*node;

	i = 0;
	while (numbers[i])
		i++;
	while (--i >= 0)
	{
		if (!check_num(numbers[i]))
		{
			ft_free_split(numbers);
			error_exit(stack, NULL);
		}
		value = ft_atol(numbers[i]);
		node = new_node((int)value);
		if (!node)
		{
			ft_free_split(numbers);
			error_exit(stack, NULL);
		}
		add_to_top(stack, node);
	}
	ft_free_split(numbers);
}

void	handle_single_arg(t_stack *stack, char *arg)
{
	char	**numbers;

	numbers = ft_split(arg, ' ');
	if (!numbers)
		error_exit(stack, NULL);
	process_numbers_array(stack, numbers);
}

void	handle_multiple_args(t_stack *stack, char **argv, int argc)
{
	int		i;
	long	value;
	t_node	*node;

	i = argc - 1;
	while (i >= 1)
	{
		if (!check_num(argv[i]))
			error_exit(stack, NULL);
		value = ft_atol(argv[i]);
		node = new_node((int)value);
		if (!node)
			error_exit(stack, NULL);
		add_to_top(stack, node);
		i--;
	}
}

void	fill_stack(t_stack *stack, char **argv, int argc)
{
	if (argc == 2)
		handle_single_arg(stack, argv[1]);
	else
		handle_multiple_args(stack, argv, argc);
	if (is_duplicated(stack))
		error_exit(stack, NULL);
	if (!index_stack(stack))
		error_exit(stack, NULL);
}

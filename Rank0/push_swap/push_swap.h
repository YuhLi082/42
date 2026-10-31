/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42.fr>                +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/09 22:20:06 by yuhli             #+#    #+#             */
/*   Updated: 2026/01/03 16:25:17 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include <stdlib.h>
# include <unistd.h>
# include <limits.h>

typedef struct s_node
{
	int				value;
	int				index;
	struct s_node	*prev;
	struct s_node	*next;
}	t_node;

typedef struct s_stack
{
	t_node	*top;
	t_node	*bottom;
	int		size;
	char	name;
}	t_stack;

/*stack_ops*/
void	swap(t_stack *stack);
void	push(t_stack *src, t_stack *dst);
void	rotate(t_stack *stack);
void	reverse_rotate(t_stack *stack);

/*ft_swap*/
void	sa(t_stack *a);
void	sb(t_stack *b);
void	ss(t_stack *a, t_stack *b);

/*ft_push*/
void	pa(t_stack *a, t_stack *b);
void	pb(t_stack *a, t_stack *b);

/*ft_rotate*/
void	ra(t_stack *a);
void	rb(t_stack *b);
void	rr(t_stack *a, t_stack *b);

/*ft_reverse_rotate*/
void	rra(t_stack *a);
void	rrb(t_stack *b);
void	rrr(t_stack *a, t_stack *b);

/*ft_split*/
void	ft_free_split(char **ptr);
size_t	ft_count(char const *s, char c);
char	**ft_empty(void);
char	**ft_fill(char **ptr, char const *s, char c);
char	**ft_split(char const *s, char c);

/*utils*/
long	ft_atol(const char *str);
void	ft_putendl(char *str);
void	ft_putstr(char *str);
char	*ft_substr(char const *s, unsigned int start, size_t len);

/*ft_utils*/
size_t	ft_strlen(const char *s);
char	*ft_strdup(const char *s1);

/*parse*/
int		is_space(char c);
int		is_digit(char c);
int		check_num(char *str);
int		is_duplicated(t_stack *stack);

/*stack_init*/
t_stack	*new_stack(void);
t_node	*new_node(int value);
void	add_to_top(t_stack *stack, t_node *node);
void	free_stack(t_stack *stack);
void	error_exit(t_stack *a, t_stack *b);

/*stack_utils*/
void	process_numbers_array(t_stack *stack, char **numbers);
void	handle_single_arg(t_stack *stack, char *arg);
void	handle_multiple_args(t_stack *stack, char **argv, int argc);
void	fill_stack(t_stack *stack, char **argv, int argc);

/*sort_utils*/
int		is_sorted(t_stack *stack);
int		index_stack(t_stack *stack);
int		get_min_index(t_stack *stack);
int		get_max_index(t_stack *stack);
void	final_rotate_a(t_stack *a);

/*sort_small*/
void	sort_stack(t_stack *a, t_stack *b);
void	sort_two(t_stack *a);
void	sort_three(t_stack *a);
void	push_min_to_b(t_stack *a, t_stack *b);
void	sort_small(t_stack *a, t_stack *b);

/* sort_large */
void	push_rotate_b(t_stack *a, t_stack *b, int *range);
void	push_max_to_a(t_stack *a, t_stack *b);
int		get_chunk_size(int size);
void	sort_large(t_stack *a, t_stack *b);

#endif
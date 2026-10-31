/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: yuhli <yuhli@student.42madrid.com>         +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/10/11 21:59:04 by yuhli             #+#    #+#             */
/*   Updated: 2025/10/11 21:59:04 by yuhli            ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static void	ft_free_split(char **ptr)
{
	size_t	i;

	i = 0;
	if (!ptr)
		return ;
	while (ptr[i])
	{
		free (ptr[i]);
		i++;
	}
	free (ptr);
}

static size_t	ft_count(char const *s, char c)
{
	size_t	x;
	size_t	count;

	x = 0;
	count = 0;
	while (*s)
	{
		if (*s != c && x == 0)
		{
			x = 1;
			count++;
		}
		else if (*s == c)
			x = 0;
		s++;
	}
	return (count);
}

static char	**ft_empty(void)
{
	char	**ptr;

	ptr = (char **)malloc(sizeof(char *));
	if (!ptr)
		return (NULL);
	ptr[0] = NULL;
	return (ptr);
}

static char	**ft_fill(char **ptr, char const *s, char c)
{
	size_t	i;
	size_t	j;
	size_t	start;

	i = 0;
	j = 0;
	while (s[i])
	{
		if (s[i] != c)
		{
			start = i;
			while (s[i] && s[i] != c)
				i++;
			ptr[j] = ft_substr(s, start, i - start);
			if (!ptr[j])
				return (ft_free_split(ptr), NULL);
			j++;
		}
		else
			i++;
	}
	ptr[j] = NULL;
	return (ptr);
}

char	**ft_split(char const *s, char c)
{
	char	**ptr;
	size_t	words;

	if (!s)
		return (NULL);
	words = ft_count(s, c);
	if (words == 0)
		return (ft_empty());
	ptr = (char **)malloc((words + 1) * sizeof(char *));
	if (!ptr)
		return (NULL);
	return (ft_fill(ptr, s, c));
}
